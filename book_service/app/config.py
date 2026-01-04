# filepath: book_service/app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Book Service"
    db_mode: str = "sqlite"  # memory | sqlite | postgres
    database_url_sqlite: str = "sqlite:///./data/books.db"
    database_url_postgres: str = "postgresql+psycopg://book:book@localhost:5432/books"
    database_url_test: str | None = None
    database_echo: bool = False
    pool_size: int = 5
    pool_timeout: int = 30

    @property
    def database_url(self) -> str:
        if self.db_mode == "postgres":
            return self.database_url_postgres
        return self.database_url_sqlite

    model_config = SettingsConfigDict(env_prefix="BOOK_", env_file=".env", extra="ignore")