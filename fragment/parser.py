from __future__ import annotations

from selectolax.lexbor import LexborHTMLParser

from .helper import to_float, parse_status
from .errors import ParserError
from .type_hints import Username, OwnershipHistoryElement, BidHistoryElement, LatestOffersElement, FullUsername


def parse_auctions(html: str) -> list[Username]:
    try:
        parser = LexborHTMLParser(html)

        container = parser.css_first(".js-search-results tbody")
        if container is None:
            return []

        result = []

        for row in container.css(".tm-row-selectable"):
            username = row.css_first(".table-cell-value.tm-value").text(strip=True).lstrip("@")

            wide_status_node = row.css_first(".wide-last-col .tm-value")
            if wide_status_node is None:
                status = "auction"
                is_resale = bool(row.css_matches(".table-cell-status-thin"))
            else:
                status = parse_status(wide_status_node.text(strip=True))
                is_resale = None

            time_node = row.css_first(".wide-last-col time")
            dt = time_node.attributes.get("datetime") if time_node is not None else None

            value = to_float(row.css_first(".thin-last-col .table-cell-value").text(strip=True))

            result.append(Username(
                username=username,
                status=status,
                value=value,
                datetime=dt,
                is_resale=is_resale
            ))

        return result
    except Exception as e:
        raise ParserError(parser.html) from e


def parse_username_info(html: str) -> FullUsername:
    try:
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

            table_rows = tm_section.css("table > tbody tr")

            for row in table_rows:
                table_cells = row.css(".table-cell")

                price = to_float(table_cells[0].text(strip=True))

                date = table_cells[1].css_first(".wide-only").text(strip=True)

                wallet_node = table_cells[2].css_first(".tm-wallet")
                wallet = wallet_node.attributes.get("href", "").removeprefix(
                    "https://tonviewer.com/")

                if header_text == "bid history":
                    bid_history_elems.append(
                        BidHistoryElement(
                            ton_price=price,
                            date=date,
                            from_=wallet,
                        )
                    )
                elif header_text == "ownership history":
                    ownership_history_elems.append(
                        OwnershipHistoryElement(
                            ton_sell_price=price,
                            date=date,
                            buyer=wallet,
                        )
                    )
                elif header_text == "latest offers":
                    latest_offers_elems.append(
                        LatestOffersElement(
                            ton_offer=price,
                            date=date,
                            offered_by=wallet,
                        )
                    )

        username_raw = parser.css_first(".tm-section-auction-info :first-child > dd").text(strip=True)
        status_raw = parser.css_first(".tm-section-header-status").text(strip=True)

        return FullUsername(
            username=username_raw.lstrip("@"),
            status=parse_status(status_raw),
            ownership_history=ownership_history_elems,
            bid_history=bid_history_elems,
            latest_offers=latest_offers_elems
        )
    except Exception as e:
        raise ParserError(parser.html) from e
