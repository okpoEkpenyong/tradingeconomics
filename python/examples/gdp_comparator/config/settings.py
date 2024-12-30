import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    
    # Redis Configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TYPE = os.getenv("CACHE_TYPE", "RedisCache")  # Use RedisCache by default
    
    # Trading Economics API
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.tradingeconomics.com")
    API_KEY = os.getenv("TRADING_ECONOMICS_API_KEY")
    
    # Allowed Countries
    ALLOWED_COUNTRIES = os.getenv("ALLOWED_COUNTRIES", "").split(",")

    # CSP Settings
    CSP_DEFAULT_SRC = "'self'"
    CSP_STYLE_SRC = ["'self'", "https://cdn.jsdelivr.net"]
    CSP_SCRIPT_SRC = ["'self'", "https://cdn.jsdelivr.net"]
    CSP_ADDITIONAL_POLICIES = [
        "img-src 'self' https:", 
        "font-src 'self' data:"
    ]
    
    # Additional Settings
    CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 300))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
   
  
    
