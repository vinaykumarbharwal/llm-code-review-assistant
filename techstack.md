# Tech Stack
## LLM-Powered Code Review Assistant

**Language:** Python 3.11+  
**Version:** 1.0.0

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Webhook                           │
│                   POST /webhook/github                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Application                          │
│          (API layer, auth, request validation)                  │
└────────┬───────────────────────────────────┬────────────────────┘
         │                                   │
         ▼                                   ▼
┌─────────────────┐                ┌─────────────────────────────┐
│  Celery Worker  │                │     RAG / Retrieval Layer   │
│  (async jobs)   │                │   (ChromaDB + Embeddings)   │
└────────┬────────┘                └─────────────┬───────────────┘
         │                                       │
         ▼                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM Review Engine                            │
│        (Prompt builder → LLM call → Response parser)           │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐    ┌──────────────────┐
│   PostgreSQL    │    │   GitHub REST    │
│  (review store) │    │   (post-back)    │
└─────────────────┘    └──────────────────┘
```

---

## 2. Core Stack

### 2.1 Language & Runtime

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.11 | Best ecosystem for LLM/ML tooling; async support via asyncio |
| Package manager | `uv` | Fast, modern; replaces pip + virtualenv |
| Dependency file | `pyproject.toml` | PEP 517 standard; works with uv, pip, Poetry |

### 2.2 Web Framework

```
fastapi==0.111.*
uvicorn[standard]==0.29.*
pydantic==2.*
```

- **FastAPI** — async-native, automatic OpenAPI docs, Pydantic v2 validation
- **Uvicorn** — ASGI server with `uvloop` for high-throughput async I/O
- **Pydantic v2** — data validation for request/response models and LLM output parsing

### 2.3 LLM Integration

```
anthropic==0.26.*          # Primary: Claude claude-sonnet-4-20250514
openai==1.*                # Fallback / alternative
langchain-core==0.2.*      # Prompt templates, output parsers (no full LangChain)
tiktoken==0.7.*            # Token counting for context window management
```

- **Claude claude-sonnet-4-20250514** is the primary model — best reasoning-to-cost ratio for code review
- Prompt templates built with `langchain-core` PromptTemplate; avoids heavy LangChain overhead
- `tiktoken` used to count tokens before each API call and chunk diffs that exceed the limit

### 2.4 Diff Parsing

```
unidiff==0.7.*             # Parse unified diff format into structured objects
pygments==2.*              # Syntax highlighting + language detection from file extension
```

- `unidiff` converts raw `git diff` output into `PatchSet → PatchedFile → Hunk → Line` objects
- Each hunk is independently reviewable; this is the unit fed to the LLM

### 2.5 RAG / Retrieval Layer

```
chromadb==0.5.*            # Vector store (local, no infra needed in dev)
sentence-transformers==3.* # Embeddings: all-MiniLM-L6-v2 (fast, good quality)
langchain-text-splitters==0.2.*  # Chunk documents before embedding
```

- **ChromaDB** runs in-process for development; swap to Chroma HTTP server for production
- Embedding model: `all-MiniLM-L6-v2` via `sentence-transformers` — no external API calls for embeddings
- At review time: embed the diff summary → retrieve top-3 relevant guideline chunks → prepend to LLM prompt

### 2.6 GitHub Integration

```
PyGithub==2.*              # GitHub REST API (post review comments, fetch diffs)
httpx==0.27.*              # Async HTTP client for webhook validation + API calls
```

- **PyGithub** handles PR comment creation, review submission, and diff fetching
- Webhook `X-Hub-Signature-256` HMAC validation done manually with `hmac` + `hashlib` (stdlib)

### 2.7 Async Job Queue

```
celery==5.*
redis==5.*
flower==2.*                # Celery monitoring UI
```

- **Celery** with Redis broker processes review jobs asynchronously
- Prevents webhook timeout (GitHub requires response < 10s; reviews take up to 30s)
- `flower` provides a job monitoring dashboard at `/flower`

### 2.8 Database

```
sqlalchemy==2.*            # Async ORM with asyncpg
alembic==1.*               # Migrations
asyncpg==0.29.*            # Async PostgreSQL driver
```

- **PostgreSQL 16** stores: reviews, comments, ingested documents, webhook events
- SQLAlchemy 2.x with async session for non-blocking DB access inside FastAPI endpoints

### 2.9 Configuration & Secrets

```
pydantic-settings==2.*     # Settings from .env / environment variables
python-dotenv==1.*         # Load .env in development
```

```python
# config.py pattern
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    github_webhook_secret: str
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    llm_model: str = "claude-sonnet-4-20250514"
    max_diff_lines: int = 1000

    class Config:
        env_file = ".env"
