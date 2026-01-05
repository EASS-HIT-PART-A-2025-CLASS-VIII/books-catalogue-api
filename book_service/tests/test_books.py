# filepath: book_service/tests/test_books.py
"""
Comprehensive test suite for Book Service API.

Tests use the 'client' fixture from conftest.py, which provides
a TestClient for making HTTP requests to our FastAPI app without
needing a real server.
"""


def test_health_includes_app_name(client):
    """Health endpoint returns status and app name."""
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "Book Service"


def test_create_book_returns_201_and_payload(client):
    """Creating a book returns 201 with normalized payload."""
    response = client.post(
        "/books",
        json={
            "title": "  Harry Potter  ",
            "author": "  J.K. Rowling ",
            "description": "Wizard boy saves world",
            "year": 1997,
            "genre": "fantasy"
        },
    )
    assert response.status_code == 201
    payload = response.json()

    # normalization tests
    assert payload["title"] == "Harry Potter"
    assert payload["author"] == "J.K. Rowling"
    assert payload["genre"] == "Fantasy"

    # field preservation tests
    assert payload["description"] == "Wizard boy saves world"
    assert payload["year"] == 1997

    # id generation
    assert payload["id"] == 1


def test_book_ids_increment(client):
    """Repository assigns sequential IDs."""
    first = client.post(
        "/books",
        json={
            "title": "Book One",
            "author": "AA",
            "description": "Desc1",
            "year": 2001,
            "genre": "fiction"
        },
    ).json()["id"]

    second = client.post(
        "/books",
        json={
            "title": "Book Two",
            "author": "BB",
            "description": "Desc2",
            "year": 2002,
            "genre": "fiction"
        },
    ).json()["id"]

    assert second == first + 1


def test_list_books_returns_empty_array_initially(client):
    """Empty repository returns empty array."""
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []


def test_list_books_returns_created_book(client):
    """Can retrieve books after creating them."""
    client.post(
        "/books",
        json={
            "title": "Dune",
            "author": "Frank Herbert",
            "description": "Sci-fi classic",
            "year": 1965,
            "genre": "sci-fi"
        },
    )

    response = client.get("/books")
    assert response.status_code == 200
    books = response.json()

    assert len(books) == 1
    assert books[0]["title"] == "Dune"


def test_get_book_by_id(client):
    """Can retrieve specific book by ID."""
    create_response = client.post(
        "/books",
        json={
            "title": "Arrival",
            "author": "Ted Chiang",
            "description": "Short story inspiration",
            "year": 1998,
            "genre": "sci-fi"
        },
    )
    book_id = create_response.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    book = response.json()

    assert book["title"] == "Arrival"
    assert book["id"] == book_id


def test_get_missing_book_returns_404(client):
    """Requesting non-existent book returns 404."""
    response = client.get("/books/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_delete_book(client):
    """Can delete a book and it's gone afterwards."""
    create_response = client.post(
        "/books",
        json={
            "title": "Interstellar",
            "author": "A Person",
            "description": "Space drama",
            "year": 2014,
            "genre": "sci-fi"
        },
    )
    book_id = create_response.json()["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404


def test_delete_missing_book_returns_404(client):
    """Deleting non-existent book returns 404."""
    response = client.delete("/books/9999")
    assert response.status_code == 404


def test_create_book_rejects_missing_title(client):
    """Missing required field returns 422."""
    response = client.post(
        "/books",
        json={
            "author": "Unknown",
            "description": "Desc",
            "year": 2020,
            "genre": "drama",
        },
    )
    assert response.status_code == 422


def test_create_book_rejects_missing_author(client):
    """Author is required."""
    response = client.post(
        "/books",
        json={
            "title": "Her",
            "description": "Desc",
            "year": 2020,
            "genre": "drama",
        },
    )
    assert response.status_code == 422


def test_create_book_rejects_missing_description(client):
    """Description is required."""
    response = client.post(
        "/books",
        json={
            "title": "Her",
            "author": "Spike Jonze",
            "year": 2020,
            "genre": "drama",
        },
    )
    assert response.status_code == 422


def test_create_book_rejects_missing_genre(client):
    """Genre is required."""
    response = client.post(
        "/books",
        json={
            "title": "Her",
            "author": "Spike Jonze",
            "description": "Desc",
            "year": 2020,
        },
    )
    assert response.status_code == 422


def test_create_book_rejects_year_too_old(client):
    """Year before 1900 is rejected with 422."""
    response = client.post(
        "/books",
        json={
            "title": "Old Book",
            "author": "Anon",
            "description": "Desc",
            "year": 1800,
            "genre": "fiction"
        },
    )
    assert response.status_code == 422


def test_create_book_rejects_year_too_new(client):
    """Year after 2100 is rejected with 422."""
    response = client.post(
        "/books",
        json={
            "title": "Future Book",
            "author": "Anon",
            "description": "Desc",
            "year": 2200,
            "genre": "fiction"
        },
    )
    assert response.status_code == 422
