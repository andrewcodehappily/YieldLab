from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from app.models import YieldCurve

PROJECT_DIR = Path(__file__).resolve().parents[2]
HISTORY_FILE = PROJECT_DIR / "data" / "treasury_history.json"


def merge_history(*groups: list[YieldCurve]) -> list[YieldCurve]:
    by_date: dict[str, YieldCurve] = {}
    for group in groups:
        for curve in group:
            by_date[curve.as_of] = curve
    return [by_date[date] for date in sorted(by_date)]


def load_history(path: Path = HISTORY_FILE) -> list[YieldCurve]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    curves = [YieldCurve.model_validate(item) for item in payload]
    return merge_history(curves)


def save_history(curves: list[YieldCurve], path: Path = HISTORY_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = merge_history(curves)
    serialized = json.dumps(
        [curve.model_dump() for curve in ordered],
        indent=2,
        ensure_ascii=False,
    ) + "\n"

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


def get_curve_by_date(curves: list[YieldCurve], as_of: str) -> YieldCurve | None:
    return next((curve for curve in curves if curve.as_of == as_of), None)
