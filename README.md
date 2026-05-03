
# LLM Code Review Assistant

AI-powered code review service with a FastAPI backend, Groq LLM integration, optional Celery worker flow, and a minimal React frontend.

## What it does

- Accepts unified git diffs at `POST /review`.
- Builds a review prompt and calls Groq.
- Returns structured review JSON:
	- `summary`
	- `stats` (`critical`, `major`, `minor`, `info`)
	- `comments` (file, lines, severity, category, message, suggested fix)
- Includes a local stub mode for offline development.

## Tech stack

- Backend: FastAPI, Pydantic v2, httpx
- Worker: Celery + Redis
- Data: SQLAlchemy + asyncpg + Alembic
- Frontend: React (CRA)
- LLM: Groq OpenAI-compatible chat completions API

## Requirements

- Python 3.11+
- Node.js 16+
- Redis (for Celery flows)
- PostgreSQL (for persistence work; schema is scaffolded)

## Environment variables

Copy `.env.example` to `.env` and set values:

- `GROQ_API_KEY`: Groq API key
- `GITHUB_WEBHOOK_SECRET`: webhook signing secret
- `DATABASE_URL`: database URL
- `REDIS_URL`: Redis URL (default: `redis://localhost:6379/0`)
- `LLM_MODEL`: Groq model name (default: `llama-3.3-70b-versatile`)
- `MAX_DIFF_LINES`: max diff lines accepted

Optional local override:

- `FORCE_STUB_LLM=1` to skip network calls and return a deterministic stub response.

## Setup (venv-first)

### 1) Backend

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install uv
uv pip install -e .[dev]
```

Run API:

```powershell
.venv\Scripts\python.exe -m uvicorn src.app.main:app --reload
```

Run worker (optional):

```powershell
.venv\Scripts\python.exe -m celery -A src.app.workers.review_worker worker --loglevel=info
```

### 2) Frontend

```powershell
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:4000`.
Backend runs on `http://localhost:8000`.

## Quick API test

PowerShell example:

```powershell
$diff = @'
diff --git a/src/example.py b/src/example.py
index 0000000..1111111 100644
--- a/src/example.py
+++ b/src/example.py
@@ -1,3 +1,3 @@
-def add(a,b):
+def add(a, b):
		 return a+b
'@

Invoke-RestMethod -Uri http://localhost:8000/review -Method Post -ContentType 'application/json' -Body (@{ diff = $diff } | ConvertTo-Json)
```

## Project structure

- `src/app/main.py`: FastAPI app + CORS
- `src/app/api/review.py`: review endpoint and response shaping
- `src/app/core/llm_client.py`: Groq client + model fallback + stub mode
- `src/app/workers/review_worker.py`: Celery review task
- `src/app/schemas/review.py`: Pydantic response schema
- `src/app/models/db.py`: DB models (scaffold)
- `scripts/run_review_test.py`: local review harness
- `frontend/src/App.js`: minimal review UI

## Testing and validation

Run tests in venv:

```powershell
.venv\Scripts\python.exe -m pytest -q
```

Run local harness:

```powershell
.venv\Scripts\python.exe scripts\run_review_test.py
```

Build frontend:

```powershell
cd frontend
npm run build
```

## Troubleshooting

- `400 Bad Request` from Groq:
	- usually caused by invalid model name or malformed payload.
	- defaults now use `llama-3.3-70b-versatile`, and fallback models are attempted in the LLM client.
- DNS/network errors (`getaddrinfo failed`):
	- verify internet/DNS access from your machine.
	- use `FORCE_STUB_LLM=1` for local/offline work.
- Frontend fetch errors:
	- ensure backend is running on port `8000` and frontend on `4000`.
- Celery connection failures:
	- verify Redis is running and `REDIS_URL` is correct.

## Current status

- Groq integration is active in backend.
- `/review` returns structured review JSON.
- Frontend can submit diffs and render responses.
- Celery task can call LLM, but full DB persistence/retrieval endpoints are still pending.

## Next recommended improvements

1. Persist review results and add `GET /reviews/{review_id}`.
2. Add mocked Groq integration tests (no external network dependency).
3. Complete RAG ingestion/retrieval pipeline and prompt enrichment.
4. Add GitHub PR inline comment posting flow.

