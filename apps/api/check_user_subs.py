import sys
sys.path.insert(0, ".")
import asyncio
from app.core.database import async_session_factory
from app.models import User, Submission
from sqlalchemy import select

async def check():
    async with async_session_factory() as session:
        # Get user 1
        result = await session.execute(select(User).where(User.id == 1))
        user = result.scalars().first()
        if user:
            print(f'User 1: {user.email}')
            
            # Get submissions for this user
            result = await session.execute(select(Submission).where(Submission.user_id == 1))
            subs = result.scalars().all()
            print(f'Submissions for user 1: {len(subs)}')
            for sub in subs[:3]:
                print(f'  - ID: {sub.id}, Status: {sub.status}, Created: {sub.created_at}')

asyncio.run(check())
