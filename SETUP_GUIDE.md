# Backend Setup & Running Guide (Windows)

## ⚡ Quick Start (5 minutes)

### 1. Terminal Setup
```powershell
# Open PowerShell as Administrator
# Navigate to project root
cd C:\Users\user\OneDrive\Desktop\Marking

# Activate Python environment
& .\.venv\Scripts\Activate.ps1

# Verify activation (should show (.venv) prefix)
```

### 2. Set PYTHONPATH (Critical Fix)
```powershell
# Set environment variable for current session
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)\apps\api"

# Verify
echo $env:PYTHONPATH
```

### 3. Run Backend
```powershell
# Navigate to API folder
cd apps\api

# Start uvicorn with proper module path
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# Press CTRL+C to quit
```

### 4. Test Backend
```
Visit in browser:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/healthz
```

---

## 🔧 Running Scripts

### Using run_backend.ps1
```powershell
# From project root
.\run_backend.ps1

# This script does:
# 1. Activates .venv
# 2. Sets PYTHONPATH
# 3. Starts uvicorn
```

### Running Frontend in Parallel
```powershell
# Open a NEW PowerShell window

# Navigate to web app
cd C:\Users\user\OneDrive\Desktop\Marking\apps\web

# Start dev server
npm run dev

# Expected output:
# VITE v5.x.x  ready in XXX ms
# ➜  Local:   http://localhost:5173/
```

---

## 🗄️ Database Setup (One-time)

### If PostgreSQL Not Installed
1. Download: https://www.postgresql.org/download/windows/
2. During installation, set password (remember it!)
3. Add PostgreSQL bin to PATH (installer asks)

### Create Database
```powershell
# From project root (admin PowerShell)
.\scripts\create_db.ps1 -pgUser "postgres" -pgPassword "your_password" -dbName "ai_handwritten"

# Success message:
# Database 'ai_handwritten' created successfully
```

### Configure .env
```powershell
# Copy example
Copy-Item .env.example .env

# Edit .env with your values:
# DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/ai_handwritten
# REDIS_URL=redis://localhost:6379/0
```

---

## 🚨 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"

**Root Cause:** PYTHONPATH not set or wrong working directory

**Fix:**
```powershell
# Option 1: Run from apps\api directory
cd C:\Users\user\OneDrive\Desktop\Marking\apps\api
python -m uvicorn app.main:app --reload

# Option 2: Set PYTHONPATH first
$env:PYTHONPATH = "C:\Users\user\OneDrive\Desktop\Marking\apps\api"
cd C:\Users\user\OneDrive\Desktop\Marking
python -m uvicorn app.main:app --reload
```

### Error: "Port 8000 already in use"

**Fix:**
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
Get-Process -Id <PID> | Stop-Process -Force

# Or use different port
python -m uvicorn app.main:app --port 8001 --reload
```

### Error: "Cannot connect to database"

**Fix:**
```powershell
# 1. Check PostgreSQL is running
# 2. Verify DATABASE_URL in .env
# 3. Create database:
.\scripts\create_db.ps1

# 4. For quick testing, use SQLite (edit .env):
# DATABASE_URL=sqlite+aiosqlite:///./test.db
```

### Error: "CORS error in browser console"

**Fix:**
1. Verify frontend URL is in CORS_ORIGINS in config.py
2. Restart backend
3. Hard refresh frontend (Ctrl+Shift+R)

---

## 📊 Verify Setup

### Check Python
```powershell
python --version
# Should output: Python 3.13.x
```

### Check Node
```powershell
node --version
npm --version
# Should output versions
```

### Check PostgreSQL
```powershell
psql --version
# Should output version
```

### Check Backend Connection
```powershell
# From project root
curl http://localhost:8000/healthz

# Should return JSON:
# {"status":"ok"}
```

### Check Frontend Connection
```powershell
# From apps\web
npm run dev

# Visit http://localhost:5173
# Should see login page
```

---

## 📝 Environment Variables

**Minimal .env for development:**
```
PROJECT_NAME=AI Handwritten Answer Evaluation Platform
API_V1_STR=/api/v1

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_handwritten
SYNC_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_handwritten
REDIS_URL=redis://localhost:6379/0

JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key

OCR_MODEL_EN=microsoft/trocr-base-handwritten
SENTENCE_TRANSFORMER_MODEL=sentence-transformers/all-MiniLM-L6-v2

SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_BUCKET=answer-sheets

KW_WEIGHT=0.5
SEM_WEIGHT=0.5
```

---

## 🎯 What Each Component Does

| Component | Purpose | Port | Command |
|-----------|---------|------|---------|
| **Backend (FastAPI)** | API server, business logic | 8000 | `uvicorn app.main:app --reload` |
| **Frontend (Vite)** | React web app | 5173 | `npm run dev` |
| **Database (PostgreSQL)** | Store users, exams, results | 5432 | Auto (psql in PATH) |
| **Cache (Redis)** | Cache, task queue | 6379 | Optional for dev |
| **Celery Worker** | Async OCR/scoring jobs | N/A | `celery -A app.celery_app worker` |

---

## 🔗 URLs During Development

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/healthz

---

## ✅ Success Checklist

- [ ] Python 3.13 installed
- [ ] PostgreSQL installed and running
- [ ] Node.js 20+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file configured
- [ ] Database created
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] API docs load at http://localhost:8000/docs
- [ ] Login page loads at http://localhost:5173

---

## 💡 Pro Tips

1. **Use VS Code Terminal**: Built-in terminal makes managing multiple processes easier
2. **Keep Terminals Organized**: One for backend, one for frontend
3. **Monitor Logs**: Watch for errors in real-time
4. **Hot Reload**: Both backend (uvicorn) and frontend (vite) auto-reload on file changes
5. **Clear Cache**: If things break, delete `.venv` and `node_modules`, reinstall

---

**Last Updated**: December 2025
**Status**: Ready for local development
