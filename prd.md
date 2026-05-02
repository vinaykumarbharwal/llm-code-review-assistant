# Product Requirements Document (PRD)
## LLM-Powered Code Review Assistant

**Version:** 1.0.0  
**Status:** Draft  
**Author:** Senior Engineering  
**Last Updated:** 2026-05-02

---

## 1. Executive Summary

The LLM-Powered Code Review Assistant is an AI-driven backend service that automatically analyzes Git pull request diffs and produces structured, actionable code review feedback. It targets engineering teams that want to reduce reviewer load, enforce consistency, and catch bugs and security issues earlier in the development lifecycle.

---

## 2. Problem Statement

Manual code review is slow, inconsistent, and expensive. Senior engineers spend disproportionate time on routine issues — style violations, obvious bugs, common anti-patterns — that could be caught automatically. Existing static analysis tools (ESLint, Pylint, Bandit) are rule-based and miss context-dependent issues. LLMs can reason about intent, patterns, and context in ways static tools cannot.

---

## 3. Goals & Non-Goals

### Goals
- Automatically review PR diffs and produce inline, structured feedback
- Classify issues by category: `bug`, `security`, `performance`, `readability`, `style`
- Suggest corrected code snippets for detected issues
- Integrate with GitHub via webhook for real-time PR review
- Support RAG to inject team-specific coding guidelines into review context
- Expose a REST API (FastAPI) for programmatic access and dashboard integration

### Non-Goals
- Auto-merging or auto-approving PRs
- Full IDE integration (out of scope for v1)
- Support for non-Python repositories in v1 (expandable later)
- Fine-tuning a custom model (prompt engineering + RAG is sufficient for v1)

---

## 4. Target Users

| User | Need |
|------|------|
| Engineering teams | Reduce manual review burden, enforce standards |
| Solo developers | Get AI feedback on their own PRs before requesting human review |
| DevOps / Platform teams | Automate quality gates in CI/CD pipelines |

---

## 5. User Stories

**As a developer**, I want to open a pull request and automatically receive structured AI feedback within 2 minutes, so I can fix obvious issues before requesting human review.

**As a tech lead**, I want the assistant to enforce our internal coding guidelines consistently across all PRs, so I don't have to repeat the same comments manually.

**As a security engineer**, I want the assistant to flag potential security vulnerabilities (e.g., SQL injection, hardcoded secrets, insecure deserialization) in every PR, so nothing ships with obvious CVEs.

**As a platform engineer**, I want to call the review API from our CI/CD pipeline, so review feedback becomes a required gate before merge.

---

## 6. Functional Requirements

### 6.1 PR Ingestion
- Accept GitHub webhook events (`pull_request` opened / synchronized)
- Accept direct API calls with a repo URL + PR number or a raw diff string
- Parse unified diffs into file-level and hunk-level segments
- Support PRs up to 1,000 changed lines in v1; larger PRs are chunked

### 6.2 LLM Review Engine
- Send each diff chunk to the LLM with a structured system prompt
- Produce per-line or per-hunk comments in a consistent JSON schema
- Support multi-pass review: bug pass → security pass → style pass (configurable)
- Each comment must include: `file`, `line_range`, `severity` (critical / major / minor / info), `category`, `message`, `suggested_fix`

### 6.3 RAG / Context Layer
- Ingest team guidelines from Markdown/PDF/Confluence sources
- Store embeddings in a vector database (ChromaDB in v1)
- At review time, retrieve top-k relevant guidelines based on the diff content
- Inject retrieved context into the LLM prompt alongside the diff

### 6.4 API Surface (FastAPI)
- `POST /review` — submit a diff or PR reference, returns review JSON
- `POST /ingest` — upload a new guidelines document into the RAG store
- `GET /reviews/{review_id}` — retrieve a past review by ID
- `GET /health` — liveness probe
- All endpoints return structured JSON; errors follow RFC 7807

### 6.5 GitHub Integration
- Webhook receiver validates `X-Hub-Signature-256` header
- On valid event, triggers async review job
- Posts review comments back to the PR via GitHub REST API (as a review with inline comments)
- Configurable: can run in "dry-run" mode (no post-back, just logs)

### 6.6 Dashboard (Optional v1 / Required v2)
- Simple web UI showing review history per repo
- Filter by severity, category, file
- Not blocking v1 API release

---

## 7. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Review latency (p95) | < 30 seconds for PRs ≤ 200 lines |
| Availability | 99.5% uptime |
| Throughput | 50 concurrent review jobs |
| Security | API key auth on all endpoints; secrets never logged |
| Observability | Structured JSON logs; Prometheus metrics endpoint |
| Test coverage | ≥ 80% unit + integration test coverage |

---

## 8. Review Comment Schema

```json
{
  "review_id": "uuid",
  "pr_reference": "owner/repo#42",
  "created_at": "ISO8601",
  "summary": "High-level review summary string",
  "stats": {
    "critical": 1,
    "major": 3,
    "minor": 5,
    "info": 2
  },
  "comments": [
    {
      "file": "src/auth/login.py",
      "line_start": 42,
      "line_end": 45,
      "severity": "critical",
      "category": "security",
      "message": "User input passed directly to SQL query — SQL injection risk.",
      "suggested_fix": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
    }
  ]
}
```

---

## 9. Milestones

| Milestone | Deliverables | Target |
|-----------|-------------|--------|
| M1 — Core Engine | Diff parser, LLM review pass, JSON output | Week 2 |
| M2 — API | FastAPI service, `/review` + `/health` endpoints, Docker | Week 4 |
| M3 — RAG | Embedding pipeline, ChromaDB integration, `/ingest` endpoint | Week 6 |
| M4 — GitHub | Webhook receiver, PR comment post-back, dry-run mode | Week 8 |
| M5 — Hardening | Auth, rate limiting, observability, 80% test coverage | Week 10 |

---

## 10. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| LLM hallucinating false positives | Confidence scoring; users can dismiss comments |
| Large PRs exceed context window | Chunk diffs; prioritize changed functions over context lines |
| Rate limits on LLM API | Async job queue with retry + backoff (Celery + Redis) |
| Sensitive code sent to external API | Support local model deployment (Ollama) as alternative backend |

---

## 11. Success Metrics

- 70% of LLM-flagged issues rated "useful" by developers in post-review survey
- < 5% false-positive rate on `critical` severity comments
- Review turnaround time < 30s p95 for standard PRs
- Adoption by ≥ 3 internal teams within 60 days of v1 launch
