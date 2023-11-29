from selectolax.lexbor import LexborHTMLParser

import re
from typing import List

from .helper import to_float, parse_status
from .errors import ParserError
from .type_hints import Username, OwnershipHistoryElement, BidHistoryElement, LatestOffersElement, FullUsername


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
                status = parse_status(raw_status.text())
            
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


def parse_username_info(html: str) -> FullUsername:
    parser = LexborHTMLParser(html)

    bid_history_elems = []
    ownership_history_elems = []
    latest_offers_elems = []

    tm_sections = parser.css("main > section.tm-section.clearfix")
    for tm_section in tm_sections:
        header = tm_section.css_first(".tm-section-header-text")
        if header is None:
            continue
        header_text = header.text(strip=True).lower()

        if header_text == "bid history":
            table_elems = tm_section.css("table > tbody tr")
            for table_elem in table_elems:
                table_cells = table_elem.css(".table-cell")
                bid_history_elems.append(BidHistoryElement(
                    ton_price=to_float(table_cells[0].text(strip=True)),
                    date=table_cells[1].css_first(".wide-only").text(strip=True),
                    from_=table_cells[2].text(strip=True)
                ))
        elif header_text == "ownership history":
            table_elems = tm_section.css("table > tbody tr")
            for table_elem in table_elems:
                table_cells = table_elem.css(".table-cell")
                ownership_history_elems.append(OwnershipHistoryElement(
                    ton_sell_price=to_float(table_cells[0].text(strip=True)),
                    date=table_cells[1].css_first(".wide-only").text(strip=True),
                    buyer=table_cells[2].text(strip=True)
                ))
        elif header_text == "latest offers":
            table_elems = tm_section.css("table > tbody tr")
            for table_elem in table_elems:
                table_cells = table_elem.css(".table-cell")
                latest_offers_elems.append(LatestOffersElement(
                    ton_offer=to_float(table_cells[0].text(strip=True)),
                    date=table_cells[1].css_first(".wide-only").text(strip=True),
                    offered_by=table_cells[2].text(strip=True)
                ))

    return FullUsername(
        username=parser.css_first(".tm-section-auction-info :first-child > dd").text(strip=True)[1:],
        status=parse_status(parser.css_first(".tm-section-header-status").text()),
        ownership_history=ownership_history_elems,
        bid_history=bid_history_elems,
        latest_offers=latest_offers_elems
    )
