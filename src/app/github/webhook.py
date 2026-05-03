import hmac
import hashlib

def validate_github_signature(secret: str, payload: bytes, signature: str) -> bool:
	mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
	expected = f"sha256={mac.hexdigest()}"
	return hmac.compare_digest(expected, signature)
