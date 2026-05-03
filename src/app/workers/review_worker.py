import os
from celery import Celery
from src.app.config import Settings

settings = Settings()

celery_app = Celery(
	"review_worker",
	broker=settings.redis_url,
	backend=settings.redis_url,
)

@celery_app.task
def run_review_job(diff: str):
	# Dummy implementation: just returns the diff length
	return {"diff_length": len(diff)}
