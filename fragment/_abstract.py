from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


class AbstractClient(ABC):
    __slots__ = (
        "base_url",
        "_proxy"
    )

    DEFAULT_URL = "https://fragment.com"
    DEFAULT_TIMEOUT = 20
    MAX_RETRIES = 3
    MAX_RETRY_WAIT = 30

    def __init__(
        self,
        base_url: str | None = None,
        proxy: str | None = None
    ) -> None:
        self.base_url = self.DEFAULT_URL if base_url is None else base_url
        self._proxy = proxy

    @property
    @abstractmethod
    def closed(self) -> bool:
        ...

    @classmethod
    def _retry_wait(cls, attempt: int) -> float:
        return min(2 ** (attempt + 1), cls.MAX_RETRY_WAIT)

    @abstractmethod
    def _request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        method: str = "GET",
        timeout: int | None = None,
        max_retries: int | None = None,
        proxy: str | None = None
    ) -> Any:
        ...
