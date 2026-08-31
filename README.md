# YieldLab

[繁體中文](#繁體中文) · [English](#english)

---

## 繁體中文

YieldLab 是一個互動式固定收益分析與殖利率曲線研究工具，專門用來探索美國國債殖利率曲線、期限利差與債券利率風險。

目前版本刻意保持架構簡單：後端使用 FastAPI，前端使用零框架原生瀏覽器介面。Treasury collector 會讀取美國財政部官方 XML 資料，並以原子方式更新本地 JSON 快取；Web API 只讀取快取，因此即使上游資料來源暫時故障，也不會拖慢使用者請求。

### v0.1 功能

- 美國國債票面殖利率曲線資料擷取與本地快取
- 10年－2年利差（2s10s）分析
- 30年－5年利差（5s30s）分析
- 殖利率曲線形狀分類
- 債券定價
- 麥考利存續期間
- 修正存續期間
- 凸性
- DV01
- 互動式瀏覽器債券計算器
- 前端繁體中文 / English 即時切換
- `/docs` OpenAPI 文件
- 單元測試與 API 測試

### 本機執行

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
uvicorn app.main:app --reload
```

接著開啟：

```text
http://127.0.0.1:8000
```

手動更新美國財政部殖利率曲線快取：

```bash
python -m app.collectors.treasury
```

若美國財政部網站暫時無法使用或對請求進行限流，collector 會保留最後一次成功取得的快取，不會把好資料覆蓋掉。

### API

#### `GET /api/curve`

回傳目前 YieldLab 使用的殖利率曲線資料。

#### `GET /api/curve/metrics`

回傳曲線利差與曲線形狀分類。

#### `POST /api/bonds/analyze`

範例請求：

```json
{
  "face_value": 1000,
  "coupon_rate_pct": 4.25,
  "yield_to_maturity_pct": 4.5,
  "maturity_years": 10,
  "payments_per_year": 2
}
```

### 專案架構

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

### 開發路線

- 歷史殖利率曲線資料儲存
- 自訂任意期限利差計算器
- Bull / Bear Steepener、Flattener 分類
- 利率情境衝擊引擎
- 投資組合層級 DV01 與損益分析
- Nelson-Siegel / Svensson 曲線擬合
- PCA Level / Slope / Curvature 分解
- 歷史市場事件重播

### 免責聲明

YieldLab 是研究與教育用途專案，不構成投資建議。

---

## English

YieldLab is an interactive fixed-income analytics and yield-curve research toolkit for exploring U.S. Treasury yield curves, maturity spreads, and bond interest-rate risk.

The current version intentionally keeps the stack simple: FastAPI on the backend and a framework-free browser UI on the frontend. A separate Treasury collector reads the official U.S. Department of the Treasury XML feed and atomically refreshes a local JSON cache. The web API only reads that cache, so upstream outages do not block user requests.

### v0.1 Features

- U.S. Treasury par yield-curve ingestion with local caching
- 10Y − 2Y spread (2s10s) analytics
- 30Y − 5Y spread (5s30s) analytics
- Yield-curve shape classification
- Bond pricing
- Macaulay duration
- Modified duration
- Convexity
- DV01
- Interactive browser bond calculator
- Instant Traditional Chinese / English frontend switching
- OpenAPI docs at `/docs`
- Unit and API tests

### Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

Refresh the Treasury cache manually with:

```bash
python -m app.collectors.treasury
```

If Treasury is temporarily unavailable or rate-limiting requests, the collector keeps the last successful cache instead of overwriting good data.

### API

#### `GET /api/curve`

Returns the current YieldLab yield-curve dataset.

#### `GET /api/curve/metrics`

Returns curve spreads and curve-shape classification.

#### `POST /api/bonds/analyze`

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

### Architecture

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

### Roadmap

- Historical yield-curve storage
- Arbitrary maturity spread builder
- Bull / bear steepener and flattener classification
- Interest-rate scenario shock engine
- Portfolio-level DV01 and P/L
- Nelson-Siegel / Svensson curve fitting
- PCA level / slope / curvature decomposition
- Historical market-event replay

### Disclaimer

YieldLab is a research and educational project, not investment advice.
