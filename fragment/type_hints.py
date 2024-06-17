from typing import Optional, List, TypedDict, Literal, TypeVar


T = TypeVar("T")

FragmentFilter = Literal[
    "", # default value
    "auction",
    "sold",
    "sale"
]
FragmentSort = Literal[
    "", # default value
    "price_desc",
    "price_asc",
    "listed",
    "ending"
]

UsernameStatus = Literal[
    "available",
    "unavailable",
    "auction",
    "sale",
    "sold",
    "taken"
]


class Username(TypedDict):
    username: str
    status: UsernameStatus
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
    status: UsernameStatus
    ownership_history: List[OwnershipHistoryElement]
    bid_history: List[BidHistoryElement]
    latest_offers: List[LatestOffersElement]
