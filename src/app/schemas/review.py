from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class ReviewComment(BaseModel):
	file: str
	line_start: int
	line_end: int
	severity: Literal["critical", "major", "minor", "info"]
	category: Literal["bug", "security", "performance", "readability", "style"]
	message: str
	suggested_fix: Optional[str] = None

class ReviewStats(BaseModel):
	critical: int = 0
	major: int = 0
	minor: int = 0
	info: int = 0

class ReviewResponse(BaseModel):
	review_id: str
	pr_reference: Optional[str] = None
	created_at: datetime
	summary: str
	stats: ReviewStats
	comments: List[ReviewComment]
