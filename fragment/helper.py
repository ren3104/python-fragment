import re
from typing import Optional


def to_float(value: str) -> Optional[float]:
    new_value = re.sub(r"[^\d\.]", "", value)
    if len(new_value) != 0:
        return float(new_value)
