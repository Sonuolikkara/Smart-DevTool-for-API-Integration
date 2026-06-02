# Setup Guide

Complete step-by-step instructions to get Smart DevTool running on your machine.

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **Ollama** ([Download](https://ollama.ai))
- **Git** ([Download](https://git-scm.com/))
- **4GB+ RAM** (recommended 8GB)
- **GPU optional** (speeds up AI processing)

### Verify Installations

```bash
# Check Python
python --version  # Should be 3.10+

# Check Node.js
node --version    # Should be 16+
npm --version     # Should be 8+

# Check Git
git --version
```

---

## Step 1: Clone Repository

```bash
git clone https://github.com/Sonuolikkara/Smart-DevTool-for-API-Integration.git
cd Smart-DevTool-for-API-Integration
```

---

## Step 2: Install Ollama Models

Ollama provides local LLM models. Install it first, then download required models.

### 2.1 Install Ollama

1. Download from [ollama.ai](https://ollama.ai)
2. Run installer
3. Verify installation:

```bash
ollama --version
```

### 2.2 Download Models

Ollama models are downloaded on-demand. Run:

```bash
# Primary model for code generation
ollama pull qwen2.5-coder

# Fallback model
ollama pull nomic-embed-text
```

This may take 10-15 minutes depending on internet speed.

### 2.3 Verify Models

```bash
ollama list
```

You should see:
```
NAME                  ID              SIZE    MODIFIED
qwen2.5-coder:latest  ...             3.5GB   2 hours ago
nomic-embed-text:...  ...             274MB   1 hour ago
```

### 2.4 Start Ollama Service

In a new terminal, start the Ollama service:

```bash
ollama serve
```

**Keep this terminal open** while using the app. You'll see:
```
Starting Ollama server on 127.0.0.1:11434
```

---

## Step 3: Backend Setup

### 3.1 Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### 3.2 Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI
- Uvicorn
- Pydantic
- LangChain
- ChromaDB
- Ollama
- BeautifulSoup4
- Playwright
- And more...

### 3.4 Create .env File

```bash
cp .env.example .env
```

Or create `backend/.env` with:
```
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_PRIMARY_MODEL=qwen2.5-coder
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

# Backend Configuration
API_PORT=8000
API_HOST=0.0.0.0

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### 3.5 Start Backend Server

```bash
uvicorn main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ Backend is running on `http://localhost:8000`

**Keep this terminal open.**

---

## Step 4: Frontend Setup

### 4.1 Install Dependencies

In a **new terminal**, navigate to frontend:

```bash
cd frontend
npm install
```

This installs React, TailwindCSS, Framer Motion, and all dependencies.

### 4.2 Start Development Server

```bash
npm run dev
```

**Output:**
```
  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

✅ Frontend is running on `http://localhost:5173`

---

## Step 5: Open Application

Open your browser and navigate to:

```
http://localhost:5173
```

You should see the Smart DevTool home page with the logo and problem/solution overview.

---

## Testing the Setup

### Test 1: Health Check

Open in browser or terminal:

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Smart DevTool API",
  "version": "1.0.0"
}
```

### Test 2: API Documentation

Open in browser:

```
http://localhost:8000/docs
```

You'll see interactive Swagger UI for all API endpoints.

### Test 3: Analyze Sample API

1. Open `http://localhost:5173`
2. Paste this GitHub API docs URL:
   ```
   https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28
   ```
3. Click "Analyze"
4. Watch the execution trace
5. See extracted endpoints

---

## 🐛 Troubleshooting

### Issue: "Connection refused" on localhost:8000

**Solution:**
- Ensure backend is running: `uvicorn main:app --reload`
- Check backend terminal for errors
- Verify Python version is 3.10+

### Issue: "Ollama service not available"

**Solution:**
- Ensure Ollama is running: `ollama serve`
- Check `http://localhost:11434/api/status` in browser
- Verify models are downloaded: `ollama list`

### Issue: "Models not found"

**Solution:**
- Pull models: `ollama pull qwen2.5-coder`
- Check disk space (models need 4GB+)
- Verify internet connection

### Issue: "CORS error in browser console"

**Solution:**
- Backend must be running on `http://localhost:8000`
- Check CORS configuration in `backend/config.py`
- Ensure frontend runs on `http://localhost:5173`

### Issue: "npm ERR! code ERESOLVE"

**Solution:**
```bash
npm install --legacy-peer-deps
```

### Issue: "Python: No module named 'main'"

**Solution:**
- Ensure you're in `backend/` directory
- Verify virtual environment is activated
- Run: `pip install -r requirements.txt`

### Issue: Frontend shows blank page

**Solution:**
- Check browser console for errors (F12)
- Verify backend is accessible
- Clear browser cache (Ctrl+Shift+Delete)
- Restart frontend: `npm run dev`

---

## Production Deployment

### Backend Deployment

For production, use Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

Or use Docker:

```dockerfile
FROM python:3.10
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Frontend Deployment

Build for production:

```bash
npm run build
```

This creates `dist/` folder. Deploy to:
- **Vercel** (easiest)
- **Netlify**
- **GitHub Pages**
- **AWS S3 + CloudFront**

---

## Environment Variables

### Backend (.env)

```
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_PRIMARY_MODEL=qwen2.5-coder
OLLAMA_FALLBACK_MODEL=llama3
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# CORS
CORS_ORIGINS=["http://localhost:5173"]

# Database
CHROMADB_PATH=./chromadb
MAX_CHUNK_SIZE=2000

# Timeouts
REQUEST_TIMEOUT=30
OLLAMA_TIMEOUT=60
```

### Frontend (.env.local)

```
VITE_API_URL=http://localhost:8000
```

---

## Next Steps

1. ✅ **Setup complete!** Try analyzing an API:
   - Visit http://localhost:5173
   - Paste API documentation
   - Watch code generation

2. 📚 **Learn the features:**
   - Read [FEATURES.md](FEATURES.md)
   - Check [API_SPEC.md](API_SPEC.md)

3. 🔧 **Contributing:**
   - Read [CONTRIBUTING.md](../CONTRIBUTING.md)
   - Create a feature branch
   - Submit PR

4. 🚀 **Next milestones:**
   - Day 2: Enhanced endpoint extraction
   - Day 3: Auth detection improvements
   - Day 4: SDK detection system
   - Day 5: Advanced code generation

---

## Getting Help

- **Issues:** [GitHub Issues](https://github.com/Sonuolikkara/Smart-DevTool-for-API-Integration/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Sonuolikkara/Smart-DevTool-for-API-Integration/discussions)
- **Email:** sonu@example.com

---

**Happy coding! 🚀**
