from typing import Optional
import re

# --- Currency normalization ---

_CURRENCY_MAP = {
    "rp": "IDR",
    "rupiah": "IDR",
    "idr": "IDR",
}


def normalize_currency(value: Optional[str]) -> Optional[str]:
    if not value or not isinstance(value, str):
        return None

    key = value.strip().lower()
    return _CURRENCY_MAP.get(key)


# --- Platform normalization ---

_PLATFORM_MAP = {
    "bank bri": "BRI",
    "bri": "BRI",
    "pt. bank rakyat indonesia": "BRI",
    "pt bank rakyat indonesia": "BRI",

    "shopeepay": "SHOPEEPAY",
    "bp shopeepay": "SHOPEEPAY",
}


def normalize_platform(value: Optional[str]) -> Optional[str]:
    if not value or not isinstance(value, str):
        return None

    key = value.strip().lower()

    # exact mapping first
    if key in _PLATFORM_MAP:
        return _PLATFORM_MAP[key]

    # fallback: uppercase cleaned value
    return value.strip().upper()



def normalize_account_number(value: Optional[str]) -> Optional[str]:
    """
    Normalize account / identifier numbers by removing noise.
    Keeps digits and letters only.
    """
    if not value or not isinstance(value, str):
        return None

    # Remove spaces and common OCR noise
    cleaned = re.sub(r"[^0-9A-Za-z]", "", value)

    return cleaned or None


# --- Note normalization ---

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
