from __future__ import annotations

from itertools import permutations

import numpy as np

from app.models import (
    CurveScenario,
    FactorShockRequest,
    FactorShockResult,
    PcaAnalysis,
    PcaFactorSummary,
    PcaLoadingPoint,
    ShockPoint,
    YieldCurve,
)
from app.services.scenarios import shock_curve


_FACTOR_NAMES = ("level", "slope", "curvature")


def _common_curve_matrix(curves: list[YieldCurve]) -> tuple[list[YieldCurve], np.ndarray, list[str], np.ndarray]:
    ordered_curves = sorted(curves, key=lambda curve: curve.as_of)
    if len(ordered_curves) < 4:
        raise ValueError("PCA requires at least four trading days")

    maturity_sets = [
        {round(point.maturity_years, 12) for point in curve.points}
        for curve in ordered_curves
    ]
    common = sorted(set.intersection(*maturity_sets))
    if len(common) < 3:
        raise ValueError("PCA requires at least three common maturities")

    labels_by_maturity = {
        round(point.maturity_years, 12): point.label
        for point in ordered_curves[-1].points
    }

    matrix_rows: list[list[float]] = []
    for curve in ordered_curves:
        values = {
            round(point.maturity_years, 12): point.yield_pct
            for point in curve.points
        }
        matrix_rows.append([values[maturity] for maturity in common])

    return (
        ordered_curves,
        np.asarray(common, dtype=float),
        [labels_by_maturity.get(maturity, f"{maturity:g}Y") for maturity in common],
        np.asarray(matrix_rows, dtype=float),
    )


def _normalized(vector: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vector))
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero PCA template")
    return vector / norm


def _factor_templates(maturities: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    log_maturity = np.log(maturities)
    x = (log_maturity - np.mean(log_maturity)) / np.std(log_maturity)
    level = np.ones_like(x)
    slope = x - np.mean(x)
    curvature = -(x**2 - np.mean(x**2))
    return _normalized(level), _normalized(slope), _normalized(curvature)


def _compute_pca(curves: list[YieldCurve]) -> dict[str, object]:
    ordered_curves, maturities, labels, yields = _common_curve_matrix(curves)

    changes_bp = np.diff(yields, axis=0) * 100
    centered = changes_bp - np.mean(changes_bp, axis=0, keepdims=True)
    if centered.shape[0] < 3:
        raise ValueError("PCA requires at least three daily curve changes")

    _, singular_values, vh = np.linalg.svd(centered, full_matrices=False)
    if len(singular_values) < 3:
        raise ValueError("PCA could not produce three factors")

    eigenvalues = (singular_values**2) / max(centered.shape[0] - 1, 1)
    total_variance = float(np.sum(eigenvalues))
    if total_variance <= 1e-15:
        raise ValueError("historical curve changes contain no variance")

    pcs = vh[:3].copy()
    templates = _factor_templates(maturities)

    best_permutation = max(
        permutations(range(3)),
        key=lambda perm: sum(abs(float(np.dot(templates[i], pcs[perm[i]]))) for i in range(3)),
    )

    factors: dict[str, dict[str, object]] = {}
    for factor_index, factor_name in enumerate(_FACTOR_NAMES):
        pc_index = best_permutation[factor_index]
        component = pcs[pc_index].copy()
        if float(np.dot(component, templates[factor_index])) < 0:
            component *= -1

        scores = centered @ component
        score_std = float(np.std(scores, ddof=1)) if len(scores) > 1 else 0.0
        latest_score = float(scores[-1])
        latest_sigma = latest_score / score_std if score_std > 1e-15 else 0.0
        explained = float(eigenvalues[pc_index] / total_variance * 100)

        factors[factor_name] = {
            "component": component,
            "scores": scores,
            "score_std_bp": score_std,
            "latest_score_bp": latest_score,
            "latest_sigma": latest_sigma,
            "explained_variance_pct": explained,
            "pc_index": pc_index,
        }

    return {
        "curves": ordered_curves,
        "maturities": maturities,
        "labels": labels,
        "changes_bp": changes_bp,
        "centered": centered,
        "factors": factors,
    }


def analyze_pca(curves: list[YieldCurve]) -> PcaAnalysis:
    result = _compute_pca(curves)
    ordered_curves = result["curves"]
    maturities = result["maturities"]
    labels = result["labels"]
    factors = result["factors"]

    summaries = [
        PcaFactorSummary(
            name=name,
            explained_variance_pct=round(float(factors[name]["explained_variance_pct"]), 6),
            latest_score_bp=round(float(factors[name]["latest_score_bp"]), 6),
            score_std_bp=round(float(factors[name]["score_std_bp"]), 6),
            latest_sigma=round(float(factors[name]["latest_sigma"]), 6),
        )
        for name in _FACTOR_NAMES
    ]

    loading_points = []
    for index, maturity in enumerate(maturities):
        loading_points.append(
            PcaLoadingPoint(
                maturity_years=round(float(maturity), 12),
                label=labels[index],
                level=round(float(factors["level"]["component"][index]), 8),
                slope=round(float(factors["slope"]["component"][index]), 8),
                curvature=round(float(factors["curvature"]["component"][index]), 8),
            )
        )

    return PcaAnalysis(
        start_date=ordered_curves[0].as_of,
        end_date=ordered_curves[-1].as_of,
        trading_days=len(ordered_curves),
        change_observations=len(ordered_curves) - 1,
        factors=summaries,
        loadings=loading_points,
    )


def build_factor_scenario(curves: list[YieldCurve], request: FactorShockRequest) -> CurveScenario:
    result = _compute_pca(curves)
    maturities = result["maturities"]
    factors = result["factors"]
    multipliers = {
        "level": request.level_sigma,
        "slope": request.slope_sigma,
        "curvature": request.curvature_sigma,
    }

    shock_vector = np.zeros(len(maturities), dtype=float)
    for factor_name in _FACTOR_NAMES:
        factor = factors[factor_name]
        shock_vector += (
            float(multipliers[factor_name])
            * float(factor["score_std_bp"])
            * factor["component"]
        )

    return CurveScenario(
        name="pca_factor_shock",
        shocks=[
            ShockPoint(
                maturity_years=round(float(maturity), 12),
                shock_bp=round(float(shock), 6),
            )
            for maturity, shock in zip(maturities, shock_vector)
        ],
    )


def factor_shock(
    history: list[YieldCurve],
    target_curve: YieldCurve,
    request: FactorShockRequest,
) -> FactorShockResult:
    scenario = build_factor_scenario(history, request)
    return FactorShockResult(
        scenario=scenario,
        shock_result=shock_curve(target_curve, scenario),
    )
