# filepath: book_service/app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    app_name: str = "Book Service"
    default_page_size: int = 20
    feature_preview: bool = False
    database_url: str = "sqlite:///./data/books.db"

    model_config = SettingsConfigDict(
        env_file=".env",           # Load from .env file
        env_prefix="BOOK_",       # Only read BOOK_* variables
        extra="ignore",            # Ignore unknown variables
    )


