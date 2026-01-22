"""
Seed script for Editorial Decision Statistics Platform
Populates database with publishers, journals, and sample data

IMPORTANT: All sample data is flagged with is_sample=True
Sample data can be purged via admin controls without affecting real user data
"""
import asyncio
import os
import random
import uuid
import hashlib
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Default platform settings
DEFAULT_PLATFORM_SETTINGS = {
    "settings_id": "global",
    "visibility_mode": "user_only",  # user_only | threshold_based | admin_forced
    "demo_mode_enabled": True,  # Show sample data in analytics
    "public_stats_enabled": False,  # Enable public statistics display
    "min_submissions_per_journal": 3,
    "min_unique_users_per_journal": 3,
    "visibility_overrides": {
        "journals": {},  # journal_id: true/false
        "publishers": {},  # publisher_id: true/false
        "areas": {}  # area_id: true/false
    },
    "created_at": datetime.now(timezone.utc).isoformat(),
    "updated_at": datetime.now(timezone.utc).isoformat()
}

# Publishers and their journals
PUBLISHERS_AND_JOURNALS = {
    "Elsevier": [
        "Journal of Cleaner Production",
        "Ecological Indicators",
        "Biological Control",
        "Crop Protection",
        "Applied Soil Ecology",
        "Science of The Total Environment",
        "Environmental Research",
        "Journal of Environmental Management",
        "Agriculture, Ecosystems & Environment",
        "Food Chemistry"
    ],
    "Springer Nature": [
        "Scientific Reports",
        "Nature Communications",
        "Nature Ecology & Evolution",
        "European Journal of Entomology",
        "Plant and Soil",
        "Biodiversity and Conservation",
        "Environmental Science and Pollution Research",
        "Journal of Plant Research",
        "Theoretical Ecology",
        "Oecologia"
    ],
    "Wiley": [
        "Journal of Applied Entomology",
        "Pest Management Science",
        "Entomologia Experimentalis et Applicata",
        "Ecology Letters",
        "Journal of Ecology",
        "Methods in Ecology and Evolution",
        "Global Change Biology",
        "Molecular Ecology",
        "Functional Ecology",
        "Journal of Biogeography"
    ],
    "MDPI": [
        "Insects",
        "Animals",
        "Sustainability",
        "Agriculture",
        "Plants",
        "Agronomy",
        "Diversity",
        "Forests",
        "Water",
        "Land"
    ],
    "Frontiers": [
        "Frontiers in Ecology and Evolution",
        "Frontiers in Insect Science",
        "Frontiers in Plant Science",
        "Frontiers in Environmental Science",
        "Frontiers in Sustainable Food Systems",
        "Frontiers in Forests and Global Change",
        "Frontiers in Marine Science",
        "Frontiers in Microbiology",
        "Frontiers in Conservation Science",
        "Frontiers in Biogeography"
    ],
    "Taylor & Francis": [
        "International Journal of Pest Management",
        "Biocontrol Science and Technology",
        "Journal of Sustainable Agriculture",
        "Archives of Agronomy and Soil Science",
        "Experimental Agriculture",
        "Agroecology and Sustainable Food Systems",
        "Journal of Crop Improvement",
        "Communications in Soil Science and Plant Analysis",
        "Plant Ecology & Diversity",
        "Biodiversity"
    ],
    "IEEE": [
        "IEEE Transactions on Pattern Analysis",
        "IEEE Transactions on Neural Networks",
        "IEEE Access",
        "IEEE Sensors Journal",
        "IEEE Internet of Things Journal",
        "IEEE Transactions on Cybernetics",
        "IEEE Computational Intelligence Magazine",
        "IEEE Transactions on Automation Science",
        "IEEE Robotics and Automation Letters",
        "IEEE Signal Processing Letters"
    ],
    "American Chemical Society": [
        "Journal of Agricultural and Food Chemistry",
        "Environmental Science & Technology",
        "ACS Sustainable Chemistry & Engineering",
        "Journal of Chemical Education",
        "ACS Applied Materials & Interfaces",
        "Analytical Chemistry",
        "ACS Nano",
        "Journal of the American Chemical Society",
        "ACS Catalysis",
        "Langmuir"
    ],
    "PLOS": [
        "PLOS ONE",
        "PLOS Biology",
        "PLOS Computational Biology",
        "PLOS Genetics",
        "PLOS Medicine",
        "PLOS Neglected Tropical Diseases",
        "PLOS Pathogens",
        "PLOS Sustainability and Transformation",
        "PLOS Climate",
        "PLOS Water"
    ],
    "Oxford University Press": [
        "Annals of Botany",
        "Journal of Experimental Botany",
        "Bioinformatics",
        "Nucleic Acids Research",
        "Molecular Biology and Evolution",
        "Systematic Biology",
        "Conservation Physiology",
        "ICES Journal of Marine Science",
        "Environmental Entomology",
        "Journal of Economic Entomology"
    ]
}

