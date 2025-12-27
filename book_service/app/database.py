from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from .config import Settings


def get_settings() -> Settings:
    """Dependency for accessing application settings."""
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]

# Create engine using settings
settings = get_settings()
engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
)


def init_db() -> None:
    """Initialize database tables. Import models before calling this."""
    from . import models  # noqa: F401
    
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Provide a database session for dependency injection."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]