from __future__ import annotations

from requests import Session
from requests.exceptions import ConnectionError, Timeout

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

from .methods import SyncMethods
from ..base_client import BaseClient
from ..__version__ import __version__
from ..errors import FragmentHTTPError


class Client(BaseClient, SyncMethods):
    __slots__ = (
        "_session",
    )

    DEFAULT_TIMEOUT = 10

    def __init__(
        self,
        base_url: str | None = None
    ) -> None:
        super().__init__(base_url)

        self._session: Session | None = None

    @property
    def closed(self) -> bool:
        return self._session is None

    def _create_session(self) -> Session:
        session = Session()
        session.headers["User-Agent"] = "python-fragment-" + __version__
        return session

    def _request(
        self,
        path: str,
        method: str = "GET",
        max_retries: int | None = None,
        **request_kwargs: Any
    ) -> str:
        if self._session is None:
            raise RuntimeError("HTTP session is not initialized. Use the context manager")

        if max_retries is None:
            max_retries = self.MAX_RETRIES

        for attempt in range(max_retries + 1):
            try:
                response = self._session.request(
                    method=method,
                    url=self.base_url + path,
                    timeout=request_kwargs.pop("timeout", self.DEFAULT_TIMEOUT),
                    **request_kwargs
                )
                if not response.ok:
                    raise FragmentHTTPError(
                            response.request.method or "?",
                            response.status_code,
                            response.url
                        )

                return response.text
            except (
                ConnectionError, # Connection-level error
                Timeout # Request timeout
            ):
                if attempt == max_retries:
                    raise

            time.sleep(self._retry_wait(attempt))

    def __enter__(self) -> Client:
        if self.closed:
            self._session = self._create_session()

        return self

    def __exit__(self, *_: Any) -> None:
        if not self.closed:
            session, self._session = self._session, None
            session.close()
