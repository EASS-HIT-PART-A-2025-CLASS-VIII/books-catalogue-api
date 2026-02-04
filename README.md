# 📚 Books Catalogue API – EX3 

Backend FastAPI + Typer CLI + JWT + Redis + Worker + PostgreSQL.

## ⚡ Features

* JWT authentication (`/token/login`)
* Role-protected endpoints
* CRUD for books (`/books`)
* SQLModel + PostgreSQL
* Alembic migrations
* CLI commands (Typer):

  * `login`
  * `list`
  * `add`
  * `read`
  * `delete`
  * `export`
  * `refresh` (async background job via Redis/Worker)
* Docker Compose: backend + CLI + PostgreSQL + Redis + Worker
* Tests: backend + CLI

---

## 📂 Project Structure

```
books-catalogue-api/
├── book_service/
│   ├── app/
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   └── security.py
│   ├── scripts/refresh.py
│   ├── worker/tasks.py
│   └── tests/
├── interface/
│   ├── cli.py
│   ├── client.py
│   ├── token_store.py
│   └── test_cli.py
├── migrations/
├── data/
├── docker-compose.yml
└── pyproject.toml
```

---

## 🐳 Docker Compose

```bash
docker compose up --build
```

Services started: backend, CLI, PostgreSQL, Redis, Worker.
Backend → [http://localhost:8000](http://localhost:8000)

---

## 🔐 CLI Usage

Enter CLI container:

```bash
docker exec -it books-cli bash
```

Login:

```bash
python -m interface.cli login teacher classroom
```

List books:

```bash
python -m interface.cli list
```

Add book:

```bash
python -m interface.cli add --title "Test" --author "Me" --year 2025 --genre "Drama"
```

Read book by ID:

```bash
python -m interface.cli read 1
```

Delete book by ID:

```bash
python -m interface.cli delete 1
```

Export books:

```bash
python -m interface.cli export --filepath books.csv
```

Trigger async refresh job:

```bash
python -m interface.cli refresh
```

---

## 🧪 Tests

Backend tests:

```bash
pytest book_service/tests -v
```

CLI tests:

```bash
pytest interface/test_cli.py -v
```

---

## 📝 API Endpoints

* POST `/token/login` → JWT
* GET `/books` → list all (auth required)
* POST `/books` → add (auth required)
* GET `/books/{id}` → read (auth required)
* DELETE `/books/{id}` → delete (auth required)
* POST `/refresh` → async job (auth required)
