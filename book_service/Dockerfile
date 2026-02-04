# book_service/Dockerfile


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/book_service"

WORKDIR /app

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Create persistent data directory
RUN mkdir -p /app/data

# Copy backend code
COPY book_service ./book_service

EXPOSE 8000

# Start FastAPI
CMD ["uv", "run", "uvicorn", "book_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]


