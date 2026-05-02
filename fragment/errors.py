from __future__ import annotations


class FragmentHTTPError(Exception):
    __slots__ = ("method", "status", "url")

    def __init__(self, method: str, status: int, url: str) -> None:
        self.method = method
        self.status = status
        self.url = url

    def __str__(self) -> str:
        return "\n%s (%s) %s" % (
            self.method,
            self.status,
            self.url
        )


class ParserError(Exception):
    __slots__ = ("html",)

    def __init__(self, html: str) -> None:
        self.html = html

        super().__init__("An error occurred while parsing html")