```

---

## 3. Testing

```
pytest==8.*
pytest-asyncio==0.23.*     # Async test support
pytest-cov==5.*            # Coverage reporting
httpx                      # TestClient for FastAPI (already in deps)
respx==0.21.*              # Mock httpx calls in tests
factory-boy==3.*           # Test data factories
```

- Unit tests: diff parser, prompt builder, response parser
- Integration tests: full review flow against a mocked LLM response
- Contract tests: webhook payload handling
- Target: ≥ 80% coverage enforced in CI via `pytest --cov --cov-fail-under=80`

---

## 4. Observability

```
structlog==24.*            # Structured JSON logging
prometheus-fastapi-instrumentator==6.*  # Auto-expose /metrics
sentry-sdk[fastapi]==2.*   # Error tracking
```

- All logs emitted as JSON with `review_id`, `pr_reference`, `duration_ms` fields
- Prometheus metrics: `review_duration_seconds`, `review_errors_total`, `llm_tokens_used_total`
- Sentry for exception capture in production

---

## 5. Infrastructure & Deployment

### Local Development

```
docker-compose.yml
├── app (FastAPI + Uvicorn)
├── worker (Celery)
├── postgres:16-alpine
├── redis:7-alpine
└── flower
```

### Production (Recommended)

| Component | Service |
|-----------|---------|
| Container orchestration | Docker + Fly.io or Render |
| PostgreSQL | Supabase or Railway |
| Redis | Upstash Redis |
| Secrets management | Environment variables via platform |
| CI/CD | GitHub Actions |

### GitHub Actions CI Pipeline

```yaml
# .github/workflows/ci.yml
steps:
  - Lint: ruff check . + ruff format --check
  - Type check: mypy src/
  - Test: pytest --cov --cov-fail-under=80
  - Build: docker build
  - Deploy: fly deploy (on main branch merge)
```

---

## 6. Code Quality Tools

```
ruff==0.4.*                # Linter + formatter (replaces black + isort + flake8)
mypy==1.*                  # Static type checking
pre-commit==3.*            # Git hooks: ruff + mypy on every commit
```

`pyproject.toml` configuration:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "N", "S", "B", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

---

## 7. Project Structure

```
code-review-assistant/
├── pyproject.toml
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── alembic/
│   └── versions/
├── src/
│   └── app/
│       ├── main.py              # FastAPI app factory
│       ├── config.py            # Pydantic settings
│       ├── api/
│       │   ├── review.py        # POST /review
│       │   ├── ingest.py        # POST /ingest
│       │   └── webhook.py       # POST /webhook/github
│       ├── core/
│       │   ├── diff_parser.py   # unidiff wrapper
│       │   ├── prompt_builder.py
│       │   ├── llm_client.py    # Anthropic / OpenAI abstraction
│       │   └── response_parser.py
│       ├── rag/
│       │   ├── embedder.py      # sentence-transformers
│       │   └── retriever.py     # ChromaDB queries
│       ├── github/
│       │   ├── client.py        # PyGithub wrapper
│       │   └── webhook.py       # Signature validation
│       ├── workers/
│       │   └── review_worker.py # Celery task
│       ├── models/
│       │   └── db.py            # SQLAlchemy ORM models
│       └── schemas/
│           └── review.py        # Pydantic request/response schemas
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

---

## 8. Key Design Decisions

**Why not LangChain?** LangChain adds significant abstraction overhead for a focused use case. Using `langchain-core` (prompt templates + output parsers only) keeps the dependency surface small while still benefiting from battle-tested primitives.

**Why Celery over FastAPI BackgroundTasks?** GitHub webhooks must return 200 within 10 seconds. Full reviews can take 15–30 seconds. Celery with Redis gives durable, retriable, observable async processing — BackgroundTasks don't survive worker restarts.

**Why ChromaDB over Pinecone/Weaviate?** Zero infrastructure for local development. Chromadb HTTP server mode is production-ready without a managed service. Easy swap if scale demands it.

**Why Claude over GPT-4?** Claude claude-sonnet-4-20250514 has a 200k token context window (critical for large diffs), strong instruction-following for structured JSON output, and competitive pricing for high-volume review workloads.

---

## 9. Full Dependency List

```toml
[project]
name = "code-review-assistant"
version = "1.0.0"
requires-python = ">=3.11"

dependencies = [
    # Web
    "fastapi==0.111.*",
    "uvicorn[standard]==0.29.*",
    "pydantic==2.*",
    "pydantic-settings==2.*",
    "python-dotenv==1.*",
    # LLM
    "anthropic==0.26.*",
    "openai==1.*",
    "langchain-core==0.2.*",
    "tiktoken==0.7.*",
    # Diff parsing
    "unidiff==0.7.*",
    "pygments==2.*",
    # RAG
    "chromadb==0.5.*",
    "sentence-transformers==3.*",
    "langchain-text-splitters==0.2.*",
    # GitHub
    "PyGithub==2.*",
    "httpx==0.27.*",
    # Queue
    "celery==5.*",
    "redis==5.*",
    "flower==2.*",
    # Database
    "sqlalchemy==2.*",
    "alembic==1.*",
    "asyncpg==0.29.*",
    # Observability
    "structlog==24.*",
    "prometheus-fastapi-instrumentator==6.*",
    "sentry-sdk[fastapi]==2.*",
]

[project.optional-dependencies]
dev = [
    "pytest==8.*",
    "pytest-asyncio==0.23.*",
    "pytest-cov==5.*",
    "respx==0.21.*",
    "factory-boy==3.*",
    "ruff==0.4.*",
    "mypy==1.*",
    "pre-commit==3.*",
]
```
