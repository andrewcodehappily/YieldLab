from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


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
