from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "yieldlab",
        "version": "0.2.0",
    }


def test_current_spread_endpoint() -> None:
    response = client.get("/api/spread", params={"short": 2, "long": 10})
    assert response.status_code == 200
    payload = response.json()
    assert payload["short_label"] == "2Y"
    assert payload["long_label"] == "10Y"
    expected = round((payload["long_yield_pct"] - payload["short_yield_pct"]) * 100, 2)
    assert payload["spread_bp"] == expected


def test_history_endpoint_contains_current_curve() -> None:
    response = client.get("/api/curves/history")
    assert response.status_code == 200
    curves = response.json()["curves"]
    assert curves
    current = client.get("/api/curve").json()
    assert curves[-1]["as_of"] == current["as_of"]


def test_bond_analysis_endpoint() -> None:
    response = client.post(
        "/api/bonds/analyze",
        json={
            "face_value": 1000,
            "coupon_rate_pct": 5,
            "yield_to_maturity_pct": 5,
            "maturity_years": 10,
            "payments_per_year": 2,
        },
    )
    assert response.status_code == 200
    assert response.json()["price"] == 1000.0
