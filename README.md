# YieldLab

[繁體中文](#繁體中文) · [English](#english)

---

## 繁體中文

YieldLab 是一個互動式固定收益分析、殖利率曲線建模、因子研究與利率風險壓力測試工具。它可以探索美國國債殖利率曲線、期限利差、歷史曲線變化、單一債券風險，以及整個債券投資組合在不同利率情境下的損益。

後端使用 FastAPI，前端保持零框架原生瀏覽器介面。Treasury collector 讀取美國財政部官方 XML 資料，將最新曲線與歷史交易日資料原子寫入本地 JSON；Web API 只讀本地資料，因此上游暫時故障時不會把整個網站一起拖下水。

### v0.4 功能

v0.4 在 v0.3 的 scenario / portfolio risk engine 上加入真正的曲線模型與歷史因子分析：

- 美國國債票面殖利率曲線資料擷取與本地快取
- 歷史殖利率曲線持久化與日期查詢
- 任意可用期限的自訂利差計算器
- 10年－2年利差（2s10s）與 30年－5年利差（5s30s）
- 兩個交易日殖利率曲線疊圖比較
- Bull / Bear Steepener、Flattener 與近似平移自動分類
- Normal / Flat / Inverted 曲線形狀分類
- **Nelson–Siegel 曲線擬合**
- **Nelson–Siegel–Svensson 曲線擬合**
- 擬合 RMSE 與模型參數
- 1M～30Y 觀測期限範圍內的任意期限擬合殖利率查詢
- **近似 Forward Rate Lab**
- **PCA Level / Slope / Curvature 分解**
- PCA 因子 explained variance、loading、最新 factor score 與 σ
- **PCA factor shock**，可把 Level / Slope / Curvature 的 σ 衝擊轉回整條殖利率曲線
- PCA factor shock 可直接送進投資組合壓力測試
- 利率情境衝擊引擎：全曲線平移 + 任意期限節點 shock 線性插值
- 內建 Parallel ±100 bp、Bull/Bear Steepener、Bull/Bear Flattener 情境
- 多債券投資組合壓力測試
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

若使用 `uv`：

```bash
uv sync --extra dev
uv run uvicorn app.main:app --reload
```

### 更新 Treasury 資料

更新最新曲線與最近兩個月份的歷史資料：

```bash
python -m app.collectors.treasury
```

也可以指定月份數：

```bash
python -m app.collectors.treasury --months 6
```

若美國財政部網站暫時無法使用或限流，collector 會保留最後一次成功資料，不覆蓋正常快取。

### v0.4 API

#### `GET /api/curve/fit`

擬合目前或歷史曲線：

```text
/api/curve/fit?model=svensson&grid_points=140
```

支援：

```text
model=nelson_siegel
model=svensson
```

回傳模型參數、RMSE、原始觀測點與平滑擬合曲線。

#### `GET /api/curve/fitted-yield`

查詢觀測期限範圍內任意 maturity：

```text
/api/curve/fitted-yield?model=svensson&maturity=12.5
```

YieldLab 不允許超過目前 Treasury 曲線最長期限的外插，避免模型在遠端開始通靈。

#### `GET /api/curve/forward`

範例：

```text
/api/curve/forward?model=svensson&start=5&end=10
```

回傳近似 5Y5Y forward rate。

**重要：** Treasury 輸入是 par-yield curve。v0.4 的 Forward Rate Lab 為了研究與互動，將擬合後的 par-yield curve 視為連續複利 zero curve，再用：

```text
f(T1,T2) = [y(T2)T2 - y(T1)T1] / (T2 - T1)
```

計算 forward。這是研究近似，不是完整 coupon-bond bootstrap，也不應視為精確無套利 forward curve。

#### `GET /api/factors/pca`

對歷史每日殖利率變化做 PCA：

```text
/api/factors/pca?limit=180
```

YieldLab 使用所有交易日共同存在的期限建立矩陣，並將前三個主成分依 loading 與典型形狀配對為：

- Level
- Slope
- Curvature

回傳 explained variance、每日 factor score 的標準差、最新 score / sigma 與各期限 loading。

#### `POST /api/factors/shock`

例如：

```json
{
  "level_sigma": 1.0,
  "slope_sigma": -0.5,
  "curvature_sigma": 0.25
}
```

YieldLab 會利用歷史 factor score 的標準差與 PCA loading，把 σ 單位重新組合成每個期限的 basis-point shock，再套回目前曲線。

### 既有 API

- `GET /api/curve`
- `GET /api/curve/metrics`
- `GET /api/curves/history`
- `GET /api/spread`
- `GET /api/curve/compare`
- `GET /api/scenarios/presets`
- `POST /api/scenarios/curve`
- `POST /api/portfolio/stress`
- `POST /api/bonds/analyze`

### PCA 方法

YieldLab 對相鄰交易日殖利率變化（bp）做 PCA，而不是對殖利率水準直接做 PCA。前三個主成分的正負號本身沒有數學唯一性，因此程式會用典型 Level / Slope / Curvature 模板決定方向，並用最佳排列把前三個 PC 配對到這三個名稱。

這是一個研究用 factor decomposition。當歷史樣本很短時，特別是 Slope / Curvature 的 loading 與 explained variance 可能不穩定。

### 曲線擬合方法

Nelson–Siegel：

```text
y(t) = β0 + β1 L1(t,τ1) + β2 L2(t,τ1)
```

Svensson 再加入第二個 curvature term：

```text
y(t) = β0 + β1 L1(t,τ1) + β2 L2(t,τ1) + β3 L2(t,τ2)
```

v0.4 直接擬合 Treasury par yields，目標是平滑與研究曲線形狀。它不是先 bootstrap 出 zero rates 再校準模型，因此若要做精確 discounting / forward pricing，未來版本還需要完整 zero-curve bootstrap。

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
│       ├── factors.py
│       ├── fitting.py
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

- Treasury coupon-bond bootstrap 與真正的 zero / discount curve
- Key-rate DV01 與期限風險分解
- Historical Event Replay
- PCA / curve-model rolling stability diagnostics
- 更完整的投資組合匯入 / 匯出

### 免責聲明

YieldLab 是研究與教育用途專案，不構成投資建議。

---

## English

YieldLab is an interactive fixed-income analytics, yield-curve modelling, factor-research, and interest-rate stress-testing toolkit. It explores U.S. Treasury yield curves, maturity spreads, historical curve movements, single-bond risk, and portfolio P/L under custom rate scenarios.

The backend uses FastAPI while the frontend stays framework-free. A Treasury collector reads the official U.S. Department of the Treasury XML feed and atomically stores the latest curve plus historical trading-day curves in local JSON files. The web API reads local data only, so upstream outages do not block normal user requests.

### v0.4 Features

v0.4 adds quantitative curve modelling and historical factor analysis on top of the v0.3 scenario and portfolio risk engine:

- U.S. Treasury par yield-curve ingestion with local caching
- Persistent historical yield curves with date lookup
- Arbitrary maturity spread builder
- 10Y − 2Y (2s10s) and 30Y − 5Y (5s30s) analytics
- Two-date yield-curve overlay comparison
- Automatic bull / bear steepener, flattener, and near-parallel classification
- Normal / flat / inverted curve classification
- **Nelson–Siegel curve fitting**
- **Nelson–Siegel–Svensson curve fitting**
- Fit RMSE and calibrated parameters
- Arbitrary fitted-yield queries inside the observed Treasury maturity range
- **Approximate Forward Rate Lab**
- **PCA Level / Slope / Curvature decomposition**
- Explained variance, loadings, latest factor scores, and sigma values
- **PCA factor shocks** converted back into basis-point shocks across the curve
- Direct PCA-factor-to-portfolio stress testing
- Interest-rate scenario engine with parallel shifts and interpolated maturity-anchor shocks
- Built-in Parallel ±100 bp and bull/bear steepener/flattener scenarios
- Multi-bond portfolio stress testing
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

Or with `uv`:

```bash
uv sync --extra dev
uv run uvicorn app.main:app --reload
```

### Refresh Treasury data

```bash
python -m app.collectors.treasury
```

Or request a larger history window:

```bash
python -m app.collectors.treasury --months 6
```

### v0.4 API

#### `GET /api/curve/fit`

```text
/api/curve/fit?model=svensson&grid_points=140
```

Supported models:

- `nelson_siegel`
- `svensson`

The response includes calibrated parameters, RMSE, observations, and a dense fitted curve.

#### `GET /api/curve/fitted-yield`

```text
/api/curve/fitted-yield?model=svensson&maturity=12.5
```

Queries are deliberately restricted to the observed Treasury maturity range. YieldLab does not encourage long-horizon extrapolation from an unconstrained parametric fit.

#### `GET /api/curve/forward`

```text
/api/curve/forward?model=svensson&start=5&end=10
```

This returns an approximate 5Y5Y forward rate.

**Important:** Treasury inputs are par yields. The v0.4 Forward Rate Lab treats the fitted par-yield curve as a continuously compounded zero curve and calculates:

```text
f(T1,T2) = [y(T2)T2 - y(T1)T1] / (T2 - T1)
```

This is a research approximation, not a full coupon-bond bootstrap or an exact arbitrage-free forward curve.

#### `GET /api/factors/pca`

```text
/api/factors/pca?limit=180
```

YieldLab performs PCA on daily yield changes in basis points using maturities common to every selected trading day. The first three PCs are assigned to Level / Slope / Curvature using shape templates and sign orientation.

#### `POST /api/factors/shock`

```json
{
  "level_sigma": 1.0,
  "slope_sigma": -0.5,
  "curvature_sigma": 0.25
}
```

Historical factor-score volatility and PCA loadings are used to reconstruct a maturity-by-maturity basis-point shock, which is then applied to the target curve.

### Existing API

- `GET /api/curve`
- `GET /api/curve/metrics`
- `GET /api/curves/history`
- `GET /api/spread`
- `GET /api/curve/compare`
- `GET /api/scenarios/presets`
- `POST /api/scenarios/curve`
- `POST /api/portfolio/stress`
- `POST /api/bonds/analyze`

### PCA methodology

PCA is performed on day-over-day yield changes, not yield levels. PCA component signs are arbitrary, so YieldLab orients and assigns the first three PCs by matching them against canonical level, slope, and curvature templates.

With short historical samples, especially for slope and curvature, loadings and explained variance may be unstable. The factor engine is designed for research and visualization rather than production risk limits.

### Curve-fitting methodology

Nelson–Siegel:

```text
y(t) = β0 + β1 L1(t,τ1) + β2 L2(t,τ1)
```

Svensson adds a second curvature term:

```text
y(t) = β0 + β1 L1(t,τ1) + β2 L2(t,τ1) + β3 L2(t,τ2)
```

v0.4 fits the observed Treasury par yields directly for smooth curve research. It does not first bootstrap a zero-rate curve. Precise discounting and forward pricing will require a future coupon-bond bootstrap layer.

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
│       ├── factors.py
│       ├── fitting.py
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

- Treasury coupon-bond bootstrap with a true zero / discount curve
- Key-rate DV01 and maturity-bucket risk decomposition
- Historical Event Replay
- Rolling PCA / curve-model stability diagnostics
- Richer portfolio import / export

### Disclaimer

YieldLab is a research and educational project, not investment advice.
