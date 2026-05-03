
# LLM Code Review Assistant

## What is this?

This project is an AI-powered backend service that helps you review code automatically. It uses a Large Language Model (LLM) to analyze code changes and gives you helpful feedback, just like a human code reviewer.

---

## What can it do?

- **Review code changes:** Submit a code diff or pull request, and the AI will check for bugs, security issues, and style problems.
- **Give structured feedback:** You get clear comments about what’s wrong and how to fix it.
- **Integrate with GitHub:** You can connect it to GitHub to review pull requests automatically.
- **Store results:** All reviews are saved in a database for future reference.
- **API access:** You can use the API from your own tools, scripts, or a future frontend.

---

## How do I use it?

1. **Set up your environment:**
	- Install Python 3.11+, PostgreSQL, and Redis.
	- Copy `.env.example` to `.env` and fill in your keys and database info.

2. **Install dependencies:**
	```
	pip install uv
	uv pip install -e .[dev]
	```

3. **Start the services:**
	- Run Redis and PostgreSQL.
	- Start the FastAPI app:
	  ```
	  uvicorn src.app.main:app --reload
	  ```
	- Start the Celery worker (in another terminal):
	  ```
	  celery -A src.app.workers.review_worker worker --loglevel=info
	  ```

4. **Try it out:**
	- Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.
	- Use the `/review` endpoint to submit a code diff and see the AI’s feedback.

---

## Project Structure

- `src/app/api/` — API endpoints (review, ingest, webhook)
- `src/app/core/` — Core logic (diff parsing, LLM client, prompt builder)
- `src/app/rag/` — Retrieval-Augmented Generation (embeddings, retrieval)
- `src/app/github/` — GitHub integration
- `src/app/models/` — Database models
- `src/app/schemas/` — Data schemas
- `src/app/workers/` — Celery worker for async jobs
- `tests/` — Unit and integration tests

---

## Why use this?

- **Saves time:** Automates routine code review tasks.
- **Catches more issues:** Finds bugs and security problems early.
- **Consistent feedback:** Enforces coding standards every time.
- **Easy to extend:** Add your own rules, connect to your tools, or build a frontend.

---
