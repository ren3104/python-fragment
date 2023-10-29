from typing import Any, Optional, Dict, TypedDict, Literal, TypeVar


T = TypeVar("T")
JsonObject = Dict[str, Any]

FragmentFilter = Literal[
    "",
    "auction",
    "sold",
    "sale"
]
FragmentSort = Literal[
    "",
    "price_desc",
    "price_asc",
    "listed",
    "ending"
]


class Username(TypedDict):
    username: str
    status: str
    value: Optional[float]
    datetime: Optional[str]
    is_resale: Optional[bool]
