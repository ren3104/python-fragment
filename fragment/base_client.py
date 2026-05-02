from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


class BaseClient:
    __slots__ = (
        "base_url",
    )

    DEFAULT_URL = "https://fragment.com"
    MAX_RETRIES = 3
    MAX_RETRY_WAIT = 30

    def __init__(
        self,
        base_url: str | None = None
    ) -> None:
        self.base_url = self.DEFAULT_URL if base_url is None else base_url

    @property
    def closed(self) -> bool:
        raise NotImplementedError

    @classmethod
    def _retry_wait(cls, attempt: int) -> float:
        return min(2 ** (attempt + 1), cls.MAX_RETRY_WAIT)

    def _request(
        self,
        path: str,
        method: str = "GET",
        max_retries: int | None = None,
        **request_kwargs: Any
    ) -> str: # type: ignore [override]
        raise NotImplementedError
