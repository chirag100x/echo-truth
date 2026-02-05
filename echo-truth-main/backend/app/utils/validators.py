"""
validators.py
Input validation utilities

Validates request inputs before processing.
"""

import re
from typing import Optional


def validate_audio_url(url: str) -> bool:
    """
    Validate audio URL format and extension
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid audio URL
    """
    if not url:
        return False
    
    # Check URL format
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return False
    
    # Check for audio extension (loose check)
    audio_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.webm', '.flac']
    has_audio_ext = any(ext in url.lower() for ext in audio_extensions)
    has_audio_in_path = 'audio' in url.lower() or 'sound' in url.lower()
    
    return has_audio_ext or has_audio_in_path


def validate_base64(data: str) -> bool:
    """
    Validate base64 encoded data
    
    Args:
        data: Base64 string to validate
        
    Returns:
        True if valid base64
    """
    if not data:
        return False
    
    # Remove data URL prefix if present
    if ',' in data:
        data = data.split(',')[1]
    
    # Check base64 pattern
    base64_pattern = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')
    
    # Check length is multiple of 4
    if len(data) % 4 != 0:
        return False
    
    return bool(base64_pattern.match(data))


def validate_language(code: str) -> bool:
    """
    Validate language code
    
    Args:
        code: Language code to validate
        
    Returns:
        True if supported language
    """
    supported = ['en', 'hi', 'ta', 'te', 'ml']
    return code.lower() in supported


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path separators and null bytes
    filename = re.sub(r'[/\\:\x00]', '', filename)
    # Remove leading dots
    filename = filename.lstrip('.')
    # Limit length
    return filename[:100] if filename else 'audio'
