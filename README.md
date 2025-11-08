# AI Handwritten Answer Evaluation Platform

Production-ready monorepo scaffold for an AI-assisted assessment pipeline built with React, FastAPI, Celery, PostgreSQL, and Supabase storage. The platform automates OCR extraction, semantic scoring, analytics, and incorporates a teacher feedback loop for continuous retraining.

## Repository Structure

```
.
├── apps
│   ├── api                # FastAPI application
│   │   ├── app            # Source code
│   │   └── requirements.txt
│   └── web                # React + Vite + Tailwind frontend
├── infra                  # Docker, deployment, infrastructure assets
├── scripts                # Maintenance scripts (e.g., retraining)
├── .github/workflows      # CI/CD automation
└── .env.example           # Environment variable template
```

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional for containerized setup)
- Redis, PostgreSQL, and Supabase credentials for production deployments

## Getting Started (Local Dev)

1. **Clone & configure environment**

   ```bash
   cp .env.example .env
   # Update secrets, Supabase credentials, database URLs, etc.
   ```

2. **Backend setup**

   ```bash
   cd apps/api
   python -m venv .venv && source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Celery worker**

   ```bash
   celery -A app.celery_app.celery worker --loglevel=info
   ```

4. **Frontend setup**

   ```bash
   cd ../../apps/web
   npm install
   npm run dev
   ```

   The frontend is available at `http://localhost:5173`, proxied to the FastAPI backend at `http://localhost:8000`.

5. **Seed demo data (optional but recommended)**

   ```bash
   cd ../../scripts
   python seed_demo_data.py
   ```

   This creates a demo teacher account (`teacher@example.com` / `Password123!`) along with sample exams and questions for local testing.

## Docker Compose

Run the full stack (API, worker, PostgreSQL, Redis):

```bash
cd infra
docker compose up --build
```

> Mounts the local `apps/api` directory for hot reloading. Ensure `.env` is configured before running.

## Key Backend Endpoints

| Endpoint                    | Method | Description                                  |
|-----------------------------|--------|----------------------------------------------|
| `/api/v1/auth/register`     | POST   | Register and receive JWT tokens               |
| `/api/v1/auth/login`        | POST   | Authenticate a user                           |
| `/api/v1/uploads`           | POST   | Upload handwritten answer sheets              |
| `/api/v1/process/start/{id}`| POST   | Trigger OCR + scoring pipeline                |
| `/api/v1/results/{id}`      | GET    | Retrieve evaluation scores and confidence     |
| `/api/v1/feedback`          | POST   | Submit teacher corrections                    |
| `/api/v1/analytics/overview`| GET    | Aggregated class/answer analytics             |
| `/api/v1/batch`             | POST   | Batch upload of PDFs / images                 |
| `/healthz`                  | GET    | Health check for uptime monitoring            |

## AI Service Stubs

- **OCR**: `services/ocr_service.py` uses TrOCR with Hindi detection + Tesseract fallback.
- **Layout Detection**: `services/layout_service.py` integrates YOLOv8 stubs for diagrams & bounding boxes.
- **Scoring**: `services/scoring_service.py` combines RapidFuzz keyword matching with Sentence-BERT semantics.
- **Diagram Analysis**: `services/diagram_service.py` applies OpenCV edge detection heuristics.
- **Feedback & Retraining**: `services/feedback_service.py` captures teacher feedback and exposes a retrain stub (`scripts/retrain_model.py`).
- **Analytics**: `services/analytics_service.py` aggregates marks, confidences, and keyword gaps with caching.

All heavy ML dependencies are optional; graceful fallbacks ensure the API remains responsive even when GPU-specific packages are missing.

## 🤖 Machine Learning in Evaluation

This project uses **Sentence Transformers** (`paraphrase-MiniLM-L6-v2`) to semantically compare handwritten OCR text with the reference answer. The ML-based evaluation service (`services/evaluation_service.py`) calculates text similarity using cosine similarity between embeddings and converts it into a normalized score (0–10).

### How It Works

