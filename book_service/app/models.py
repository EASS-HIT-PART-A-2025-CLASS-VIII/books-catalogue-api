# filepath: book_service/app/models.py
from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from sqlmodel import SQLModel, Field
from typing import Optional


class BookBase(SQLModel):
    """Shared fields for create/read models.

    Designed to stay unchanged when swapping persistence layers (for example,
    when moving to SQLModel). The split between BookBase/Book/BookCreate
    establishes the pattern reused throughout the course.
    """
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=50)
    description: str
    year: int = Field(ge=1900, le=2100)  # Between 1900-2100 
    genre: str 


class Book(BookBase, table=True):
    """Database model for books."""
    
    __tablename__ = "books"
    
    id: Optional[int] = Field(default=None, primary_key=True)



class BookCreate(BookBase):
    """Incoming payload with validation + normalization.

    This validator carries forward unchanged when the persistence layer swaps,
    demonstrating how validation rules survive storage changes.

    normalization is for Title-case, for example: 'sci-fi' → 'Sci-Fi'.
    """

    @model_validator(mode="after")
    def normalize(self) -> "BookCreate":
        self.genre = self.genre.title()
        self.author = self.author.strip()
        self.title = self.title.strip()
        return self


