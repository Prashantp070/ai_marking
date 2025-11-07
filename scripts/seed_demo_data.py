"""Seed baseline data for local development."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import bcrypt
from sqlalchemy import select

PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_DIR = PROJECT_ROOT / "apps" / "api"
if str(API_DIR) not in sys.path:
    sys.path.append(str(API_DIR))

from app.core.database import async_session_factory  # noqa: E402
from app.models import Exam, Question, User  # noqa: E402


async def ensure_default_teacher(session) -> User:
    result = await session.execute(select(User).where(User.email == "teacher@example.com"))
    user = result.scalars().first()
    if user:
        return user

    hashed = bcrypt.hashpw("Password123!".encode(), bcrypt.gensalt()).decode()
    user = User(
        email="teacher@example.com",
        full_name="Demo Teacher",
        hashed_password=hashed,
        role="teacher",
        is_active=True,
    )
    session.add(user)
    await session.flush()
    return user


async def ensure_demo_exam(session, owner: User) -> Exam:
    result = await session.execute(select(Exam).where(Exam.name == "Science Midterm"))
    exam = result.scalars().first()
    if exam:
        return exam

    exam = Exam(
        name="Science Midterm",
        description="Demo exam for handwritten evaluation",
        subject="Science",
    )
    session.add(exam)
    await session.flush()
    return exam


async def ensure_exam_questions(session, exam: Exam) -> None:
    existing_numbers = {
        row[0]
        for row in (
            await session.execute(select(Question.number).where(Question.exam_id == exam.id))
        ).all()
    }

    seed_questions = [
        {
            "number": "Q1",
            "text": "Explain the process of photosynthesis in plants.",
            "answer_type": "long",
            "keywords": ["chlorophyll", "sunlight", "carbon dioxide", "glucose", "oxygen"],
            "model_answer": "Photosynthesis uses chlorophyll to convert sunlight, water and carbon dioxide into glucose and oxygen inside chloroplasts.",
            "marks": 10,
        },
        {
            "number": "Q2",
            "text": "State Newton's three laws of motion with examples.",
            "answer_type": "very_long",
            "keywords": ["inertia", "F=ma", "action", "reaction", "force"],
            "model_answer": "Newton's laws describe inertia, the relationship between force and acceleration, and equal/opposite reactions.",
            "marks": 12,
        },
        {
            "number": "Q3",
            "text": "Define ecosystem and list its main components.",
            "answer_type": "short",
            "keywords": ["ecosystem", "biotic", "abiotic", "community", "environment"],
            "model_answer": "An ecosystem is a community of organisms interacting with biotic and abiotic components of their environment.",
            "marks": 5,
        },
    ]

    for question in seed_questions:
        if question["number"] in existing_numbers:
            continue
        session.add(Question(exam_id=exam.id, **question))


async def seed() -> None:
    async with async_session_factory() as session:
        teacher = await ensure_default_teacher(session)
        exam = await ensure_demo_exam(session, teacher)
        await ensure_exam_questions(session, exam)
        await session.commit()
    print("Seed data applied: teacher@example.com / Science Midterm with questions")


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()


