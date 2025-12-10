# AI Handwritten Answer Evaluation Platform - Complete Project Overview

## 🎯 Project Summary
This is a full-stack web application that uses AI to automatically evaluate handwritten answer sheets. It combines OCR (Optical Character Recognition), semantic similarity matching, and teacher feedback to score student answers intelligently.

**Tech Stack:**
- Backend: FastAPI + Python 3.13
- Frontend: React + TypeScript + Vite + TailwindCSS
- Database: PostgreSQL
- Cache/Queue: Redis
- Task Queue: Celery
- Storage: Supabase (Cloud) or Local
- ML Models: Sentence-BERT for semantic similarity, TrOCR for OCR

---

## 📁 Project Structure

```
Marking/
├── apps/
│   ├── api/                    # FastAPI Backend
│   │   ├── app/
│   │   │   ├── main.py        # FastAPI app initialization
│   │   │   ├── core/          # Core configs & database
│   │   │   │   ├── config.py  # Settings (CORS, DB URLs, JWT secrets)
│   │   │   │   └── database.py# DB session & initialization
│   │   │   ├── models/        # SQLAlchemy DB models
│   │   │   │   ├── user.py, exam.py, question.py, submission.py, etc.
│   │   │   ├── schemas/       # Pydantic request/response models
│   │   │   ├── repositories/  # Database access layer
│   │   │   ├── services/      # Business logic
│   │   │   │   ├── ocr_service.py          # Text extraction from images
│   │   │   │   ├── evaluation_service.py   # ML-based scoring
│   │   │   │   ├── feedback_service.py     # Teacher feedback collection
│   │   │   │   ├── analytics_service.py    # Statistics & reporting
│   │   │   │   └── [other services]
│   │   │   ├── api/routes/    # API endpoints
│   │   │   │   ├── auth.py    # Login/Register
│   │   │   │   ├── uploads.py # File upload handling
│   │   │   │   ├── process.py # Trigger OCR/scoring
│   │   │   │   ├── results.py # Fetch evaluation results
│   │   │   │   ├── feedback.py# Accept teacher corrections
│   │   │   │   ├── analytics.py# Get statistics
│   │   │   │   └── batch.py   # Batch processing
│   │   │   ├── tasks/         # Celery async jobs
│   │   │   └── utils/         # Helper functions
│   │   └── requirements.txt
│   │
│   └── web/                    # React Frontend
│       ├── src/
│       │   ├── main.tsx        # Entry point
│       │   ├── App.tsx         # Root component
│       │   ├── pages/          # Page components
│       │   │   ├── LoginPage.tsx
│       │   │   ├── UploadPage.tsx
│       │   │   ├── DashboardPage.tsx
│       │   │   ├── AnalyticsPage.tsx
│       │   │   └── AdminPage.tsx
│       │   ├── components/     # Reusable components
│       │   ├── api/
│       │   │   └── useApi.ts   # Axios API hook for backend calls
│       │   ├── types/          # TypeScript interfaces
│       │   └── routes/
│       ├── package.json
│       ├── vite.config.ts      # Vite bundler config
│       └── tailwind.config.js  # TailwindCSS config
│
├── infra/
│   ├── docker-compose.yml      # Local dev environment (PostgreSQL, Redis, etc.)
│   ├── Dockerfile.api          # API container
│   └── Dockerfile.worker       # Celery worker container
│
├── scripts/
│   ├── create_db.ps1           # Create PostgreSQL database (Windows)
│   ├── seed_demo_data.py       # Create test data
│   ├── retrain_model.py        # ML model retraining
│   └── cleanup_git_node.ps1
│
├── .env.example                # Environment variables template
├── run_backend.ps1             # Start backend script (Windows)
├── fix_frontend.ps1            # Start frontend script (Windows)
└── README.md
```

---

## 🔄 Core Workflow

