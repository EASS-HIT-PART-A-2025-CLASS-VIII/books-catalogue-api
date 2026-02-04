# filepath: interface/client.py

# filepath: interface/client.py
from __future__ import annotations

import csv
import os
from typing import Any, Optional

import httpx

# -----------------------
# Configuration
# -----------------------
BASE_URL = os.getenv("BOOK_API_BASE_URL", "http://backend:8000")
DEFAULT_TIMEOUT = 5.0


# -----------------------
# Errors
# -----------------------
class ClientError(RuntimeError):
    """Friendly client error for network / HTTP failures."""


# -----------------------
# Helpers
# -----------------------
def _auth_headers(token: Optional[str]) -> dict[str, str]:
    """Return Authorization header if token exists."""
    if not token:
        return {}

    # Debugging output
    #print(f"Using token: {token}")

    return {"Authorization": f"Bearer {token}"}


def _handle_http_errors(exc: Exception, context: str) -> None:
    raise ClientError(
        f"{context}\n"
        f"Backend URL: {BASE_URL}\n"
        f"Is the FastAPI backend running?\n"
        f"If using Docker: docker compose up\n"
        f"If local: uv run uvicorn book_service.app.main:app --reload"
    ) from exc


# -----------------------
# Public API
# -----------------------
def health() -> dict[str, Any]:
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.get(f"{BASE_URL}/healthz")
            resp.raise_for_status()
            return resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, "Unable to contact backend health endpoint.")


def login(username: str, password: str) -> str:
    """Login to the backend and return JWT token."""
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.post(
                f"{BASE_URL}/token/login",
                json={
                    "username": username,
                    "password": password,
                },
            )
            resp.raise_for_status()
            data = resp.json()

            token = data.get("access_token")
            if not token:
                raise ClientError("Login succeeded but no access_token returned")

            return token
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, f"Unable to login user '{username}'.")


def list_books(token: Optional[str]) -> list[dict[str, Any]]:
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.get(
                f"{BASE_URL}/books",
                headers=_auth_headers(token),
            )
            resp.raise_for_status()
            return resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, "Unable to fetch books.")


def read_book(book_id: int, token: Optional[str]) -> dict[str, Any]:
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.get(
                f"{BASE_URL}/books/{book_id}",
                headers=_auth_headers(token),
            )
            if resp.status_code == 404:
                return {}
            resp.raise_for_status()
            return resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, f"Unable to read book with id={book_id}.")


def add_book(book: dict[str, Any], token: Optional[str]) -> dict[str, Any]:
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.post(
                f"{BASE_URL}/books",
                json=book,
                headers=_auth_headers(token),
            )
            resp.raise_for_status()
            return resp.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, "Unable to add new book.")


def delete_book(book_id: int, token: Optional[str]) -> bool:
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            resp = client.delete(
                f"{BASE_URL}/books/{book_id}",
                headers=_auth_headers(token),
            )
            if resp.status_code == 404:
                return False
            resp.raise_for_status()
            return True
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        _handle_http_errors(exc, f"Unable to delete book with id={book_id}.")


def export_books_csv(filepath: str, token: Optional[str]) -> None:
    books = list_books(token)
    if not books:
        return

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)


