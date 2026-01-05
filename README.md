
# 📚 Books Catalogue API


A FastAPI-based backend service for managing a catalogue of books, now with a friendly interface (CLI with Typer) and full SQLite persistence via SQLModel.

This project implements EX01 (backend API) and EX02 (friendly interface)
## ⚡ Features

- CRUD endpoints for books (/books)
- Validation using Pydantic
- Persistent Storage: SQLite database integration via SQLModel
- Database Migrations: Alembic schema versioning
- Seed script for example books
- EX02: Friendly interface using Typer CLI
- CLI features:

    - List all books 

    - Add a new book 

    - Read a book by ID
    
    - Delete a book by ID
    
    - Export books to CSV 

- Bonus: automated CLI test using Typer's CliRunner

- Docker support for isolated environment

- HTTP playground for quick API testing
## 🐳 Requirements
- Python 3.12+

- uv (environment & dependency manager)

- Docker (optional, for containerized runs)

## 📂 Project Structure
```bash
  books-catalogue-api/
  ├── book_service/        # Backend (FastAPI)
  │   ├── app/
  │   ├── Dockerfile
  │   └── tests/
  ├── interface/           # CLI (Typer)
  │   ├── cli.py
  │   ├── client.py
  │   ├── Dockerfile
  │   └── test_cli.py
  ├── migrations/          # Alembic migrations
  ├── data/                # SQLite databases (mounted)
  ├── docker-compose.yml
  ├── .env.example
  ├── pyproject.toml
  └── README.md
```

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

Create a .env file based on .env.example:

```bash
cp .env.example .env
```

Here’s a valid .env example::

`BOOK_APP_NAME="Book Service"`

`BOOK_DEFAULT_PAGE_SIZE=20`

`BOOK_FEATURE_PREVIEW=false`

`BOOK_DB_MODE=sqlite`

`BOOK_DATABASE_URL_SQLITE=sqlite:///./data/books.db`

`BOOK_DATABASE_URL_TEST=sqlite:///./data/books-test.db`

`BOOK_DATABASE_URL_POSTGRES=postgresql+psycopg://book:book@localhost:5432/books`

`BOOK_DATABASE_ECHO=false`

`BOOK_POOL_SIZE=5`

`BOOK_POOL_TIMEOUT=30`

`BOOK_API_BASE_URL=http://backend:8000`

Note: BOOK_DB_MODE options are memory | sqlite | postgres

#### Database Initialization (Migrations)

Before running the app, ensure the database schema is up to date:
```bash
mkdir -p data
uv run alembic upgrade head 
```

### 🚀 Running the Backend + CLI
#### Start the FastAPI backend

```bash
uv run uvicorn book_service.app.main:app --reload
```
Access the API:

- Browser/Tools: http://127.0.0.1:8000

- OpenAPI docs: http://127.0.0.1:8000/docs

#### Start the Typer CLI
In a new terminal (ensure .env is loaded):

```bash
uv run python -m interface.cli --help
```
Available commands:
```bash
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  health   Check backend health
  list     List all books
  add      Add a new book (interactive)
  read     Read a book by ID
  delete   Delete a book by ID
  export   Export all books to CSV

```
#### Example CLI Usage
Check backend health
``` bash
uv run python -m interface.cli health
```

List all books
``` bash
uv run python -m interface.cli list
```

Add a book interactively
``` bash
uv run python -m interface.cli add

```
Note: Add Prompts for Title, Author, Description, Year, Genre

Read a book by ID
``` bash
uv run python -m interface.cli read 1

```

Delete a book by ID
``` bash
uv run python -m interface.cli delete 1

```

Export all books to CSV
``` bash
uv run python -m interface.cli export --filepath my_books.csv
```

## 🐳 Option B – Running with Docker (Backend + CLI)

This project includes two Docker images:
* Backend – FastAPI service
* Frontend – Typer CLI (EX02)
They are orchestrated using Docker Compose.

### 📦 Build and Run All Services
From the project root:

```bash
docker compose up --build
```
This will start:
* Backend API on http://localhost:8000
* CLI container (interactive)
* PostgreSQL (optional, if enabled)

Note:
- When running locally, use:
  BOOK_API_BASE_URL=http://127.0.0.1:8000
- When running with Docker Compose, use:
  BOOK_API_BASE_URL=http://backend:8000

### 🧪 Using the CLI (EX02)
Open a shell inside the CLI container:

```bash
docker exec -it books-cli bash
```
Run CLI commands:

```bash
uv run python -m interface.cli health
uv run python -m interface.cli list
uv run python -m interface.cli add
uv run python -m interface.cli export --filepath books.csv
```
Note: The CLI communicates with the backend via HTTP using BOOK_API_BASE_URL.


## 🧪 Running Tests
### Backend Tests

To run tests for backend, run the following command:

```bash
  uv run pytest book_service/tests -v
```

### Bonus: CLI Automated Test (EX02)
To run the bonus test using Typer’s CliRunner:
``` bash 
uv run pytest interface/test_cli.py -v
```
This automates workflows like:

- Adding a book

- Listing books

Note: Bonus CLI tests are hermetic and mock network calls using monkeypatch,
so the backend does not need to be running.

## 🌱 Seed Example Books
Populate the repository with example books:
```bash
uv run python -m scripts.seed_books
```
This will add books like:

- Dune by Frank Herbert

- Harry Potter by J.K. Rowling

- The Hobbit by J.R.R. Tolkien
## 📝 HTTP Playground

You can quickly test the API endpoints using the VS Code REST Client, Postman, or any HTTP client. Example requests:

### Health Check
```http
GET http://127.0.0.1:8000/healthz
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