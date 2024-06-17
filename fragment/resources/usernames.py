from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..type_hints import FragmentFilter, FragmentSort

from .base import BaseResource
from ..parser import parse_auctions, parse_username_info


class Usernames(BaseResource):
    async def search(
        self,
        query: str = "",
        filter_: "FragmentFilter" = "",
        sort: "FragmentSort" = "",
        **request_kwargs: Any
    ):
        """
        Returns a list of username auctions.
        """
        return await self._api._request(
            parse_method=parse_auctions,
            method="GET",
            url="/",
            params={
                "query": query,
                "filter": filter_,
                "sort": sort
            },
            **request_kwargs
        )
    
    async def info(
        self,
        username: str,
        **request_kwargs: Any
    ):
        """
        Returns full info about the username.
        """
        return await self._api._request(
            parse_method=parse_username_info,
            method="GET",
            url="/username/" + username,
            **request_kwargs
        )
