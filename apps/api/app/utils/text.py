"""Text normalization utilities."""

import re


HINDI_NUMERAL_MAP = str.maketrans("०१२३४५६७८९", "0123456789")


def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.translate(HINDI_NUMERAL_MAP)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text



