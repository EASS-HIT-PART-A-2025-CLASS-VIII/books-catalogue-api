from typing import Optional, Sequence
from sqlmodel import Session, select
from .models import Book, BookCreate

class BookRepository:
    """SQLModel-backed storage for books with proper session handling."""

    def __init__(self, session: Session) -> None:
        """
        Initializes the repository with a database session.
        In Session 05, this is injected via the dependency factory.
        """
        self.session = session

    def list(self, *, skip: int = 0, limit: int = 100) -> Sequence[Book]:
        """
        List all books with pagination support.
        """
        statement = select(Book).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def create(self, payload: BookCreate) -> Book:
        """
        Create a new book and persist it to the database.
        """

        record = Book.model_validate(payload)
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def get(self, book_id: int) -> Optional[Book]:
        """
        Retrieve a single book by its primary key ID.
        """
        return self.session.get(Book, book_id)

    def delete(self, book_id: int) -> bool:
        """
        Delete a book by ID. 
        Returns True if the book existed and was deleted, False otherwise.
        """
        record = self.get(book_id)
        if record is None:
            return False
        
        self.session.delete(record)
        self.session.commit()
        return True

    def delete_all(self) -> int:
        """
        Delete all books from the table and return the count of deleted items.
        Commonly used in test cleanups.
        """
        statement = select(Book)
        records = self.session.exec(statement).all()
        count = len(records)
        
        for record in records:
            self.session.delete(record)
        
        self.session.commit()
        return count