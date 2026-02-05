# EchoTruth Documentation

## 🎙️ Project Overview
EchoTruth is an AI-powered voice detection application designed to identify AI-generated speech. It uses a React frontend and a FastAPI backend to analyze audio files and provide a probability score along with an explanation.

## 🏗️ Architecture

### Frontend (`src/`)
- **Framework:** React (Vite)
- **UI Component Library:** shadcn/ui
- **Styling:** Tailwind CSS
- **State Management:** React Query
- **Routing:** React Router

### Backend (`backend/`)
- **Framework:** FastAPI (Python)
- **AI Model:** Integration with Gemini/Groq for analysis
- **Audio Processing:** Internal audio feature extraction

## 🚀 Setup & Installation

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)

### 1. Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```
The application will be available at `http://localhost:8080`.

### 2. Backend Setup
```bash
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment Variables
cp .env.example .env
# Edit .env and add your API keys (API_KEY, LLM_API_KEY)

# Start API server
uvicorn app.main:app --reload
```
The API will run at `http://localhost:8000`.

## 📡 API Usage

**Endpoint:** `POST /api/v1/detect`

**Request Body:**
```json
{
  "audio_url": "https://example.com/file.mp3",
  "language": "en"
}
```

**Response:**
```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.95,
  "explanation": "The audio exhibits unnatural prosody and lack of breath pauses characteristic of TTS models."
}
```

## 🛠️ Development Guide

### Folder Structure
- `src/components`: Reusable UI components
- `src/pages`: Main application pages
- `src/hooks`: Custom React hooks
- `src/lib`: Utility functions
- `backend/app`: Python application code

### Adding New Features
1. Create new components in `src/components`.
2. specific logic should go into `src/lib` or custom hooks.
3. Update backend endpoints in `backend/app/main.py` if needed.

## 🤝 Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes
4. Push to branch
5. Open a Pull Request
