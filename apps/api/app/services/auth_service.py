"""Service for authentication and user management."""

import bcrypt

from app.models import User
from app.repositories.user import UserRepository
from app.schemas.auth import UserCreate


class AuthService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register_user(self, payload: UserCreate) -> User:
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise ValueError("User already exists")
        hashed = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt()).decode()
        user = User(email=payload.email, full_name=payload.full_name, hashed_password=hashed)
        return await self.repo.create(user)

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self.repo.get_by_email(email)
        if not user:
            return None
        if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
            return None
        return user




