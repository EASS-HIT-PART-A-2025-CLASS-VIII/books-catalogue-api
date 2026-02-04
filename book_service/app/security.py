# book_service/app/security.py

# filepath: book_service/app/security.py

from datetime import datetime, timedelta
from typing import Optional

import jwt
from passlib.context import CryptContext

from .config import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)


def create_access_token(
    *,
    subject: str,
    settings: Settings,
    expires_delta: Optional[timedelta] = None,
    roles: Optional[list[str]] = None,
) -> str:
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=30))
    payload = {
        "sub": subject,
        "iat": now.timestamp(),
        "exp": expire.timestamp(),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "roles": roles or ["student"],
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")






