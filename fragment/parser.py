from selectolax.lexbor import LexborHTMLParser

import re
from typing import List

from .helper import to_float
from .errors import ParserError
from .type_hints import Username


def parse_api_hash(html: str) -> str:
    parser = LexborHTMLParser(html)
    for script_tag in parser.body.css("script"):
        try:
            text = script_tag.text()
            if text.startswith("ajInit"):
                matches = re.findall('api\?hash=(.*)",', text)
                if len(matches) > 0:
                    return matches[0]
                else:
                    raise Exception("Api hash not found!")
        except Exception as e:
            raise ParserError(script_tag.html) from e


def parse_auctions(html: str) -> List[Username]:
    parser = LexborHTMLParser(html)
    result = []
    for element in parser.css(".tm-row-selectable"):
        try:
            is_resale = None
            username = element.css_first(".table-cell-value.tm-value").text()

            raw_status = element.css_first(".wide-last-col .table-cell-value.tm-value")
            if raw_status is None:
                status = "auction"
                is_resale = element.css_matches(".table-cell-status-thin")
            else:
                raw_status_text = raw_status.text().lower()
                if raw_status_text == "on auction":
                    status = "auction"
                elif raw_status_text == "for sale":
                    status = "sale"
                else:
                    status = raw_status_text
            
            if status in ["available", "unavailable", "taken"]:
                dt = None
            else:
                dt = element.css_first(".wide-last-col time").attributes.get("datetime")
            
            result.append(Username(
                username=username[1:],
                status=status,
                value=to_float(element.css_first(".thin-last-col .table-cell-value").text()),
                datetime=dt,
                is_resale=is_resale
            ))
        except Exception as e:
            raise ParserError(element.html) from e
    return result
