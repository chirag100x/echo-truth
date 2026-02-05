"""
api_key.py
API Key authentication middleware

============================================
API KEY VALIDATION
============================================
This middleware validates the Authorization header.
Expected format: "Bearer <API_KEY>"

The API_KEY is loaded from environment variables.
See config.py for configuration.
============================================
"""

from fastapi import HTTPException, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

# HTTP Bearer security scheme
security = HTTPBearer()


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> bool:
    """
    Verify API key from Authorization header
    
    ============================================
    AUTHENTICATION FLOW
    ============================================
    1. Extract token from "Authorization: Bearer <token>" header
    2. Compare with API_KEY from environment
    3. Raise 401 if invalid
    ============================================
    
    Args:
        credentials: HTTP Bearer credentials from header
        
    Returns:
        True if valid
        
    Raises:
        HTTPException: 401 if invalid or missing
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    # ============================================
    # API KEY COMPARISON
    # The expected API_KEY is loaded from config.py
    # which reads from environment variables
    # ============================================
    if token != settings.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return True


from typing import Optional

def get_api_key_from_header(request: Request) -> Optional[str]:
    """
    Extract API key from request header (utility function)
    
    Returns:
        API key string or None if not present
    """
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None
