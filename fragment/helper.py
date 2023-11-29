import re
from typing import Optional


def to_float(value: str) -> Optional[float]:
    try:
        return float(re.sub(r"[^\d\.\-]", "", value))
    except ValueError:
        pass


def parse_status(text: str) -> str:
    text = text.lower()
    if text == "on auction":
        return "auction"
    elif text == "for sale":
        return "sale"
    else:
        return text
