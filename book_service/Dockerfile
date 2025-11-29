# Base image with Python 3.12 slim
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy uv binary from official image (faster than pip install)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using locked versions
# --frozen: use exact versions from uv.lock
# --no-dev: skip dev dependencies like pytest
RUN uv sync --frozen --no-dev

# Copy application code
COPY book_service ./book_service

# Copy environment template
COPY .env.example ./.env

EXPOSE 8000

# Command to run the FastAPI app
CMD ["uv", "run", "uvicorn", "book_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
