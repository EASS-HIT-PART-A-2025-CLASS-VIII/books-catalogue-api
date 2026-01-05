# filepath: book_service/app/dependencies.py


from typing import Annotated, Protocol

from fastapi import Depends

from .database import SessionDep, SettingsDep
from .repository import BookRepository as InMemoryRepository
from .repository_db import BookRepository as SqlRepository



class BookRepositoryProtocol(Protocol):
    def list(self, *, skip: int = 0, limit: int = 100): ...
    def create(self, payload): ...
    def get(self, book_id: int): ...
    def delete(self, book_id: int): ...


# singleton in-memory repo
# _memory_repo = InMemoryRepository()


def get_repository(settings: SettingsDep, session: SessionDep) -> BookRepositoryProtocol:
    if settings.db_mode == "memory":
        return InMemoryRepository()
    # if settings.db_mode == "memory":
    #     return _memory_repo  # always return the same instance
    if session is None:
        raise RuntimeError("Database session required for non-memory modes")
    return SqlRepository(session)


RepositoryDep = Annotated[BookRepositoryProtocol, Depends(get_repository)]