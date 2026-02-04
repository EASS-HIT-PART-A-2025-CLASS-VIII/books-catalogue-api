# interface/Dockerfile

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy only the CLI code
COPY interface ./interface

# Copy the scripts folder so refresh.py is available
COPY scripts ./scripts

# Default command: open shell (CLI is run manually)
CMD ["bash"]
