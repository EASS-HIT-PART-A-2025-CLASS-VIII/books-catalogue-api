# filepath: book_service/scripts/seed_books.py
"""
Seed script for Book Service API.
Adds a few example books to the in-memory repository.
"""

from sqlmodel import Session, select
from book_service.app.database import engine, init_db
from book_service.app.models import Book, BookCreate
from book_service.app.repository import BookRepository
from fastapi.testclient import TestClient
from book_service.app.main import app

def seed_books() -> None: 
    """Seed the database with sample books if empty."""

    init_db()

    with Session(engine) as session:
        #check if db already has data 
        statement = select(Book)
        existing_books = session.exec(statement).first()
        
        if existing_books:
            print("Database already contains books. Skipping seed.")
            return
        
        # Seed initial movies
        repo = BookRepository(session)
        books = [
            BookCreate(title= "Dune", author= "Frank Herbert", description= "Sci-fi classic", year=  1965, genre= "Sci-fi"),
            BookCreate(title="Harry Potter", author="J.K. Rowling", description="Wizard boy saves world", year=1997, genre="Fantasy"),
            BookCreate(title="The Hobbit", author="J.R.R. Tolkien", description="Fantasy adventure", year=1937, genre="Fantasy"),
        ]
        
        for book_data in books:
            repo.create(book_data)
        
        print(f"Successfully seeded {len(books)} books.")


if __name__ == "__main__":
    seed_books()




# from fastapi.testclient import TestClient
# from book_service.app.main import app

# client = TestClient(app)

# books = [
#     {
#         "title": "Dune",
#         "author": "Frank Herbert",
#         "description": "Sci-fi classic",
#         "year": 1965,
#         "genre": "Sci-fi"
#     },
#     {
#         "title": "Harry Potter",
#         "author": "J.K. Rowling",
#         "description": "Wizard boy saves world",
#         "year": 1997,
#         "genre": "Fantasy"
#     },
#     {
#         "title": "The Hobbit",
#         "author": "J.R.R. Tolkien",
#         "description": "Fantasy adventure",
#         "year": 1937,
#         "genre": "Fantasy"
#     }
# ]

# for book in books:
#     response = client.post("/books", json=book)
#     if response.status_code != 201:
#         print(f"Failed to create book: {book['title']}")
#     else:
#         print(f"Created book: {book['title']} (id: {response.json()['id']})")

# print("\n Seeded books successfully!")
