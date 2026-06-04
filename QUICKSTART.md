# ⚡ Quick Start Guide

## 30-Second Setup

### 1. Start Backend
```bash
cd backend
python main.py
```
✅ Backend ready at: `http://localhost:8000`

### 2. Start Frontend
```bash
cd frontend
npm run dev
```
✅ Frontend ready at: `http://localhost:5173`

### 3. Open Browser
Navigate to: **`http://localhost:5173`**

---

## 🎯 Try It Now

### Option A: Upload API Docs
1. Click **"Upload File"** tab
2. Upload any API documentation file
3. See endpoints automatically extracted
4. Click **"Generate Code"** to get SDK

### Option B: Fetch from URL
1. Click **"Fetch from URL"** tab
2. Enter API docs URL (e.g., `https://docs.github.com/en/rest`)
3. Click **"Fetch & Analyze"**
4. See endpoints and generate SDK

### Option C: Try Examples
1. See 4 example API buttons:
   - 🔵 Stripe API
   - ⚫ GitHub API
   - 🔴 Twilio API
   - 🟢 OpenAI API
2. Click any button
3. Auto-fetches, analyzes, shows results
4. Generate SDK in Python, JavaScript, TypeScript, Go, or Java

---

## 🔌 Verify It's Working

### Check Backend Health
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

### Check API Docs
Open: `http://localhost:8000/docs`
- See all 14 endpoints
- Try API calls directly

---

## 📝 What You Can Do

✅ Upload API documentation (PDF, TXT, MD, HTML, JSON)
✅ Fetch API docs from URL
✅ Extract all endpoints automatically
✅ Detect authentication methods
✅ Identify response formats
✅ Analyze security aspects
✅ Generate SDK wrapper code (5 languages)
✅ Generate unit tests
✅ View all history
✅ Copy/download code

---

## 🏠 Pages

| Page | URL | Purpose |
|------|-----|---------|
| **Home** | `/` | Upload/fetch API docs, see examples |
| **Results** | `/results` | View extracted endpoints & analysis |
| **CodeGen** | `/codegen` | Generate and view SDK code |
| **History** | `/history` | View all past analyses & generations |
| **Workspace** | `/workspace` | Placeholder for future features |

---

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Need 3.9+

# Reinstall dependencies
pip install -r requirements.txt

# Check port 8000 is free
# Windows: netstat -ano | findstr :8000
```

### Frontend won't start
```bash
# Reinstall Node modules
rm -rf node_modules
npm install

# Clear cache
npm cache clean --force
npm run dev
```

### API request failing
- ✅ Check backend is running (`http://localhost:8000/health`)
- ✅ Check frontend can reach backend
- ✅ Check API docs URL is accessible
- ✅ Try a simpler URL first

---

## 📚 Documentation

- **PROJECT_COMPLETE.md** - Full feature list & API reference
- **COMPLETION_REPORT.md** - What's included & next steps
- **API_SPEC.md** - Detailed API endpoint documentation
- **README.md** - Original project overview

---

## 🎓 Example: Generate Python SDK

1. Home → Enter GitHub API URL
2. Click "Fetch & Analyze"
3. Results page shows 30+ endpoints
4. Click "Generate Code"
5. Select "Python" language
6. Copy code and paste in your project:

```python
client = GitHubClient(
    base_url="https://api.github.com",
    api_key="your-token"
)

# Use the SDK
response = client.get_repos()
print(response.data)
```

---

## 🎉 You're All Set!

**Your complete API integration platform is ready to use.**

Start building SDKs in seconds instead of hours!

---

For questions, see PROJECT_COMPLETE.md or COMPLETION_REPORT.md
