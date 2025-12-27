# filepath: book_service/tests/conftest.py
# import pytest
# from fastapi.testclient import TestClient

# from book_service.app.main import app
# from book_service.app.dependencies import get_repository


# @pytest.fixture(autouse=True)
# def clear_repository():
#     """Clear repository before and after each test."""
#     repo = next(get_repository())
#     repo.clear()
#     yield
#     repo.clear()


# @pytest.fixture
# def client():
#     """Provide a TestClient for making requests."""
#     return TestClient(app)


from collections.abc import Generator
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from book_service.app.main import app
from book_service.app.database import get_session


@pytest.fixture(name="engine")
def engine_fixture(tmp_path):
    """Create a temporary SQLite database for testing."""
    test_db = tmp_path / "test.db"
    test_engine = create_engine(
        f"sqlite:///{test_db}",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    # Cleanup: drop all tables and dispose engine
    SQLModel.metadata.drop_all(test_engine)
    test_engine.dispose()


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    """Provide a SQLModel session connected to the test database."""
    with Session(engine) as session:
        yield session
        # Rollback any uncommitted changes
        session.rollback()


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Provide a test client with overridden dependencies."""
    
    def get_session_override() -> Generator[Session, None, None]:
        yield session
    
    app.dependency_overrides[get_session] = get_session_override
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup: remove override
    app.dependency_overrides.clear()


