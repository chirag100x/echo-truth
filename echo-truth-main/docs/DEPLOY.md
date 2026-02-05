# EchoTruth Deployment Guide

Deploy EchoTruth backend to popular cloud platforms.

## Prerequisites

- Python 3.10+
- FFmpeg installed on deployment platform
- LLM API key (OpenAI, Gemini, or Groq)

---

## Option 1: Render

### Steps

1. **Create Render Account**: https://render.com

2. **Create New Web Service**:
   - Connect your GitHub repository
   - Select the `backend` directory as root

3. **Configure Build**:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**:
   - `API_KEY` = your-secure-key
   - `LLM_PROVIDER` = gemini
   - `LLM_API_KEY` = your-llm-key

5. **Install FFmpeg** (add to build):
   Create `render.yaml`:
   ```yaml
   services:
     - type: web
       name: echotruth-api
       env: python
       buildCommand: |
         apt-get update && apt-get install -y ffmpeg
         pip install -r requirements.txt
       startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

6. **Deploy** - Render will build and deploy automatically

---

## Option 2: Railway

### Steps

1. **Create Railway Account**: https://railway.app

2. **New Project** → Deploy from GitHub

3. **Configure**:
   - Root Directory: `backend`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Variables** in Railway dashboard:
   ```
   API_KEY=your-secure-key
   LLM_PROVIDER=gemini
   LLM_API_KEY=your-llm-key
   ```

5. **Add FFmpeg** via Nixpacks:
   Create `nixpacks.toml`:
   ```toml
   [phases.setup]
   aptPkgs = ["ffmpeg"]
   ```

6. **Deploy** - Railway handles the rest

---

## Option 3: Fly.io

### Steps

1. **Install Fly CLI**: https://fly.io/docs/getting-started/installing-flyctl/

2. **Login**: `fly auth login`

3. **Create `fly.toml`** in `backend/`:
   ```toml
   app = "echotruth-api"
   primary_region = "sjc"

   [build]
     builder = "paketobuildpacks/builder:base"

   [env]
     PORT = "8080"

   [http_service]
     internal_port = 8080
     force_https = true

   [[services]]
     http_checks = []
     internal_port = 8080
     protocol = "tcp"
   ```

4. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim

   RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
   ```

5. **Set Secrets**:
   ```bash
   fly secrets set API_KEY=your-secure-key
   fly secrets set LLM_PROVIDER=gemini
   fly secrets set LLM_API_KEY=your-llm-key
   ```

6. **Deploy**: `fly deploy`

---

## Option 4: Docker (Any Platform)

### Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create temp directory
RUN mkdir -p app/tmp

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build & Run

```bash
# Build image
docker build -t echotruth-api .

# Run container
docker run -d \
  -p 8000:8000 \
  -e API_KEY=your-secure-key \
  -e LLM_PROVIDER=gemini \
  -e LLM_API_KEY=your-llm-key \
  echotruth-api
```

---

## Frontend Deployment

### Vercel (Recommended)

1. Push frontend code to GitHub
2. Import project in Vercel
3. Set environment variable:
   - `VITE_API_BASE_URL` = your-backend-url

### Netlify

1. Build command: `npm run build`
2. Publish directory: `dist`
3. Add environment variable for API URL

---

## Post-Deployment Checklist

- [ ] Backend responds to `/health` endpoint
- [ ] API key authentication works
- [ ] Audio URL detection works
- [ ] Frontend can connect to backend (CORS configured)
- [ ] LLM calls succeed (check logs)
- [ ] SSL/HTTPS enabled

---

## Troubleshooting

### FFmpeg Not Found
Make sure FFmpeg is installed. For Docker, add to Dockerfile. For PaaS, use build scripts.

### CORS Errors
Update `app/main.py` CORS origins to include your frontend URL.

### LLM Timeouts
Increase timeout in `llm_adapter.py` or use a faster model (Groq/Gemini Flash).

### Audio Processing Fails
Check temp directory permissions. Ensure enough disk space for temp files.
