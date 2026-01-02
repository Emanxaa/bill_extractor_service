from datetime import datetime
import re

MONTHS_ID = {
    "Januari": "January",
    "Februari": "February",
    "Maret": "March",
    "April": "April",
    "Mei": "May",
    "Juni": "June",
    "Juli": "July",
    "Agustus": "August",
    "September": "September",
    "Oktober": "October",
    "November": "November",
    "Desember": "December",
}

def parse_id_datetime(value: str) -> datetime | None:
    """
    Parse Indonesian datetime strings into Python datetime.

    Handles variants like:
    - '30 Desember 2025, 16:58:12 WIB'
    - '30 Desember 2025, 16:58:12WIB'
    - '30 Desember 2025,16:58:12 WIB'
    """
    if not value or not isinstance(value, str):
        return None

    text = value.strip()

    # 1. Normalize timezone tokens (remove WIB/WITA/WIT regardless of spacing)
    text = re.sub(r"\s*(WIB|WITA|WIT)\b", "", text, flags=re.IGNORECASE)

    # 2. Normalize spacing after comma
    text = re.sub(r",\s*", ", ", text)

    # 3. Translate Indonesian month names to English
    for id_month, en_month in MONTHS_ID.items():
        text = text.replace(id_month, en_month)

    # 4. Final cleanup
    text = text.strip()

    # 5. Parse deterministically
    try:
        return datetime.strptime(text, "%d %B %Y, %H:%M:%S")
    except ValueError:
        return None
