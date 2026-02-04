# EX3 Project Notes - Books Catalogue API

## Architecture & Orchestration
The project consists of four main services coordinated via Docker Compose:
* **Backend**: FastAPI service handling the logic and JWT auth.
* **Database**: PostgreSQL for persistent storage.
* **Worker & Redis**: Celery/Redis stack for async background tasks (refresh job).
* **CLI**: Typer-based interface for user interaction.

## Security Baseline (Session 11)
* **JWT Auth**: Implemented using `OAuth2PasswordBearer`. Tokens are issued at `/token/login`.
* **Role Checks**: Endpoints verify user roles (e.g., `teacher`) before allowing mutations.
* **Token Storage**: The CLI stores tokens locally in `interface/token_store.py` to maintain sessions.

## Async Refresher (Session 09)
The `refresh` command triggers a background worker via Redis. 
**Trace/Verification:**
`[Redis] Task queued: book_service.worker.tasks.refresh_catalog`
`[Worker] Processing refresh... Success.`