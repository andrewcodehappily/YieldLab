from app.models import YieldCurve, YieldPoint
from app.services.treasury import (
    load_cached_curve,
    parse_treasury_xml,
    parse_treasury_xml_history,
    save_cached_curve,
)


SAMPLE_XML = b'''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"
      xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices">
  <entry>
    <content type="application/xml">
      <m:properties>
        <d:NEW_DATE>2026-08-27T00:00:00</d:NEW_DATE>
        <d:BC_2YEAR>4.30</d:BC_2YEAR>
        <d:BC_10YEAR>4.70</d:BC_10YEAR>
      </m:properties>
    </content>
  </entry>
  <entry>
    <content type="application/xml">
      <m:properties>
        <d:NEW_DATE>2026-08-28T00:00:00</d:NEW_DATE>
        <d:BC_1MONTH>3.84</d:BC_1MONTH>
        <d:BC_2YEAR>4.34</d:BC_2YEAR>
        <d:BC_10YEAR>4.73</d:BC_10YEAR>
        <d:BC_30YEAR>5.22</d:BC_30YEAR>
      </m:properties>
    </content>
  </entry>
</feed>'''


def test_parser_selects_latest_observation() -> None:
    curve = parse_treasury_xml(SAMPLE_XML)
    assert curve.as_of == "2026-08-28"
    assert curve.source == "U.S. Department of the Treasury"
    assert [point.label for point in curve.points] == ["1M", "2Y", "10Y", "30Y"]
    assert curve.points[2].yield_pct == 4.73


def test_history_parser_keeps_all_dated_observations() -> None:
    curves = parse_treasury_xml_history(SAMPLE_XML)
    assert [curve.as_of for curve in curves] == ["2026-08-27", "2026-08-28"]
    assert curves[0].points[0].label == "2Y"
    assert curves[1].points[-1].label == "30Y"


def test_cache_round_trip(tmp_path) -> None:
    path = tmp_path / "curve.json"
    expected = YieldCurve(
        as_of="2026-08-28",
        source="test",
        points=[
            YieldPoint(maturity_years=2, yield_pct=4.34, label="2Y"),
            YieldPoint(maturity_years=10, yield_pct=4.73, label="10Y"),
        ],
    )

    save_cached_curve(expected, path)
    assert load_cached_curve(path) == expected