### 1. **User Registration/Login**
- Endpoint: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`
- Creates user account or authenticates
- Returns JWT token for subsequent requests

### 2. **Upload Answer Sheets**
- Endpoint: `POST /api/v1/uploads` (single) or `POST /api/v1/batch` (multiple)
- Accepts image/PDF files containing handwritten answers
- Stores files in Supabase or local storage
- Returns submission ID

### 3. **Process & Evaluate**
- Endpoint: `POST /api/v1/process/start/{submission_id}`
- Triggers asynchronous pipeline (via Celery):
  - **OCR**: Extract text from image using TrOCR
  - **Scoring**: Compare extracted text with reference answer using Sentence-BERT
  - **Confidence**: Calculate confidence score
  - **Auto-flag**: Mark low-confidence answers for review

### 4. **Retrieve Results**
- Endpoint: `GET /api/v1/results/{submission_id}`
- Returns:
  - `score`: 0-10 evaluation score
  - `confidence`: 0-1 confidence metric
  - `similarity`: 0-1 semantic similarity
  - `student_answer`: OCR-extracted text
  - `reference_answer`: Model answer

### 5. **Teacher Feedback**
- Endpoint: `POST /api/v1/feedback`
- Teacher submits corrections and confidence adjustments
- Data collected for model retraining

### 6. **Analytics**
- Endpoint: `GET /api/v1/analytics/overview`
- Provides aggregate statistics:
  - Average scores, confidence distribution
  - Keyword coverage, common errors
  - Submission status breakdown

---

## 🔧 Configuration (config.py)

**Key Settings:**
```python
PROJECT_NAME = "AI Handwritten Answer Evaluation Platform"
API_V1_STR = "/api/v1"

# CORS Origins (frontend can call backend from these URLs)
CORS_ORIGINS = [
    "http://localhost:5173",      # Frontend dev server
    "http://127.0.0.1:5173",
    "http://localhost:8000",      # Backend docs
    "http://127.0.0.1:8000"
]

# Database
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_handwritten"

# Cache
REDIS_URL = "redis://localhost:6379/0"

# Authentication
JWT_SECRET_KEY = "change-me"      # Change in production!
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Cloud Storage (Optional)
SUPABASE_URL = ""
SUPABASE_KEY = ""
SUPABASE_BUCKET = "answer-sheets"

# ML Models
OCR_MODEL_EN = "microsoft/trocr-base-handwritten"
SENTENCE_TRANSFORMER_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Scoring Weights
KW_WEIGHT = 0.5        # Keyword matching weight
SEM_WEIGHT = 0.5       # Semantic similarity weight
```

---

## 🚀 Running the Project (Windows)

### Prerequisites
1. **Python 3.13** - Download from python.org
2. **PostgreSQL 16** - Download from postgresql.org
3. **Node.js 20+** - Download from nodejs.org
4. **Redis** (optional for local dev with Docker)

### Step 1: Setup Backend

```powershell
# Navigate to api folder
cd apps\api

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Go to project root
cd ..\..

# Create database
.\scripts\create_db.ps1 -pgUser "postgres" -pgPassword "YOUR_DB_PASSWORD" -dbName "ai_handwritten"

# Copy environment file
copy .env.example .env

# Edit .env and update:
# - DATABASE_URL with your PostgreSQL credentials
# - JWT_SECRET_KEY with a secure secret
# - SUPABASE credentials (if using cloud storage)
```

### Step 2: Start Backend

```powershell
# From project root
.\run_backend.ps1

# This runs: uvicorn app.main:app --reload
# Backend available at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

### Step 3: Setup Frontend

```powershell
# In a new PowerShell window, from project root
cd apps\web

# Install dependencies
npm install

# Start dev server
npm run dev

# Frontend available at: http://localhost:5173
```

### Step 4: (Optional) Start Celery Worker

```powershell
# For async task processing
cd apps\api
celery -A app.celery_app.celery worker --loglevel=info
```

### Step 5: (Optional) Seed Demo Data

```powershell
cd scripts
python seed_demo_data.py

# Creates:
# - Teacher account: teacher@example.com / Password123!
# - Sample exams and questions
```

---

## 📊 ML Evaluation Process

### How Scoring Works

1. **Text Extraction (OCR)**
   - Image → TrOCR model → Extracted text

2. **Semantic Comparison**
   - Student answer → Sentence-BERT embedding
   - Reference answer → Sentence-BERT embedding
   - Calculate cosine similarity (0-1)

3. **Score Mapping**
   - Similarity < 0.4 → Score = 2 (low)
   - Similarity 0.4-0.7 → Score = 2-8 (proportional)
   - Similarity ≥ 0.7 → Score = 8-10 (high)

4. **Confidence Flagging**
   - Confidence < 0.5 → Auto-flag for teacher review
   - Higher confidence = model is more certain

