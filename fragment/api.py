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
    
    async def _request(
        self,
        parse_method: Callable[[str], T],
        method: str,
        url: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> T:
        if url is None:
            url = self._base_url + "/api"
            if params is None:
                params = {}
            params["hash"] = self._api_hash
        
        async with self._session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers
        ) as response:
            if not response.ok:
                raise FragmentHTTPError(response)

            try:
                json_data: JsonObject = await response.json()
                text = ""
                for key in ["html", "h"]:
                    try:
                        text: str = json_data[key]
                    except KeyError:
                        pass
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
