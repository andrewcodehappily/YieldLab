# YieldLab

[繁體中文](#繁體中文) · [English](#english)

---

## 繁體中文

YieldLab 是一個互動式固定收益分析與殖利率曲線研究工具，用來探索美國國債殖利率曲線、期限利差、歷史曲線變化與債券利率風險。

後端使用 FastAPI，前端保持零框架原生瀏覽器介面。Treasury collector 讀取美國財政部官方 XML 資料，將最新曲線與歷史交易日資料以原子方式寫入本地 JSON；Web API 只讀本地資料，因此上游暫時故障時不會把整個網站一起拖下水。

### v0.2 功能

- 美國國債票面殖利率曲線資料擷取與本地快取
- 歷史殖利率曲線持久化與日期查詢
- 任意可用期限的自訂利差計算器
- 10年－2年利差（2s10s）與 30年－5年利差（5s30s）
- 兩個交易日殖利率曲線疊圖比較
- Bull / Bear Steepener、Flattener 與近似平移自動分類
- 殖利率曲線 Normal / Flat / Inverted 分類
- 債券定價
- 麥考利存續期間
- 修正存續期間
- 凸性
- DV01
- 互動式瀏覽器債券計算器
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

手動更新最新曲線與最近兩個月份的歷史資料：

```bash
python -m app.collectors.treasury
```

也可以指定要抓取幾個月份：

```bash
python -m app.collectors.treasury --months 6
```

若美國財政部網站暫時無法使用或進行限流，collector 會保留最後一次成功取得的資料，不會把正常快取覆蓋掉。

### API

#### `GET /api/curve`

回傳目前殖利率曲線。可加入：

```text
?as_of=2026-08-28
```

查詢已儲存的歷史交易日。

#### `GET /api/curve/metrics`

回傳曲線利差與曲線形狀分類，也支援 `as_of`。

#### `GET /api/curves/history`

回傳歷史殖利率曲線。可用 `limit` 控制最多回傳筆數。

#### `GET /api/spread?short=2&long=10`

計算指定期限的「長端 − 短端」利差。例如 `short=2&long=30` 即為 30Y − 2Y。

#### `GET /api/curve/compare`

範例：

```text
/api/curve/compare?from_date=2026-08-20&to_date=2026-08-28&short=2&long=10
```

回傳短端、長端、利差與平均利率變化，並分類曲線移動型態。

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

### 曲線移動分類

YieldLab 使用指定的短端與長端比較兩個交易日：

- **Bull**：平均殖利率下降
- **Bear**：平均殖利率上升
- **Steepener**：長端 − 短端利差擴大
- **Flattener**：長端 − 短端利差縮小
- **Parallel**：利差變動很小，接近整體平移

例如短端下跌 100 bp、長端下跌 50 bp，整體利率下降而利差擴大，會被分類成 **Bull Steepener**。

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

- 利率情境衝擊引擎
- 投資組合層級 DV01 與損益分析
- Nelson-Siegel / Svensson 曲線擬合
- PCA Level / Slope / Curvature 分解
- 歷史市場事件重播

### 免責聲明

YieldLab 是研究與教育用途專案，不構成投資建議。

---

## English

YieldLab is an interactive fixed-income analytics and yield-curve research toolkit for exploring U.S. Treasury yield curves, maturity spreads, historical curve movements, and bond interest-rate risk.

The backend uses FastAPI while the frontend stays framework-free. A Treasury collector reads the official U.S. Department of the Treasury XML feed and atomically stores both the latest curve and historical trading-day curves in local JSON files. The web API reads local data only, so an upstream outage does not block normal user requests.

### v0.2 Features

- U.S. Treasury par yield-curve ingestion with local caching
- Persistent historical yield curves with date lookup
- Arbitrary maturity spread builder
- 10Y − 2Y (2s10s) and 30Y − 5Y (5s30s) analytics
- Two-date yield-curve overlay comparison
- Automatic bull / bear steepener, flattener, and near-parallel classification
- Normal / flat / inverted curve classification
- Bond pricing
- Macaulay duration
- Modified duration
- Convexity
- DV01
- Interactive browser bond calculator
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

Or request a larger historical window:

```bash
python -m app.collectors.treasury --months 6
```

If Treasury is temporarily unavailable or rate-limiting requests, the collector keeps the last successful data instead of overwriting good cache files.

### API

#### `GET /api/curve`

Returns the current yield curve. Add:

```text
?as_of=2026-08-28
```

to request a stored historical trading day.

#### `GET /api/curve/metrics`

Returns curve spreads and curve-shape classification, with optional `as_of`.

#### `GET /api/curves/history`

Returns stored historical curves. Use `limit` to cap the response size.

#### `GET /api/spread?short=2&long=10`

Calculates a custom long-end minus short-end spread. For example, `short=2&long=30` returns 30Y − 2Y.

#### `GET /api/curve/compare`

Example:

```text
/api/curve/compare?from_date=2026-08-20&to_date=2026-08-28&short=2&long=10
```

Returns short-end, long-end, spread, and average yield changes and classifies the curve movement.

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

### Curve-movement classification

YieldLab compares a selected short maturity and long maturity across two trading days:

- **Bull**: average yields fell
- **Bear**: average yields rose
- **Steepener**: long-minus-short spread widened
- **Flattener**: long-minus-short spread narrowed
- **Parallel**: the spread barely moved, so the curve shifted roughly in parallel

For example, if the short end falls 100 bp while the long end falls 50 bp, yields fell overall while the spread widened, producing a **Bull Steepener**.

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

- Interest-rate scenario shock engine
- Portfolio-level DV01 and P/L
- Nelson-Siegel / Svensson curve fitting
- PCA level / slope / curvature decomposition
- Historical market-event replay

### Disclaimer

YieldLab is a research and educational project, not investment advice.