SCIENTIFIC_AREAS = [
    "life_sciences", "physical_sciences", "earth_environmental", 
    "health_sciences", "social_sciences", "engineering",
    "mathematics", "computer_science", "agriculture", "interdisciplinary"
]

MANUSCRIPT_TYPES = ["experimental", "methodological", "review", "short_communication"]

DECISION_TYPES = ["desk_reject", "reject_after_review", "major_revision", "minor_revision"]

REVIEWER_COUNTS = ["0", "1", "2+"]

TIME_RANGES = ["0-30", "31-90", "90+"]

APC_RANGES = ["no_apc", "under_1000", "1000_3000", "over_3000"]

REVIEW_COMMENT_TYPES = ["methodology", "statistics", "conceptual", "formatting_language", "generic_editorial"]

EDITOR_COMMENT_TYPES = ["yes_technical", "yes_generic", "no"]

COHERENCE_OPTIONS = ["yes", "partially", "no"]


async def seed_publishers_and_journals():
    """Seed publishers and journals (reference data, not sample)"""
    print("Seeding publishers and journals...")
    
    # Clear existing data
    await db.publishers.delete_many({})
    await db.journals.delete_many({})
    
    for publisher_name, journals in PUBLISHERS_AND_JOURNALS.items():
        publisher_id = f"pub_{uuid.uuid4().hex[:12]}"
        
        publisher_doc = {
            "publisher_id": publisher_id,
            "name": publisher_name,
            "is_user_added": False,
            "is_verified": True,  # Pre-seeded publishers are verified
            "is_sample": False,  # Reference data, not sample
            "validated_submission_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.publishers.insert_one(publisher_doc)
        print(f"  Added publisher: {publisher_name}")
        
        for journal_name in journals:
            journal_id = f"journal_{uuid.uuid4().hex[:12]}"
            journal_doc = {
                "journal_id": journal_id,
                "name": journal_name,
                "publisher_id": publisher_id,
                "is_user_added": False,
                "is_verified": True,  # Pre-seeded journals are verified
                "is_sample": False,  # Reference data, not sample
                "validated_submission_count": 0,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await db.journals.insert_one(journal_doc)
        
        print(f"    Added {len(journals)} journals")
    
    print("Publishers and journals seeded successfully!")


async def seed_sample_submissions(count: int = 500):
    """Seed sample submission data - ALL FLAGGED AS is_sample=True"""
    print(f"Seeding {count} sample submissions...")
    
    # Clear existing SAMPLE submissions only
    await db.submissions.delete_many({"is_sample": True})
    
    # Get all journals and publishers
    publishers = await db.publishers.find({}, {"_id": 0}).to_list(100)
    journals = await db.journals.find({}, {"_id": 0}).to_list(1000)
    
    # Create sample anonymous users (flagged as sample)
    sample_users = []
    for i in range(50):
        hashed_id = hashlib.sha256(f"sample_user_{i}".encode()).hexdigest()[:16]
        sample_users.append(hashed_id)
    
    submissions = []
    for i in range(count):
        journal = random.choice(journals)
        publisher_id = journal["publisher_id"]
        
        # Create realistic distributions
        # More rejections than acceptances in reality
        decision_weights = [0.35, 0.30, 0.20, 0.15]  # desk_reject, reject_after_review, major, minor
        decision_type = random.choices(DECISION_TYPES, weights=decision_weights)[0]
        
        # Reviewer count based on decision
        if decision_type == "desk_reject":
            reviewer_count = random.choices(["0", "1", "2+"], weights=[0.8, 0.15, 0.05])[0]
        else:
            reviewer_count = random.choices(["0", "1", "2+"], weights=[0.1, 0.3, 0.6])[0]
        
        # Time based on decision type
        if decision_type == "desk_reject":
            time_range = random.choices(TIME_RANGES, weights=[0.7, 0.25, 0.05])[0]
        else:
            time_range = random.choices(TIME_RANGES, weights=[0.2, 0.5, 0.3])[0]
        
        # Review comments based on reviewer count
        if reviewer_count == "0":
            review_comments = random.choices([["generic_editorial"], []], weights=[0.7, 0.3])[0]
        elif reviewer_count == "1":
            review_comments = random.sample(REVIEW_COMMENT_TYPES, random.randint(1, 3))
        else:
            review_comments = random.sample(REVIEW_COMMENT_TYPES, random.randint(2, 4))
        
        # Editor comments
        if decision_type == "desk_reject":
            editor_comments = random.choices(EDITOR_COMMENT_TYPES, weights=[0.1, 0.3, 0.6])[0]
        else:
            editor_comments = random.choices(EDITOR_COMMENT_TYPES, weights=[0.3, 0.4, 0.3])[0]
        
        # Coherence based on review quality
        if "generic_editorial" in review_comments or reviewer_count == "0":
            coherence = random.choices(COHERENCE_OPTIONS, weights=[0.2, 0.3, 0.5])[0]
        else:
            coherence = random.choices(COHERENCE_OPTIONS, weights=[0.5, 0.35, 0.15])[0]
        
        submission = {
            "submission_id": f"sub_sample_{uuid.uuid4().hex[:12]}",
            "user_hashed_id": random.choice(sample_users),
            "scientific_area": random.choice(SCIENTIFIC_AREAS),
            "manuscript_type": random.choice(MANUSCRIPT_TYPES),
            "journal_id": journal["journal_id"],
            "publisher_id": publisher_id,
            "decision_type": decision_type,
            "reviewer_count": reviewer_count,
            "time_to_decision": time_range,
            "apc_range": random.choice(APC_RANGES),
            "review_comments": review_comments,
            "editor_comments": editor_comments,
            "perceived_coherence": coherence,
            "evidence_file_id": None,
            "status": "validated",
            "is_sample": True,  # CRITICAL: Flag as sample data
            "created_at": (datetime.now(timezone.utc) - timedelta(days=random.randint(1, 365))).isoformat()
        }
        submissions.append(submission)
    
    # Insert in batches
    batch_size = 100
    for i in range(0, len(submissions), batch_size):
        batch = submissions[i:i+batch_size]
        await db.submissions.insert_many(batch)
        print(f"  Inserted {min(i+batch_size, len(submissions))}/{count} sample submissions")
    
    print("Sample submissions seeded successfully!")


async def seed_platform_settings():
    """Initialize platform settings if not exists"""
    print("Initializing platform settings...")
    
    existing = await db.platform_settings.find_one({"settings_id": "global"})
    if not existing:
        await db.platform_settings.insert_one(DEFAULT_PLATFORM_SETTINGS)
        print("  Platform settings initialized with defaults")
    else:
        print("  Platform settings already exist, skipping")


async def main():
    """Main seed function"""
    print("=" * 50)
    print("Editorial Decision Statistics Platform - Database Seeder")
    print("=" * 50)
    
    await seed_platform_settings()
    await seed_publishers_and_journals()
    await seed_sample_submissions(500)
    
    print("=" * 50)
    print("Seeding complete!")
    print("=" * 50)
    
    # Print summary
    publisher_count = await db.publishers.count_documents({})
    journal_count = await db.journals.count_documents({})
    submission_count = await db.submissions.count_documents({})
    sample_count = await db.submissions.count_documents({"is_sample": True})
    real_count = await db.submissions.count_documents({"is_sample": {"$ne": True}})
    
    print(f"\nDatabase Summary:")
    print(f"  Publishers: {publisher_count}")
    print(f"  Journals: {journal_count}")
    print(f"  Total Submissions: {submission_count}")
    print(f"    - Sample Data: {sample_count}")
    print(f"    - Real User Data: {real_count}")


if __name__ == "__main__":
    asyncio.run(main())
