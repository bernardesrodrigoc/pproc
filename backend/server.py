from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, UploadFile, File, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
import hashlib
from datetime import datetime, timezone, timedelta
import httpx
from cryptography.fernet import Fernet
import base64
from urllib.parse import urlencode

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Encryption key for evidence files
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', Fernet.generate_key().decode())
fernet = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)

# ORCID OAuth Configuration
ORCID_CLIENT_ID = os.environ.get('ORCID_CLIENT_ID', '')
ORCID_CLIENT_SECRET = os.environ.get('ORCID_CLIENT_SECRET', '')
# Use sandbox for development, production for live
ORCID_BASE_URL = os.environ.get('ORCID_BASE_URL', 'https://sandbox.orcid.org')
ORCID_API_URL = os.environ.get('ORCID_API_URL', 'https://pub.sandbox.orcid.org')
# ORCID redirect URI - must be absolute URL matching ORCID Developer Portal registration
ORCID_REDIRECT_URI = os.environ.get('ORCID_REDIRECT_URI', '')

# Upload directory
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Create the main app
app = FastAPI(title="Editorial Decision Statistics Platform")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============== MODELS ==============

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    orcid: Optional[str] = None
    auth_provider: str = "google"  # google or orcid
    hashed_id: str  # Anonymous identifier for public data
    trust_score: float = 0.0  # Internal trust score (0-100), starts at 0
    contribution_count: int = 0
    validated_count: int = 0  # Count of validated submissions
    validated_with_evidence_count: int = 0  # Validated submissions with evidence
    flagged_count: int = 0  # Count of flagged submissions
    is_admin: bool = False  # Admin role flag
    created_at: datetime

class UserSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    session_id: str
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime

class UserProfileUpdate(BaseModel):
    orcid: Optional[str] = None

class SubmissionModeration(BaseModel):
    status: str  # validated, flagged, pending
    admin_notes: Optional[str] = None

class AdminStats(BaseModel):
    total_users: int
    total_submissions: int
    pending_submissions: int
    validated_submissions: int
    flagged_submissions: int

class Submission(BaseModel):
    model_config = ConfigDict(extra="ignore")
    submission_id: str
    user_hashed_id: str  # Links to user anonymously
    # Manuscript context
    scientific_area: str
    manuscript_type: str
    # Journal context
    journal_id: str
    publisher_id: str
    # Decision process
    decision_type: str
    reviewer_count: str
    time_to_decision: str
    apc_range: str
    # Review characteristics
    review_comments: List[str]
    editor_comments: str
    perceived_coherence: str
    # Evidence (private)
    evidence_file_id: Optional[str] = None
    # Metadata
    created_at: datetime
    status: str = "pending"  # pending, validated, flagged

class SubmissionCreate(BaseModel):
    scientific_area: str
    manuscript_type: str
    journal_id: str
    publisher_id: str
    decision_type: str
    reviewer_count: str
    time_to_decision: str
    apc_range: str
    review_comments: List[str]
    editor_comments: str
    perceived_coherence: str
    # User-added journal/publisher fields
    custom_journal_name: Optional[str] = None
    custom_publisher_name: Optional[str] = None
    custom_journal_open_access: Optional[bool] = None
    custom_journal_apc_required: Optional[str] = None  # yes, no, unknown

class Journal(BaseModel):
    model_config = ConfigDict(extra="ignore")
    journal_id: str
    name: str
    publisher_id: str
    is_user_added: bool = False
    is_verified: bool = True  # False for user-added until promoted
    open_access: Optional[bool] = None
    apc_required: Optional[str] = None
    validated_submission_count: int = 0  # For promotion tracking
    created_at: datetime

class Publisher(BaseModel):
    model_config = ConfigDict(extra="ignore")
    publisher_id: str
    name: str
    is_user_added: bool = False
    is_verified: bool = True  # False for user-added until promoted
    validated_submission_count: int = 0
    created_at: datetime

class EvidenceFile(BaseModel):
    model_config = ConfigDict(extra="ignore")
    file_id: str
    user_hashed_id: str
    encrypted_path: str
    original_filename: str
    mime_type: str
    retention_until: datetime
    created_at: datetime

# ============== AUTH HELPERS ==============

