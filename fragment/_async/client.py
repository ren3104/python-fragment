from __future__ import annotations

import re
import sys
from typing import TYPE_CHECKING

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

if TYPE_CHECKING:
    from typing import Any

    from ..type_hints import (
        FragmentFilter,
        FragmentSort,
        Username,
        FullUsername
    )

from ._base import BaseClient
from ..parser import (
    parse_init_data,
    parse_auctions,
    parse_username_info
)


class AsyncClient(BaseClient):
    async def search_usernames(
        self,
        query: str = "",
        filter: FragmentFilter = "",
        sort: FragmentSort = "",
        **request_kwargs: Any
    ) -> list[Username]:
        raw_data = await self._request(
            path="/",
            params={
                "query": query,
                "filter": filter,
                "sort": sort
            },
            **request_kwargs
        )
        return parse_auctions(raw_data)

    async def username_info(
        self,
        username: str,
        **request_kwargs: Any
    ) -> FullUsername:
        raw_data = await self._request(
            path="/username/" + username,
            **request_kwargs
        )
        return parse_username_info(raw_data)

    async def get_init_data(
        self,
        **request_kwargs: Any
    ) -> dict[str, Any]:
        raw_data = await self._request(
            path="/",
            **request_kwargs
        )
        return parse_init_data(raw_data)

    async def __aenter__(self) -> Self:
        await super().__aenter__()

        init_data = await self.get_init_data()
        if (api_url := init_data.get("apiUrl")) and (
            match := re.search(r"hash=(\w+)", api_url)
        ):
            self._api_hash = match.group(1)
        else:
            raise RuntimeError("Failed to get api_hash")

        return self
