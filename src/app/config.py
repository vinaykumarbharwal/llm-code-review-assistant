from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    github_webhook_secret: str
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    llm_model: str = "llama3-70b-8192"
    max_diff_lines: int = 1000

    class Config:
        env_file = ".env"
