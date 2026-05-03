from fastapi import FastAPI

from .api import review, ingest, webhook

app = FastAPI(title="LLM Code Review Assistant")

app.include_router(review.router)
app.include_router(ingest.router)
app.include_router(webhook.router)

@app.get("/health")
def health():
    return {"status": "ok"}
