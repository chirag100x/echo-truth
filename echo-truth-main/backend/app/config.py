"""
config.py
Application configuration using environment variables

============================================
API KEY CONFIGURATION
============================================
This file reads API keys from environment variables.
Never hardcode API keys in code!

Create a .env file with:
  API_KEY=your-api-key-here
  LLM_API_KEY=your-llm-api-key
  LLM_PROVIDER=gemini
============================================
"""

import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    ============================================
    API KEYS GO HERE (via environment variables)
    ============================================
    """
    
    # ============================================
    # API_KEY: Used for authenticating requests
    # Generate a secure random string for production
    # ============================================
    API_KEY: str = os.getenv("API_KEY", "demo-key-12345")
    
    # ============================================
    # LLM_API_KEY: Your LLM provider API key
    # Get from: 
    #   - OpenAI: https://platform.openai.com/api-keys
    #   - Google AI: https://makersuite.google.com/app/apikey
    #   - Groq: https://console.groq.com/keys
    # ============================================
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    
    # ============================================
    # LLM_PROVIDER: Which LLM to use
    # Options: "openai" | "gemini" | "groq"
    # ============================================
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    
    # LLM Model settings
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    
    # Audio processing settings
    MAX_AUDIO_DURATION: int = 300  # 5 minutes max
    TEMP_DIR: str = os.getenv("TEMP_DIR", "app/tmp")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def validate_config():
    """Validate required configuration is present"""
    errors = []
    
    if not settings.API_KEY:
        errors.append("API_KEY is not set")
    
    if not settings.LLM_API_KEY:
        errors.append("LLM_API_KEY is not set - LLM features will use fallback heuristics")
    
    if errors:
        print("⚠️ Configuration warnings:")
        for error in errors:
            print(f"  - {error}")
    
    return len([e for e in errors if "not set" in e and "LLM" not in e]) == 0
