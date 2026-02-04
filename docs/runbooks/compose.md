# Compose Runbook

## Launching the Stack
1. Ensure Docker is running.
2. Run `docker compose up --build`.

## Health Checks
* **API**: Access [http://localhost:8000/docs](http://localhost:8000/docs).
* **Redis**: Run `docker exec books-redis redis-cli ping`.

## Running Tests in CI
To execute the test suite:
* Backend: `pytest book_service/tests`.
* CLI: `pytest interface/test_cli.py`.