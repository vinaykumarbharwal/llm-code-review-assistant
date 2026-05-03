from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    groq_api_key: str | None = None
    github_webhook_secret: str
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    llm_model: str = "llama-3.3-70b-versatile"
    max_diff_lines: int = 1000

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        extra="ignore",
        case_sensitive=False,
    )
