from fastapi import APIRouter, Body
from datetime import datetime
import uuid
from ..schemas.review import ReviewResponse, ReviewStats, ReviewComment

router = APIRouter(prefix="/review")

@router.post("", response_model=ReviewResponse)
def review(diff: str = Body(..., embed=True)):
    # Dummy implementation: always returns a static review
    return ReviewResponse(
        review_id=str(uuid.uuid4()),
        pr_reference=None,
        created_at=datetime.utcnow(),
        summary="Dummy review: 1 critical security issue found.",
        stats=ReviewStats(critical=1, major=0, minor=0, info=0),
        comments=[
            ReviewComment(
                file="src/auth/login.py",
                line_start=42,
                line_end=45,
                severity="critical",
                category="security",
                message="User input passed directly to SQL query — SQL injection risk.",
                suggested_fix="Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
            )
        ]
    )