async def get_current_user(request: Request) -> Optional[User]:
    """Get current user from session token (cookie or header)"""
    session_token = request.cookies.get("session_token")
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header[7:]
    
    if not session_token:
        return None
    
    session_doc = await db.user_sessions.find_one(
        {"session_token": session_token},
        {"_id": 0}
    )
    
    if not session_doc:
        return None
    
    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        return None
    
    user_doc = await db.users.find_one(
        {"user_id": session_doc["user_id"]},
        {"_id": 0}
    )
    
    if not user_doc:
        return None
    
    # Convert datetime strings back to datetime objects
    if isinstance(user_doc.get('created_at'), str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    
    return User(**user_doc)

async def require_auth(request: Request) -> User:
    """Require authentication for protected routes"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

async def require_admin(request: Request) -> User:
    """Require admin authentication for admin routes"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def generate_hashed_id(email: str) -> str:
    """Generate anonymous hashed ID from email"""
    salt = os.environ.get('HASH_SALT', 'editorial-stats-salt')
    return hashlib.sha256(f"{email}{salt}".encode()).hexdigest()[:16]

# ============== AUTH ENDPOINTS ==============

@api_router.post("/auth/session")
async def create_session(request: Request, response: Response):
    """Exchange session_id for session_token after Google OAuth"""
    session_id = request.headers.get("X-Session-ID")
    if not session_id:
        body = await request.json()
        session_id = body.get("session_id")
    
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID required")
    
    # Call Emergent auth to get user data
    async with httpx.AsyncClient() as client_http:
        try:
            auth_response = await client_http.get(
                "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
                headers={"X-Session-ID": session_id}
            )
            if auth_response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid session")
            
            user_data = auth_response.json()
        except Exception as e:
            logger.error(f"Auth error: {e}")
            raise HTTPException(status_code=401, detail="Authentication failed")
    
    email = user_data.get("email")
    name = user_data.get("name")
    picture = user_data.get("picture")
    session_token = user_data.get("session_token")
    
    # Check if user exists
    existing_user = await db.users.find_one({"email": email}, {"_id": 0})
    
    if existing_user:
        user_id = existing_user["user_id"]
        # Update name/picture if changed
        await db.users.update_one(
            {"user_id": user_id},
            {"$set": {"name": name, "picture": picture}}
        )
    else:
        # Create new user
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        hashed_id = generate_hashed_id(email)
        
        new_user = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "picture": picture,
            "orcid": None,
            "auth_provider": "google",
            "hashed_id": hashed_id,
            "trust_score": 0.0,  # Start at 0
            "contribution_count": 0,
            "validated_count": 0,
            "validated_with_evidence_count": 0,
            "flagged_count": 0,
            "is_admin": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(new_user)
    
    # Create session
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    session_doc = {
        "session_id": str(uuid.uuid4()),
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": expires_at.isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.user_sessions.insert_one(session_doc)
    
    # Set cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=7 * 24 * 60 * 60
    )
    
    # Get updated user data
    user_doc = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    
    # Calculate if trust score should be visible
    validated_count = user_doc.get("validated_count", 0)
    validated_with_evidence = user_doc.get("validated_with_evidence_count", 0)
    trust_score_visible = validated_count >= 2 or validated_with_evidence >= 1
    
    return {
        "user_id": user_doc["user_id"],
        "email": user_doc["email"],
        "name": user_doc["name"],
        "picture": user_doc.get("picture"),
        "orcid": user_doc.get("orcid"),
        "auth_provider": user_doc.get("auth_provider", "google"),
        "trust_score": user_doc.get("trust_score", 0.0),
        "trust_score_visible": trust_score_visible,
        "contribution_count": user_doc.get("contribution_count", 0),
        "validated_count": validated_count,
        "validated_with_evidence_count": validated_with_evidence,
        "flagged_count": user_doc.get("flagged_count", 0),
        "is_admin": user_doc.get("is_admin", False)
    }

@api_router.get("/auth/me")
async def get_me(request: Request):
    """Get current authenticated user"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Get fresh user data for accurate counts
    user_doc = await db.users.find_one({"user_id": user.user_id}, {"_id": 0})
    
    validated_count = user_doc.get("validated_count", 0)
    validated_with_evidence = user_doc.get("validated_with_evidence_count", 0)
    trust_score_visible = validated_count >= 2 or validated_with_evidence >= 1
    
    return {
        "user_id": user_doc["user_id"],
        "email": user_doc["email"],
        "name": user_doc["name"],
        "picture": user_doc.get("picture"),
        "orcid": user_doc.get("orcid"),
        "auth_provider": user_doc.get("auth_provider", "google"),
        "trust_score": user_doc.get("trust_score", 0.0),
        "trust_score_visible": trust_score_visible,
        "contribution_count": user_doc.get("contribution_count", 0),
        "validated_count": validated_count,
        "validated_with_evidence_count": validated_with_evidence,
        "flagged_count": user_doc.get("flagged_count", 0),
        "is_admin": user_doc.get("is_admin", False)
    }

@api_router.get("/auth/orcid/authorize")
async def orcid_authorize(request: Request):
    """Initiate ORCID OAuth flow - redirect user to ORCID authorization page"""
    if not ORCID_CLIENT_ID:
        raise HTTPException(status_code=500, detail="ORCID OAuth not configured")
    
    if not ORCID_REDIRECT_URI:
        raise HTTPException(status_code=500, detail="ORCID_REDIRECT_URI not configured")
    
    # Get the redirect URL from frontend (where to go after auth completes)
    redirect_after = request.query_params.get("redirect", "/dashboard")
    
    # Store the redirect URL in a temporary state
    state = f"{uuid.uuid4().hex}:{redirect_after}"
    
    # Build ORCID authorization URL with absolute redirect_uri from env
    params = {
        "client_id": ORCID_CLIENT_ID,
        "response_type": "code",
        "scope": "/authenticate",
        "redirect_uri": ORCID_REDIRECT_URI,
        "state": state
    }
    
    auth_url = f"{ORCID_BASE_URL}/oauth/authorize?{urlencode(params)}"
    
    # Log the full URL for debugging
    logger.info(f"ORCID auth URL generated with redirect_uri: {ORCID_REDIRECT_URI}")
    
    return {"authorization_url": auth_url, "state": state}

@api_router.post("/auth/orcid/callback")
async def orcid_callback(request: Request, response: Response):
    """Handle ORCID OAuth callback - exchange code for token and create session"""
    body = await request.json()
    code = body.get("code")
    state = body.get("state")
    
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code required")
    
    if not ORCID_CLIENT_ID or not ORCID_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="ORCID OAuth not configured")
    
    if not ORCID_REDIRECT_URI:
        raise HTTPException(status_code=500, detail="ORCID_REDIRECT_URI not configured")
    
    # Log the redirect_uri being used for token exchange
    logger.info(f"ORCID token exchange with redirect_uri: {ORCID_REDIRECT_URI}")
    
    # Exchange authorization code for access token - MUST use same redirect_uri as authorize
    async with httpx.AsyncClient() as http_client:
        try:
            token_response = await http_client.post(
                f"{ORCID_BASE_URL}/oauth/token",
                data={
                    "client_id": ORCID_CLIENT_ID,
                    "client_secret": ORCID_CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": ORCID_REDIRECT_URI
                },
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            
            if token_response.status_code != 200:
                logger.error(f"ORCID token exchange failed: {token_response.text}")
                raise HTTPException(status_code=401, detail="Failed to authenticate with ORCID")
            
            token_data = token_response.json()
            
        except httpx.RequestError as e:
            logger.error(f"ORCID request error: {e}")
            raise HTTPException(status_code=500, detail="Failed to connect to ORCID")
    
    # Extract ORCID iD and name from token response
    # ORCID returns the iD and name in the token response itself
    orcid_id = token_data.get("orcid")
    name = token_data.get("name")
    
    if not orcid_id:
        raise HTTPException(status_code=400, detail="Could not retrieve ORCID iD")
    
    # Hash the ORCID iD for storage (never store raw ORCID)
    hashed_orcid = hashlib.sha256(f"orcid:{orcid_id}".encode()).hexdigest()
    
    # Create synthetic email for internal use only
    synthetic_email = f"{hashed_orcid[:16]}@orcid.internal"
    
    # Check if user exists by hashed ORCID
    existing_user = await db.users.find_one({"orcid_hash": hashed_orcid}, {"_id": 0})
    
    if existing_user:
        user_id = existing_user["user_id"]
        # Update name if available and different
        if name and name != existing_user.get("name"):
            await db.users.update_one(
                {"user_id": user_id},
                {"$set": {"name": name}}
            )
    else:
        # Create new user with hashed ORCID
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        user_hashed_id = generate_hashed_id(hashed_orcid)
        
        new_user = {
            "user_id": user_id,
            "email": synthetic_email,
            "name": name or "ORCID User",
            "picture": None,
            "orcid_hash": hashed_orcid,  # Store hashed ORCID only
            "auth_provider": "orcid",
            "hashed_id": user_hashed_id,
            "trust_score": 0.0,
            "contribution_count": 0,
            "validated_count": 0,
            "validated_with_evidence_count": 0,
            "flagged_count": 0,
            "is_admin": False,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(new_user)
    
    # Create session (DO NOT store access token long-term)
    session_token = f"orcid_{uuid.uuid4().hex}"
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    session_doc = {
        "session_id": str(uuid.uuid4()),
        "user_id": user_id,
        "session_token": session_token,
        "auth_provider": "orcid",
        "expires_at": expires_at.isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.user_sessions.insert_one(session_doc)
    
    # Set cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=7 * 24 * 60 * 60
    )
    
    # Get updated user data
    user_doc = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    
    validated_count = user_doc.get("validated_count", 0)
    validated_with_evidence = user_doc.get("validated_with_evidence_count", 0)
    trust_score_visible = validated_count >= 2 or validated_with_evidence >= 1
    
    # Parse redirect from state
    redirect_after = "/dashboard"
    if state and ":" in state:
        redirect_after = state.split(":", 1)[1]
    
    return {
        "user_id": user_doc["user_id"],
        "name": user_doc["name"],
        "auth_provider": "orcid",
        "trust_score": user_doc.get("trust_score", 0.0),
        "trust_score_visible": trust_score_visible,
        "contribution_count": user_doc.get("contribution_count", 0),
        "validated_count": validated_count,
        "validated_with_evidence_count": validated_with_evidence,
        "flagged_count": user_doc.get("flagged_count", 0),
        "is_admin": user_doc.get("is_admin", False),
        "redirect": redirect_after
    }

@api_router.get("/auth/orcid/status")
async def orcid_status():
    """Check if ORCID OAuth is configured"""
    return {
        "configured": bool(ORCID_CLIENT_ID and ORCID_CLIENT_SECRET),
        "sandbox": "sandbox" in ORCID_BASE_URL.lower()
    }

@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    """Logout user and clear session"""
    session_token = request.cookies.get("session_token")
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    
    response.delete_cookie(key="session_token", path="/")
    return {"message": "Logged out successfully"}

# ============== USER ENDPOINTS ==============

@api_router.put("/users/profile")
async def update_profile(update: UserProfileUpdate, request: Request):
    """Update user profile (ORCID)"""
    user = await require_auth(request)
    
    update_data = {}
    if update.orcid is not None:
        update_data["orcid"] = update.orcid
    
    if update_data:
        await db.users.update_one(
            {"user_id": user.user_id},
            {"$set": update_data}
        )
    
    user_doc = await db.users.find_one({"user_id": user.user_id}, {"_id": 0})
    return user_doc

# ============== JOURNALS & PUBLISHERS ==============

@api_router.get("/publishers")
async def get_publishers():
    """Get all publishers"""
    publishers = await db.publishers.find({}, {"_id": 0}).sort("name", 1).to_list(1000)
    return publishers

@api_router.get("/journals")
async def get_journals(publisher_id: Optional[str] = None):
    """Get journals, optionally filtered by publisher"""
    query = {}
    if publisher_id:
        query["publisher_id"] = publisher_id
    
    journals = await db.journals.find(query, {"_id": 0}).sort("name", 1).to_list(1000)
    return journals

@api_router.post("/journals")
async def add_journal(request: Request, name: str, publisher_id: str):
    """Add a new journal (user-submitted, flagged for review)"""
    user = await require_auth(request)
    
    journal_id = f"journal_{uuid.uuid4().hex[:12]}"
    journal = {
        "journal_id": journal_id,
        "name": name,
        "publisher_id": publisher_id,
        "is_user_added": True,
        "added_by_hashed_id": user.hashed_id,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.journals.insert_one(journal)
    
    return {"journal_id": journal_id, "name": name, "publisher_id": publisher_id}

# ============== SUBMISSIONS ==============

@api_router.post("/submissions")
async def create_submission(submission: SubmissionCreate, request: Request):
    """Create a new editorial decision submission"""
    user = await require_auth(request)
    
    submission_id = f"sub_{uuid.uuid4().hex[:12]}"
    
    publisher_id = submission.publisher_id
    journal_id = submission.journal_id
    
    # Handle user-added publisher ("other")
    if submission.publisher_id == "other" and submission.custom_publisher_name:
        publisher_id = f"pub_user_{uuid.uuid4().hex[:12]}"
        new_publisher = {
            "publisher_id": publisher_id,
            "name": submission.custom_publisher_name.strip(),
            "is_user_added": True,
            "is_verified": False,
            "validated_submission_count": 0,
            "added_by_hashed_id": user.hashed_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.publishers.insert_one(new_publisher)
    
    # Handle user-added journal ("other")
    if submission.journal_id == "other" and submission.custom_journal_name:
        journal_id = f"journal_user_{uuid.uuid4().hex[:12]}"
        new_journal = {
            "journal_id": journal_id,
            "name": submission.custom_journal_name.strip(),
            "publisher_id": publisher_id,
            "is_user_added": True,
            "is_verified": False,
            "open_access": submission.custom_journal_open_access,
            "apc_required": submission.custom_journal_apc_required,
            "validated_submission_count": 0,
            "added_by_hashed_id": user.hashed_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.journals.insert_one(new_journal)
    
    submission_doc = {
        "submission_id": submission_id,
        "user_hashed_id": user.hashed_id,
        "scientific_area": submission.scientific_area,
        "manuscript_type": submission.manuscript_type,
        "journal_id": journal_id,
        "publisher_id": publisher_id,
        "decision_type": submission.decision_type,
        "reviewer_count": submission.reviewer_count,
        "time_to_decision": submission.time_to_decision,
        "apc_range": submission.apc_range,
        "review_comments": submission.review_comments,
        "editor_comments": submission.editor_comments,
        "perceived_coherence": submission.perceived_coherence,
        "evidence_file_id": None,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.submissions.insert_one(submission_doc)
    
    # Update user contribution count (trust score updated on validation, not submission)
    await db.users.update_one(
        {"user_id": user.user_id},
        {"$inc": {"contribution_count": 1}}
    )
    
    return {"submission_id": submission_id, "status": "pending"}

@api_router.post("/submissions/{submission_id}/evidence")
async def upload_evidence(
    submission_id: str,
    request: Request,
    file: UploadFile = File(...)
):
    """Upload evidence file for a submission (encrypted storage)"""
    user = await require_auth(request)
    
    # Verify submission belongs to user
    submission = await db.submissions.find_one(
        {"submission_id": submission_id, "user_hashed_id": user.hashed_id},
        {"_id": 0}
    )
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Read and encrypt file
    content = await file.read()
    encrypted_content = fernet.encrypt(content)
    
    # Save encrypted file
    file_id = f"evidence_{uuid.uuid4().hex[:12]}"
    file_path = UPLOAD_DIR / f"{file_id}.enc"
    
    with open(file_path, "wb") as f:
        f.write(encrypted_content)
    
    # Save file metadata
    retention_until = datetime.now(timezone.utc) + timedelta(days=365)  # 12 months retention
    evidence_doc = {
        "file_id": file_id,
        "user_hashed_id": user.hashed_id,
        "encrypted_path": str(file_path),
        "original_filename": file.filename,
        "mime_type": file.content_type,
        "retention_until": retention_until.isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.evidence_files.insert_one(evidence_doc)
    
    # Update submission with file reference
    await db.submissions.update_one(
        {"submission_id": submission_id},
        {"$set": {"evidence_file_id": file_id}}
    )
    
    return {"file_id": file_id, "status": "uploaded"}

@api_router.get("/submissions/my")
async def get_my_submissions(request: Request):
    """Get current user's submissions"""
    user = await require_auth(request)
    
    submissions = await db.submissions.find(
        {"user_hashed_id": user.hashed_id},
        {"_id": 0}
    ).sort("created_at", -1).to_list(1000)
    
    # Enrich with journal/publisher names
    for sub in submissions:
        journal = await db.journals.find_one({"journal_id": sub["journal_id"]}, {"_id": 0, "name": 1})
        publisher = await db.publishers.find_one({"publisher_id": sub["publisher_id"]}, {"_id": 0, "name": 1})
        sub["journal_name"] = journal["name"] if journal else "Unknown"
        sub["publisher_name"] = publisher["name"] if publisher else "Unknown"
    
    return submissions

# ============== ANALYTICS ENDPOINTS ==============

K_ANONYMITY_THRESHOLD = 5  # Minimum cases for public display

@api_router.get("/analytics/overview")
async def get_analytics_overview():
    """Get overall platform statistics"""
    total_submissions = await db.submissions.count_documents({"status": {"$ne": "flagged"}})
    
    if total_submissions < K_ANONYMITY_THRESHOLD:
        return {
            "total_submissions": total_submissions,
            "sufficient_data": False,
            "message": "Insufficient data for aggregated statistics"
        }
    
    # Decision type distribution
    decision_pipeline = [
        {"$match": {"status": {"$ne": "flagged"}}},
        {"$group": {"_id": "$decision_type", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gte": K_ANONYMITY_THRESHOLD}}}
    ]
    decision_dist = await db.submissions.aggregate(decision_pipeline).to_list(100)
    
    # Reviewer count distribution
    reviewer_pipeline = [
        {"$match": {"status": {"$ne": "flagged"}}},
        {"$group": {"_id": "$reviewer_count", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gte": K_ANONYMITY_THRESHOLD}}}
    ]
    reviewer_dist = await db.submissions.aggregate(reviewer_pipeline).to_list(100)
    
    # Time to decision distribution
    time_pipeline = [
        {"$match": {"status": {"$ne": "flagged"}}},
        {"$group": {"_id": "$time_to_decision", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gte": K_ANONYMITY_THRESHOLD}}}
    ]
    time_dist = await db.submissions.aggregate(time_pipeline).to_list(100)
    
    return {
        "total_submissions": total_submissions,
        "sufficient_data": True,
        "decision_distribution": {d["_id"]: d["count"] for d in decision_dist},
        "reviewer_distribution": {d["_id"]: d["count"] for d in reviewer_dist},
        "time_distribution": {d["_id"]: d["count"] for d in time_dist}
    }

@api_router.get("/analytics/publishers")
async def get_publisher_analytics():
    """Get publisher-level analytics (only verified publishers)"""
    # Get list of verified publisher IDs
    verified_publishers = await db.publishers.find(
        {"$or": [{"is_verified": True}, {"is_verified": {"$exists": False}}]},
        {"_id": 0, "publisher_id": 1}
    ).to_list(1000)
    verified_pub_ids = [p["publisher_id"] for p in verified_publishers]
    
    pipeline = [
        {"$match": {"status": {"$ne": "flagged"}, "publisher_id": {"$in": verified_pub_ids}}},
        {"$group": {
            "_id": "$publisher_id",
            "total_cases": {"$sum": 1},
            "desk_rejects": {"$sum": {"$cond": [{"$eq": ["$decision_type", "desk_reject"]}, 1, 0]}},
            "no_reviewer": {"$sum": {"$cond": [{"$eq": ["$reviewer_count", "0"]}, 1, 0]}},
            "one_reviewer": {"$sum": {"$cond": [{"$eq": ["$reviewer_count", "1"]}, 1, 0]}},
            "generic_reviews": {"$sum": {"$cond": [{"$in": ["generic_editorial", "$review_comments"]}, 1, 0]}},
            "editor_technical": {"$sum": {"$cond": [{"$eq": ["$editor_comments", "yes_technical"]}, 1, 0]}},
            "coherent_reviews": {"$sum": {"$cond": [{"$eq": ["$perceived_coherence", "yes"]}, 1, 0]}}
        }},
        {"$match": {"total_cases": {"$gte": K_ANONYMITY_THRESHOLD}}}
    ]
    
    results = await db.submissions.aggregate(pipeline).to_list(1000)
    
    # Enrich with publisher names and calculate scores
    analytics = []
    for r in results:
        publisher = await db.publishers.find_one({"publisher_id": r["_id"]}, {"_id": 0})
        if not publisher:
            continue
        
        total = r["total_cases"]
        
        # Calculate multi-dimensional scores (0-100)
        # Transparency: Based on reviewer presence and editor engagement
        transparency_score = round(100 - ((r["no_reviewer"] / total) * 50) - ((r["desk_rejects"] / total) * 30), 1)
        
        # Review Depth: Based on number of reviewers and non-generic reviews
        review_depth_score = round(100 - ((r["one_reviewer"] / total) * 40) - ((r["generic_reviews"] / total) * 40), 1)
        
        # Editorial Effort: Based on editor technical comments
        editorial_effort_score = round((r["editor_technical"] / total) * 100, 1)
        
        # Consistency: Based on coherent reviews
        consistency_score = round((r["coherent_reviews"] / total) * 100, 1)
        
        analytics.append({
            "publisher_id": r["_id"],
            "publisher_name": publisher["name"],
            "total_cases": total,
            "transparency_score": max(0, min(100, transparency_score)),
            "review_depth_score": max(0, min(100, review_depth_score)),
            "editorial_effort_score": max(0, min(100, editorial_effort_score)),
            "consistency_score": max(0, min(100, consistency_score)),
            "desk_reject_rate": round((r["desk_rejects"] / total) * 100, 1),
            "no_peer_review_rate": round((r["no_reviewer"] / total) * 100, 1)
        })
    
    return analytics

@api_router.get("/analytics/journals")
async def get_journal_analytics(publisher_id: Optional[str] = None):
    """Get journal-level analytics (only verified journals)"""
    # Get list of verified journal IDs
    journal_query = {"$or": [{"is_verified": True}, {"is_verified": {"$exists": False}}]}
    if publisher_id:
        journal_query["publisher_id"] = publisher_id
    
    verified_journals = await db.journals.find(
        journal_query,
        {"_id": 0, "journal_id": 1}
    ).to_list(1000)
    verified_journal_ids = [j["journal_id"] for j in verified_journals]
    
    match_stage = {"status": {"$ne": "flagged"}, "journal_id": {"$in": verified_journal_ids}}
    if publisher_id:
        match_stage["publisher_id"] = publisher_id
    
    pipeline = [
        {"$match": match_stage},
        {"$group": {
            "_id": "$journal_id",
            "publisher_id": {"$first": "$publisher_id"},
            "total_cases": {"$sum": 1},
            "desk_rejects": {"$sum": {"$cond": [{"$eq": ["$decision_type", "desk_reject"]}, 1, 0]}},
            "no_reviewer": {"$sum": {"$cond": [{"$eq": ["$reviewer_count", "0"]}, 1, 0]}},
            "one_reviewer": {"$sum": {"$cond": [{"$eq": ["$reviewer_count", "1"]}, 1, 0]}},
            "generic_reviews": {"$sum": {"$cond": [{"$in": ["generic_editorial", "$review_comments"]}, 1, 0]}},
            "editor_technical": {"$sum": {"$cond": [{"$eq": ["$editor_comments", "yes_technical"]}, 1, 0]}},
            "coherent_reviews": {"$sum": {"$cond": [{"$eq": ["$perceived_coherence", "yes"]}, 1, 0]}}
        }},
        {"$match": {"total_cases": {"$gte": K_ANONYMITY_THRESHOLD}}}
    ]
    
    results = await db.submissions.aggregate(pipeline).to_list(1000)
    
    analytics = []
    for r in results:
        journal = await db.journals.find_one({"journal_id": r["_id"]}, {"_id": 0})
        publisher = await db.publishers.find_one({"publisher_id": r["publisher_id"]}, {"_id": 0})
        if not journal or not publisher:
            continue
        
        total = r["total_cases"]
        
        transparency_score = round(100 - ((r["no_reviewer"] / total) * 50) - ((r["desk_rejects"] / total) * 30), 1)
        review_depth_score = round(100 - ((r["one_reviewer"] / total) * 40) - ((r["generic_reviews"] / total) * 40), 1)
        editorial_effort_score = round((r["editor_technical"] / total) * 100, 1)
        consistency_score = round((r["coherent_reviews"] / total) * 100, 1)
        
        analytics.append({
            "journal_id": r["_id"],
            "journal_name": journal["name"],
            "publisher_id": r["publisher_id"],
            "publisher_name": publisher["name"],
            "total_cases": total,
            "transparency_score": max(0, min(100, transparency_score)),
            "review_depth_score": max(0, min(100, review_depth_score)),
            "editorial_effort_score": max(0, min(100, editorial_effort_score)),
            "consistency_score": max(0, min(100, consistency_score)),
            "desk_reject_rate": round((r["desk_rejects"] / total) * 100, 1),
            "no_peer_review_rate": round((r["no_reviewer"] / total) * 100, 1)
        })
    
    return analytics

@api_router.get("/analytics/areas")
async def get_area_analytics():
    """Get scientific area analytics"""
    pipeline = [
        {"$match": {"status": {"$ne": "flagged"}}},
        {"$group": {
            "_id": "$scientific_area",
            "total_cases": {"$sum": 1},
            "desk_rejects": {"$sum": {"$cond": [{"$eq": ["$decision_type", "desk_reject"]}, 1, 0]}},
            "no_reviewer": {"$sum": {"$cond": [{"$eq": ["$reviewer_count", "0"]}, 1, 0]}},
            "fast_decisions": {"$sum": {"$cond": [{"$eq": ["$time_to_decision", "0-30"]}, 1, 0]}},
            "slow_decisions": {"$sum": {"$cond": [{"$eq": ["$time_to_decision", "90+"]}, 1, 0]}}
        }},
        {"$match": {"total_cases": {"$gte": K_ANONYMITY_THRESHOLD}}}
    ]
    
    results = await db.submissions.aggregate(pipeline).to_list(100)
    
    return [{
        "area": r["_id"],
        "total_cases": r["total_cases"],
        "desk_reject_rate": round((r["desk_rejects"] / r["total_cases"]) * 100, 1),
        "no_peer_review_rate": round((r["no_reviewer"] / r["total_cases"]) * 100, 1),
        "fast_decision_rate": round((r["fast_decisions"] / r["total_cases"]) * 100, 1),
        "slow_decision_rate": round((r["slow_decisions"] / r["total_cases"]) * 100, 1)
    } for r in results]

# ============== FORM OPTIONS ==============

@api_router.get("/options/scientific-areas")
async def get_scientific_areas():
    """Get list of scientific areas"""
    return [
        {"id": "life_sciences", "name": "Life Sciences"},
        {"id": "physical_sciences", "name": "Physical Sciences"},
        {"id": "earth_environmental", "name": "Earth & Environmental Sciences"},
        {"id": "health_sciences", "name": "Health Sciences"},
        {"id": "social_sciences", "name": "Social Sciences"},
        {"id": "humanities", "name": "Humanities"},
        {"id": "engineering", "name": "Engineering & Technology"},
        {"id": "mathematics", "name": "Mathematics & Statistics"},
        {"id": "computer_science", "name": "Computer Science"},
        {"id": "agriculture", "name": "Agriculture & Food Sciences"},
        {"id": "interdisciplinary", "name": "Interdisciplinary"}
    ]

@api_router.get("/options/manuscript-types")
async def get_manuscript_types():
    """Get list of manuscript types"""
    return [
        {"id": "experimental", "name": "Experimental"},
        {"id": "methodological", "name": "Methodological"},
        {"id": "review", "name": "Review"},
        {"id": "short_communication", "name": "Short Communication"}
    ]

@api_router.get("/options/decision-types")
async def get_decision_types():
    """Get list of decision types"""
    return [
        {"id": "desk_reject", "name": "Desk Reject"},
        {"id": "reject_after_review", "name": "Reject After Review"},
        {"id": "major_revision", "name": "Major Revision"},
        {"id": "minor_revision", "name": "Minor Revision"}
    ]

@api_router.get("/options/reviewer-counts")
async def get_reviewer_counts():
    """Get reviewer count options"""
    return [
        {"id": "0", "name": "0 (No reviewers)"},
        {"id": "1", "name": "1 reviewer"},
        {"id": "2+", "name": "2 or more reviewers"}
    ]

@api_router.get("/options/time-ranges")
async def get_time_ranges():
    """Get time to decision ranges"""
    return [
        {"id": "0-30", "name": "0–30 days"},
        {"id": "31-90", "name": "31–90 days"},
        {"id": "90+", "name": "90+ days"}
    ]

@api_router.get("/options/apc-ranges")
async def get_apc_ranges():
    """Get APC ranges"""
    return [
        {"id": "no_apc", "name": "No APC"},
        {"id": "under_1000", "name": "< $1,000"},
        {"id": "1000_3000", "name": "$1,000–$3,000"},
        {"id": "over_3000", "name": "> $3,000"}
    ]

@api_router.get("/options/review-comment-types")
async def get_review_comment_types():
    """Get review comment types"""
    return [
        {"id": "methodology", "name": "Methodology"},
        {"id": "statistics", "name": "Statistics"},
        {"id": "conceptual", "name": "Conceptual Discussion"},
        {"id": "formatting_language", "name": "Formatting/Language Only"},
        {"id": "generic_editorial", "name": "Generic/Editorial Only"}
    ]

@api_router.get("/options/editor-comment-types")
async def get_editor_comment_types():
    """Get editor comment types"""
    return [
        {"id": "yes_technical", "name": "Yes – Technical"},
        {"id": "yes_generic", "name": "Yes – Generic"},
        {"id": "no", "name": "No"}
    ]

@api_router.get("/options/coherence-options")
async def get_coherence_options():
    """Get perceived coherence options"""
    return [
        {"id": "yes", "name": "Yes"},
        {"id": "partially", "name": "Partially"},
        {"id": "no", "name": "No"}
    ]

# ============== ADMIN ENDPOINTS ==============

@api_router.get("/admin/stats")
async def get_admin_stats(request: Request):
    """Get admin dashboard statistics"""
    await require_admin(request)
    
    total_users = await db.users.count_documents({})
    total_submissions = await db.submissions.count_documents({})
    pending_submissions = await db.submissions.count_documents({"status": "pending"})
    validated_submissions = await db.submissions.count_documents({"status": "validated"})
    flagged_submissions = await db.submissions.count_documents({"status": "flagged"})
    
    return {
        "total_users": total_users,
        "total_submissions": total_submissions,
        "pending_submissions": pending_submissions,
        "validated_submissions": validated_submissions,
        "flagged_submissions": flagged_submissions
    }

@api_router.get("/admin/submissions")
async def get_all_submissions(
    request: Request,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    """Get all submissions for admin review"""
    await require_admin(request)
    
    query = {}
    if status:
        query["status"] = status
    
    submissions = await db.submissions.find(
        query,
        {"_id": 0}
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    # Enrich with journal/publisher names
    for sub in submissions:
        journal = await db.journals.find_one({"journal_id": sub["journal_id"]}, {"_id": 0, "name": 1})
        publisher = await db.publishers.find_one({"publisher_id": sub["publisher_id"]}, {"_id": 0, "name": 1})
        sub["journal_name"] = journal["name"] if journal else "Unknown"
        sub["publisher_name"] = publisher["name"] if publisher else "Unknown"
        
        # Check if has evidence
        sub["has_evidence"] = sub.get("evidence_file_id") is not None
    
    total = await db.submissions.count_documents(query)
    
    return {
        "submissions": submissions,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@api_router.get("/admin/submissions/{submission_id}")
async def get_submission_detail(submission_id: str, request: Request):
    """Get detailed submission for admin review"""
    await require_admin(request)
    
    submission = await db.submissions.find_one(
        {"submission_id": submission_id},
        {"_id": 0}
    )
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Enrich with journal/publisher info
    journal = await db.journals.find_one({"journal_id": submission["journal_id"]}, {"_id": 0})
    publisher = await db.publishers.find_one({"publisher_id": submission["publisher_id"]}, {"_id": 0})
    submission["journal"] = journal
    submission["publisher"] = publisher
    
    # Get evidence file info if exists
    if submission.get("evidence_file_id"):
        evidence = await db.evidence_files.find_one(
            {"file_id": submission["evidence_file_id"]},
            {"_id": 0, "encrypted_path": 0}  # Don't expose encrypted path
        )
        submission["evidence"] = evidence
    
    # Get moderation history
    moderation_history = await db.moderation_logs.find(
        {"submission_id": submission_id},
        {"_id": 0}
    ).sort("created_at", -1).to_list(100)
    submission["moderation_history"] = moderation_history
    
    return submission

@api_router.put("/admin/submissions/{submission_id}/moderate")
async def moderate_submission(
    submission_id: str,
    moderation: SubmissionModeration,
    request: Request
):
    """Moderate a submission (validate, flag, or set pending)"""
    admin = await require_admin(request)
    
    # Validate status
    if moderation.status not in ["pending", "validated", "flagged"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    submission = await db.submissions.find_one(
        {"submission_id": submission_id},
        {"_id": 0}
    )
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    old_status = submission["status"]
    has_evidence = submission.get("evidence_file_id") is not None
    
    # Update submission status
    await db.submissions.update_one(
        {"submission_id": submission_id},
        {"$set": {
            "status": moderation.status,
            "moderated_at": datetime.now(timezone.utc).isoformat(),
            "moderated_by": admin.user_id
        }}
    )
    
    # Log moderation action
    log_entry = {
        "log_id": f"log_{uuid.uuid4().hex[:12]}",
        "submission_id": submission_id,
        "admin_user_id": admin.user_id,
        "admin_name": admin.name,
        "old_status": old_status,
        "new_status": moderation.status,
        "notes": moderation.admin_notes,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.moderation_logs.insert_one(log_entry)
    
    # Update user trust score and counts based on moderation
    # Trust Score Rules: +20 per validated, +10 per validated with evidence, -15 per flagged
    user_update = {}
    
    if moderation.status == "validated" and old_status != "validated":
        # Validated: +20 points, +10 if has evidence
        score_increase = 20 + (10 if has_evidence else 0)
        user_update["$inc"] = {
            "validated_count": 1,
            "trust_score": score_increase
        }
        if has_evidence:
            user_update["$inc"]["validated_with_evidence_count"] = 1
        
        # Update journal/publisher validated count for promotion tracking
        await db.journals.update_one(
            {"journal_id": submission["journal_id"]},
            {"$inc": {"validated_submission_count": 1}}
        )
        await db.publishers.update_one(
            {"publisher_id": submission["publisher_id"]},
            {"$inc": {"validated_submission_count": 1}}
        )
        
        # Check if user-added journal should be promoted to verified
        await check_and_promote_journal(submission["journal_id"])
        await check_and_promote_publisher(submission["publisher_id"])
        
    elif moderation.status == "flagged" and old_status != "flagged":
        # Flagged: -15 points
        user_update["$inc"] = {
            "flagged_count": 1,
            "trust_score": -15
        }
    elif old_status == "validated" and moderation.status != "validated":
        # Reverting from validated: remove the points
        score_decrease = 20 + (10 if has_evidence else 0)
        user_update["$inc"] = {
            "validated_count": -1,
            "trust_score": -score_decrease
        }
        if has_evidence:
            user_update["$inc"]["validated_with_evidence_count"] = -1
        
        # Decrease journal/publisher count
        await db.journals.update_one(
            {"journal_id": submission["journal_id"]},
            {"$inc": {"validated_submission_count": -1}}
        )
        await db.publishers.update_one(
            {"publisher_id": submission["publisher_id"]},
            {"$inc": {"validated_submission_count": -1}}
        )
    elif old_status == "flagged" and moderation.status != "flagged":
        # Reverting from flagged: restore points
        user_update["$inc"] = {
            "flagged_count": -1,
            "trust_score": 15
        }
    
    if user_update:
        await db.users.update_one(
            {"hashed_id": submission["user_hashed_id"]},
            user_update
        )
        # Ensure trust score stays within 0-100
        await db.users.update_one(
            {"hashed_id": submission["user_hashed_id"], "trust_score": {"$lt": 0}},
            {"$set": {"trust_score": 0}}
        )
        await db.users.update_one(
            {"hashed_id": submission["user_hashed_id"], "trust_score": {"$gt": 100}},
            {"$set": {"trust_score": 100}}
        )
    
    return {"message": "Submission moderated successfully", "status": moderation.status}

async def check_and_promote_journal(journal_id: str):
    """Check if a user-added journal should be promoted to verified"""
    journal = await db.journals.find_one({"journal_id": journal_id}, {"_id": 0})
    if not journal or not journal.get("is_user_added") or journal.get("is_verified"):
        return
    
    # Promotion requires 3+ validated submissions
    if journal.get("validated_submission_count", 0) >= 3:
        await db.journals.update_one(
            {"journal_id": journal_id},
            {"$set": {"is_verified": True}}
        )
        logger.info(f"Journal {journal['name']} promoted to verified status")

async def check_and_promote_publisher(publisher_id: str):
    """Check if a user-added publisher should be promoted to verified"""
    publisher = await db.publishers.find_one({"publisher_id": publisher_id}, {"_id": 0})
    if not publisher or not publisher.get("is_user_added") or publisher.get("is_verified"):
        return
    
    # Promotion requires 3+ validated submissions
    if publisher.get("validated_submission_count", 0) >= 3:
        await db.publishers.update_one(
            {"publisher_id": publisher_id},
            {"$set": {"is_verified": True}}
        )
        logger.info(f"Publisher {publisher['name']} promoted to verified status")

@api_router.get("/admin/evidence/{file_id}")
async def get_evidence_file(file_id: str, request: Request):
    """Get decrypted evidence file for admin review"""
    from fastapi.responses import StreamingResponse
    import io
    
    await require_admin(request)
    
    evidence = await db.evidence_files.find_one(
        {"file_id": file_id},
        {"_id": 0}
    )
    
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence file not found")
    
    # Read and decrypt file
    try:
        encrypted_path = Path(evidence["encrypted_path"])
        if not encrypted_path.exists():
            raise HTTPException(status_code=404, detail="File not found on disk")
        
        with open(encrypted_path, "rb") as f:
            encrypted_content = f.read()
        
        decrypted_content = fernet.decrypt(encrypted_content)
        
        return StreamingResponse(
            io.BytesIO(decrypted_content),
            media_type=evidence["mime_type"],
            headers={
                "Content-Disposition": f'inline; filename="{evidence["original_filename"]}"'
            }
        )
    except Exception as e:
        logger.error(f"Error decrypting evidence: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving evidence file")

@api_router.get("/admin/users")
async def get_admin_users(
    request: Request,
    skip: int = 0,
    limit: int = 50
):
    """Get all users for admin review"""
    await require_admin(request)
    
    users = await db.users.find(
        {},
        {"_id": 0, "hashed_id": 0}  # Don't expose hashed_id
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    total = await db.users.count_documents({})
    
    return {
        "users": users,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@api_router.put("/admin/users/{user_id}/toggle-admin")
async def toggle_admin_status(user_id: str, request: Request):
    """Toggle admin status for a user"""
    admin = await require_admin(request)
    
    # Prevent self-demotion
    if admin.user_id == user_id:
        raise HTTPException(status_code=400, detail="Cannot modify your own admin status")
    
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_admin_status = not user.get("is_admin", False)
    
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"is_admin": new_admin_status}}
    )
    
    return {"user_id": user_id, "is_admin": new_admin_status}

# ============== HEALTH CHECK ==============

@api_router.get("/")
async def root():
    return {"message": "Editorial Decision Statistics Platform API", "status": "running"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
