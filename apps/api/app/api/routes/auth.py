"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import create_access_token, create_refresh_token
from app.core.database import get_async_session
from app.repositories.user import UserRepository
from app.schemas.auth import Token, UserCreate, UserLogin
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth")


@router.post("/register", response_model=Token, summary="Register a new user")
async def register_user(payload: UserCreate, session: AsyncSession = Depends(get_async_session)) -> Token:
    repo = UserRepository(session)
    service = AuthService(repo)
    try:
        user = await service.register_user(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=Token, summary="Authenticate a user")
async def login(payload: UserLogin, session: AsyncSession = Depends(get_async_session)) -> Token:
    repo = UserRepository(session)
    service = AuthService(repo)
    user = await service.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    return Token(access_token=access_token, refresh_token=refresh_token)

