from __future__ import annotations

import csv
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from io import StringIO
import json
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import xlrd

from app.models import MarketHistoryData, MarketHistoryPoint
from app.services.market_history import DAILY_MARKET_HISTORY_FILE, MARKET_HISTORY_FILE

MULTPL_URL = "https://www.multpl.com/s-p-500-historical-prices/table/by-month"
ACM_XLS_URL = "https://www.newyorkfed.org/medialibrary/media/research/data_indicators/ACMTermPremium.xls"
FRED_SP500_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500"
FRED_T10Y2Y_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y"
EQUIBLES_SP500_CSV_URL = "https://equibles.com/economicdata/sp500.csv"
EQUIBLES_T10Y2Y_CSV_URL = "https://equibles.com/economicdata/t10y2y.csv"
DATAQUEST_SP500_CSV_URL = "https://raw.githubusercontent.com/dataquestio/project-walkthroughs/master/sp_500/sp500.csv"
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
    for attempt in range(attempts):
        request = Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "*/*",
                "Accept-Encoding": "identity",
                "Connection": "close",
            },
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                return response.read()
        except (TimeoutError, OSError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(1.0 + attempt)

    try:
        result = subprocess.run(
            [
                "curl",
                "-fsSL",
                "--retry",
                "4",
                "--retry-all-errors",
                "--connect-timeout",
                "15",
                "--max-time",
                str(int(timeout * 2)),
                "-A",
                USER_AGENT,
                url,
            ],
            check=True,
            capture_output=True,
            timeout=timeout * 3,
        )
        if result.stdout:
            return result.stdout
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
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


def _fetch_fred_daily_series(url: str, field: str) -> dict[str, float]:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/csv,*/*",
            "Accept-Encoding": "identity",
            "Connection": "close",
        },
    )
    try:
        with urlopen(request, timeout=10.0) as response:
            text = response.read().decode("utf-8", errors="replace")
    except (TimeoutError, OSError) as exc:
        raise RuntimeError(f"Unable to fetch FRED {field} daily data") from exc
    reader = csv.DictReader(StringIO(text))
    daily: dict[str, float] = {}
    for row in reader:
        raw_date = (row.get("observation_date") or "").strip()
        raw_value = (row.get(field) or "").strip()
        if not raw_date or raw_value in {"", "."}:
            continue
        try:
            datetime.strptime(raw_date, "%Y-%m-%d")
            daily[raw_date] = round(float(raw_value), 8)
        except ValueError:
            continue
    if not daily:
        raise RuntimeError(f"No FRED {field} observations were parsed")
    return daily


def _recent_fred_url(base_url: str) -> str:
    end = datetime.now(timezone.utc).date()
    try:
        start = end.replace(year=end.year - 10)
    except ValueError:
        start = end.replace(year=end.year - 10, day=28)
    separator = "&" if "?" in base_url else "?"
    return f"{base_url}{separator}cosd={start.isoformat()}&coed={end.isoformat()}"


def _fetch_equibles_series(url: str, series_id: str) -> dict[str, float]:
    text = _fetch_bytes(url).decode("utf-8", errors="replace")
    reader = csv.DictReader(StringIO(text))
    daily: dict[str, float] = {}
    for row in reader:
        if (row.get("Series ID") or "").strip().upper() != series_id.upper():
            continue
        raw_date = (row.get("Date") or "").strip()
        raw_value = (row.get("Value") or "").strip()
        if not raw_date or not raw_value:
            continue
        try:
            datetime.strptime(raw_date, "%Y-%m-%d")
            daily[raw_date] = round(float(raw_value), 8)
        except ValueError:
            continue
    if not daily:
        raise RuntimeError(f"No Equibles {series_id} observations were parsed")
    return daily


def _fetch_dataquest_sp500_daily() -> dict[str, float]:
    text = _fetch_bytes(DATAQUEST_SP500_CSV_URL).decode("utf-8", errors="replace")
    reader = csv.DictReader(StringIO(text))
    daily: dict[str, float] = {}
    for row in reader:
        raw_date = (row.get("Date") or "").strip()
        raw_close = (row.get("Close") or "").strip()
        if not raw_date or not raw_close:
            continue
        try:
            datetime.strptime(raw_date, "%Y-%m-%d")
            daily[raw_date] = round(float(raw_close), 8)
        except ValueError:
            continue
    if not daily:
        raise RuntimeError("No Dataquest S&P 500 observations were parsed")
    return daily


def _fetch_sp500_daily() -> tuple[dict[str, float], str]:
    try:
        return (
            _fetch_fred_daily_series(_recent_fred_url(FRED_SP500_CSV_URL), "SP500"),
            "FRED SP500 daily close (S&P Dow Jones Indices LLC)",
        )
    except RuntimeError:
        historical = _fetch_dataquest_sp500_daily()
        recent = _fetch_equibles_series(EQUIBLES_SP500_CSV_URL, "SP500")
        historical.update(recent)
        return (
            historical,
            "Dataquest S&P 500 daily history + Equibles FRED SP500 mirror",
        )


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


def _parse_acm_sheet(
    workbook: xlrd.book.Book,
    sheet_name: str,
    *,
    monthly: bool,
) -> dict[str, tuple[list[float], list[float], list[float]]]:
    sheet = workbook.sheet_by_name(sheet_name)
    header = [str(value).strip() for value in sheet.row_values(0)]
    column_index = {name: index for index, name in enumerate(header)}

    fitted_columns = [column_index[f"ACMY{maturity:02d}"] for maturity in ACM_MATURITIES]
    premium_columns = [column_index[f"ACMTP{maturity:02d}"] for maturity in ACM_MATURITIES]
    expected_columns = [column_index[f"ACMRNY{maturity:02d}"] for maturity in ACM_MATURITIES]

    parsed: dict[str, tuple[list[float], list[float], list[float]]] = {}
    for row_index in range(1, sheet.nrows):
        row = sheet.row_values(row_index)
        try:
            date = _date_from_acm_cell(row[0], workbook.datemode)
            fitted = [round(float(row[index]), 8) for index in fitted_columns]
            premia = [round(float(row[index]), 8) for index in premium_columns]
            expected = [round(float(row[index]), 8) for index in expected_columns]
        except (ValueError, TypeError, IndexError):
            continue

        if any(abs(fitted[i] - (expected[i] + premia[i])) > 1e-5 for i in range(10)):
            continue

        key = f"{date.year:04d}-{date.month:02d}" if monthly else date.date().isoformat()
        parsed[key] = (fitted, premia, expected)

    if not parsed:
        raise RuntimeError(f"No ACM observations were parsed from {sheet_name}")
    return parsed


def _fetch_acm_monthly(payload: bytes | None = None) -> dict[str, tuple[list[float], list[float], list[float]]]:
    workbook = xlrd.open_workbook(file_contents=payload or _fetch_bytes(ACM_XLS_URL))
    return _parse_acm_sheet(workbook, "ACM Monthly", monthly=True)


def _fetch_acm_daily(payload: bytes | None = None) -> dict[str, tuple[list[float], list[float], list[float]]]:
    workbook = xlrd.open_workbook(file_contents=payload or _fetch_bytes(ACM_XLS_URL))
    return _parse_acm_sheet(workbook, "ACM Daily", monthly=False)


def _fetch_fred_10y2y_daily() -> tuple[dict[str, float], str]:
    try:
        return (
            _fetch_fred_daily_series(FRED_T10Y2Y_CSV_URL, "T10Y2Y"),
            "FRED T10Y2Y daily spread",
        )
    except RuntimeError:
        return (
            _fetch_equibles_series(EQUIBLES_T10Y2Y_CSV_URL, "T10Y2Y"),
            "Equibles mirror of FRED T10Y2Y daily spread",
        )


def build_market_history() -> MarketHistoryData:
    sp500 = _fetch_sp500_monthly()
    acm = _fetch_acm_monthly()

    points: list[MarketHistoryPoint] = []
    for month, (date, close) in sorted(sp500.items()):
        components = acm.get(month)
        fitted = premia = expected = None
        if components is not None:
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
        frequency="monthly",
        points=points,
    )


def build_daily_market_history() -> MarketHistoryData:
    sp500, sp500_source = _fetch_sp500_daily()
    acm_payload = _fetch_bytes(ACM_XLS_URL)
    acm = _fetch_acm_daily(acm_payload)
    try:
        fred, fred_source = _fetch_fred_10y2y_daily()
    except RuntimeError:
        fred, fred_source = {}, "FRED T10Y2Y unavailable during refresh"

    points: list[MarketHistoryPoint] = []
    for date, close in sorted(sp500.items()):
        components = acm.get(date)
        fitted = premia = expected = None
        if components is not None:
            fitted, premia, expected = components
        points.append(
            MarketHistoryPoint(
                date=date,
                sp500_close=round(close, 6),
                acm_fitted_yields_pct=fitted,
                acm_term_premia_pct=premia,
                acm_expected_avg_short_rates_pct=expected,
                fred_10y2y_pct=fred.get(date),
            )
        )

    if not points:
        raise RuntimeError("No daily S&P 500 observations were downloaded")

    return MarketHistoryData(
        start_date=points[0].date,
        end_date=points[-1].date,
        sp500_source=sp500_source,
        rates_source=(
            "Federal Reserve Bank of New York ACM Daily + "
            f"{fred_source}"
        ),
        acm_maturities_years=ACM_MATURITIES,
        frequency="daily",
        points=points,
    )


def save_market_history(data: MarketHistoryData, path: Path = MARKET_HISTORY_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path == DAILY_MARKET_HISTORY_FILE:
        serialized = json.dumps(data.model_dump(), separators=(",", ":"), ensure_ascii=False) + "\n"
    else:
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
    daily = build_daily_market_history()
    save_market_history(daily, DAILY_MARKET_HISTORY_FILE)
    available_acm_daily = sum(point.acm_fitted_yields_pct is not None for point in daily.points)
    available_fred = sum(point.fred_10y2y_pct is not None for point in daily.points)
    print(
        f"Daily market history refreshed: {daily.start_date} -> {daily.end_date} "
        f"({len(daily.points)} S&P observations; ACM={available_acm_daily}; FRED={available_fred})"
    )

    try:
        monthly = build_market_history()
        save_market_history(monthly, MARKET_HISTORY_FILE)
        available_acm_monthly = sum(point.acm_fitted_yields_pct is not None for point in monthly.points)
        print(
            f"Monthly market history refreshed: {monthly.start_date} -> {monthly.end_date} "
            f"({len(monthly.points)} S&P observations; ACM={available_acm_monthly})"
        )
    except RuntimeError as exc:
        print(f"Monthly cache refresh skipped: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
