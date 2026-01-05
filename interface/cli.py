# filepath: interface/cli.py
from __future__ import annotations

import typer
from typing import Optional

from . import client

app = typer.Typer(
    help="📚 Book Service CLI – Friendly interface for the Books Catalogue API"
)


@app.command()
def health():
    """Check backend health."""
    try:
        info = client.health()
        typer.echo(info)
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)


@app.command(name="list")
def list_books():
    """List all books."""
    try:
        books = client.list_books()
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


@app.command()
def add(
    title: str = typer.Option(..., prompt=True),
    author: str = typer.Option(..., prompt=True),
    description: str = typer.Option(..., prompt=True),
    year: int = typer.Option(..., prompt=True),
    genre: str = typer.Option(..., prompt=True),
):
    """Add a new book."""
    try:
        created = client.add_book(
            {
                "title": title,
                "author": author,
                "description": description,
                "year": year,
                "genre": genre,
            }
        )
        typer.echo(
            f"✅ Added book (id={created['id']}): "
            f"{created['title']} by {created['author']}"
        )
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)


@app.command()
def read(book_id: int):
    """Read a book by ID."""
    try:
        book = client.read_book(book_id)
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    if not book:
        typer.echo(f"Book with ID {book_id} not found.")
        raise typer.Exit(code=1)

    typer.echo(book)


@app.command()
def delete(book_id: int):
    """Delete a book by ID."""
    try:
        success = client.delete_book(book_id)
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    if not success:
        typer.echo(f"Book with ID {book_id} not found.")
        raise typer.Exit(code=1)

    typer.echo(f"🗑 Deleted book with ID {book_id}")


@app.command()
def export(
    filepath: Optional[str] = typer.Option(
        "books.csv", help="CSV file path to export books"
    )
):
    """Export all books to CSV (EX02 small extra)."""
    try:
        client.export_books_csv(filepath)
        typer.echo(f"📁 Exported books to {filepath}")
    except client.ClientError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
