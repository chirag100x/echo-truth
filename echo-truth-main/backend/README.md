# EchoTruth Backend

AI-Generated Voice Detection API with multi-language support.

## 🎯 Problem Statement

With the rise of AI voice cloning and text-to-speech, it's increasingly difficult to distinguish between authentic human speech and AI-generated audio. EchoTruth provides an API to analyze audio and detect synthetic voices.

## 🔬 Detection Pipeline

```
Audio Input → Download/Decode → FFmpeg Conversion → Feature Extraction → LLM Analysis → Result
```

### Features Analyzed:
- **Pitch Variance**: AI voices tend to have unnaturally consistent pitch
- **Silence Ratio**: Human speech includes natural pauses; AI often lacks micro-breaks
- **Volume Dynamics**: Synthetic audio is often over-normalized
- **Spectral Patterns**: AI generation leaves detectable artifacts

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- FFmpeg installed (`brew install ffmpeg` or `apt install ffmpeg`)

### Installation

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

Server runs at `http://localhost:8000`

## 📡 API Usage

### Detect Voice

```bash
curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "audio_url": "https://example.com/audio.mp3",
    "language": "en"
  }'
```

### Response

```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87,
  "explanation": "Audio exhibits consistent pitch patterns and lacks natural micro-pauses typically found in human speech."
}
```

## 🔑 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_KEY` | Your API authentication key | Yes |
| `LLM_API_KEY` | LLM provider API key | No* |
| `LLM_PROVIDER` | "openai", "gemini", or "groq" | No |
| `LLM_MODEL` | Specific model to use | No |

*Without LLM_API_KEY, the system uses heuristic fallback (lower confidence)

### Swap LLM Providers

1. Set `LLM_PROVIDER` in `.env`:
   - `openai` - Uses GPT-4
   - `gemini` - Uses Gemini 1.5 Flash (recommended for hackathon - free tier)
   - `groq` - Uses Llama 3.1 (fast, free tier available)

2. Get your API key:
   - OpenAI: https://platform.openai.com/api-keys
   - Gemini: https://makersuite.google.com/app/apikey
   - Groq: https://console.groq.com/keys

3. Set `LLM_API_KEY` in `.env`

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Configuration & env vars
│   ├── api/
│   │   └── v1.py         # API routes
│   ├── controllers/
│   │   └── detect.py     # Detection orchestration
│   ├── services/
│   │   ├── audio_service.py    # Audio processing
│   │   ├── decision_service.py # Classification logic
│   │   └── ai_service.py       # LLM integration
│   ├── adapters/
│   │   └── llm_adapter.py      # Multi-provider LLM adapter
│   ├── middleware/
│   │   └── api_key.py    # Authentication
│   └── utils/
│       ├── prompts.py    # LLM prompts
│       └── validators.py # Input validation
├── tests/
│   └── local_test.sh     # Curl test script
├── requirements.txt
└── .env.example
```

## ⚠️ Limitations

- **Not ML-trained**: Uses feature heuristics + LLM reasoning, not a trained classifier
- **Accuracy varies**: Works best on clear speech; music/noise reduces accuracy
- **Max duration**: 5-minute audio limit
- **Languages**: Optimized for en, hi, ta, te, ml (works on others with reduced accuracy)

## 🔍 Find API Keys in Code

```bash
grep -R "API_KEY\|LLM_API_KEY" .
```

All API keys should only appear in:
- `.env.example` (template)
- `.env` (your values - not committed)
- `config.py` (reads from env)

## 📄 License

MIT - Built for hackathon use.
