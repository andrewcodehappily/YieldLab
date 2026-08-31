from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.error import URLError
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from app.models import YieldCurve, YieldPoint
from app.services.curve import DEMO_CURVE

PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_DIR / "data" / "treasury_curve.json"
TREASURY_XML_URL = (
    "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
    "pages/xml?data=daily_treasury_yield_curve&field_tdr_date_value_month={year_month}"
)
USER_AGENT = (
    "Mozilla/5.0 (compatible; YieldLab/0.1; "
    "+https://github.com/andrewcodehappily/YieldLab)"
)

_NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
    "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
}

_FIELD_MAP: tuple[tuple[str, float, str], ...] = (
    ("BC_1MONTH", 1 / 12, "1M"),
    ("BC_1_5MONTH", 1.5 / 12, "1.5M"),
    ("BC_2MONTH", 2 / 12, "2M"),
    ("BC_3MONTH", 0.25, "3M"),
    ("BC_4MONTH", 4 / 12, "4M"),
    ("BC_6MONTH", 0.5, "6M"),
    ("BC_1YEAR", 1, "1Y"),
    ("BC_2YEAR", 2, "2Y"),
    ("BC_3YEAR", 3, "3Y"),
    ("BC_5YEAR", 5, "5Y"),
    ("BC_7YEAR", 7, "7Y"),
    ("BC_10YEAR", 10, "10Y"),
    ("BC_20YEAR", 20, "20Y"),
    ("BC_30YEAR", 30, "30Y"),
)


def _property_text(properties: ET.Element, field: str) -> str | None:
    suffix = f"}}{field}"
    for child in properties:
        if child.tag.endswith(suffix):
            return child.text
    return None


def parse_treasury_xml(payload: bytes) -> YieldCurve:
    root = ET.fromstring(payload)
    entries = root.findall("atom:entry", _NAMESPACES)
    if not entries:
        raise ValueError("Treasury feed returned no yield-curve entries")

    latest: tuple[datetime, ET.Element] | None = None
    for entry in entries:
        properties = entry.find("atom:content/m:properties", _NAMESPACES)
        if properties is None:
            continue

        raw_date = _property_text(properties, "NEW_DATE")
        if not raw_date:
            continue

        date = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
        if latest is None or date > latest[0]:
            latest = (date, properties)

    if latest is None:
        raise ValueError("Treasury feed contained no dated observations")

    date, properties = latest
    points: list[YieldPoint] = []
    for field, maturity, label in _FIELD_MAP:
        raw_yield = _property_text(properties, field)
        if raw_yield in (None, "", "N/A"):
            continue
        points.append(
            YieldPoint(
                maturity_years=maturity,
                yield_pct=float(raw_yield),
                label=label,
            )
        )

    if len(points) < 2:
        raise ValueError("Treasury feed did not contain enough valid maturities")

    return YieldCurve(
        as_of=date.date().isoformat(),
        source="U.S. Department of the Treasury",
        points=points,
    )


def _candidate_months() -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    current = f"{now.year}{now.month:02d}"
    if now.month == 1:
        previous = f"{now.year - 1}12"
    else:
        previous = f"{now.year}{now.month - 1:02d}"
    return current, previous


def fetch_latest_treasury_curve(timeout: float = 6.0) -> YieldCurve:
    last_error: Exception | None = None

    for year_month in _candidate_months():
        request = Request(
            TREASURY_XML_URL.format(year_month=year_month),
            headers={"User-Agent": USER_AGENT, "Accept": "application/xml,text/xml"},
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                return parse_treasury_xml(response.read())
        except (URLError, TimeoutError, ET.ParseError, ValueError) as exc:
            last_error = exc

    raise RuntimeError("Unable to fetch Treasury yield curve") from last_error


def load_cached_curve(path: Path = DATA_FILE) -> YieldCurve:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return YieldCurve.model_validate(payload)


def save_cached_curve(curve: YieldCurve, path: Path = DATA_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(curve.model_dump(), indent=2, ensure_ascii=False) + "\n"

    # Atomic replace keeps readers from ever seeing a half-written JSON file.
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


def refresh_cached_curve() -> YieldCurve:
    curve = fetch_latest_treasury_curve()
    save_cached_curve(curve)
    return curve


def get_current_curve() -> YieldCurve:
    try:
        return load_cached_curve()
    except (OSError, json.JSONDecodeError, ValueError):
        return DEMO_CURVE.model_copy(
            update={"source": "YieldLab demo data (local Treasury cache unavailable)"}
        )
