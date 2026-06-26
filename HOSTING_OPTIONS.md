# Hosting Options for SkillSetu

## Important Limitation
This is a **full-stack app** (React frontend + FastAPI backend + SQLite database + Ollama AI). GitHub Pages **only hosts static sites**, so you need additional services.

---

## Option 1: Quick Demo (Frontend Only - Read Only)

### Render.com (FREE tier recommended)
1. Go to https://render.com
2. Create account (use GitHub login)
3. Click **"New"** → **"Static Site"**
4. Connect your GitHub repo
5. Settings:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
6. Deploy

**Note**: Backend won't work, but you can show the UI.

---

## Option 2: Full App Deployment (Both Frontend & Backend)

### Railway.app (FREE tier, easiest)
1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repo
4. Railway auto-detects backend (Python) and frontend
5. Set environment variables:
   - `GEMINI_API_KEY`: your-key
   - `OLLAMA_URL`: keep empty (use Gemini only)
6. Deploy

**Cost**: Free tier includes 500 hours/month, enough for testing.

---

## Option 3: Render.com Full Stack

### Step 1: Deploy Backend (Web Service)
- **Runtime**: Python 3
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `GEMINI_API_KEY`: your-key
  - `OLLAMA_URL`: empty or external Ollama URL

### Step 2: Deploy Frontend (Static Site)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `frontend/dist`
- Update `frontend/src/lib/utils.js` to point to backend URL

---

## Option 4: Codespaces / Cloud IDEs

### GitHub Codespaces
1. Push code to GitHub
2. Click **"Code"** → **"Codespaces"** → **"Create codespace"**
3. Opens VS Code in browser
4. Run locally in cloud:
   ```bash
   cd backend && uvicorn main:app --reload
   cd frontend && npm run dev
   ```
5. Share codespace URL for demo

### Replit
1. Create account at https://replit.com
2. Import from GitHub
3. Configure secrets (GEMINI_API_KEY)
4. Run with `uvicorn` and `npm`

---

## Option 5: Netlify + Fly.io (Production)

### Frontend on Netlify
```bash
cd frontend
npm run build
```
Deploy `dist/` folder to Netlify

### Backend on Fly.io
```bash
fly launch
fly deploy
```
More complex, need Docker setup.

---

## Recommendation for Your Use Case

1. **For demo/presentation**: Use **Render static site** for frontend only
2. **For full functionality**: Use **Railway.app** (owns backend + frontend)
3. **For free testing**: Use **GitHub Codespaces** or **Replit**

---

## Required Changes for Deployment

### If using Gemini only (no Ollama):
Update `backend/app/services.py` to remove/disable Ollama calls.

### If frontend on different domain:
Update CORS settings in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)