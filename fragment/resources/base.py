from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api import FragmentAPI


class BaseResource:
    __slots__ = frozenset(["_api"])

    def __init__(self, api: "FragmentAPI") -> None:
        self._api = api
