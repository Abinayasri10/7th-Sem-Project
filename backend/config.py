import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    PORT = int(os.getenv("PORT", 5000))
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"
    
    # Earth Engine config
    GEE_PRIVATE_KEY_PATH = os.getenv("GEE_PRIVATE_KEY_PATH", "gee_credentials.json")
    # Resolve relative paths relative to backend root directory
    if GEE_PRIVATE_KEY_PATH and not os.path.isabs(GEE_PRIVATE_KEY_PATH):
        GEE_PRIVATE_KEY_PATH = str(BASE_DIR / GEE_PRIVATE_KEY_PATH)
        
    # CORS configuration
    cors_raw = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    CORS_ORIGINS = [origin.strip() for origin in cors_raw.split(",") if origin.strip()]

