from __future__ import annotations

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientConnectionError

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

from .methods import AsyncMethods
from ..base_client import BaseClient
from ..__version__ import __version__
from ..errors import FragmentHTTPError


class AsyncClient(BaseClient, AsyncMethods):
    __slots__ = (
        "_session",
    )

    DEFAULT_TIMEOUT = ClientTimeout(total=10)

    def __init__(
        self,
        base_url: str | None = None
    ) -> None:
        super().__init__(base_url)

        self._session: ClientSession | None = None

    @property
    def closed(self) -> bool:
        return self._session is None or self._session.closed

    def _create_session(self) -> ClientSession:
        return ClientSession(
            headers={
                "User-Agent": "python-fragment-" + __version__
            }
        )

    async def _request(
        self,
        path: str,
        method: str = "GET",
        max_retries: int | None = None,
        **request_kwargs: Any
    ) -> str:
        if max_retries is None:
            max_retries = self.MAX_RETRIES

        for attempt in range(max_retries + 1):
            if self._session is None:
                raise RuntimeError("HTTP session is not initialized. Use the context manager")
            elif self._session.closed:
                self._session = self._create_session()

            try:
                async with self._session.request(
                    method=method,
                    url=self.base_url + path,
                    timeout=request_kwargs.pop("timeout", self.DEFAULT_TIMEOUT),
                    **request_kwargs
                ) as response:
                    if not response.ok:
                        raise FragmentHTTPError(
                            response.method,
                            response.status,
                            str(response.url)
                        )

                    return await response.text()
            except (
                ClientConnectionError, # Connector is closed
                asyncio.TimeoutError # Request timeout
            ):
                if attempt == max_retries:
                    raise

            await asyncio.sleep(self._retry_wait(attempt))

    async def __aenter__(self) -> AsyncClient:
        if self.closed:
            self._session = self._create_session()

        return self

    async def __aexit__(self, *_: Any) -> None:
        if not self.closed:
            session, self._session = self._session, None
            await session.close()

            # Wait 250 ms for the underlying SSL connections to close
            # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
            await asyncio.sleep(0.25)
