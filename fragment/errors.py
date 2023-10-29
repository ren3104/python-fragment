from aiohttp import ClientResponse


class FragmentHTTPError(Exception):
    __slots__ = frozenset(["response"])

    def __init__(
            self,
            response: ClientResponse
        ) -> None:
        self.response = response
    
    def __str__(self) -> str:
        return "\n%s (%s) %s" % (
            self.response.method,
            self.response.status,
            self.response.url
        )


class ParserError(Exception):
    __slots__ = frozenset(["html"])

    def __init__(self, html: str) -> None:
        self.html = html
        super().__init__("An error occurred while parsing html")
    