import os
from dotenv import load_dotenv

# load .env
load_dotenv()

# ================================
# MODEL
# ================================
MODEL_PATH = os.getenv("MODEL_PATH", "./model")

MAX_LENGTH = int(os.getenv("MAX_LENGTH", 128))

# ================================
# THRESHOLDS
# ================================
APPROVE_THRESHOLD = float(
    os.getenv("APPROVE_THRESHOLD", 0.7)
)

PENDING_THRESHOLD = float(
    os.getenv("PENDING_THRESHOLD", 0.4)
)

# ================================
# API
# ================================
API_HOST = os.getenv("API_HOST", "0.0.0.0")

API_PORT = int(os.getenv("API_PORT", 8000))

# ================================
# SPAM KEYWORDS
# ================================
SPAM_KEYWORDS = [
    "free money",
    "click here",
    "urgent transfer",
    "bitcoin fast",
    "double your money",
]