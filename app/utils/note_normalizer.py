from typing import Optional
import re


def normalize_note(raw: Optional[str]) -> dict:
    """
    Normalize note text without semantic inference.
    """
    if not raw:
        return {
            "raw": None,
            "clean": None,
        }

    clean = raw.lower()
    clean = re.sub(r"[^a-z0-9\s]", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()

    return {
        "raw": raw.strip(),
        "clean": clean or None,
    }
