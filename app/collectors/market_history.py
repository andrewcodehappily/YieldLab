from __future__ import annotations

import csv
from datetime import datetime
from html.parser import HTMLParser
import io
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.models import MarketHistoryData, MarketHistoryPoint
from app.services.market_history import MARKET_HISTORY_FILE

MULTPL_URL = "https://www.multpl.com/s-p-500-historical-prices/table/by-month"
FED_H15_OUTPUT_URL = "https://www.federalreserve.gov/datadownload/Output.aspx"
FED_H15_MONTHLY_PACKAGE = "d7e27b7b09a3a7feae95b9c61781fcd8"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
)


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_table = False
        self.in_td = False
        self.current_cell: list[str] = []
        self.current_row: list[str] = []
        self.rows: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "table" and attrs_dict.get("id") == "datatable":
            self.in_table = True
        elif self.in_table and tag == "td":
            self.in_td = True
            self.current_cell = []
        elif self.in_table and tag == "tr":
            self.current_row = []

    def handle_data(self, data: str) -> None:
        if self.in_td:
            self.current_cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.in_table and tag == "td" and self.in_td:
            text = " ".join("".join(self.current_cell).split())
            self.current_row.append(text)
            self.in_td = False
        elif self.in_table and tag == "tr":
            if len(self.current_row) >= 2:
                self.rows.append(self.current_row[:2])
            self.current_row = []
        elif self.in_table and tag == "table":
            self.in_table = False


def _fetch_bytes(url: str, timeout: float = 30.0, attempts: int = 3) -> bytes:
    last_error: Exception | None = None
    for _ in range(attempts):
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        try:
            with urlopen(request, timeout=timeout) as response:
                return response.read()
        except (TimeoutError, OSError) as exc:
            last_error = exc
    raise RuntimeError(f"Unable to download market-history source: {url}") from last_error


def _fetch_sp500_monthly() -> dict[str, tuple[str, float]]:
    parser = _TableParser()
    parser.feed(_fetch_bytes(MULTPL_URL).decode("utf-8", errors="replace"))

    monthly: dict[str, tuple[str, float]] = {}
    for raw_date, raw_value in parser.rows:
        try:
            date = datetime.strptime(raw_date, "%b %d, %Y").date()
            value = float(raw_value.replace(",", ""))
        except ValueError:
            continue
        if date.year < 1950:
            continue
        monthly[f"{date.year:04d}-{date.month:02d}"] = (date.isoformat(), value)

    if not monthly:
        raise RuntimeError("No S&P 500 observations were parsed from Multpl")
    return monthly


def _parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if value in {"", ".", "NA", "N/A"}:
        return None
    return float(value)


def _fetch_h15_monthly() -> tuple[dict[str, float], dict[str, float], dict[str, float]]:
    today = datetime.now().date()
    params = urlencode(
        {
            "rel": "H15",
            "series": FED_H15_MONTHLY_PACKAGE,
            "lastobs": "",
            "from": "01/01/1950",
            "to": today.strftime("%m/%d/%Y"),
            "filetype": "csv",
            "label": "include",
            "layout": "seriescolumn",
            "type": "package",
        }
    )
    payload = _fetch_bytes(f"{FED_H15_OUTPUT_URL}?{params}").decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(payload)))
    header_index = next(
        (index for index, row in enumerate(rows) if row and row[0] == "Time Period"),
        None,
    )
    if header_index is None:
        raise RuntimeError("Federal Reserve H.15 CSV did not contain a Time Period header")

    header = rows[header_index]
    column_index = {name: index for index, name in enumerate(header)}
    required = {
        "3m": "RIFSGFSM03_N.M",
        "2y": "RIFLGFCY02_N.M",
        "10y": "RIFLGFCY10_N.M",
    }
    if any(series not in column_index for series in required.values()):
        raise RuntimeError("Federal Reserve H.15 CSV is missing required Treasury series")

    series_data: dict[str, dict[str, float]] = {key: {} for key in required}
    for row in rows[header_index + 1 :]:
        if not row or len(row) <= max(column_index[series] for series in required.values()):
            continue
        month = row[0].strip()
        if len(month) != 7 or month[4] != "-":
            continue
        for key, series in required.items():
            value = _parse_float(row[column_index[series]])
            if value is not None:
                series_data[key][month] = value

    return series_data["10y"], series_data["3m"], series_data["2y"]


def _subtract_series(long_series: dict[str, float], short_series: dict[str, float]) -> dict[str, float]:
    return {
        month: round((long_series[month] - short_series[month]) * 100, 4)
        for month in long_series.keys() & short_series.keys()
    }


def build_market_history() -> MarketHistoryData:
    sp500 = _fetch_sp500_monthly()
    ten_year, three_month, two_year = _fetch_h15_monthly()
    spread_10y3m = _subtract_series(ten_year, three_month)
    spread_10y2y = _subtract_series(ten_year, two_year)

    points = [
        MarketHistoryPoint(
            date=date,
            sp500_close=round(close, 4),
            spread_10y3m_bp=spread_10y3m.get(month),
            spread_10y2y_bp=spread_10y2y.get(month),
        )
        for month, (date, close) in sorted(sp500.items())
    ]
    if not points:
        raise RuntimeError("No S&P 500 observations were downloaded")

    return MarketHistoryData(
        start_date=points[0].date,
        end_date=points[-1].date,
        sp500_source="Multpl monthly S&P 500 historical prices (Standard & Poor's / Robert Shiller)",
        rates_source="Board of Governors of the Federal Reserve System H.15 monthly averages",
        points=points,
    )


def save_market_history(data: MarketHistoryData, path: Path = MARKET_HISTORY_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(data.model_dump(), indent=2, ensure_ascii=False) + "\n"
    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as handle:
        handle.write(serialized)
        temporary_path = Path(handle.name)
    temporary_path.replace(path)


def main() -> int:
    data = build_market_history()
    save_market_history(data)
    available_10y3m = sum(point.spread_10y3m_bp is not None for point in data.points)
    available_10y2y = sum(point.spread_10y2y_bp is not None for point in data.points)
    print(
        f"Market history refreshed: {data.start_date} -> {data.end_date} "
        f"({len(data.points)} monthly S&P observations; "
        f"10Y-3M={available_10y3m}, 10Y-2Y={available_10y2y})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
