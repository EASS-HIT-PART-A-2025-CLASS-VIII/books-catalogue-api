# filepath: book_service/app/repository.py
# from __future__ import annotations

# from typing import Dict

# from .models import Book, BookCreate


# class BookRepository:
#     """In-memory storage for books.

#     You can swap in SQLModel + SQLite later without changing the
#     interface (list/create/get/delete), so routes stay the same.
#     """

#     def __init__(self) -> None:
#         self._items: Dict[int, Book] = {}
#         self._next_id = 1

#     def list(self) -> list[Book]:
#         """Get all books.
        
#         Always returns list[books] for consistency. SQLModel queries
#         return sequences, but convert with list() to maintain this interface.
#         """
#         return list(self._items.values())

#     def create(self, payload: BookCreate) -> Book:
#         """Add a new book and return it with assigned ID.
        
#         In a SQLModel-backed version this maps to `session.add()` +
#         `session.commit()` while keeping the same signature.
#         """
#         book = Book(id=self._next_id, **payload.model_dump())
#         self._items[book.id] = book
#         self._next_id += 1
#         return book

#     def get(self, book_id: int) -> Book | None:
#         """Get a book by ID, or None if not found.
        
#         A SQLModel-backed repository would use `session.get(Book, book_id)`.
#         """
#         return self._items.get(book_id)

#     def delete(self, book_id: int) -> None:
#         """Remove a book by ID.
        
#         A SQLModel-backed repository would call `session.delete()` +
#         `session.commit()`.
#         """
#         self._items.pop(book_id, None)

#     def clear(self) -> None:
#         """Remove all books (useful for tests).
        
#         SQL-backed fixtures should use separate test databases instead of
#         clearing a shared repository.
#         """
#         self._items.clear()
#         self._next_id = 1


################################################3

from typing import Optional
from sqlmodel import Session, select
from .models import Book, BookCreate


class BookRepository:
    """SQLite-backed storage for movies with proper session handling."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, *, skip: int = 0, limit: int = 100) -> list[Book]:
        """List all books with pagination support."""
        statement = select(Book).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def create(self, payload: BookCreate) -> Book:
        """Create a new book and persist to database."""
        record = Book.model_validate(payload)
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def get(self, book_id: int) -> Optional[Book]:
        """Retrieve a book by ID."""
        return self.session.get(Book, book_id)

    def delete(self, book_id: int) -> bool:
        """Delete a book by ID. Returns True if deleted, False if not found."""
        record = self.get(book_id)
        if record is None:
            return False
        self.session.delete(record)
        self.session.commit()
        return True

    def delete_all(self) -> int:
        """Delete all books and return count. Use with caution."""
        statement = select(Book)
        records = self.session.exec(statement).all()
        count = len(records)
        for record in records:
            self.session.delete(record)
        self.session.commit()
        return count