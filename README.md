# YieldLab

[繁體中文](#繁體中文) · [English](#english)

---

## 繁體中文

YieldLab 是一個互動式固定收益分析、殖利率曲線建模、因子研究與利率風險壓力測試工具。它可以探索美國國債殖利率曲線、期限利差、歷史曲線變化、單一債券風險，以及整個債券投資組合在不同利率情境下的損益。

後端使用 FastAPI，前端保持零框架原生瀏覽器介面。Treasury collector 讀取美國財政部官方 XML 資料，將最新曲線與歷史交易日資料原子寫入本地 JSON；Web API 只讀本地資料，因此上游暫時故障時不會把整個網站一起拖下水。

### v1.0.1

v1.0.1 修正長時間窗 X 軸重複年份標籤。多年圖現在依日曆年份產生刻度，最後一個年份若與既有刻度重疊會取代而不是追加，避免右側出現 `2026 2026` 或中間出現重複年份。

### v1.0.0

YieldLab v1.0.0 將原本的單頁研究介面重構成正式研究終端。前端仍保持零框架，但功能依用途拆成獨立 URL，且每個路由只初始化自己需要的資料與分析模組。

主要頁面：

- `/` / `/dashboard`：研究總覽與目前殖利率曲線
- `/curve`：殖利率曲線、利差、歷史比較、Nelson–Siegel / Svensson 與 PCA
- `/backtest`：日頻／月頻倒掛事件研究，支援 ACM 與 FRED `T10Y2Y`
- `/risk`：利率情境、債券分析與投資組合壓力測試
- `/docs`：OpenAPI 文件

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
- **1950～2026 S&P 500 長期圖**，使用對數縱軸
- 倒掛期間以全高紅色區帶標示，未倒掛為綠色，利率資料尚未開始的區間為灰色
- 倒掛定義改為 `Eavg(T₂) − Eavg(T₁) < L(T₁) − L(T₂)`，其中 `Eavg` 使用 ACM risk-neutral yield、`L(T)` 使用 ACM term premium
- `T₁` / `T₂` 可自由選擇 1Y～10Y 的 ACM 整數期限，並要求 `T₁ < T₂`
- 可自由選擇精確到**日期**的圖表區間；預設只開最近 10 年，`全部 / 10年 / 5年 / 2年 / 1年` 可快速切換
- 新增 **日頻 / 月頻**切換；日頻為預設，月頻長歷史仍保留
- 日頻 ACM 使用 New York Fed `ACM Daily`，1Y～10Y 期限皆可自由組合
- 新增 **FRED `T10Y2Y` 日頻交叉驗證**：`T10Y2Y < 0` 為倒掛，僅適用 2Y / 10Y
- 日頻 S&P 500 快取涵蓋 1950-01-03～2026，約 19,000 個交易日；ACM Daily 約 16,000 筆，FRED T10Y2Y 自 1976 起
- 超過 15 年的全景模式只畫 S&P 500 與紅／綠倒掛區間；15 年以下細節模式顯示 +6 個月線並切成線性 Y 軸
- 圖表同時顯示預期短率平均差、期限溢酬門檻、ACM fitted-yield spread 或 FRED 2s10s 與最新倒掛狀態
- 日頻事件研究以每次 `倒掛 → 未倒掛` 的第一個日頻觀測作為**倒掛結束日**
- `+6 個月` 使用**六個日曆月後第一個 S&P 500 交易日**，不是固定 126 個交易日
- 6 個月事件研究直接計算 S&P 500 報酬、負報酬比例、中位報酬與**日頻最大回撤**
- 事件表可逐筆檢查；點任一事件會自動縮放到倒掛結束前 3 個月至後 9 個月
- `上一個事件 / 下一個事件` 可跨完整日頻事件歷史逐次跳轉
- 2019 的 FRED 2s10s 日頻案例：倒掛結束 `2019-08-30`，+6 個日曆月落在最近交易日 `2020-03-02`
- 日頻與月頻資料分別快取於 `data/sp500_inversion_daily.json` 與 `data/sp500_inversion_history.json`
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

更新 S&P 500 與長期倒掛歷史：

```bash
python -m app.collectors.market_history
```

這個 collector 會同時更新兩份快取：

- `data/sp500_inversion_daily.json`：S&P 500 日線 + New York Fed `ACM Daily` + FRED `T10Y2Y` 日頻。S&P 日線優先使用 FRED，若上游暫時斷線則使用長期歷史資料搭配 FRED 鏡像補齊近期；T10Y2Y 也有鏡像備援。
- `data/sp500_inversion_history.json`：原本的 Multpl 月度 S&P 500 + `ACM Monthly`，保留作長期全景與備援。

### v1.0.0 API

#### `GET /api/market/sp500-inversions`

支援 `t1`、`t2`、`start_month`、`end_month`（`YYYY-MM`）；舊的 `start_year` / `end_year` 仍保留相容。例如：

```text
/api/market/sp500-inversions?t1=2&t2=10&start_month=2000-01&end_month=2010-12
```

對每個 ACM 月份回傳：

- `expected_path_difference_bp = Eavg(T₂) − Eavg(T₁)`
- `term_premium_threshold_bp = L(T₁) − L(T₂)`
- `fitted_yield_spread_bp = ACMY(T₂) − ACMY(T₁)`
- `inverted = expected_path_difference_bp < term_premium_threshold_bp`
- `events`：每次 `True → False` 的倒掛結束事件，包含 `inversion_end_date`、+6 個月 S&P 500 報酬與該 6 個月內的月度最大回撤
- `event_summary`：事件數、完成樣本數、負報酬比例、平均／中位報酬與最差報酬／回撤

因為 `ACMY(T)=ACMRNY(T)+ACMTP(T)`，這個條件與 ACM fitted-yield spread 小於 0 完全等價。1961 前保留 S&P 500，但 ACM inversion 欄位為空，前端顯示灰色。事件研究把每次原始 `True → False` 穿越視為倒掛結束事件，因此在零附近反覆穿越時仍可能出現相鄰事件，不等同於把整段 whipsaw 合併成單一景氣循環。

#### `GET /api/market/sp500-inversions/daily`

日頻事件研究。例如 ACM：

```text
/api/market/sp500-inversions/daily?t1=2&t2=10&mode=acm&start_date=2019-01-01&end_date=2020-04-01
```

或 FRED 經典 2s10s：

```text
/api/market/sp500-inversions/daily?t1=2&t2=10&mode=fred_2s10s&start_date=2019-01-01&end_date=2020-04-01
```

`mode=fred_2s10s` 固定使用 2Y / 10Y。日頻事件的 `inversion_end_date` 是精確交易日，`six_month_date` 則是六個日曆月後第一個可用 S&P 500 交易日。

#### `GET /api/market/sp500-inversions/daily/events`

只回傳日頻事件清單與摘要，不回傳數千個圖表點，供前端「上一個／下一個事件」快速導航。

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
- `GET /api/market/sp500-inversions`
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
│   │   ├── market_history.py
│   │   └── treasury.py
│   └── services/
│       ├── bonds.py
│       ├── curve.py
│       ├── factors.py
│       ├── fitting.py
│       ├── history.py
│       ├── market_history.py
│       ├── scenarios.py
│       └── treasury.py
├── data/
│   ├── sp500_inversion_history.json
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

### v1.0.1

v1.0.1 fixes duplicate year labels on long-window x-axes. Multi-year charts now derive ticks from calendar years, and a final-year tick replaces a nearby duplicate instead of being appended.

### v1.0.0

YieldLab v1.0.0 restructures the former single-page research interface into a route-based research terminal. The frontend remains framework-free, while each URL initializes only the data and analytics required for that workspace.

Primary pages:

- `/` / `/dashboard`: research overview and current yield curve
- `/curve`: yield curve, spreads, historical comparison, Nelson–Siegel / Svensson, and PCA
- `/backtest`: daily/monthly inversion event studies with ACM and FRED `T10Y2Y`
- `/risk`: rate scenarios, bond analytics, and portfolio stress testing
- `/docs`: OpenAPI documentation

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
- **1950–2026 S&P 500 long-run chart** with a logarithmic y-axis
- Full-height red inversion regimes, green non-inverted regimes, and gray pre-data periods
- Inversion condition: `Eavg(T₂) − Eavg(T₁) < L(T₁) − L(T₂)`, using ACM risk-neutral yields for `Eavg` and ACM term premia for `L(T)`
- Freely selectable integer ACM maturities from 1Y to 10Y with `T₁ < T₂`
- Freely selectable exact **date** window with `All / 10Y / 5Y / 2Y / 1Y` presets
- **Daily / monthly** frequency switch, with daily as the default
- Daily ACM uses New York Fed `ACM Daily` for freely selectable 1Y–10Y maturity pairs
- **FRED `T10Y2Y` daily cross-check** where values below zero are inverted; this mode is fixed to 2Y / 10Y
- Daily S&P 500 cache spans 1950-01-03 through 2026 with roughly 19,000 trading days; ACM Daily has roughly 16,000 observations and T10Y2Y begins in 1976
- Windows longer than 15 years show only the S&P 500 and inversion regimes; shorter windows show +6-month markers and switch to a linear y-axis
- Latest cards show the expected-rate difference, term-premium threshold, ACM fitted spread, or FRED 2s10s depending on the selected mode
- Each `inverted → not inverted` transition defines an exact daily inversion-end event
- The +6-month target is the first S&P 500 trading day on or after **six calendar months**, not a fixed trading-day count
- Previous/next-event controls can step through the daily event history
- Six-month event-study statistics include return, negative-return rate, median return, and **daily max drawdown**
- The FRED 2019 example ends on `2019-08-30`; six calendar months later maps to S&P trading day `2020-03-02`
- Daily and monthly caches are stored separately in `data/sp500_inversion_daily.json` and `data/sp500_inversion_history.json`
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

Refresh the long-run S&P 500 / inversion cache:

```bash
python -m app.collectors.market_history
```

The market-history collector refreshes two caches:

- `data/sp500_inversion_daily.json`: daily S&P 500, New York Fed `ACM Daily`, and FRED `T10Y2Y`, with fallback sources when an upstream endpoint is temporarily unavailable.
- `data/sp500_inversion_history.json`: the original Multpl monthly S&P 500 plus `ACM Monthly` long-run fallback/overview.

### v1.0.0 API

#### `GET /api/market/sp500-inversions`

Supports `t1`, `t2`, `start_month`, and `end_month` in `YYYY-MM` form; `start_year` / `end_year` remain available for compatibility. Example:

```text
/api/market/sp500-inversions?t1=2&t2=10&start_month=2000-01&end_month=2010-12
```

For each ACM month it returns the expected-rate path difference, the reverse term-premium difference, the ACM fitted-yield spread, and the resulting inversion flag. The response also includes raw `true → false` inversion-end events using `inversion_end_date`, six-month S&P 500 returns, monthly max drawdowns, and aggregate event-study statistics. Since `ACMY(T)=ACMRNY(T)+ACMTP(T)`, the requested inequality is algebraically equivalent to a negative ACM fitted-yield spread. Raw zero-crossing events are intentionally not merged, so whipsaws around zero can create neighboring events.

#### `GET /api/market/sp500-inversions/daily`

Daily ACM example:

```text
/api/market/sp500-inversions/daily?t1=2&t2=10&mode=acm&start_date=2019-01-01&end_date=2020-04-01
```

Classic FRED 2s10s example:

```text
/api/market/sp500-inversions/daily?t1=2&t2=10&mode=fred_2s10s&start_date=2019-01-01&end_date=2020-04-01
```

`fred_2s10s` requires 2Y / 10Y. Daily `inversion_end_date` values are exact observation/trading dates. The six-month target uses the first S&P 500 trading day on or after six calendar months later.

#### `GET /api/market/sp500-inversions/daily/events`

Returns only daily events and summary statistics, omitting thousands of chart points so event navigation stays light.

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
- `GET /api/market/sp500-inversions`
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
│   │   ├── market_history.py
│   │   └── treasury.py
│   └── services/
│       ├── bonds.py
│       ├── curve.py
│       ├── factors.py
│       ├── fitting.py
│       ├── history.py
│       ├── market_history.py
│       ├── scenarios.py
│       └── treasury.py
├── data/
│   ├── sp500_inversion_history.json
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
