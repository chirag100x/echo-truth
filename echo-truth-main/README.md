# 🎙️ EchoTruth – AI Voice Detection

**Detect AI-generated voices in seconds. Multi-language support.**

## 🚀 Quick Start

### Frontend (this project)
```bash
npm install && npm run dev
```

### Backend (Python)
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add API keys
uvicorn app.main:app --reload
```

## 📡 API

```bash
curl -X POST http://localhost:8000/api/v1/detect \
  -H "Authorization: Bearer demo-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "https://example.com/audio.mp3", "language": "en"}'
```

**Response:**
```json
{"classification": "AI_GENERATED", "confidence": 0.87, "explanation": "..."}
```

## 🔑 API Keys

```bash
grep -R "API_KEY\|LLM_API_KEY" .
```

Set in `backend/.env`:
- `API_KEY` - Authentication key
- `LLM_API_KEY` - Get from [Gemini](https://makersuite.google.com/app/apikey) or [Groq](https://console.groq.com/keys)

## 📁 Structure

- `src/` - React frontend
- `backend/` - FastAPI Python backend  
- `docs/` - API.md, ARCHITECTURE.md, DEPLOY.md
- `DOCUMENTATION.md` - Comprehensive project documentation

## 🧪 Sample Audio

`https://www2.cs.uic.edu/~i101/SoundFiles/BaachRecordingPiano.mp3`

---
**Built for hackathons** | MIT License
