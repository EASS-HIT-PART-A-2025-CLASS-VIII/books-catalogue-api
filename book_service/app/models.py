# filepath: book_service/app/models.py
from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class BookBase(BaseModel):
    """Shared fields for create/read models.

    Designed to stay unchanged when swapping persistence layers (for example,
    when moving to SQLModel). The split between BookBase/Book/BookCreate
    establishes the pattern reused throughout the course.
    """
    title: str
    author: str
    description: str
    year: int = Field(ge=1900, le=2100)  # Between 1900-2100 //TODO: Change to current year
    genre: str


class Book(BookBase):
    """Response model that includes the server-generated ID.

    When migrating to SQLModel, add `table=True` while keeping the HTTP
    contract identical.
    """
    id: int


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
