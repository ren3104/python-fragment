from __future__ import annotations

from requests import Session
from requests.exceptions import ConnectionError, Timeout

import time
import sys
from typing import TYPE_CHECKING

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

if TYPE_CHECKING:
    from typing import Any

from .._abstract import AbstractClient
from ..__version__ import __version__
from ..errors import FragmentHTTPError


class BaseClient(AbstractClient):
    __slots__ = ("_session",)

    def __init__(
        self,
        base_url: str | None = None,
        proxy: str | None = None
    ) -> None:
        super().__init__(base_url, proxy)

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
        params: dict[str, Any] | None = None,
        method: str = "GET",
        timeout: int | None = None,
        max_retries: int | None = None,
        proxy: str | None = None
    ) -> Any:
        if self._session is None:
            raise RuntimeError("HTTP session is not initialized. Use the context manager")

        if max_retries is None:
            max_retries = self.MAX_RETRIES

        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        if proxy is None:
            if self._proxy is None:
                real_proxy = None
            else:
                real_proxy = {"http": self._proxy, "https": self._proxy}
        else:
            real_proxy = {"http": proxy, "https": proxy}

        for attempt in range(max_retries + 1):
            try:
                response = self._session.request(
                    method=method,
                    url=self.base_url + path,
                    params=params,
                    timeout=timeout,
                    proxies=real_proxy
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

    def __enter__(self) -> Self:
        if self.closed:
            self._session = self._create_session()

        return self

    def __exit__(self, *_: Any) -> None:
        if not self.closed:
            session, self._session = self._session, None
            session.close()
