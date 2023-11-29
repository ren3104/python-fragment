from .base import BaseResource
from ..parser import parse_auctions, parse_username_info
from ..type_hints import FragmentFilter, FragmentSort


class Usernames(BaseResource):
    async def search(
        self,
        query: str = "",
        filter_: FragmentFilter = "",
        sort: FragmentSort = ""
    ):
        """
        Returns a list of username auctions.
        """
        return await self._api._request(
            parse_method=parse_auctions,
            method="POST", 
            data={
                "type": "usernames",
                "query": query,
                "filter": filter_,
                "sort": sort,
                "method": "searchAuctions"
            }
        )
    
    async def info(self, username: str):
        return await self._api._request(
            parse_method=parse_username_info,
            method="GET",
            url=f"{self._api._base_url}/username/{username}",
            headers={
                "X-Aj-Referer": self._api._base_url,
                "X-Requested-With": "XMLHttpRequest"
            }
        )
