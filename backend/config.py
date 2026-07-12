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
        
    # Model config
    MODEL_PATH = os.getenv("MODEL_PATH", "ml/models/crop_disease_model.keras")
    if MODEL_PATH and not os.path.isabs(MODEL_PATH):
        MODEL_PATH = str(BASE_DIR / MODEL_PATH)
        
    CLASS_NAMES_PATH = os.getenv("CLASS_NAMES_PATH", "ml/class_names.json")
    if CLASS_NAMES_PATH and not os.path.isabs(CLASS_NAMES_PATH):
        CLASS_NAMES_PATH = str(BASE_DIR / CLASS_NAMES_PATH)

    # CORS configuration
    cors_raw = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    CORS_ORIGINS = [origin.strip() for origin in cors_raw.split(",") if origin.strip()]

    # File uploads limits
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB maximum upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
