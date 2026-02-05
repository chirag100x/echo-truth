"""
main.py
FastAPI application entry point

This is the main entry point for the EchoTruth backend.
Run with: uvicorn app.main:app --reload

============================================
CONFIGURATION
============================================
Set your environment variables in .env file:
- API_KEY: Your API key for authentication
- LLM_API_KEY: Your LLM provider API key (OpenAI/Gemini/Groq)
- LLM_PROVIDER: "openai" | "gemini" | "groq"
============================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router as api_v1_router
from app.config import settings

# Create FastAPI application
app = FastAPI(
    title="EchoTruth API",
    description="AI-Generated Voice Detection API - Multi-Language Support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============================================
# CORS Configuration
# Update origins for your production domains
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Vite dev server
        "http://localhost:8080",
        "*", # Allow all origins for Vercel deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": "EchoTruth API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for uptime monitoring"""
    return {
        "status": "healthy",
        "service": "echotruth-api",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
