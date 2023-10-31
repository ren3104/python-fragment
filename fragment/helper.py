import re
from typing import Optional


def to_float(value: str) -> Optional[float]:
    try:
        return float(re.sub(r"[^\d\.\-]", "", value))
    except ValueError:
        pass
