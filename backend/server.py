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

# Platform Settings Models
class PlatformSettingsUpdate(BaseModel):
    visibility_mode: Optional[str] = None  # user_only, threshold_based, admin_forced
    demo_mode_enabled: Optional[bool] = None
    public_stats_enabled: Optional[bool] = None
    min_submissions_per_journal: Optional[int] = None
    min_unique_users_per_journal: Optional[int] = None

class VisibilityOverride(BaseModel):
    entity_type: str  # journal, publisher, area
    entity_id: str
    force_visible: bool

class Submission(BaseModel):
    model_config = ConfigDict(extra="ignore")
    submission_id: str
    user_hashed_id: str  # Links to user anonymously
    # Manuscript context - CNPq hierarchical areas
    scientific_area: str  # Legacy field (kept for backwards compatibility)
    scientific_area_grande: Optional[str] = None  # CNPq Grande Área code (e.g., "1")
    scientific_area_area: Optional[str] = None  # CNPq Área code (e.g., "1.01")
    scientific_area_subarea: Optional[str] = None  # CNPq Subárea code (e.g., "1.01.01")
    manuscript_type: str
    # Journal context
    journal_id: str
    publisher_id: str
    # Decision process
    decision_type: str
    reviewer_count: str
    time_to_decision: str
    apc_range: str
    # Review characteristics (legacy)
    review_comments: List[str]
    editor_comments: str
    perceived_coherence: str
    # NEW: Quality assessment fields (neutral, captures positive/neutral/negative)
    overall_review_quality: Optional[int] = None  # 1-5 scale (very low → very high)
    feedback_clarity: Optional[int] = None  # 1-5 scale (very unclear → very clear)
    decision_fairness: Optional[str] = None  # agree / neutral / disagree
    would_recommend: Optional[str] = None  # yes / neutral / no
    # Evidence (private)
    evidence_file_id: Optional[str] = None
    # Metadata
    created_at: datetime
    status: str = "pending"  # pending, validated, flagged
    is_sample: bool = False  # Flag for sample/demo data
    valid_for_stats: bool = True  # Flag for statistical validity

class SubmissionCreate(BaseModel):
    # CNPq hierarchical scientific areas
    scientific_area: Optional[str] = None  # Legacy field (deprecated but kept for compatibility)
    scientific_area_grande: Optional[str] = None  # CNPq Grande Área code (e.g., "1")
    scientific_area_area: Optional[str] = None  # CNPq Área code (e.g., "1.01")
    scientific_area_subarea: Optional[str] = None  # CNPq Subárea code (e.g., "1.01.01") - optional
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
    # NEW: Quality assessment fields (neutral, captures positive/neutral/negative)
    overall_review_quality: Optional[int] = None  # 1-5 scale
    feedback_clarity: Optional[int] = None  # 1-5 scale
    decision_fairness: Optional[str] = None  # agree / neutral / disagree
    would_recommend: Optional[str] = None  # yes / neutral / no
    # User-added journal/publisher fields
    custom_journal_name: Optional[str] = None
    custom_publisher_name: Optional[str] = None
    custom_journal_open_access: Optional[bool] = None
    custom_journal_apc_required: Optional[str] = None  # yes, no, unknown
    # CONDITIONAL FIELDS - Open Access / APC
    journal_is_open_access: Optional[bool] = None  # Controls if APC questions should appear
    # CONDITIONAL FIELDS - Editor comments quality (only if comments were provided)
    editor_comments_quality: Optional[int] = None  # 1-5 scale (only if editor_comments != 'no')

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

# ============== PLATFORM SETTINGS HELPERS ==============

# Default settings (used when no settings exist in DB)
DEFAULT_PLATFORM_SETTINGS = {
    "settings_id": "global",
    "visibility_mode": "user_only",
    "demo_mode_enabled": True,
    "public_stats_enabled": False,
    "min_submissions_per_journal": 3,
    "min_unique_users_per_journal": 3,
    "visibility_overrides": {
        "journals": {},
        "publishers": {},
        "areas": {}
    }
}

async def get_platform_settings() -> dict:
    """Get current platform settings, create defaults if not exist"""
    settings = await db.platform_settings.find_one({"settings_id": "global"}, {"_id": 0})
    if not settings:
        settings = DEFAULT_PLATFORM_SETTINGS.copy()
        settings["created_at"] = datetime.now(timezone.utc).isoformat()
        settings["updated_at"] = datetime.now(timezone.utc).isoformat()
        await db.platform_settings.insert_one(settings)
    return settings

