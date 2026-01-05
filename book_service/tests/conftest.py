# filepath: book_service/tests/conftest.py


import uuid
import psycopg
import pytest
from collections.abc import Generator
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from book_service.app.main import app
from book_service.app.database import get_session
from book_service.app.config import Settings

ADMIN_URL = "postgresql://book:book@localhost:5432/books"
DB_TEMPLATE = "postgresql+psycopg://book:book@localhost:5432/{db_name}"

@pytest.fixture(name="engine")
def engine_fixture(tmp_path):
    settings = Settings()
    

    if settings.db_mode == "postgres":
        test_db_name = f"test_{uuid.uuid4().hex[:8]}"
        
        with psycopg.connect(ADMIN_URL, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE {test_db_name}")
        
        url = DB_TEMPLATE.format(db_name=test_db_name)
        test_engine = create_engine(url)
        SQLModel.metadata.create_all(test_engine)
        
        yield test_engine
        
        test_engine.dispose()
        with psycopg.connect(ADMIN_URL, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DROP DATABASE {test_db_name} WITH (FORCE)")

    else:
        test_db = tmp_path / "test.db"
        test_engine = create_engine(
            f"sqlite:///{test_db}",
            connect_args={"check_same_thread": False},
        )
        SQLModel.metadata.create_all(test_engine)
        yield test_engine
        test_engine.dispose()

@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    def get_session_override():
        yield session
    
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# @pytest.fixture(autouse=True)
# def reset_memory_repo():
#     """Reset the in-memory repository before each test."""
#     _memory_repo.delete_all()








    