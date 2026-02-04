# book_service/app/main.py

from __future__ import annotations
import uuid
import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .database import engine, SettingsDep
from .dependencies import RepositoryDep, require_role
from .models import Book, BookCreate
from .auth import router as auth_router
from fastapi import Query
from fastapi import Depends
# from .deps import require_role


logger = logging.getLogger("book-service")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

app = FastAPI(title="Book Service", version="0.5.0")
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-Id") or f"req-{uuid.uuid4().hex[:8]}"
    request.state.trace_id = trace_id
    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    return response

@app.get("/healthz", tags=["health"])
def healthcheck(settings: SettingsDep) -> dict[str, str]:
    if engine:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    backend = settings.db_mode if engine else "memory"
    return {"status": "ok", "app": settings.app_name, "database": backend}



@app.get("/books", response_model=list[Book], tags=["books"])
def list_books(repository: RepositoryDep) -> list[Book]:
    """Get all books."""
    return list(repository.list())


@app.post(
    "/books",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    tags=["books"],
)
def create_book(
    payload: BookCreate,
    repository: RepositoryDep,
    token: dict = Depends(require_role("editor")),
) -> Book:
    """Create a new book."""
    book = repository.create(payload)
    logger.info("book.created id=%s title=%s", book.id, book.title)
    return book


@app.get("/books/{book_id}", response_model=Book, tags=["books"])
def read_book(book_id: int, repository: RepositoryDep) -> Book:
    """Get a specific book by ID."""
    book = repository.get(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["books"],
)
def delete_book(book_id: int, repository: RepositoryDep) -> None:
    """Delete a book by ID."""
    if repository.get(book_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    repository.delete(book_id)
    logger.info("book.deleted id=%s", book_id)

@app.get("/books/search", response_model=list[Book], tags=["books"])
def search_books(
    repository: RepositoryDep,
    title: str | None = Query(None),
    author: str | None = Query(None),
    year: int | None = Query(None),
    genre: str | None = Query(None),
) -> list[Book]:
    """
    Search books by optional filters.
    """
    return list(
        repository.search(
            title=title,
            author=author,
            year=year,
            genre=genre,
        )
    )



