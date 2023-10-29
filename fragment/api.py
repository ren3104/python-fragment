from aiohttp import ClientSession, ContentTypeError

from types import TracebackType
from typing import Any, Dict, Optional, Callable, Type

from .resources import *
from .errors import FragmentHTTPError
from .parser import parse_api_hash
from .type_hints import T, JsonObject


class FragmentAPI:
    __slots__ = frozenset(
        [
            "_session",
            "_base_url",
            "_api_hash",
            "usernames"
        ]
    )

    def __init__(
        self,
        session: Optional[ClientSession] = None,
        base_url: str = "https://fragment.com"
    ) -> None:
        if session is None:
            session = ClientSession()
        self._session = session

        self._base_url = base_url
        self._api_hash = ""

        self.usernames = Usernames(self)
    
    def _prepare_request(
        self,
        method: str,
        url: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if url is None:
            url = self._base_url + "/api"
            if params is None:
                params = {}
            params["hash"] = self._api_hash
            
        return {
            "method": method,
            "url": url,
            "params": params,
            "data": data
        }
    
    async def _request(
        self,
        parse_method: Callable[[str], T],
        method: str,
        url: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> T:
        async with self._session.request(
            **self._prepare_request(method, url, params, data)
        ) as response:
            if not response.ok:
                raise FragmentHTTPError(response)

            try:
                data: JsonObject = await response.json()
                text: str = data.get("html", "")
            except ContentTypeError:
                text = await response.text()
            
        return parse_method(text)
    
    async def __aenter__(self) -> "FragmentAPI":
        await self._session.__aenter__()
        self._api_hash = await self._request(
            parse_method=parse_api_hash,
            method="GET",
            url=self._base_url
        )
        return self
    
    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType
    ) -> None:
        await self._session.__aexit__(exc_type, exc_value, traceback)
