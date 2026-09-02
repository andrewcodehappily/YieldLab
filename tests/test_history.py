from app.models import YieldCurve, YieldPoint
from app.services.history import get_curve_by_date, load_history, merge_history, save_history


def _curve(date: str, value: float) -> YieldCurve:
    return YieldCurve(
        as_of=date,
        source="test",
        points=[
            YieldPoint(maturity_years=2, yield_pct=value, label="2Y"),
            YieldPoint(maturity_years=10, yield_pct=value + 0.5, label="10Y"),
        ],
    )


def test_history_merge_deduplicates_and_sorts() -> None:
    older = _curve("2026-08-27", 4.2)
    newer = _curve("2026-08-28", 4.3)
    replacement = _curve("2026-08-27", 4.25)

    merged = merge_history([newer, older], [replacement])
    assert [curve.as_of for curve in merged] == ["2026-08-27", "2026-08-28"]
    assert merged[0].points[0].yield_pct == 4.25


def test_history_round_trip_and_lookup(tmp_path) -> None:
    path = tmp_path / "history.json"
    curves = [_curve("2026-08-27", 4.2), _curve("2026-08-28", 4.3)]

    save_history(curves, path)
    loaded = load_history(path)
    assert loaded == curves
    assert get_curve_by_date(loaded, "2026-08-28") == curves[1]
    assert get_curve_by_date(loaded, "2099-01-01") is None
