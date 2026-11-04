from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "sqlite:///./interview_pilot.db"
    secret_key: str = "change-me-to-a-random-string"
    auth_password: str = "change-me"
    ai_provider: str = "demo"
    anthropic_api_key: str = ""
    backend_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    access_token_expire_minutes: int = 1440

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
