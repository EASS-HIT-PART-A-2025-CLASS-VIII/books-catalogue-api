from pathlib import Path

TOKEN_PATH = Path("/app/.books_token")

def save_token(token: str):
    TOKEN_PATH.write_text(token)

def load_token() -> str | None:
    if TOKEN_PATH.exists():
        return TOKEN_PATH.read_text().strip()
    return None

def clear_token():
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
