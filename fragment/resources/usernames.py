from .base import BaseResource
from ..parser import parse_auctions
from ..type_hints import FragmentFilter, FragmentSort


class Usernames(BaseResource):
    async def search(
        self,
        query: str = "",
        filter_: FragmentFilter = "",
        sort: FragmentSort = ""
    ):
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
