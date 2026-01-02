import re
from typing import Optional

def extract_amount(text: str) -> Optional[float]:
    match = re.search(r"Rp\s?([\d\.]+)", text)
    if not match:
        return None
    return float(match.group(1).replace(".", ""))

def extract_reference(text: str) -> Optional[str]:
    match = re.search(r"(No\.?\s?Ref|Ref)\s?:?\s?(\d+)", text)
    return match.group(2) if match else None