async def get_submission_base_query(settings: dict, include_sample: bool = None) -> dict:
    """Build base query for submissions based on settings
    
    Args:
        settings: Platform settings dict
        include_sample: Override for sample data inclusion. If None, uses demo_mode_enabled
    
    Returns:
        MongoDB query dict
    """
    query = {
        "status": {"$ne": "flagged"},
        "valid_for_stats": {"$ne": False}  # Only include statistically valid submissions
    }
    
    # Determine if we should include sample data
    if include_sample is None:
        include_sample = settings.get("demo_mode_enabled", True)
    
    if not include_sample:
        # Exclude sample data - only real user submissions
        query["is_sample"] = {"$ne": True}
    
    return query

async def check_journal_visibility(journal_id: str, settings: dict) -> dict:
    """Check if a journal meets visibility thresholds
    
    Returns:
        {
            "visible": bool,
            "reason": str,
            "submission_count": int,
            "unique_users": int,
            "threshold_met": bool
        }
    """
    # Check for admin override
    overrides = settings.get("visibility_overrides", {}).get("journals", {})
    if journal_id in overrides:
        return {
            "visible": overrides[journal_id],
            "reason": "admin_override",
            "submission_count": 0,
            "unique_users": 0,
            "threshold_met": False
        }
    
    # Check visibility mode
    mode = settings.get("visibility_mode", "user_only")
    if mode == "user_only":
        return {
            "visible": False,
            "reason": "user_only_mode",
            "submission_count": 0,
            "unique_users": 0,
            "threshold_met": False
        }
    
    if mode == "admin_forced":
        return {
            "visible": settings.get("public_stats_enabled", False),
            "reason": "admin_forced",
            "submission_count": 0,
            "unique_users": 0,
            "threshold_met": True
        }
    
    # Threshold-based mode - check actual data
    base_query = await get_submission_base_query(settings)
    base_query["journal_id"] = journal_id
    
    # Count submissions
    submission_count = await db.submissions.count_documents(base_query)
    
    # Count unique users
    unique_users_pipeline = [
        {"$match": base_query},
        {"$group": {"_id": "$user_hashed_id"}},
        {"$count": "count"}
    ]
    unique_result = await db.submissions.aggregate(unique_users_pipeline).to_list(1)
    unique_users = unique_result[0]["count"] if unique_result else 0
    
    min_submissions = settings.get("min_submissions_per_journal", 3)
    min_users = settings.get("min_unique_users_per_journal", 3)
    
    threshold_met = submission_count >= min_submissions and unique_users >= min_users
    
    return {
        "visible": threshold_met and settings.get("public_stats_enabled", False),
        "reason": "threshold_check",
        "submission_count": submission_count,
        "unique_users": unique_users,
        "threshold_met": threshold_met
    }

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
    
    # Determine scientific_area from hierarchical fields (backwards compatibility)
    scientific_area = submission.scientific_area
    if submission.scientific_area_grande:
        # Use hierarchical fields if provided
        scientific_area = submission.scientific_area_grande
        if submission.scientific_area_area:
            scientific_area = submission.scientific_area_area
        if submission.scientific_area_subarea:
            scientific_area = submission.scientific_area_subarea
    
    # Validate submission for statistical validity
    valid_for_stats, validation_flags = await validate_submission_for_stats(
        user.hashed_id, journal_id, submission
    )
    
    submission_doc = {
        "submission_id": submission_id,
        "user_hashed_id": user.hashed_id,
        # CNPq hierarchical scientific areas
        "scientific_area": scientific_area,  # Most specific level selected
        "scientific_area_grande": submission.scientific_area_grande,
        "scientific_area_area": submission.scientific_area_area,
        "scientific_area_subarea": submission.scientific_area_subarea,
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
        # NEW: Quality assessment fields
        "overall_review_quality": getattr(submission, 'overall_review_quality', None),
        "feedback_clarity": getattr(submission, 'feedback_clarity', None),
        "decision_fairness": getattr(submission, 'decision_fairness', None),
        "would_recommend": getattr(submission, 'would_recommend', None),
        # CONDITIONAL FIELDS
        "journal_is_open_access": getattr(submission, 'journal_is_open_access', None),
        "editor_comments_quality": getattr(submission, 'editor_comments_quality', None),
        # Metadata
        "evidence_file_id": None,
        "status": "pending",
        "is_sample": False,
        "valid_for_stats": valid_for_stats,
        "validation_flags": validation_flags,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.submissions.insert_one(submission_doc)
    
    # Update user contribution count (trust score updated on validation, not submission)
    await db.users.update_one(
        {"user_id": user.user_id},
        {"$inc": {"contribution_count": 1}}
    )
    
    return {"submission_id": submission_id, "status": "pending", "valid_for_stats": valid_for_stats}


async def validate_submission_for_stats(user_hashed_id: str, journal_id: str, submission) -> tuple:
    """
    Validate if a submission should be included in aggregated statistics.
    
    Returns:
        tuple: (valid_for_stats: bool, validation_flags: dict)
    
    Checks:
    1. Completeness - all required fields present
    2. Logical consistency - no contradictory responses
    3. Conditional field validation - conditional fields only present when appropriate
    4. Duplicates - not a duplicate submission (same user + journal within 30 days)
    """
    flags = {
        "is_complete": True,
        "is_consistent": True,
        "is_unique": True,
        "issues": []
    }
    
    # 1. Check completeness (required fields)
    # Note: scientific_area can be the legacy field OR the hierarchical fields
    has_scientific_area = (
        getattr(submission, 'scientific_area', None) or 
        getattr(submission, 'scientific_area_grande', None)
    )
    
    if not has_scientific_area:
        flags["is_complete"] = False
        flags["issues"].append("missing_scientific_area")
    
    required_fields = ['manuscript_type', 'decision_type', 'reviewer_count', 
                       'time_to_decision', 'editor_comments', 'perceived_coherence']
    
    for field in required_fields:
        value = getattr(submission, field, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            flags["is_complete"] = False
            flags["issues"].append(f"missing_{field}")
    
    # Review comments can be empty for desk rejects
    decision_type = getattr(submission, 'decision_type', '')
    review_comments = getattr(submission, 'review_comments', [])
    if decision_type != 'desk_reject' and (not review_comments or len(review_comments) == 0):
        flags["is_complete"] = False
        flags["issues"].append("missing_review_comments")
    
    # 2. Check logical consistency
    reviewer_count = getattr(submission, 'reviewer_count', '')
    editor_comments = getattr(submission, 'editor_comments', '')
    
    # Inconsistency: detailed review comments but 0 reviewers
    if reviewer_count == "0" and review_comments:
        detailed_comments = ['methodology', 'statistics', 'conceptual']
        if any(c in review_comments for c in detailed_comments):
            flags["is_consistent"] = False
            flags["issues"].append("inconsistent_reviewers_comments")
    
    # Inconsistency: desk reject with 2+ reviewers (unusual but not impossible - just flag)
    if decision_type == "desk_reject" and reviewer_count == "2+":
        flags["issues"].append("unusual_desk_reject_reviewers")  # Warning, not invalid
    
    # 3. Conditional field validation
    # APC range should only be provided for open access journals
    journal_is_open_access = getattr(submission, 'journal_is_open_access', None)
    apc_range = getattr(submission, 'apc_range', None)
    
    # If journal is NOT open access, APC range should be 'no_apc' or None
    if journal_is_open_access is False and apc_range and apc_range not in ['no_apc', '']:
        flags["is_consistent"] = False
        flags["issues"].append("apc_provided_for_non_open_access")
    
    # Editor comments quality should only be provided if editor provided comments
    editor_comments_quality = getattr(submission, 'editor_comments_quality', None)
    if editor_comments == 'no' and editor_comments_quality is not None:
        flags["is_consistent"] = False
        flags["issues"].append("editor_quality_without_comments")
    
    # Quality assessment: feedback_clarity only meaningful if there was feedback
    feedback_clarity = getattr(submission, 'feedback_clarity', None)
    if reviewer_count == "0" and editor_comments == 'no' and feedback_clarity is not None:
        flags["issues"].append("feedback_clarity_without_feedback")  # Warning
    
    # 4. Check for duplicates (same user + journal within 30 days)
    thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    
    existing = await db.submissions.find_one({
        "user_hashed_id": user_hashed_id,
        "journal_id": journal_id,
        "created_at": {"$gte": thirty_days_ago}
    })
    
    if existing:
        flags["is_unique"] = False
        flags["issues"].append("duplicate_within_30_days")
    
    # Determine overall validity
    valid_for_stats = flags["is_complete"] and flags["is_consistent"] and flags["is_unique"]
    
    return valid_for_stats, flags

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

@api_router.get("/analytics/visibility-status")
async def get_visibility_status():
    """Get current platform visibility status for frontend banner logic"""
    settings = await get_platform_settings()
    
    return {
        "visibility_mode": settings.get("visibility_mode", "user_only"),
        "public_stats_enabled": settings.get("public_stats_enabled", False),
        "demo_mode_enabled": settings.get("demo_mode_enabled", True),
        "message": get_visibility_message(settings)
    }

def get_visibility_message(settings: dict) -> Optional[str]:
    """Generate appropriate message based on visibility settings
    
    Messages use institutional, methodologically responsible, neutral tone.
    Avoid language suggesting platform is 'empty' or 'in testing'.
    """
    mode = settings.get("visibility_mode", "user_only")
    public_enabled = settings.get("public_stats_enabled", False)
    
    if mode == "user_only":
        return "As estatísticas agregadas são exibidas automaticamente quando há volume mínimo de dados para garantir interpretação adequada."
    elif mode == "threshold_based" and not public_enabled:
        return "Sua contribuição ajuda a construir uma infraestrutura de dados para análise do processo editorial científico."
    elif mode == "admin_forced" and not public_enabled:
        return "As estatísticas públicas estão em revisão metodológica."
    return None

@api_router.get("/analytics/overview")
async def get_analytics_overview():
    """Get overall platform statistics with quality indices"""
    settings = await get_platform_settings()
    base_query = await get_submission_base_query(settings)
    
    # Check if public stats should be shown
    mode = settings.get("visibility_mode", "user_only")
    public_enabled = settings.get("public_stats_enabled", False)
    
    # Count total submissions (respecting demo mode)
    total_submissions = await db.submissions.count_documents(base_query)
    
    # Threshold for showing observation count (hidden until 400+)
    OBSERVATION_THRESHOLD = 400
    show_observation_count = total_submissions >= OBSERVATION_THRESHOLD
    
    # For user_only mode, return minimal info
    if mode == "user_only" and not public_enabled:
        return {
            "total_submissions": total_submissions if show_observation_count else None,
            "sufficient_data": False,
            "visibility_restricted": True,
            "message": get_visibility_message(settings),
            "observation_status": "collecting" if not show_observation_count else "available"
        }
    
    if total_submissions < K_ANONYMITY_THRESHOLD:
        return {
            "total_submissions": total_submissions if show_observation_count else None,
            "sufficient_data": False,
            "visibility_restricted": False,
            "message": "As estatísticas agregadas são exibidas automaticamente quando há volume mínimo de dados para garantir interpretação adequada.",
            "observation_status": "collecting" if not show_observation_count else "available"
        }
    
    # Decision type distribution
    decision_pipeline = [
        {"$match": base_query},
        {"$group": {"_id": "$decision_type", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gte": K_ANONYMITY_THRESHOLD}}}
    ]
    decision_dist = await db.submissions.aggregate(decision_pipeline).to_list(100)
    
    # Reviewer count distribution
    reviewer_pipeline = [
        {"$match": base_query},
        {"$group": {"_id": "$reviewer_count", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gte": K_ANONYMITY_THRESHOLD}}}
    ]
    reviewer_dist = await db.submissions.aggregate(reviewer_pipeline).to_list(100)
    
    # Time to decision distribution
    time_pipeline = [
        {"$match": base_query},
        {"$group": {"_id": "$time_to_decision", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gte": K_ANONYMITY_THRESHOLD}}}
    ]
    time_dist = await db.submissions.aggregate(time_pipeline).to_list(100)
    
    # NEW: Calculate quality indices from new fields
    quality_indices = await calculate_quality_indices(base_query, total_submissions)
    
    return {
        "total_submissions": total_submissions if show_observation_count else None,
        "sufficient_data": True,
        "visibility_restricted": False,
        "observation_status": "collecting" if not show_observation_count else "available",
        "decision_distribution": {d["_id"]: d["count"] for d in decision_dist},
        "reviewer_distribution": {d["_id"]: d["count"] for d in reviewer_dist},
        "time_distribution": {d["_id"]: d["count"] for d in time_dist},
        # NEW: Quality indices
        **quality_indices
    }


async def calculate_quality_indices(base_query: dict, total_count: int) -> dict:
    """
    Calculate aggregated quality indices from new assessment fields.
    
    Returns indices:
    - average_review_quality_score: Mean of overall_review_quality (1-5)
    - editorial_transparency_index: Based on reviewer count and editor engagement
    - decision_fairness_index: % agreeing decision was fair
    - reviewer_engagement_index: Based on feedback clarity and review depth
    """
    if total_count < K_ANONYMITY_THRESHOLD:
        return {
            "quality_indices": None,
            "indices_available": False
        }
    
    # Aggregate quality metrics
    quality_pipeline = [
        {"$match": {**base_query, "overall_review_quality": {"$exists": True, "$ne": None}}},
        {"$group": {
            "_id": None,
            "avg_review_quality": {"$avg": "$overall_review_quality"},
            "avg_feedback_clarity": {"$avg": "$feedback_clarity"},
            "count": {"$sum": 1}
        }}
    ]
    quality_result = await db.submissions.aggregate(quality_pipeline).to_list(1)
    
    # Fairness distribution
    fairness_pipeline = [
        {"$match": {**base_query, "decision_fairness": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": "$decision_fairness", "count": {"$sum": 1}}}
    ]
    fairness_dist = await db.submissions.aggregate(fairness_pipeline).to_list(10)
    fairness_map = {f["_id"]: f["count"] for f in fairness_dist}
    
    # Recommendation distribution
    recommend_pipeline = [
        {"$match": {**base_query, "would_recommend": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": "$would_recommend", "count": {"$sum": 1}}}
    ]
    recommend_dist = await db.submissions.aggregate(recommend_pipeline).to_list(10)
    recommend_map = {r["_id"]: r["count"] for r in recommend_dist}
    
    # Calculate indices
    indices = {
        "indices_available": False,
        "quality_indices": {}
    }
    
    if quality_result and quality_result[0].get("count", 0) >= K_ANONYMITY_THRESHOLD:
        q = quality_result[0]
        indices["indices_available"] = True
        
        # Average Review Quality Score (1-5 scale, displayed as 0-100)
        if q.get("avg_review_quality"):
            indices["quality_indices"]["average_review_quality"] = {
                "value": round((q["avg_review_quality"] / 5) * 100, 1),
                "scale": "0-100",
                "description": "Average quality of peer review feedback"
            }
        
        # Feedback Clarity Index
        if q.get("avg_feedback_clarity"):
            indices["quality_indices"]["feedback_clarity_index"] = {
                "value": round((q["avg_feedback_clarity"] / 5) * 100, 1),
                "scale": "0-100",
                "description": "Average clarity and actionability of feedback"
            }
    
    # Decision Fairness Index
    total_fairness = sum(fairness_map.values())
    if total_fairness >= K_ANONYMITY_THRESHOLD:
        indices["indices_available"] = True
        agree_count = fairness_map.get("agree", 0)
        indices["quality_indices"]["decision_fairness_index"] = {
            "value": round((agree_count / total_fairness) * 100, 1),
            "scale": "0-100",
            "description": "Percentage reporting decision aligned with feedback",
            "distribution": {
                "agree": fairness_map.get("agree", 0),
                "neutral": fairness_map.get("neutral", 0),
                "disagree": fairness_map.get("disagree", 0)
            }
        }
    
    # Recommendation Index
    total_recommend = sum(recommend_map.values())
    if total_recommend >= K_ANONYMITY_THRESHOLD:
        indices["indices_available"] = True
        yes_count = recommend_map.get("yes", 0)
        indices["quality_indices"]["recommendation_index"] = {
            "value": round((yes_count / total_recommend) * 100, 1),
            "scale": "0-100",
            "description": "Percentage who would recommend based on editorial process",
            "distribution": {
                "yes": recommend_map.get("yes", 0),
                "neutral": recommend_map.get("neutral", 0),
                "no": recommend_map.get("no", 0)
            }
        }
    
    return indices

@api_router.get("/analytics/publishers")
async def get_publisher_analytics():
    """Get publisher-level analytics (only verified publishers, respects visibility settings)"""
    settings = await get_platform_settings()
    base_query = await get_submission_base_query(settings)
    
    # Check visibility mode
    mode = settings.get("visibility_mode", "user_only")
    public_enabled = settings.get("public_stats_enabled", False)
    
    if mode == "user_only" and not public_enabled:
        return []  # No public publisher stats in user_only mode
    
    # Get list of verified publisher IDs
    verified_publishers = await db.publishers.find(
        {"$or": [{"is_verified": True}, {"is_verified": {"$exists": False}}]},
        {"_id": 0, "publisher_id": 1}
    ).to_list(1000)
    verified_pub_ids = [p["publisher_id"] for p in verified_publishers]
    
    pipeline = [
        {"$match": {**base_query, "publisher_id": {"$in": verified_pub_ids}}},
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
    """Get journal-level analytics (only verified journals, respects visibility settings)"""
    settings = await get_platform_settings()
    base_query = await get_submission_base_query(settings)
    
    # Check visibility mode
    mode = settings.get("visibility_mode", "user_only")
    public_enabled = settings.get("public_stats_enabled", False)
    
    if mode == "user_only" and not public_enabled:
        return []  # No public journal stats in user_only mode
    
    # Get list of verified journal IDs
    journal_query = {"$or": [{"is_verified": True}, {"is_verified": {"$exists": False}}]}
    if publisher_id:
        journal_query["publisher_id"] = publisher_id
    
    verified_journals = await db.journals.find(
        journal_query,
        {"_id": 0, "journal_id": 1}
    ).to_list(1000)
    verified_journal_ids = [j["journal_id"] for j in verified_journals]
    
    match_stage = {**base_query, "journal_id": {"$in": verified_journal_ids}}
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
    """Get scientific area analytics (respects visibility settings)"""
    settings = await get_platform_settings()
    base_query = await get_submission_base_query(settings)
    
    # Check visibility mode
    mode = settings.get("visibility_mode", "user_only")
    public_enabled = settings.get("public_stats_enabled", False)
    
    if mode == "user_only" and not public_enabled:
        return []  # No public area stats in user_only mode
    
    pipeline = [
        {"$match": base_query},
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

# ============== USER PERSONAL INSIGHTS ==============

@api_router.get("/users/my-insights")
async def get_my_insights(request: Request):
    """Get personal aggregated insights for the current user
    
    This allows users to see value from their contributions even when
    public statistics are not yet available.
    """
    user = await require_auth(request)
    
    # Get user's submissions (real data only, not sample)
    user_submissions = await db.submissions.find(
        {"user_hashed_id": user.hashed_id, "is_sample": {"$ne": True}},
        {"_id": 0}
    ).to_list(1000)
    
    if not user_submissions:
        return {
            "has_data": False,
            "message": "Submit your first editorial decision to start seeing your personal insights."
        }
    
    total = len(user_submissions)
    validated = sum(1 for s in user_submissions if s.get("status") == "validated")
    pending = sum(1 for s in user_submissions if s.get("status") == "pending")
    
    # Calculate personal metrics
    no_peer_review = sum(1 for s in user_submissions if s.get("reviewer_count") == "0")
    single_reviewer = sum(1 for s in user_submissions if s.get("reviewer_count") == "1")
    desk_rejects = sum(1 for s in user_submissions if s.get("decision_type") == "desk_reject")
    
    # Time distribution
    fast_decisions = sum(1 for s in user_submissions if s.get("time_to_decision") == "0-30")
    medium_decisions = sum(1 for s in user_submissions if s.get("time_to_decision") == "31-90")
    slow_decisions = sum(1 for s in user_submissions if s.get("time_to_decision") == "90+")
    
    # Group by journal
    journals_submitted = {}
    for s in user_submissions:
        jid = s.get("journal_id")
        if jid not in journals_submitted:
            journals_submitted[jid] = 0
        journals_submitted[jid] += 1
    
    # Get journal names
    top_journals = []
    for jid, count in sorted(journals_submitted.items(), key=lambda x: -x[1])[:5]:
        journal = await db.journals.find_one({"journal_id": jid}, {"_id": 0, "name": 1})
        if journal:
            top_journals.append({"name": journal["name"], "count": count})
    
    # Group by scientific area
    areas_submitted = {}
    for s in user_submissions:
        area = s.get("scientific_area")
        if area not in areas_submitted:
            areas_submitted[area] = 0
        areas_submitted[area] += 1
    
    return {
        "has_data": True,
        "summary": {
            "total_submissions": total,
            "validated": validated,
            "pending": pending,
            "contribution_impact": "Your submissions contribute to improving transparency in scholarly publishing."
        },
        "insights": {
            "no_peer_review_rate": round((no_peer_review / total) * 100, 1) if total > 0 else 0,
            "single_reviewer_rate": round((single_reviewer / total) * 100, 1) if total > 0 else 0,
            "desk_reject_rate": round((desk_rejects / total) * 100, 1) if total > 0 else 0
        },
        "time_distribution": {
            "fast_0_30_days": round((fast_decisions / total) * 100, 1) if total > 0 else 0,
            "medium_31_90_days": round((medium_decisions / total) * 100, 1) if total > 0 else 0,
            "slow_90_plus_days": round((slow_decisions / total) * 100, 1) if total > 0 else 0
        },
        "top_journals": top_journals,
        "areas_distribution": areas_submitted
    }

# ============== FORM OPTIONS ==============

# Import CNPq hierarchical areas
from data.cnpq_areas import get_grande_areas, get_areas, get_subareas, get_area_by_code

@api_router.get("/options/scientific-areas")
async def get_scientific_areas():
    """Get list of scientific areas (legacy - returns Grande Áreas for backwards compatibility)"""
    # Return Grande Áreas in legacy format for backwards compatibility
    grande_areas = get_grande_areas()
    return [
        {"id": ga["code"], "name": ga["name"], "name_en": ga["name_en"]}
        for ga in grande_areas
    ]

# ============== CNPq HIERARCHICAL AREAS ==============

@api_router.get("/options/cnpq/grande-areas")
async def get_cnpq_grande_areas():
    """Get list of CNPq Grande Áreas (top level)"""
    return get_grande_areas()

@api_router.get("/options/cnpq/areas/{grande_area_code}")
async def get_cnpq_areas(grande_area_code: str):
    """Get list of CNPq Áreas for a given Grande Área"""
    areas = get_areas(grande_area_code)
    if not areas:
        raise HTTPException(status_code=404, detail="Grande Área not found")
    return areas

@api_router.get("/options/cnpq/subareas/{area_code}")
async def get_cnpq_subareas(area_code: str):
    """Get list of CNPq Subáreas for a given Área"""
    subareas = get_subareas(area_code)
    # Note: Some áreas don't have subáreas, so empty list is valid
    return subareas

@api_router.get("/options/cnpq/lookup/{code}")
async def get_cnpq_area_lookup(code: str):
    """Lookup CNPq area by full code (e.g., '1.01.02')"""
    area = get_area_by_code(code)
    if not area:
        raise HTTPException(status_code=404, detail="Area code not found")
    return area

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

# NEW: Quality assessment options (neutral language, captures positive/neutral/negative)

@api_router.get("/options/review-quality-scale")
async def get_review_quality_scale():
    """Get overall review quality scale (1-5)"""
    return [
        {"id": 1, "value": 1, "label": "Very Low", "description": "Review provided minimal useful feedback"},
        {"id": 2, "value": 2, "label": "Low", "description": "Review had significant gaps"},
        {"id": 3, "value": 3, "label": "Average", "description": "Review met basic expectations"},
        {"id": 4, "value": 4, "label": "High", "description": "Review was thorough and helpful"},
        {"id": 5, "value": 5, "label": "Very High", "description": "Review was exceptional in quality"}
    ]

@api_router.get("/options/feedback-clarity-scale")
async def get_feedback_clarity_scale():
    """Get feedback clarity scale (1-5)"""
    return [
        {"id": 1, "value": 1, "label": "Very Unclear", "description": "Feedback was difficult to understand or act upon"},
        {"id": 2, "value": 2, "label": "Unclear", "description": "Feedback lacked clarity in several areas"},
        {"id": 3, "value": 3, "label": "Neutral", "description": "Feedback was understandable but not detailed"},
        {"id": 4, "value": 4, "label": "Clear", "description": "Feedback was mostly clear and actionable"},
        {"id": 5, "value": 5, "label": "Very Clear", "description": "Feedback was highly clear and actionable"}
    ]

@api_router.get("/options/decision-fairness")
async def get_decision_fairness_options():
    """Get decision fairness perception options"""
    return [
        {"id": "agree", "label": "Agree", "description": "The decision aligned with the review feedback"},
        {"id": "neutral", "label": "Neutral", "description": "No strong opinion on the alignment"},
        {"id": "disagree", "label": "Disagree", "description": "The decision did not align with the review feedback"}
    ]

@api_router.get("/options/would-recommend")
async def get_would_recommend_options():
    """Get recommendation options based on editorial process"""
    return [
        {"id": "yes", "label": "Yes", "description": "Would recommend based on the editorial process"},
        {"id": "neutral", "label": "Neutral", "description": "No strong recommendation either way"},
        {"id": "no", "label": "No", "description": "Would not recommend based on the editorial process"}
    ]

# ============== ADMIN ENDPOINTS ==============

# --- Platform Settings ---

@api_router.get("/admin/settings")
async def get_admin_settings(request: Request):
    """Get current platform settings"""
    await require_admin(request)
    settings = await get_platform_settings()
    return settings

@api_router.put("/admin/settings")
async def update_admin_settings(update: PlatformSettingsUpdate, request: Request):
    """Update platform settings"""
    await require_admin(request)
    
    update_data = {}
    if update.visibility_mode is not None:
        if update.visibility_mode not in ["user_only", "threshold_based", "admin_forced"]:
            raise HTTPException(status_code=400, detail="Invalid visibility mode")
        update_data["visibility_mode"] = update.visibility_mode
    
    if update.demo_mode_enabled is not None:
        update_data["demo_mode_enabled"] = update.demo_mode_enabled
    
    if update.public_stats_enabled is not None:
        update_data["public_stats_enabled"] = update.public_stats_enabled
    
    if update.min_submissions_per_journal is not None:
        if update.min_submissions_per_journal < 1:
            raise HTTPException(status_code=400, detail="Minimum submissions must be at least 1")
        update_data["min_submissions_per_journal"] = update.min_submissions_per_journal
    
    if update.min_unique_users_per_journal is not None:
        if update.min_unique_users_per_journal < 1:
            raise HTTPException(status_code=400, detail="Minimum unique users must be at least 1")
        update_data["min_unique_users_per_journal"] = update.min_unique_users_per_journal
    
    if update_data:
        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        await db.platform_settings.update_one(
            {"settings_id": "global"},
            {"$set": update_data},
            upsert=True
        )
    
    settings = await get_platform_settings()
    logger.info(f"Platform settings updated: {update_data}")
    return settings

@api_router.put("/admin/visibility/override")
async def set_visibility_override(override: VisibilityOverride, request: Request):
    """Set visibility override for a specific entity"""
    await require_admin(request)
    
    if override.entity_type not in ["journal", "publisher", "area"]:
        raise HTTPException(status_code=400, detail="Invalid entity type")
    
    # Map to plural form for storage
    entity_key = f"{override.entity_type}s"
    
    await db.platform_settings.update_one(
        {"settings_id": "global"},
        {"$set": {f"visibility_overrides.{entity_key}.{override.entity_id}": override.force_visible}},
        upsert=True
    )
    
    logger.info(f"Visibility override set: {override.entity_type}/{override.entity_id} = {override.force_visible}")
    return {"message": "Override set successfully", "entity_type": override.entity_type, "entity_id": override.entity_id, "force_visible": override.force_visible}

@api_router.delete("/admin/visibility/override/{entity_type}/{entity_id}")
async def remove_visibility_override(entity_type: str, entity_id: str, request: Request):
    """Remove visibility override for a specific entity"""
    await require_admin(request)
    
    if entity_type not in ["journal", "publisher", "area"]:
        raise HTTPException(status_code=400, detail="Invalid entity type")
    
    entity_key = f"{entity_type}s"
    
    await db.platform_settings.update_one(
        {"settings_id": "global"},
        {"$unset": {f"visibility_overrides.{entity_key}.{entity_id}": ""}}
    )
    
    return {"message": "Override removed successfully"}

# --- Data Management ---

@api_router.get("/admin/data/stats")
async def get_data_stats(request: Request):
    """Get sample vs real data statistics"""
    await require_admin(request)
    
    total_submissions = await db.submissions.count_documents({})
    sample_submissions = await db.submissions.count_documents({"is_sample": True})
    real_submissions = await db.submissions.count_documents({"is_sample": {"$ne": True}})
    
    total_users = await db.users.count_documents({})
    sample_users = await db.users.count_documents({"is_sample": True})
    real_users = await db.users.count_documents({"is_sample": {"$ne": True}})
    
    return {
        "submissions": {
            "total": total_submissions,
            "sample": sample_submissions,
            "real": real_submissions
        },
        "users": {
            "total": total_users,
            "sample": sample_users,
            "real": real_users
        }
    }

@api_router.post("/admin/data/purge-sample")
async def purge_sample_data(request: Request):
    """Purge all sample data from the database"""
    await require_admin(request)
    
    # Delete sample submissions
    submissions_result = await db.submissions.delete_many({"is_sample": True})
    
    # Delete sample users (if any)
    users_result = await db.users.delete_many({"is_sample": True})
    
    # Reset validated_submission_count on journals/publishers since sample data is gone
    # Only if there's no real data for them
    
    logger.info(f"Sample data purged: {submissions_result.deleted_count} submissions, {users_result.deleted_count} users")
    
    return {
        "message": "Sample data purged successfully",
        "deleted": {
            "submissions": submissions_result.deleted_count,
            "users": users_result.deleted_count
        }
    }

# --- Original Admin Stats ---

@api_router.get("/admin/stats")
async def get_admin_stats(request: Request):
    """Get admin dashboard statistics"""
    await require_admin(request)
    
    total_users = await db.users.count_documents({})
    total_submissions = await db.submissions.count_documents({})
    pending_submissions = await db.submissions.count_documents({"status": "pending"})
    validated_submissions = await db.submissions.count_documents({"status": "validated"})
    flagged_submissions = await db.submissions.count_documents({"status": "flagged"})
    
    # Add sample vs real breakdown
    sample_submissions = await db.submissions.count_documents({"is_sample": True})
    real_submissions = await db.submissions.count_documents({"is_sample": {"$ne": True}})
    
    return {
        "total_users": total_users,
        "total_submissions": total_submissions,
        "pending_submissions": pending_submissions,
        "validated_submissions": validated_submissions,
        "flagged_submissions": flagged_submissions,
        "sample_submissions": sample_submissions,
        "real_submissions": real_submissions
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
