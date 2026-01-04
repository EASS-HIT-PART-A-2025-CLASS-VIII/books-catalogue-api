
from sqlmodel import Session
from book_service.app.config import Settings
from book_service.app.database import engine, init_db
from book_service.app.models import BookCreate
from book_service.app.repository import BookRepository as MemoryRepo
from book_service.app.repository_db import BookRepository as DbRepo

import typer

app = typer.Typer(help="Database utilities for Books Catalogue")

@app.command()
def bootstrap(sample: int = 5) -> None:
    """
    Creates tables and seeds the database with sample data.
    Respects BOOK_DB_MODE (memory/sqlite/postgres).
    """
    settings = Settings()
    
    if settings.db_mode == "memory":
        repo = MemoryRepo()
        for idx in range(sample):
            repo.create(BookCreate(
                title=f"Sample Book {idx+1}", 
                author="System", 
                description="Sample data", 
                year=2020 + idx, 
                genre="Fiction"
            ))
        typer.echo("Seeded in-memory repo (Note: this data will vanish when CLI exits).")
        return

    #create db table if isn't exist
    init_db()
    
    # connection to db sqlite/postgress 
    with Session(engine) as session:
        repo = DbRepo(session)
        if repo.list():
            typer.echo(f"Database ({settings.db_mode}) already contains data; skipping seed.")
            return  
        for idx in range(sample):
            repo.create(BookCreate(
                title=f"Sample Book {idx+1}", 
                author="System", 
                description="Sample data", 
                year=2020 + idx, 
                genre="Fiction"
            ))
        session.commit()
        
    typer.echo(f"Successfully seeded {sample} books in {settings.db_mode} mode.")

if __name__ == "__main__":
    app()