1. **Model Loading**: The sentence transformer model is loaded once at startup and cached for performance.
2. **Semantic Similarity**: Student answers and reference answers are converted to embeddings, and cosine similarity is calculated.
3. **Score Mapping**: 
   - Similarity < 0.4 → Score = 2
   - Similarity 0.4–0.7 → Score = 2–8 (linear mapping)
   - Similarity ≥ 0.7 → Score = 8–10 (linear mapping)
4. **Confidence**: The normalized similarity (0–1) is used as the confidence metric.
5. **Auto-Flagging**: Answers with confidence < 0.5 are automatically flagged for teacher review.

### ML Evaluation Features

- **Pure ML-based scoring**: Uses semantic similarity instead of keyword matching
- **Confidence metrics**: Provides confidence scores for each evaluation
- **Automatic review flags**: Low-confidence answers are flagged for manual review
- **Fallback support**: Gracefully falls back to simple similarity if ML model is unavailable

The evaluation results include:
- `score`: ML-based score (0–10)
- `confidence`: Model confidence (0–1)
- `similarity`: Semantic similarity between answers (0–1)
- `student_answer`: OCR-extracted text
- `reference_answer`: Model/reference answer text

## Frontend Highlights

- **Upload Page**: Handles multi-format uploads with live messaging.
- **Dashboard**: Displays scoring + confidence summaries per submission.
- **Analytics**: Recharts-based visualisations for confidence and keyword coverage.
- **Admin Panel**: Manage question metadata, keyword lists, and weighting.

The frontend uses TailwindCSS for styling and Axios with a simple API hook for JWT-authenticated requests.

## Batch Processing & Jobs

- `/api/v1/batch` accepts multiple files and queues Celery jobs.
- `/api/v1/jobs/{job_id}` provides progress + final status.
- `app/tasks/batch.py` is the extension point for orchestrating OCR + scoring pipelines across large uploads.

## Retraining Pipeline

`scripts/retrain_model.py` demonstrates how to pull curated feedback records and prepare for fine-tuning (e.g., Sentence-BERT). Extend this script to push updated embeddings back into production models.

## Deployment

- **Backend**: Render / Railway using `infra/Dockerfile.api`.
- **Worker**: Render worker or Railway via `infra/Dockerfile.worker`.
- **Frontend**: Vercel deployment using standard Vite workflow.
- **Database & Storage**: Supabase (PostgreSQL + bucket storage).

GitHub Actions workflow (`.github/workflows/deploy.yml`) builds & deploys both frontend and backend on pushes to `main`. Configure the following secrets:

- `RENDER_DEPLOY_HOOK`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

## Testing & Linting

- Backend: `python -m compileall app` (placeholder, extend with pytest).
- Frontend: `npm run lint` (ESLint + React rules).

## Next Steps

- Connect Supabase storage for uploads & metadata.
- Integrate true OCR + layout pipelines and update Celery tasks accordingly.
- Expand analytics dashboards with live data.
- Harden authentication (password reset, role-based access).

---

This scaffold provides a robust baseline to accelerate feature development while keeping production deployment paths clear and auditable.

## 🚀 LOCAL RUN (Windows)

1. Install PostgreSQL 16 → https://www.postgresql.org/download/windows/  

   Note your password during setup.



2. Ensure PostgreSQL `bin` is in PATH, or use pgAdmin.



3. From project root:

```powershell
# Activate Python environment
& .\.venv\Scripts\Activate.ps1

# Create database
.\scripts\create_db.ps1 -pgUser "postgres" -pgPassword "YOUR_PASSWORD" -dbName "markingdb"

# Copy .env.example → .env and edit:
# DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/markingdb

# Start backend
.\run_backend.ps1

# In another PowerShell window
.\fix_frontend.ps1

# Access:
# Backend → http://localhost:8000/docs
# Frontend → http://localhost:5173
```

4. (Optional) To clean node_modules before commit:

```powershell
.\scripts\cleanup_git_node.ps1
```

5. (Optional) For quick dev without PostgreSQL, edit `.env`:

```
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

Then rerun backend.

