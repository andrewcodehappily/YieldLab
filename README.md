# YieldLab

Interactive fixed-income analytics and yield-curve research lab.

YieldLab is a small, cloud-friendly toolkit for exploring Treasury yield curves, curve spreads, and bond interest-rate risk. The first version intentionally keeps the stack simple: FastAPI on the backend and a dependency-free browser UI on the frontend. A separate collector pulls the official U.S. Treasury XML feed and atomically refreshes a local JSON cache, while the web API only reads the cache so upstream outages do not block user requests.

## v0.1

- Live U.S. Treasury par yield-curve ingestion with a cached demo fallback
- 2s10s and 5s30s spread analytics
- Curve shape classification
- Bond pricing
- Macaulay duration
- Modified duration
- Convexity
- DV01
- Interactive browser calculator
- OpenAPI docs at `/docs`
- Unit and API tests

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000`.

Refresh the Treasury cache manually with:

```bash
python -m app.collectors.treasury
```

If Treasury is unavailable or rate-limiting requests, the collector leaves the last good cache untouched.

## API

### `GET /api/curve`
Returns the current YieldLab curve dataset.

### `GET /api/curve/metrics`
Returns curve spreads and shape classification.

### `POST /api/bonds/analyze`

Example request:

```json
{
  "face_value": 1000,
  "coupon_rate_pct": 4.25,
  "yield_to_maturity_pct": 4.5,
  "maturity_years": 10,
  "payments_per_year": 2
}
```

## Architecture

```text
YieldLab/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── collectors/
│   │   └── treasury.py
│   └── services/
│       ├── bonds.py
│       ├── curve.py
│       └── treasury.py
├── data/
│   └── treasury_curve.json
├── static/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
├── pyproject.toml
└── README.md
```

## Roadmap

- Historical Treasury curve storage
- Historical curve storage
- Arbitrary maturity spread builder
- Bull/bear steepener and flattener classification
- Scenario shock engine
- Portfolio-level DV01 and P/L
- Nelson-Siegel / Svensson curve fitting
- PCA level/slope/curvature decomposition
- Historical event replay

## Disclaimer

YieldLab is a research and educational project, not investment advice.
