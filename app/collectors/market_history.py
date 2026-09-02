from __future__ import annotations

from datetime import datetime
from html.parser import HTMLParser
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.request import Request, urlopen

import xlrd

from app.models import MarketHistoryData, MarketHistoryPoint
from app.services.market_history import MARKET_HISTORY_FILE

MULTPL_URL = "https://www.multpl.com/s-p-500-historical-prices/table/by-month"
ACM_XLS_URL = "https://www.newyorkfed.org/medialibrary/media/research/data_indicators/ACMTermPremium.xls"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
)
ACM_MATURITIES = list(range(1, 11))


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


def _fetch_bytes(url: str, timeout: float = 35.0, attempts: int = 3) -> bytes:
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


def _date_from_acm_cell(value: object, datemode: int) -> datetime:
    if isinstance(value, (int, float)):
        return xlrd.xldate_as_datetime(value, datemode)
    raw = str(value).strip()
    for fmt in ("%d-%b-%Y", "%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            pass
    raise ValueError(f"Unsupported ACM date: {raw}")


def _fetch_acm_monthly() -> dict[str, tuple[list[float], list[float], list[float]]]:
    payload = _fetch_bytes(ACM_XLS_URL)
    workbook = xlrd.open_workbook(file_contents=payload)
    sheet = workbook.sheet_by_name("ACM Monthly")
    header = [str(value).strip() for value in sheet.row_values(0)]
    column_index = {name: index for index, name in enumerate(header)}

    fitted_columns = [column_index[f"ACMY{maturity:02d}"] for maturity in ACM_MATURITIES]
    premium_columns = [column_index[f"ACMTP{maturity:02d}"] for maturity in ACM_MATURITIES]
    expected_columns = [column_index[f"ACMRNY{maturity:02d}"] for maturity in ACM_MATURITIES]

    monthly: dict[str, tuple[list[float], list[float], list[float]]] = {}
    for row_index in range(1, sheet.nrows):
        row = sheet.row_values(row_index)
        try:
            date = _date_from_acm_cell(row[0], workbook.datemode)
            fitted = [round(float(row[index]), 8) for index in fitted_columns]
            premia = [round(float(row[index]), 8) for index in premium_columns]
            expected = [round(float(row[index]), 8) for index in expected_columns]
        except (ValueError, TypeError, IndexError):
            continue

        # Sanity check the ACM identity: fitted yield = expected-average short rate + term premium.
        if any(abs(fitted[i] - (expected[i] + premia[i])) > 1e-5 for i in range(10)):
            continue

        monthly[f"{date.year:04d}-{date.month:02d}"] = (fitted, premia, expected)

    if not monthly:
        raise RuntimeError("No monthly ACM term-premium observations were parsed")
    return monthly


def build_market_history() -> MarketHistoryData:
    sp500 = _fetch_sp500_monthly()
    acm = _fetch_acm_monthly()

    points: list[MarketHistoryPoint] = []
    for month, (date, close) in sorted(sp500.items()):
        components = acm.get(month)
        if components is None:
            fitted = premia = expected = None
        else:
            fitted, premia, expected = components
        points.append(
            MarketHistoryPoint(
                date=date,
                sp500_close=round(close, 4),
                acm_fitted_yields_pct=fitted,
                acm_term_premia_pct=premia,
                acm_expected_avg_short_rates_pct=expected,
            )
        )

    if not points:
        raise RuntimeError("No S&P 500 observations were downloaded")

    return MarketHistoryData(
        start_date=points[0].date,
        end_date=points[-1].date,
        sp500_source="Multpl monthly S&P 500 historical prices (Standard & Poor's / Robert Shiller)",
        rates_source="Federal Reserve Bank of New York Adrian-Crump-Moench (ACM) Treasury Term Premia",
        acm_maturities_years=ACM_MATURITIES,
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
    available_acm = sum(point.acm_fitted_yields_pct is not None for point in data.points)
    print(
        f"Market history refreshed: {data.start_date} -> {data.end_date} "
        f"({len(data.points)} monthly S&P observations; ACM={available_acm}, maturities=1Y-10Y)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
