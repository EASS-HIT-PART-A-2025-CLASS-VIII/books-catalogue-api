# filepath: book_service/app/repository.py

from typing import Optional, Dict
from .models import Book, BookCreate

class BookRepository:
    """
    In-memory storage for books.
    This implementation does NOT require a database session.
    Used when BOOK_DB_MODE="memory".
    """

    def __init__(self) -> None:
        """Initializes the repository with an empty dictionary."""
        self._items: Dict[int, Book] = {}
        self._next_id = 1

    def list(self, *, skip: int = 0, limit: int = 100) -> list[Book]:
        """
        Get all books with pagination support.
        """
        all_books = list(self._items.values())
        return all_books[skip : skip + limit]

    def create(self, payload: BookCreate) -> Book:
        """
        Add a new book to the dictionary and return it with an assigned ID.
        """
        book = Book(id=self._next_id, **payload.model_dump())
        self._items[book.id] = book
        self._next_id += 1
        return book

    def get(self, book_id: int) -> Optional[Book]:
        """
        Get a book by ID, or None if not found.
        """
        return self._items.get(book_id)

    def delete(self, book_id: int) -> bool:
        """
        Remove a book by ID. 
        Returns True if deleted, False if not found.
        """
        if book_id in self._items:
            self._items.pop(book_id)
            return True
        return False

    def delete_all(self) -> int:
        """
        Remove all books. Useful for resetting state between tests.
        """
        count = len(self._items)
        self._items.clear()
        self._next_id = 1
        return count