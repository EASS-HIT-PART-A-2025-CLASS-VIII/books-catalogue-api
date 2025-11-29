# filepath: book_service/app/main.py
from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException, status
from .dependencies import RepositoryDep, SettingsDep
from .models import Book, BookCreate

logger = logging.getLogger("book-service")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

app = FastAPI(title="Book Service", version="0.1.0")


@app.get("/health", tags=["diagnostics"])
def health(settings: SettingsDep) -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "app": settings.app_name}


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