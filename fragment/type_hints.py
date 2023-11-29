from typing import Any, Optional, Dict, List, TypedDict, Literal, TypeVar


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
    status: str # available unavailable auction sale sold taken
    value: Optional[float]
    datetime: Optional[str]
    is_resale: Optional[bool]


class OwnershipHistoryElement(TypedDict):
    ton_sell_price: float
    date: str
    buyer: str


class BidHistoryElement(TypedDict):
    ton_price: float
    date: str
    from_: str


class LatestOffersElement(TypedDict):
    ton_offer: float
    date: str
    offered_by: str


class FullUsername(TypedDict):
    username: str
    status: str
    ownership_history: List[OwnershipHistoryElement]
    bid_history: List[BidHistoryElement]
    latest_offers: List[LatestOffersElement]
