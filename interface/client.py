# filepath: interface/client.py

from __future__ import annotations

import csv
import os
from typing import Any

import httpx

BASE_URL = os.getenv("BOOK_API_BASE_URL", "http://localhost:8000")
DEFAULT_TIMEOUT = 5.0


class ClientError(RuntimeError):
    """Friendly client error for network / HTTP failures.

    Raised by the client so the CLI can present a clean user-facing message
    instead of a raw traceback.
    """


def _handle_http_errors(exc: Exception, context: str) -> None:
    raise ClientError(
        f"{context}\n"
        f"Backend URL: {BASE_URL}\n"
        f"Is the FastAPI backend running?\n"
        f"Try: uv run uvicorn book_service.app.main:app --reload"
    ) from exc


def health() -> dict[str, Any]:
    """Check backend health."""
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.get(f"{BASE_URL}/healthz")
            resp.raise_for_status()
            return resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, "Unable to contact backend health endpoint.")


def list_books() -> list[dict[str, Any]]:
    """Return all books."""
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.get(f"{BASE_URL}/books")
            resp.raise_for_status()
            return resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, "Unable to fetch books.")


def read_book(book_id: int) -> dict[str, Any]:
    """Return a single book or empty dict if not found."""
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.get(f"{BASE_URL}/books/{book_id}")
            if resp.status_code == 404:
                return {}
            resp.raise_for_status()
            return resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, f"Unable to read book with id={book_id}.")


def add_book(book: dict[str, Any]) -> dict[str, Any]:
    """Create a new book."""
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.post(f"{BASE_URL}/books", json=book)
            resp.raise_for_status()
            return resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, "Unable to add new book.")


def delete_book(book_id: int) -> bool:
    """Delete a book. Returns False if not found."""
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.delete(f"{BASE_URL}/books/{book_id}")
            if resp.status_code == 404:
                return False
            resp.raise_for_status()
            return True
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, f"Unable to delete book with id={book_id}.")


# Export books to CSV
def export_books_csv(filepath: str) -> None:
    books = list_books()
    if not books:
        return

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)
