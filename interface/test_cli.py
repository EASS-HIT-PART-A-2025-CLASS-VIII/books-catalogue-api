
from typer.testing import CliRunner
from interface.cli import app

runner = CliRunner()


def test_cli_health(monkeypatch):
    """CLI health command should print the health dict.

    Monkeypatch the network call so the test is hermetic and fast.
    """
    monkeypatch.setattr("interface.client.health", lambda: {"status": "ok"})
    result = runner.invoke(app, ["health"])
    assert result.exit_code == 0
    assert "status" in result.stdout


def test_cli_list_books(monkeypatch):
    """CLI list command should render the Books table header.

    Monkeypatch the network call to return a small sample list.
    """
    sample = [
        {
            "id": 1,
            "title": "Sample Book",
            "author": "Author Name",
            "description": "desc",
            "year": 2020,
            "genre": "Fiction",
        }
    ]
    monkeypatch.setattr("interface.client.list_books", lambda: sample)
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Books" in result.stdout


