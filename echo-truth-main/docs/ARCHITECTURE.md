# EchoTruth System Architecture

## Overview

EchoTruth is a voice detection system that analyzes audio to determine if it contains AI-generated or authentic human speech.

## System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (React/TSX)                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  UploadCard  │  │  ResultCard  │  │  LanguageSelector    │   │
│  │  - File      │  │  - Class     │  │  - en, hi, ta, te,   │   │
│  │  - URL       │  │  - Conf %    │  │    ml                │   │
│  └──────┬───────┘  └──────▲───────┘  └──────────────────────┘   │
│         │                 │                                      │
│         ▼                 │                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    API Client (Axios)                     │   │
│  │         POST /api/v1/detect + Authorization               │   │
│  └──────────────────────────┬───────────────────────────────┘   │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼ HTTP/JSON
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI/Python)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐                                              │
│  │   API Router   │ ◄─────── Authorization Middleware            │
│  │   /api/v1/     │          (Bearer Token Validation)           │
│  └───────┬────────┘                                              │
│          │                                                       │
│          ▼                                                       │
│  ┌────────────────┐                                              │
│  │   Controller   │ ─── Orchestrates the detection flow          │
│  │   detect.py    │                                              │
│  └───────┬────────┘                                              │
│          │                                                       │
│          ├─────────────────────────────────────────┐             │
│          ▼                                         ▼             │
│  ┌────────────────┐                       ┌────────────────┐     │
│  │ Audio Service  │                       │Decision Service│     │
│  │                │                       │                │     │
│  │ 1. Download/   │                       │ 1. LLM Call    │     │
│  │    Decode      │                       │ 2. Parse JSON  │     │
│  │ 2. FFmpeg      │──────features────────▶│ 3. Heuristic   │     │
│  │    Convert     │                       │    Fallback    │     │
│  │ 3. Librosa     │                       │                │     │
│  │    Extract     │                       └───────┬────────┘     │
│  └────────────────┘                               │              │
│                                                   │              │
│                           ┌───────────────────────┘              │
│                           ▼                                      │
│                   ┌────────────────┐                             │
│                   │   AI Service   │                             │
│                   │                │                             │
│                   │ Prompt Build   │                             │
│                   │ Response Parse │                             │
│                   └───────┬────────┘                             │
│                           │                                      │
│                           ▼                                      │
│                   ┌────────────────┐                             │
│                   │  LLM Adapter   │                             │
│                   │                │                             │
│                   │ ┌────────────┐ │                             │
│                   │ │  OpenAI    │ │                             │
│                   │ │  Gemini    │ │ ◄── Configurable provider   │
│                   │ │  Groq      │ │                             │
│                   │ └────────────┘ │                             │
│                   └────────────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Request Flow

```
User Action → React Component → API Client → HTTP Request → FastAPI Router
```

### 2. Authentication Flow

```
Request Header → api_key Middleware → Verify Token → Allow/Deny
```

### 3. Detection Flow

```
Audio Input
    │
    ├─► URL: Download via requests
    │
    └─► Base64: Decode to bytes
            │
            ▼
    Save to temp file (.mp3)
            │
            ▼
    FFmpeg: Convert to WAV (mono, 16kHz)
            │
            ▼
    Librosa: Extract Features
    ┌───────────────────────────┐
    │ - duration               │
    │ - silence_ratio          │
    │ - avg_volume (RMS)       │
    │ - pitch_variance         │
    └───────────────────────────┘
            │
            ▼
    Decision Service
            │
    ┌───────┴───────┐
    │               │
    ▼               ▼
LLM Call        Heuristic
(Primary)       (Fallback)
    │               │
    └───────┬───────┘
            │
            ▼
    JSON Response
    {classification, confidence, explanation}
            │
            ▼
    Cleanup temp files
            │
            ▼
    Return to client
```

## Feature Extraction

### Audio Features

| Feature | Description | AI Indicator |
|---------|-------------|--------------|
| pitch_variance | Variance in F0 | Low = AI |
| silence_ratio | % of silent frames | Low = AI |
| avg_volume | Mean RMS energy | Consistent = AI |
| duration | Length in seconds | N/A |

### Detection Logic

```python
# Primary: LLM Analysis
response = LLM.analyze(features)
if valid(response):
    return response

# Fallback: Heuristic Rules
if pitch_variance < 0.15 and silence_ratio < 0.05:
    return {"classification": "AI_GENERATED", "confidence": 0.55}
else:
    return {"classification": "HUMAN", "confidence": 0.55}
```

## Security Considerations

1. **API Key Validation**: All `/api/v1/*` routes require Bearer token
2. **Input Validation**: Audio URLs and base64 data are validated
3. **Temp File Cleanup**: All temporary files deleted after processing
4. **Environment Variables**: All secrets stored in `.env`, never in code
5. **CORS**: Configured for specific origins

## Scalability Notes

- **Stateless**: No database required, each request is independent
- **Temp Storage**: Local temp files; for scaling, use cloud storage
- **LLM Rate Limits**: Consider caching or queue for high traffic
- **Audio Processing**: CPU-bound; consider worker processes
