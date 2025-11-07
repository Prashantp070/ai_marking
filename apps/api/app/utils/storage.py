"""Storage helper for Supabase / S3 uploads."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def save_locally(file_path: Path, data: bytes) -> Path:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(data)
    logger.debug("Saved file locally at %s", file_path)
    return file_path

