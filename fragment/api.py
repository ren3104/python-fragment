from aiohttp import ClientSession

from typing import Any, Optional, Callable, Type
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import TracebackType

from .resources import *
from .errors import FragmentHTTPError
from .type_hints import T


class FragmentAPI:
    __slots__ = (
        "_session",
        "_base_url",
        "usernames"
    )

    def __init__(
        self,
        base_url: str = "https://fragment.com",
        session: Optional[ClientSession] = None
    ) -> None:
        if session is None:
            session = ClientSession()
        self._session = session

        self._base_url = base_url

        self.usernames = Usernames(self)
    
    async def _request(
        self,
        parse_method: Callable[[str], T],
        method: str,
        url: str,
        **request_kwargs: Any
    ) -> T:
        async with self._session.request(
            method=method,
            url=self._base_url + url,
            **request_kwargs
        ) as response:
            if not response.ok:
                raise FragmentHTTPError(response)
            
            return parse_method(await response.text())
    
    async def __aenter__(self) -> "FragmentAPI":
        await self._session.__aenter__()
        return self
    
    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: "TracebackType"
    ) -> None:
        await self._session.__aexit__(
            exc_type=exc_type,
            exc_val=exc_value,
            exc_tb=traceback
        )
