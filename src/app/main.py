from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import review, ingest, webhook

app = FastAPI(title="LLM Code Review Assistant")

# Allow the frontend dev server to call the API
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:4000",
    "http://127.0.0.1:4000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review.router)
app.include_router(ingest.router)
app.include_router(webhook.router)


@app.get("/health")
def health():
    return {"status": "ok"}
