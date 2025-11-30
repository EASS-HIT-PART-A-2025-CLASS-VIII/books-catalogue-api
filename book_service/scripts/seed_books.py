# filepath: book_service/scripts/seed_books.py
"""
Seed script for Book Service API.
Adds a few example books to the in-memory repository.
"""

from fastapi.testclient import TestClient
from book_service.app.main import app

client = TestClient(app)

books = [
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "description": "Sci-fi classic",
        "year": 1965,
        "genre": "Sci-fi"
    },
    {
        "title": "Harry Potter",
        "author": "J.K. Rowling",
        "description": "Wizard boy saves world",
        "year": 1997,
        "genre": "Fantasy"
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "description": "Fantasy adventure",
        "year": 1937,
        "genre": "Fantasy"
    }
]

for book in books:
    response = client.post("/books", json=book)
    if response.status_code != 201:
        print(f"Failed to create book: {book['title']}")
    else:
        print(f"Created book: {book['title']} (id: {response.json()['id']})")

print("\n Seeded books successfully!")
