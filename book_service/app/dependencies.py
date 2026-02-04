# filepath: book_service/app/dependencies.py


from typing import Annotated, Protocol

from fastapi import Depends

from .database import SessionDep, SettingsDep
from .repository import BookRepository as InMemoryRepository
from .repository_db import BookRepository as SqlRepository
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from .database import SettingsDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def require_role(*allowed_roles: str):
    def inner(settings: SettingsDep, token: str = Security(oauth2_scheme)):
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=["HS256"],
                audience=settings.jwt_audience,
                issuer=settings.jwt_issuer,
            )
        except jwt.PyJWTError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

        roles = set(payload.get("roles", []))
        if not roles.intersection(allowed_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return payload

    return inner


class BookRepositoryProtocol(Protocol):
    def list(self, *, skip: int = 0, limit: int = 100): ...
    def create(self, payload): ...
    def get(self, book_id: int): ...
    def delete(self, book_id: int): ...
    def delete_all(self) -> int: ...
    def search(self, query: str, *, skip: int = 0, limit: int = 100): ...


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