from __future__ import annotations

from typing import TypedDict, Literal, TypeVar


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
    value: float | None
    datetime: str | None
    is_resale: bool | None


class OwnershipHistoryElement(TypedDict):
    ton_sell_price: float | None
    date: str
    buyer: str


class BidHistoryElement(TypedDict):
    ton_price: float | None
    date: str
    from_: str


class LatestOffersElement(TypedDict):
    ton_offer: float | None
    date: str
    offered_by: str


class FullUsername(TypedDict):
    username: str
    status: UsernameStatus
    ownership_history: list[OwnershipHistoryElement]
    bid_history: list[BidHistoryElement]
    latest_offers: list[LatestOffersElement]