### Output Example

```json
{
  "evaluation_id": "uuid",
  "submission_id": "uuid",
  "score": 8.5,
  "confidence": 0.87,
  "similarity": 0.82,
  "student_answer": "The capital of France is Paris...",
  "reference_answer": "The capital of France is Paris, located...",
  "flagged_for_review": false,
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

## 🔌 Key API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/healthz` | GET | Health check |
| `/api/v1/auth/register` | POST | Create account |
| `/api/v1/auth/login` | POST | Login & get JWT |
| `/api/v1/uploads` | POST | Upload single file |
| `/api/v1/batch` | POST | Upload multiple files |
| `/api/v1/process/start/{id}` | POST | Start OCR + scoring |
| `/api/v1/results/{id}` | GET | Get evaluation results |
| `/api/v1/feedback` | POST | Submit teacher feedback |
| `/api/v1/analytics/overview` | GET | Get statistics |
| `/docs` | GET | Interactive API documentation (Swagger UI) |

---

## 🐛 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'app'"
**Solution:**
```powershell
# Make sure you're in apps\api directory
cd apps\api
# And PYTHONPATH includes current directory
set PYTHONPATH=%PYTHONPATH%;.
```

### Issue 2: Database Connection Error
**Solution:**
```powershell
# Verify PostgreSQL is running
# Check .env DATABASE_URL matches your setup
# Create database if missing:
.\scripts\create_db.ps1
```

### Issue 3: CORS Error in Browser
**Solution:**
- Ensure `http://localhost:5173` is in `CORS_ORIGINS` in config.py
- Restart backend after config changes

### Issue 4: Frontend Can't Reach Backend
**Solution:**
```typescript
// In useApi.ts, verify API_BASE_URL
const API_BASE_URL = 'http://localhost:8000';
```

---

## 📝 Code Examples

### Adding a New Evaluation Endpoint

```python
# apps/api/app/api/routes/custom_evaluation.py
from fastapi import APIRouter, Depends
from app.schemas.evaluations import EvaluationResponse
from app.services.evaluation_service import EvaluationService

router = APIRouter()

@router.post("/custom-eval", response_model=EvaluationResponse)
async def custom_evaluate(
    submission_id: str,
    service: EvaluationService = Depends()
):
    result = await service.evaluate(submission_id)
    return result
```

### Using the Evaluation Service

```python
from app.services.evaluation_service import EvaluationService

service = EvaluationService()
result = await service.evaluate(
    student_answer="Paris is the capital of France",
    reference_answer="What is the capital of France? The capital is Paris.",
)
# Returns: {"score": 8.5, "confidence": 0.87, "similarity": 0.82}
```

### Frontend API Call

```typescript
// src/pages/UploadPage.tsx
import { useApi } from '../api/useApi';

export function UploadPage() {
  const { post } = useApi();

  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await post('/uploads', formData);
    console.log('Upload ID:', response.submission_id);
  };

  return (
    <button onClick={() => handleUpload(file)}>
      Upload Answer Sheet
    </button>
  );
}
```

---

## 🎓 Learning Path

1. **Start with**: `main.py` - See how FastAPI is initialized
2. **Then explore**: `routes/` - Understand API structure
3. **Study**: `services/evaluation_service.py` - Core ML logic
4. **Check**: `models/` - Database schema
5. **Review**: `frontend/pages/UploadPage.tsx` - UI integration
6. **Deploy**: `infra/docker-compose.yml` - Production setup

---

## 🔐 Security Notes

- Change JWT_SECRET_KEY in production
- Use environment variables for all secrets (.env file)
- Enable HTTPS in production
- Validate file uploads (type, size, content)
- Implement rate limiting for API endpoints
- Use strong database passwords

---

## 📚 Next Steps for Development

1. **Improve OCR**: Integrate Google Vision API or EasyOCR
2. **Add More Models**: Support math formulas, diagrams
3. **Enhance Analytics**: Add trend analysis, performance tracking
4. **Implement Feedback Loop**: Auto-retrain models with teacher corrections
5. **Add Notifications**: Email alerts for completed evaluations
6. **Mobile App**: Build React Native version
7. **Real-time Updates**: Add WebSockets for live scoring progress

---

**Status**: Development ready with placeholder ML implementations.
Use this overview as a guide when discussing specific features or debugging issues.
