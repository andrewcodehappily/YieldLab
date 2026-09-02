from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "yieldlab",
        "version": "0.4.4",
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


def test_scenario_presets_endpoint() -> None:
    response = client.get("/api/scenarios/presets")
    assert response.status_code == 200
    keys = {item["key"] for item in response.json()}
    assert "bull_steepener" in keys
    assert "parallel_up_100" in keys


def test_curve_scenario_endpoint() -> None:
    response = client.post(
        "/api/scenarios/curve",
        json={"name": "up25", "parallel_bp": 25, "shocks": []},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["scenario_name"] == "up25"
    assert payload["points"]
    assert all(point["shock_bp"] == 25 for point in payload["points"])


def test_portfolio_stress_endpoint() -> None:
    response = client.post(
        "/api/portfolio/stress",
        json={
            "scenario": {"name": "up100", "parallel_bp": 100, "shocks": []},
            "positions": [
                {
                    "name": "10Y",
                    "face_value": 100000,
                    "coupon_rate_pct": 5,
                    "yield_to_maturity_pct": 5,
                    "maturity_years": 10,
                    "payments_per_year": 2,
                }
            ],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["market_value_after"] < payload["market_value_before"]
    assert payload["pnl"] < 0
    assert payload["positions"][0]["shock_bp"] == 100


def test_curve_fit_endpoint() -> None:
    response = client.get("/api/curve/fit", params={"model": "svensson", "grid_points": 80})
    assert response.status_code == 200
    payload = response.json()
    assert payload["model"] == "svensson"
    assert payload["rmse_bp"] >= 0
    assert len(payload["points"]) >= 80


def test_forward_rate_endpoint() -> None:
    response = client.get("/api/curve/forward", params={"start": 5, "end": 10, "model": "svensson"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["start_years"] == 5
    assert payload["end_years"] == 10
    assert "approximation" in payload["methodology"]


def test_pca_endpoint() -> None:
    response = client.get("/api/factors/pca", params={"limit": 180})
    assert response.status_code == 200
    payload = response.json()
    assert payload["trading_days"] >= 4
    assert {factor["name"] for factor in payload["factors"]} == {"level", "slope", "curvature"}


def test_factor_shock_endpoint() -> None:
    response = client.post(
        "/api/factors/shock",
        params={"limit": 180},
        json={"level_sigma": 1, "slope_sigma": 0, "curvature_sigma": 0},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["scenario"]["name"] == "pca_factor_shock"
    assert payload["shock_result"]["points"]


def test_sp500_inversion_history_endpoint() -> None:
    response = client.get(
        "/api/market/sp500-inversions",
        params={"t1": 2, "t2": 10, "start_month": "2000-01", "end_month": "2010-12"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["t1_years"] == 2
    assert payload["t2_years"] == 10
    assert payload["start_date"].startswith("2000-01")
    assert payload["end_date"].startswith("2010-12")
    available = [point for point in payload["points"] if point["inverted"] is not None]
    assert available
    assert all("expected_path_difference_bp" in point for point in available)
    assert all("term_premium_threshold_bp" in point for point in available)
    assert "events" in payload
    assert "event_summary" in payload
    assert payload["event_summary"]["event_count"] == len(payload["events"])


def test_sp500_inversion_history_rejects_reversed_maturities() -> None:
    response = client.get("/api/market/sp500-inversions", params={"t1": 10, "t2": 2})
    assert response.status_code == 422


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
