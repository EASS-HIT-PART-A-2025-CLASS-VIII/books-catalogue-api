
# 📚 Books Catalogue API

A FastAPI-based backend service for managing a catalogue of books, now persisting data using SQLite and SQLModel.

This project was developed as part of EASS – EX01 & EX02 (Session 04 Integration).


## ⚡ Features

- CRUD endpoints for books (`/books`)
- Validation using Pydantic
- Fully tested with `pytest`
- Persistent Storage: SQLite database integration via SQLModel.
- Database Migrations: Schema versioning using Alembic.
- Seed script for example books
- HTTP playground for easy testing
- Docker support for isolated environment


## 🐳 Requirements
- Python 3.12+

- uv (environment & dependency manager)

- Docker (optional, for containerized runs)

## 🛠 Setup and Run

Clone the project:

```bash
  git clone https://github.com/EASS-HIT-PART-A-2025-CLASS-VIII/books-catalogue-api
```

Go to the project directory:

```bash
  cd books-catalogue-api
```


## Option A - Run Locally (using uv)

Install dependencies (creates venv automatically):

```bash
  uv sync --frozen
```
#### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`BOOKS_DATABASE_URL="sqlite:///./data/books.db"`

`BOOKS_APP_NAME="Book Catalogue Service"`

#### Database Initialization (Migrations)

Before running the app, ensure the database schema is up to date:
```bash
mkdir -p data
uv run alembic upgrade head 
```

Run the API:

```bash
uv run uvicorn book_service.app.main:app --reload
```
Access the API:

- Browser/Tools: http://127.0.0.1:8000

- OpenAPI docs: http://127.0.0.1:8000/docs


## Option B - Using Docker
Build the Docker image:

```bash
  docker build -t book-service -f book_service/Dockerfile .
```
Run the container:

```bash
  docker run -p 8000:8000 --env-file .env -v $(pwd)/data:/app/data book-service
```

Access the API:
http://127.0.0.1:8000

## 🧪 Running Tests

To run tests, run the following command:

```bash
  uv run pytest book_service/tests -v
```


## 🌱 Seed Example Books
Populate the repository with example books:
```bash
uv run python -m book_service.scripts.seed_books
```
This will add books like:

- Dune by Frank Herbert

- Harry Potter by J.K. Rowling

- The Hobbit by J.R.R. Tolkien
## 📝 HTTP Playground

You can quickly test the API endpoints using the VS Code REST Client, Postman, or any HTTP client. Example requests:

### Health Check
```http
GET http://127.0.0.1:8000/health
```

### List all books
```http
GET http://127.0.0.1:8000/books
```

### Create a new book
```http
POST http://127.0.0.1:8000/books
Content-Type: application/json

{
  "title": "1984",
  "author": "George Orwell",
  "description": "Dystopian classic",
  "year": 1949,
  "genre": "Fiction"
}
```

### Get book by ID
```http
GET http://127.0.0.1:8000/books/1
```

### Delete a book
```http
DELETE http://127.0.0.1:8000/books/1
```