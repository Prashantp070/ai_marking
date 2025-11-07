"""Stub retraining script for Sentence-BERT fine-tuning."""

from __future__ import annotations

import asyncio

from pathlib import Path
import sys

from sqlalchemy import select

PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_DIR = PROJECT_ROOT / "apps" / "api"
sys.path.append(str(API_DIR))

from app.core.database import async_session_factory  # noqa: E402
from app.models import Feedback  # noqa: E402


async def load_feedback_pairs() -> list[tuple[str, str]]:
    async with async_session_factory() as session:
        result = await session.execute(select(Feedback))
        feedback_items = result.scalars().all()
        return [(item.comments or "", str(item.suggested_score or 0.0)) for item in feedback_items]


async def main() -> None:
    pairs = await load_feedback_pairs()
    print(f"Loaded {len(pairs)} feedback pairs. TODO: fine-tune Sentence-BERT model.")


if __name__ == "__main__":
    asyncio.run(main())

