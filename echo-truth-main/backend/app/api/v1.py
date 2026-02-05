"""
v1.py
API v1 routes

Main API endpoint for voice detection.
POST /api/v1/detect
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
from app.middleware.api_key import verify_api_key
from app.controllers.detect import DetectController

router = APIRouter()


class DetectRequest(BaseModel):
    """
    Request body for voice detection
    
    Must provide either audio_url OR audio_base64 (not both required, but at least one)
    """
    audio_url: Optional[str] = Field(
        None, 
        description="URL to audio file (mp3, wav, ogg, m4a)",
        example="https://example.com/speech.mp3"
    )
    audio_base64: Optional[str] = Field(
        None, 
        description="Base64 encoded audio data"
    )
    language: str = Field(
        default="en",
        description="Audio language code",
        example="en"
    )


class DetectResponse(BaseModel):
    """
    Response from voice detection
    
    Always returns valid JSON with these fields:
    - classification: "AI_GENERATED" or "HUMAN"
    - confidence: float between 0.0 and 1.0
    - explanation: Human-readable explanation (max 240 chars)
    """
    classification: Literal["AI_GENERATED", "HUMAN"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    explanation: str = Field(..., max_length=240)


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str


@router.post(
    "/detect",
    response_model=DetectResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Missing audio"},
        401: {"model": ErrorResponse, "description": "Invalid API key"},
        422: {"model": ErrorResponse, "description": "Audio processing error"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
    summary="Detect AI-generated voice",
    description="""
    Analyze audio to determine if it's AI-generated or human speech.
    
    **Authentication**: Requires `Authorization: Bearer <API_KEY>` header.
    
    **Input**: Provide either `audio_url` (URL to audio file) or `audio_base64` (base64 encoded audio).
    
    **Supported formats**: MP3, WAV, OGG, M4A, WebM
    
    **Supported languages**: en (English), hi (Hindi), ta (Tamil), te (Telugu), ml (Malayalam)
    """,
)
async def detect_voice(
    request: DetectRequest,
    _: bool = Depends(verify_api_key),
) -> DetectResponse:
    """
    Main detection endpoint
    
    Flow:
    1. Validate request has audio_url or audio_base64
    2. Download/decode audio
    3. Convert to WAV (ffmpeg)
    4. Extract features (librosa)
    5. Run detection (LLM + heuristic fallback)
    6. Return classification result
    """
    # Validate input
    if not request.audio_url and not request.audio_base64:
        raise HTTPException(
            status_code=400,
            detail="Missing audio: provide either audio_url or audio_base64"
        )
    
    # Initialize controller and process
    controller = DetectController()
    
    try:
        result = await controller.detect(
            audio_url=request.audio_url,
            audio_base64=request.audio_base64,
            language=request.language,
        )
        return DetectResponse(**result)
    
    except ValueError as e:
        # Validation/processing errors
        raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        # Unexpected errors
        print(f"Detection error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
