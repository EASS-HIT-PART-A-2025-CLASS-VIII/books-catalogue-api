# filepath: book_service/app/dependencies.py
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends

from .config import Settings
from .repository import BookRepository

# Create singletons
_settings = Settings()
_repository = BookRepository()


def get_settings() -> Settings:
    """Provide settings to endpoints."""
    return _settings


def get_repository() -> Generator[BookRepository, None, None]:
    """Provide repository to endpoints."""
    yield _repository


# Type aliases for cleaner endpoint signatures
SettingsDep = Annotated[Settings, Depends(get_settings)]
RepositoryDep = Annotated[BookRepository, Depends(get_repository)]