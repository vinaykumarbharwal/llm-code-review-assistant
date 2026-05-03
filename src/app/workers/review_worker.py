import os
import json
from celery import Celery
from src.app.config import Settings
from src.app.core.llm_client import call_llm

settings = Settings()

celery_app = Celery(
	"review_worker",
	broker=settings.redis_url,
	backend=settings.redis_url,
)


@celery_app.task
def run_review_job(diff: str):
	"""Run a review job in the background using the LLM.

	Returns a dict with parsed review content (summary, stats, comments).
	"""
	prompt = (
		"You are a code review assistant. Given the following git diff, produce a JSON object with:"
		" summary (short text), stats (critical/major/minor/info counts), and an array of comments."
		" Each comment should include file, line_start, line_end, severity, category, message, and suggested_fix.\n\n"
		f"DIFF:\n{diff}\n"
	)

	llm_text = call_llm(prompt)
	try:
		parsed = json.loads(llm_text)
	except Exception:
		parsed = {"summary": str(llm_text), "comments": []}

	# Return parsed structure so callers can persist it
	return parsed
