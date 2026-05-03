from fastapi import APIRouter, Request, Header, HTTPException
from ..config import Settings
from ..github.webhook import validate_github_signature

router = APIRouter(prefix="/webhook/github")
settings = Settings()

@router.post("")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None)):
    body = await request.body()
    if not x_hub_signature_256 or not validate_github_signature(settings.github_webhook_secret, body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")
    # Dummy: just return event type
    event = request.headers.get("X-GitHub-Event", "unknown")
    return {"status": "ok", "event": event}
