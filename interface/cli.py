# interface/cli.py

from __future__ import annotations

import typer
from typing import Optional
from . import client
from .token_store import save_token, load_token


app = typer.Typer(
    help="📚 Book Service CLI – Friendly interface for the Books Catalogue API"
)


# -----------------------
# Health check
# -----------------------
@app.command()
def health():
    """Check backend health."""
    try:
        info = client.health()
        typer.echo(info)
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)


# -----------------------
# List books
# -----------------------
@app.command(name="list")
def list_books():
    """List all books."""
    try:
        token = load_token()
        books = client.list_books(token)
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    if not books:
        typer.echo("No books found.")
        return

    from rich.console import Console
    from rich.table import Table

    table = Table(title="Books")
    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Author")
    table.add_column("Year", justify="right")
    table.add_column("Genre")

    for b in books:
        table.add_row(
            str(b["id"]),
            b["title"],
            b["author"],
            str(b["year"]),
            b["genre"],
        )

    Console().print(table)


# -----------------------
# Add a new book (protected)
# -----------------------
@app.command()
def add(
    title: str = typer.Option(..., prompt=True),
    author: str = typer.Option(..., prompt=True),
    description: str = typer.Option(..., prompt=True),
    year: int = typer.Option(..., prompt=True),
    genre: str = typer.Option(..., prompt=True),
):
    """Add a new book (requires login)."""

    token = load_token()
    if not token:
        typer.echo("❌ No token found. Please login.")
        raise typer.Exit(code=1)

    try:
        created = client.add_book(
            {
                "title": title,
                "author": author,
                "description": description,
                "year": year,
                "genre": genre,
            },
            token
        )
        typer.echo(
            f"✅ Added book (id={created['id']}): {created['title']} by {created['author']}"
        )
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)


# -----------------------
# Read a book
# -----------------------
@app.command()
def read(book_id: int):
    """Read a book by ID."""
    try:
        token = load_token()
        book = client.read_book(book_id, token)
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    if not book:
        typer.echo(f"Book with ID {book_id} not found.")
        raise typer.Exit(code=1)

    typer.echo(book)


# -----------------------
# Delete a book (protected)
# -----------------------
@app.command()
def delete(book_id: int):
    """Delete a book by ID."""
    token = load_token()
    if not token:
        typer.echo("❌ No token found. Please login.")
        raise typer.Exit(code=1)
    try:
        success = client.delete_book(book_id, token)
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    if not success:
        typer.echo(f"Book with ID {book_id} not found.")
        raise typer.Exit(code=1)

    typer.echo(f"🗑 Deleted book with ID {book_id}")


# -----------------------
# Export books to CSV
# -----------------------
@app.command()
def export(
    filepath: Optional[str] = typer.Option(
        "books.csv", help="CSV file path to export books"
    )
):
    """Export all books to CSV."""
    token = load_token()
    if not token:
        typer.echo("❌ No token found. Please login.")
        raise typer.Exit(code=1)
    try:
        client.export_books_csv(filepath, token)
        typer.echo(f"📁 Exported books to {filepath}")
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)


# -----------------------
# Async refresh command
# -----------------------
@app.command()
def refresh():
    """Trigger async refresh (EX3)."""
    import subprocess
    subprocess.run(["python", "-m", "scripts.refresh"])
    typer.echo("🔄 Async refresh triggered.")


@app.command()
def login(username: str, password: str):
    """Login to get JWT token"""
    try:
        token = client.login(username, password)
        save_token(token)
        typer.echo("✅ Login successful! Token stored.")
    except client.ClientError as exc:
        typer.echo(f"❌ Login failed: {exc}", err=True)
        raise typer.Exit(code=1)



if __name__ == "__main__":
    app()



