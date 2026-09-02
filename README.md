# YieldLab

[繁體中文](#繁體中文) · [English](#english)

---

## 繁體中文

YieldLab 是一個互動式固定收益分析、殖利率曲線研究與利率風險壓力測試工具。它可以探索美國國債殖利率曲線、期限利差、歷史曲線變化、單一債券風險，以及整個債券投資組合在不同利率情境下的損益。

後端使用 FastAPI，前端保持零框架原生瀏覽器介面。Treasury collector 讀取美國財政部官方 XML 資料，將最新曲線與歷史交易日資料原子寫入本地 JSON；Web API 只讀本地資料，因此上游暫時故障時不會把整個網站一起拖下水。

### v0.3 功能

- 美國國債票面殖利率曲線資料擷取與本地快取
- 歷史殖利率曲線持久化與日期查詢
- 任意可用期限的自訂利差計算器
- 10年－2年利差（2s10s）與 30年－5年利差（5s30s）
- 兩個交易日殖利率曲線疊圖比較
- Bull / Bear Steepener、Flattener 與近似平移自動分類
- Normal / Flat / Inverted 曲線形狀分類
- **利率情境衝擊引擎**：全曲線平移 + 任意期限節點 shock 線性插值
- 內建 Parallel ±100 bp、Bull/Bear Steepener、Bull/Bear Flattener 情境
- 原始曲線與衝擊後曲線疊圖
- **多債券投資組合壓力測試**
- 投資組合層級 DV01、加權修正存續期間、加權凸性與 P/L
- 每個部位依衝擊後殖利率重新折現全部現金流，而不是只使用 Duration 一階近似
- 債券定價、麥考利存續期間、修正存續期間、凸性、DV01
- 繁體中文 / English 即時切換
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

更新最新曲線與最近兩個月份的歷史資料：

```bash
python -m app.collectors.treasury
```

也可以指定月份數：

```bash
python -m app.collectors.treasury --months 6
```

若美國財政部網站暫時無法使用或限流，collector 會保留最後一次成功資料，不覆蓋正常快取。

### API

#### `GET /api/curve`

回傳目前殖利率曲線；可用 `?as_of=YYYY-MM-DD` 查歷史交易日。

#### `GET /api/curve/metrics`

回傳曲線利差與形狀分類，也支援 `as_of`。

#### `GET /api/curves/history`

回傳已儲存的歷史殖利率曲線。

#### `GET /api/spread?short=2&long=10`

計算指定期限的「長端 − 短端」利差。

#### `GET /api/curve/compare`

比較兩個交易日的短端、長端、利差與平均利率變化，並分類曲線移動型態。

#### `GET /api/scenarios/presets`

回傳 YieldLab 內建的標準利率情境。

#### `POST /api/scenarios/curve`

對目前或指定歷史曲線套用 shock：

```json
{
  "name": "custom",
  "parallel_bp": 0,
  "shocks": [
    {"maturity_years": 2, "shock_bp": -100},
    {"maturity_years": 10, "shock_bp": -50},
    {"maturity_years": 30, "shock_bp": -25}
  ]
}
```

節點之間會線性插值；最短與最長 anchor 之外延用最近 anchor 的 shock。

#### `POST /api/portfolio/stress`

對多個債券部位套用同一個曲線情境，逐筆重新定價並回傳：

- 衝擊前 / 後市值
- P/L 與 P/L %
- Portfolio DV01
- 加權修正存續期間
- 加權凸性
- 每個部位的 shock、殖利率變化與 P/L

#### `POST /api/bonds/analyze`

單一債券分析範例：

```json
{
  "face_value": 1000,
  "coupon_rate_pct": 4.25,
  "yield_to_maturity_pct": 4.5,
  "maturity_years": 10,
  "payments_per_year": 2
}
```

### 情境衝擊原理

如果只給幾個期限節點，例如 2Y、10Y、30Y，YieldLab 會在線性插值後把 shock 套到其他期限。`parallel_bp` 則會額外加到整條曲線。

Portfolio stress test 不使用單純的：

```text
P/L ≈ -Duration × ΔYield
```

而是把每個部位的殖利率改成 shock 後的值，重新折現所有現金流。因此大幅利率變動時，凸性效果會自然反映在結果裡。

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
│       ├── history.py
│       ├── scenarios.py
│       └── treasury.py
├── data/
│   ├── treasury_curve.json
│   └── treasury_history.json
├── static/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
├── pyproject.toml
└── README.md
```

### 開發路線

- Key-rate DV01 與期限風險分解
- Nelson-Siegel / Svensson 曲線擬合
- PCA Level / Slope / Curvature 分解
- 歷史市場事件重播
- 更完整的投資組合匯入 / 匯出

### 免責聲明

YieldLab 是研究與教育用途專案，不構成投資建議。

---

## English

YieldLab is an interactive fixed-income analytics, yield-curve research, and interest-rate stress-testing toolkit. It explores U.S. Treasury yield curves, maturity spreads, historical curve movements, single-bond risk, and portfolio P/L under custom rate scenarios.

The backend uses FastAPI while the frontend stays framework-free. A Treasury collector reads the official U.S. Department of the Treasury XML feed and atomically stores the latest curve plus historical trading-day curves in local JSON files. The web API reads local data only, so upstream outages do not block normal user requests.

### v0.3 Features

- U.S. Treasury par yield-curve ingestion with local caching
- Persistent historical yield curves with date lookup
- Arbitrary maturity spread builder
- 10Y − 2Y (2s10s) and 30Y − 5Y (5s30s) analytics
- Two-date yield-curve overlay comparison
- Automatic bull / bear steepener, flattener, and near-parallel classification
- Normal / flat / inverted curve classification
- **Interest-rate scenario engine** with parallel shifts plus linearly interpolated maturity-anchor shocks
- Built-in Parallel ±100 bp, Bull/Bear Steepener, and Bull/Bear Flattener scenarios
- Base-vs-shocked curve overlay
- **Multi-bond portfolio stress testing**
- Portfolio DV01, weighted modified duration, weighted convexity, and P/L
- Exact per-position cash-flow repricing at shocked yields instead of relying only on first-order duration approximation
- Bond pricing, Macaulay duration, modified duration, convexity, and DV01
- Instant Traditional Chinese / English switching
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

Refresh the latest curve plus the two most recent months of history:

```bash
python -m app.collectors.treasury
```

Or request a larger window:

```bash
python -m app.collectors.treasury --months 6
```

If Treasury is temporarily unavailable or rate-limiting requests, the collector keeps the last successful data instead of overwriting good cache files.

### API

#### `GET /api/curve`

Returns the current yield curve; add `?as_of=YYYY-MM-DD` for a stored historical trading day.

#### `GET /api/curve/metrics`

Returns curve spreads and shape classification, with optional `as_of`.

#### `GET /api/curves/history`

Returns stored historical curves.

#### `GET /api/spread?short=2&long=10`

Calculates a custom long-end minus short-end spread.

#### `GET /api/curve/compare`

Compares short-end, long-end, spread, and average yield changes across two trading days and classifies the movement.

#### `GET /api/scenarios/presets`

Returns YieldLab's built-in standard rate scenarios.

#### `POST /api/scenarios/curve`

Applies a custom shock to the current or a historical curve:

```json
{
  "name": "custom",
  "parallel_bp": 0,
  "shocks": [
    {"maturity_years": 2, "shock_bp": -100},
    {"maturity_years": 10, "shock_bp": -50},
    {"maturity_years": 30, "shock_bp": -25}
  ]
}
```

Shocks are linearly interpolated between anchors and clamped to the nearest anchor outside the anchor range.

#### `POST /api/portfolio/stress`

Applies one curve scenario to multiple bond positions and exactly reprices each one. The response includes:

- Market value before / after
- P/L and P/L %
- Portfolio DV01
- Weighted modified duration
- Weighted convexity
- Per-position shocks, yield changes, and P/L

#### `POST /api/bonds/analyze`

Single-bond analysis example:

```json
{
  "face_value": 1000,
  "coupon_rate_pct": 4.25,
  "yield_to_maturity_pct": 4.5,
  "maturity_years": 10,
  "payments_per_year": 2
}
```

### Scenario methodology

When only a few maturity anchors are supplied, such as 2Y, 10Y, and 30Y, YieldLab linearly interpolates the shock for maturities in between. `parallel_bp` is then added across the entire curve.

Portfolio stress testing does not rely only on:

```text
P/L ≈ -Duration × ΔYield
```

Instead, each position is fully repriced by discounting its cash flows at the shocked yield. Convexity therefore appears naturally for larger rate moves.

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
│       ├── history.py
│       ├── scenarios.py
│       └── treasury.py
├── data/
│   ├── treasury_curve.json
│   └── treasury_history.json
├── static/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
├── pyproject.toml
└── README.md
```

### Roadmap

- Key-rate DV01 and maturity-bucket risk decomposition
- Nelson-Siegel / Svensson curve fitting
- PCA level / slope / curvature decomposition
- Historical market-event replay
- Richer portfolio import / export

### Disclaimer

YieldLab is a research and educational project, not investment advice.
