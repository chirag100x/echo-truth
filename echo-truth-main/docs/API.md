# EchoTruth API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All `/api/v1/*` endpoints require authentication via Bearer token.

```
Authorization: Bearer <API_KEY>
```

## Endpoints

### POST /api/v1/detect

Analyze audio to detect if it's AI-generated or human speech.

#### Request

**Headers:**
| Header | Value | Required |
|--------|-------|----------|
| Content-Type | application/json | Yes |
| Authorization | Bearer <API_KEY> | Yes |

**Body:**
```json
{
  "audio_url": "string (optional)",
  "audio_base64": "string (optional)",
  "language": "string (default: 'en')"
}
```

| Field | Type | Description |
|-------|------|-------------|
| audio_url | string | URL to audio file (MP3, WAV, OGG, M4A, WebM) |
| audio_base64 | string | Base64 encoded audio data |
| language | string | Language code: en, hi, ta, te, ml |

**Note:** You must provide either `audio_url` OR `audio_base64`, not both.

#### Response

**Success (200):**
```json
{
  "classification": "AI_GENERATED" | "HUMAN",
  "confidence": 0.87,
  "explanation": "Audio exhibits consistent pitch patterns..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| classification | string | Either "AI_GENERATED" or "HUMAN" |
| confidence | float | Confidence score between 0.0 and 1.0 |
| explanation | string | Human-readable explanation (max 240 chars) |

#### Error Responses

**400 Bad Request:**
```json
{
  "detail": "Missing audio: provide either audio_url or audio_base64"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Invalid API key"
}
```

**422 Unprocessable Entity:**
```json
{
  "detail": "Audio processing error: Failed to download audio"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error"
}
```

---

### GET /health

Health check endpoint for monitoring.

**Response (200):**
```json
{
  "status": "healthy",
  "service": "echotruth-api"
}
```

---

### GET /

API information endpoint.

**Response (200):**
```json
{
  "name": "EchoTruth API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

## Example Requests

### cURL - Detect with URL

```bash
curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer demo-key-12345" \
  -d '{
    "audio_url": "https://www2.cs.uic.edu/~i101/SoundFiles/BaachRecordingPiano.mp3",
    "language": "en"
  }'
```

### cURL - Detect with Base64

```bash
# First encode your audio file
AUDIO_BASE64=$(base64 -i audio.mp3)

curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer demo-key-12345" \
  -d "{
    \"audio_base64\": \"${AUDIO_BASE64}\",
    \"language\": \"en\"
  }"
```

### JavaScript/Fetch

```javascript
const response = await fetch('http://localhost:8000/api/v1/detect', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer demo-key-12345',
  },
  body: JSON.stringify({
    audio_url: 'https://example.com/audio.mp3',
    language: 'en',
  }),
});

const result = await response.json();
console.log(result.classification); // "AI_GENERATED" or "HUMAN"
```

### Python/Requests

```python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/detect',
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer demo-key-12345',
    },
    json={
        'audio_url': 'https://example.com/audio.mp3',
        'language': 'en',
    },
)

result = response.json()
print(result['classification'])  # "AI_GENERATED" or "HUMAN"
```

---

## Supported Languages

| Code | Language |
|------|----------|
| en | English |
| hi | Hindi (हिन्दी) |
| ta | Tamil (தமிழ்) |
| te | Telugu (తెలుగు) |
| ml | Malayalam (മലയാളം) |

---

## Rate Limits

- No rate limits implemented for hackathon
- For production, consider adding rate limiting

---

## OpenAPI Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
