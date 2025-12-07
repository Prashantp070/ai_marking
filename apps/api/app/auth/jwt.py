"""JWT helper utilities."""

from datetime import datetime, timedelta
from typing import Any

from jose import jwt

from app.core.config import settings


def _create_token(subject: str, expires_delta: timedelta, secret: str) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, secret, algorithm=settings.JWT_ALGORITHM)


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    delta = timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(subject, delta, settings.JWT_SECRET_KEY)


def create_refresh_token(subject: str, expires_minutes: int | None = None) -> str:
    delta = timedelta(minutes=expires_minutes or settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return _create_token(subject, delta, settings.JWT_REFRESH_SECRET_KEY)


def decode_token(token: str, refresh: bool = False) -> Any:
    secret = settings.JWT_REFRESH_SECRET_KEY if refresh else settings.JWT_SECRET_KEY
    return jwt.decode(token, secret, algorithms=[settings.JWT_ALGORITHM])




