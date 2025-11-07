"""Database session management."""

from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings


async_engine = create_async_engine(str(settings.DATABASE_URL), future=True, echo=False)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

sync_engine = create_engine(str(settings.SYNC_DATABASE_URL), future=True, echo=False)
sync_session_factory = sessionmaker(bind=sync_engine, expire_on_commit=False, class_=Session)

Base = declarative_base()


async def init_db() -> None:
    from app import models

    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


def get_sync_session() -> Session:
    return sync_session_factory()

