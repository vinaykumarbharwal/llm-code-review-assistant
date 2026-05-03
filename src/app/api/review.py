from fastapi import APIRouter, Body
from datetime import datetime
import uuid
import json
from typing import Any, Dict

from ..schemas.review import ReviewResponse, ReviewStats, ReviewComment
from src.app.core.llm_client import call_llm

router = APIRouter(prefix="/review")


def _build_response_from_llm(llm_text: str, diff: str) -> ReviewResponse:
    # Try to parse JSON first; fall back to a basic text summary
    try:
        payload = json.loads(llm_text)
    except Exception:
        payload = {"summary": str(llm_text), "comments": []}

    summary = payload.get("summary") or payload.get("summary_text") or str(payload)
    stats = payload.get("stats", {}) or {}
    comments = payload.get("comments", []) or []

    # Normalize stats
    stats_model = ReviewStats(
        critical=int(stats.get("critical", 0)),
        major=int(stats.get("major", 0)),
        minor=int(stats.get("minor", 0)),
        info=int(stats.get("info", 0)),
    )

    # Normalize comments into ReviewComment objects
    normalized_comments = []
    for c in comments:
        if not isinstance(c, dict):
            continue
        try:
            rc = ReviewComment(
                file=c.get("file", "unknown"),
                line_start=int(c.get("line_start", 0)),
                line_end=int(c.get("line_end", c.get("line_start", 0))),
                severity=c.get("severity", "info"),
                category=c.get("category", "style"),
                message=c.get("message", ""),
                suggested_fix=c.get("suggested_fix"),
            )
            normalized_comments.append(rc)
        except Exception:
            continue

    return ReviewResponse(
        review_id=str(uuid.uuid4()),
        pr_reference=None,
        created_at=datetime.utcnow(),
        summary=summary if isinstance(summary, str) else json.dumps(summary),
        stats=stats_model,
        comments=normalized_comments,
    )


@router.post("", response_model=ReviewResponse)
def review(diff: str = Body(..., embed=True)):
    # Construct a prompt for the LLM
    prompt = (
        "You are a code review assistant. Given the following git diff, produce a JSON object with:"
        " summary (short text), stats (critical/major/minor/info counts), and an array of comments."
        " Each comment should include file, line_start, line_end, severity, category, message, and suggested_fix.\n\n"
        f"DIFF:\n{diff}\n"
    )

    llm_text = call_llm(prompt)
    return _build_response_from_llm(llm_text, diff)
