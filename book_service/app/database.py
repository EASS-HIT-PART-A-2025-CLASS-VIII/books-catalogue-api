# book_service/app/database.py

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from .config import Settings

_settings = Settings()


def get_settings() -> Settings:
    """Dependency provider for FastAPI."""
    return _settings


SettingsDep = Annotated[Settings, Depends(get_settings)]


def _build_engine(settings: Settings):
    """
    Build SQLAlchemy engine according to BOOK_DB_MODE.
    """
    if settings.db_mode == "memory":
        url = "sqlite:///:memory:"
    elif settings.db_mode == "sqlite":
        url = settings.database_url_sqlite
    elif settings.db_mode == "postgres":
        url = settings.database_url_postgres
    else:
        raise ValueError(f"Invalid BOOK_DB_MODE: {settings.db_mode}")

    kwargs: dict = {"echo": settings.database_echo}

    if url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}

        # StaticPool is REQUIRED only for in-memory SQLite
        if settings.db_mode == "memory":
            kwargs["poolclass"] = StaticPool

    return create_engine(url, **kwargs)


engine = _build_engine(_settings)


def init_db() -> None:
    """
    Initializes the database schema.
    """
    from . import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a DB session."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


