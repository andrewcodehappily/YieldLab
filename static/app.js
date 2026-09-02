const $ = (id) => document.getElementById(id);

const TRANSLATIONS = {
  "zh-Hant": {
    eyebrow: "固定收益研究實驗室",
    lede: "探索殖利率曲線、利差與債券風險，不需要一台大得像小鋼琴的彭博終端機鍵盤。",
    apiDocs: "介面文件 ↗",
    curveMetricsAria: "殖利率曲線指標",
    twoTenLabel: "10年－2年利差（2s10s）",
    fiveThirtyLabel: "30年－5年利差（5s30s）",
    frontBackLabel: "短端 → 長端",
    curveShapeLabel: "曲線形狀",
    basisPoints: "基點",
    loading: "載入中",
    loadingEllipsis: "載入中…",
    curveExplorer: "曲線探索器",
    treasuryCurveTitle: "美國國債票面殖利率曲線",
    curveChartAria: "殖利率曲線圖",
    spreadLab: "利差實驗室",
    customSpreadTitle: "自訂任意期限利差",
    longMinusShort: "長端 − 短端",
    shortMaturity: "短端期限",
    longMaturity: "長端期限",
    calculateSpread: "計算利差",
    shortYield: "短端殖利率",
    longYield: "長端殖利率",
    spreadResult: "利差",
    spreadState: "狀態",
    positiveSpread: "正利差",
    invertedSpread: "倒掛",
    flatSpread: "幾乎平坦",
    spreadInputError: "短端期限必須小於長端期限，而且兩個期限都必須存在。",
    spreadGenericError: "利差暫時無法計算。",
    historyLab: "歷史實驗室",
    historyCompareTitle: "殖利率曲線時光機",
    fromDate: "起始日期",
    toDate: "比較日期",
    compareShort: "分類短端",
    compareLong: "分類長端",
    compareCurves: "比較曲線",
    historyNotEnough: "至少需要兩個歷史交易日才能比較曲線。執行 Treasury collector 後會自動累積。",
    compareChartAria: "歷史殖利率曲線比較圖",
    shortEndChange: "短端變化",
    longEndChange: "長端變化",
    spreadChange: "利差變化",
    movementClass: "曲線動態",
    historyGenericError: "歷史曲線比較暫時無法完成。",
    historyCount: (count) => `${count} 個交易日`,
    levelChange: (value) => `平均利率變化 ${value}`,
    bullSteepener: "牛市陡峭化",
    bullFlattener: "牛市平坦化",
    bearSteepener: "熊市陡峭化",
    bearFlattener: "熊市平坦化",
    bullParallel: "牛市近似平移",
    bearParallel: "熊市近似平移",
    neutralSteepener: "中性陡峭化",
    neutralFlattener: "中性平坦化",
    neutralParallel: "近似平移",
    bondEngine: "債券引擎",
    priceRiskCalculator: "價格與風險計算器",
    discreteCompounding: "離散複利",
    faceValue: "面額",
    couponRate: "票面利率 %",
    ytm: "到期殖利率 %",
    maturityYears: "到期年限（年）",
    paymentsPerYear: "每年付息次數",
    analyzeBond: "分析債券",
    price: "價格",
    macaulayDuration: "麥考利存續期間",
    modifiedDuration: "修正存續期間",
    convexity: "凸性",
    dv01: "每基點價格變動（DV01）",
    footer: "YieldLab v0.2 · 現在不只看今天，還能把昨天抓回來對質。",
    noData: "無資料",
    shapeNormal: "正常",
    shapeFlat: "平坦",
    shapeInverted: "倒掛",
    treasurySource: "美國財政部",
    builtInDemo: "YieldLab 內建示範資料",
    demoUnavailable: "YieldLab 示範資料（美國財政部資料來源暫時無法使用）",
    localCacheUnavailable: "YieldLab 示範資料（本地美國財政部快取暫時無法使用）",
    asOf: (date) => `資料日期 ${date}`,
    yearSuffix: "年",
    curveLoadError: "殖利率曲線資料暫時無法載入。",
    bondInputError: "債券分析失敗，請檢查輸入值是否合理。",
    bondGenericError: "債券分析暫時無法完成，請稍後再試。",
  },
  en: {
    eyebrow: "FIXED-INCOME RESEARCH LAB",
    lede: "Explore yield curves, spreads, and bond risk without needing a Bloomberg keyboard the size of a small piano.",
    apiDocs: "API Docs ↗",
    curveMetricsAria: "Yield curve metrics",
    twoTenLabel: "10Y − 2Y spread (2s10s)",
    fiveThirtyLabel: "30Y − 5Y spread (5s30s)",
    frontBackLabel: "Front end → long end",
    curveShapeLabel: "Curve shape",
    basisPoints: "basis points",
    loading: "loading",
    loadingEllipsis: "loading…",
    curveExplorer: "CURVE EXPLORER",
    treasuryCurveTitle: "U.S. Treasury par yield curve",
    curveChartAria: "Yield curve chart",
    spreadLab: "SPREAD LAB",
    customSpreadTitle: "Build any maturity spread",
    longMinusShort: "Long end − short end",
    shortMaturity: "Short maturity",
    longMaturity: "Long maturity",
    calculateSpread: "Calculate spread",
    shortYield: "Short-end yield",
    longYield: "Long-end yield",
    spreadResult: "Spread",
    spreadState: "State",
    positiveSpread: "Positive spread",
    invertedSpread: "Inverted",
    flatSpread: "Nearly flat",
    spreadInputError: "Short maturity must be below long maturity and both maturities must exist.",
    spreadGenericError: "The spread is temporarily unavailable.",
    historyLab: "HISTORY LAB",
    historyCompareTitle: "Yield-curve time machine",
    fromDate: "From date",
    toDate: "Compare date",
    compareShort: "Classification short end",
    compareLong: "Classification long end",
    compareCurves: "Compare curves",
    historyNotEnough: "At least two historical trading days are required. Running the Treasury collector will build history automatically.",
    compareChartAria: "Historical yield-curve comparison chart",
    shortEndChange: "Short-end change",
    longEndChange: "Long-end change",
    spreadChange: "Spread change",
    movementClass: "Curve movement",
    historyGenericError: "Historical curve comparison is temporarily unavailable.",
    historyCount: (count) => `${count} trading day${count === 1 ? "" : "s"}`,
    levelChange: (value) => `Average yield move ${value}`,
    bullSteepener: "Bull steepener",
    bullFlattener: "Bull flattener",
    bearSteepener: "Bear steepener",
    bearFlattener: "Bear flattener",
    bullParallel: "Bull near-parallel shift",
    bearParallel: "Bear near-parallel shift",
    neutralSteepener: "Neutral steepener",
    neutralFlattener: "Neutral flattener",
    neutralParallel: "Near-parallel shift",
    bondEngine: "BOND ENGINE",
    priceRiskCalculator: "Price & risk calculator",
    discreteCompounding: "Discrete compounding",
    faceValue: "Face value",
    couponRate: "Coupon rate %",
    ytm: "Yield to maturity %",
    maturityYears: "Maturity (years)",
    paymentsPerYear: "Payments / year",
    analyzeBond: "Analyze bond",
    price: "Price",
    macaulayDuration: "Macaulay duration",
    modifiedDuration: "Modified duration",
    convexity: "Convexity",
    dv01: "Price change per bp (DV01)",
    footer: "YieldLab v0.2 · today is no longer the only curve invited to the party.",
    noData: "n/a",
    shapeNormal: "Normal",
    shapeFlat: "Flat",
    shapeInverted: "Inverted",
    treasurySource: "U.S. Department of the Treasury",
    builtInDemo: "YieldLab built-in demo data",
    demoUnavailable: "YieldLab demo data (Treasury feed unavailable)",
    localCacheUnavailable: "YieldLab demo data (local Treasury cache unavailable)",
    asOf: (date) => `as of ${date}`,
    yearSuffix: "y",
    curveLoadError: "Yield curve data is temporarily unavailable.",
    bondInputError: "Bond analysis failed. Please check the input values.",
    bondGenericError: "Bond analysis is temporarily unavailable. Please try again later.",
  },
};

let currentLanguage = localStorage.getItem("yieldlab-language") || "zh-Hant";
let latestCurve = null;
let latestMetrics = null;
let latestBondAnalytics = null;
let latestSpread = null;
let historyCurves = [];
let latestComparison = null;
let comparedFromCurve = null;
let comparedToCurve = null;

function t(key) {
  return TRANSLATIONS[currentLanguage][key];
}

function applyLanguage(language) {
  currentLanguage = TRANSLATIONS[language] ? language : "zh-Hant";
  localStorage.setItem("yieldlab-language", currentLanguage);
  document.documentElement.lang = currentLanguage;

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const value = t(element.dataset.i18n);
    if (typeof value === "string") element.textContent = value;
  });

  document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
    const value = t(element.dataset.i18nAriaLabel);
    if (typeof value === "string") element.setAttribute("aria-label", value);
  });

  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.classList.toggle("active", button.dataset.lang === currentLanguage);
    button.setAttribute("aria-pressed", String(button.dataset.lang === currentLanguage));
  });

  renderDynamicText();
  renderSpreadResult();
  renderHistoryState();
}

function fmtBp(value) {
  if (value === null || value === undefined) return t("noData");
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(1)}`;
}

function fmtBpUnit(value) {
  if (value === null || value === undefined) return t("noData");
  const unit = currentLanguage === "zh-Hant" ? "基點" : "bp";
  return `${fmtBp(value)} ${unit}`;
}

function translateShape(shape) {
  const labels = {
    normal: t("shapeNormal"),
    flat: t("shapeFlat"),
    inverted: t("shapeInverted"),
  };
  return labels[shape] || shape;
}

function translateSource(source) {
  const keys = {
    "U.S. Department of the Treasury": "treasurySource",
    "YieldLab built-in demo data": "builtInDemo",
    "YieldLab demo data (Treasury feed unavailable)": "demoUnavailable",
    "YieldLab demo data (local Treasury cache unavailable)": "localCacheUnavailable",
  };
  return keys[source] ? t(keys[source]) : source;
}

function translateMovement(movement) {
  const keys = {
    bull_steepener: "bullSteepener",
    bull_flattener: "bullFlattener",
    bear_steepener: "bearSteepener",
    bear_flattener: "bearFlattener",
    bull_parallel: "bullParallel",
    bear_parallel: "bearParallel",
    neutral_steepener: "neutralSteepener",
    neutral_flattener: "neutralFlattener",
    neutral_parallel: "neutralParallel",
  };
  return keys[movement] ? t(keys[movement]) : movement;
}

function renderCurve(curve) {
  const host = $("curveChart");
  const width = Math.max(host.clientWidth || 900, 520);
  const height = 390;
  const margin = { top: 28, right: 26, bottom: 50, left: 54 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;

  const points = [...curve.points].sort((a, b) => a.maturity_years - b.maturity_years);
  const yields = points.map((p) => p.yield_pct);
  const yMinRaw = Math.min(...yields);
  const yMaxRaw = Math.max(...yields);
  const pad = Math.max((yMaxRaw - yMinRaw) * 0.3, 0.2);
  const yMin = Math.floor((yMinRaw - pad) * 10) / 10;
  const yMax = Math.ceil((yMaxRaw + pad) * 10) / 10;

  const x = (i) => margin.left + (i / Math.max(points.length - 1, 1)) * innerW;
  const y = (value) => margin.top + ((yMax - value) / (yMax - yMin || 1)) * innerH;
  const line = points.map((p, i) => `${x(i)},${y(p.yield_pct)}`).join(" ");
  const area = `${margin.left},${margin.top + innerH} ${line} ${margin.left + innerW},${margin.top + innerH}`;

  const grid = Array.from({ length: 5 }, (_, i) => {
    const value = yMax - ((yMax - yMin) * i) / 4;
    const yy = y(value);
    return `<line class="grid" x1="${margin.left}" x2="${margin.left + innerW}" y1="${yy}" y2="${yy}"/><text x="8" y="${yy + 4}">${value.toFixed(2)}%</text>`;
  }).join("");

  const labels = points.map((p, i) => `<text text-anchor="middle" x="${x(i)}" y="${height - 14}">${p.label}</text>`).join("");
  const dots = points.map((p, i) => `
    <circle class="point" cx="${x(i)}" cy="${y(p.yield_pct)}" r="5">
      <title>${p.label}: ${p.yield_pct.toFixed(2)}%</title>
    </circle>`).join("");

  host.innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#9ee7c8" stop-opacity="0.20"/>
          <stop offset="100%" stop-color="#9ee7c8" stop-opacity="0.01"/>
        </linearGradient>
      </defs>
      ${grid}
      <polygon class="area" points="${area}"/>
      <polyline class="curve" points="${line}"/>
      ${dots}
      ${labels}
    </svg>`;
}

function renderComparisonChart(fromCurve, toCurve) {
  const host = $("compareChart");
  if (!fromCurve || !toCurve) return;

  const width = Math.max(host.clientWidth || 900, 520);
  const height = 390;
  const margin = { top: 28, right: 26, bottom: 50, left: 54 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;

  const allPoints = [...fromCurve.points, ...toCurve.points];
  const maturityMap = new Map();
  allPoints.forEach((point) => maturityMap.set(point.maturity_years, point.label));
  const maturities = [...maturityMap.keys()].sort((a, b) => a - b);
  const yields = allPoints.map((point) => point.yield_pct);
  const yMinRaw = Math.min(...yields);
  const yMaxRaw = Math.max(...yields);
  const pad = Math.max((yMaxRaw - yMinRaw) * 0.3, 0.2);
  const yMin = Math.floor((yMinRaw - pad) * 10) / 10;
  const yMax = Math.ceil((yMaxRaw + pad) * 10) / 10;

  const x = (maturity) => margin.left + (maturities.indexOf(maturity) / Math.max(maturities.length - 1, 1)) * innerW;
  const y = (value) => margin.top + ((yMax - value) / (yMax - yMin || 1)) * innerH;

  const lineFor = (curve) => [...curve.points]
    .sort((a, b) => a.maturity_years - b.maturity_years)
    .map((point) => `${x(point.maturity_years)},${y(point.yield_pct)}`)
    .join(" ");

  const dotsFor = (curve, className) => curve.points.map((point) => `
    <circle class="compare-point ${className}" cx="${x(point.maturity_years)}" cy="${y(point.yield_pct)}" r="4">
      <title>${point.label}: ${point.yield_pct.toFixed(2)}%</title>
    </circle>`).join("");

  const grid = Array.from({ length: 5 }, (_, i) => {
    const value = yMax - ((yMax - yMin) * i) / 4;
    const yy = y(value);
    return `<line class="grid" x1="${margin.left}" x2="${margin.left + innerW}" y1="${yy}" y2="${yy}"/><text x="8" y="${yy + 4}">${value.toFixed(2)}%</text>`;
  }).join("");

  const labels = maturities.map((maturity) => `<text text-anchor="middle" x="${x(maturity)}" y="${height - 14}">${maturityMap.get(maturity)}</text>`).join("");

  host.innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-hidden="true">
      ${grid}
      <polyline class="compare-line compare-from" points="${lineFor(fromCurve)}"/>
      <polyline class="compare-line compare-to" points="${lineFor(toCurve)}"/>
      ${dotsFor(fromCurve, "compare-from-point")}
      ${dotsFor(toCurve, "compare-to-point")}
      ${labels}
    </svg>`;
}

function renderDynamicText() {
  if (latestCurve && latestMetrics) {
    $("twoTen").textContent = fmtBp(latestMetrics.two_ten_spread_bp);
    $("fiveThirty").textContent = fmtBp(latestMetrics.five_thirty_spread_bp);
    $("frontBack").textContent = fmtBp(latestMetrics.front_back_spread_bp);
    $("shape").textContent = translateShape(latestMetrics.shape);
    $("curveSource").textContent = translateSource(latestCurve.source);
    $("asOf").textContent = t("asOf")(latestCurve.as_of);
    renderCurve(latestCurve);
  }

  if (latestBondAnalytics) {
    $("price").textContent = `$${latestBondAnalytics.price.toFixed(2)}`;
    $("macaulay").textContent = `${latestBondAnalytics.macaulay_duration.toFixed(3)} ${t("yearSuffix")}`;
    $("modified").textContent = `${latestBondAnalytics.modified_duration.toFixed(3)} ${t("yearSuffix")}`;
    $("convexity").textContent = latestBondAnalytics.convexity.toFixed(3);
    $("dv01").textContent = `$${latestBondAnalytics.dv01.toFixed(4)}`;
  }
}

function renderSpreadResult() {
  if (!latestSpread) return;
  $("spreadShortYield").textContent = `${latestSpread.short_yield_pct.toFixed(2)}%`;
  $("spreadLongYield").textContent = `${latestSpread.long_yield_pct.toFixed(2)}%`;
  $("spreadValue").textContent = fmtBpUnit(latestSpread.spread_bp);
  $("spreadState").textContent = latestSpread.spread_bp < -1
    ? t("invertedSpread")
    : latestSpread.spread_bp > 1
      ? t("positiveSpread")
      : t("flatSpread");
}

function renderHistoryState() {
  $("historyCount").textContent = t("historyCount")(historyCurves.length);
  const enough = historyCurves.length >= 2;
  $("historyEmpty").hidden = enough;
  $("historyContent").hidden = !enough;

  if (!enough || !latestComparison) return;
  $("legendFrom").textContent = latestComparison.from_date;
  $("legendTo").textContent = latestComparison.to_date;
  $("comparisonShortLabel").textContent = `${latestComparison.short_label} · ${t("shortEndChange")}`;
  $("comparisonLongLabel").textContent = `${latestComparison.long_label} · ${t("longEndChange")}`;
  $("shortChange").textContent = fmtBpUnit(latestComparison.short_change_bp);
  $("longChange").textContent = fmtBpUnit(latestComparison.long_change_bp);
  $("spreadChange").textContent = fmtBpUnit(latestComparison.spread_change_bp);
  $("movement").textContent = translateMovement(latestComparison.movement);
  $("levelChange").textContent = t("levelChange")(fmtBpUnit(latestComparison.level_change_bp));
  renderComparisonChart(comparedFromCurve, comparedToCurve);
}

function populateMaturitySelect(select, points, preferred) {
  const previous = Number(select.value);
  select.innerHTML = points
    .slice()
    .sort((a, b) => a.maturity_years - b.maturity_years)
    .map((point) => `<option value="${point.maturity_years}">${point.label}</option>`)
    .join("");

  const candidate = Number.isFinite(previous) && points.some((point) => Math.abs(point.maturity_years - previous) < 1e-9)
    ? previous
    : preferred;
  if (points.some((point) => Math.abs(point.maturity_years - candidate) < 1e-9)) {
    select.value = String(candidate);
  }
}

function populateMaturityControls() {
  if (!latestCurve) return;
  populateMaturitySelect($("spreadShort"), latestCurve.points, 2);
  populateMaturitySelect($("spreadLong"), latestCurve.points, 10);
  populateMaturitySelect($("compareShort"), latestCurve.points, 2);
  populateMaturitySelect($("compareLong"), latestCurve.points, 10);
}

function populateHistoryControls() {
  const options = historyCurves.map((curve) => `<option value="${curve.as_of}">${curve.as_of}</option>`).join("");
  $("historyFrom").innerHTML = options;
  $("historyTo").innerHTML = options;

  if (historyCurves.length >= 2) {
    const toIndex = historyCurves.length - 1;
    const fromIndex = Math.max(0, toIndex - 5);
    $("historyFrom").value = historyCurves[fromIndex].as_of;
    $("historyTo").value = historyCurves[toIndex].as_of;
  }
}

async function loadCurve() {
  const [curveRes, metricsRes] = await Promise.all([
    fetch("/api/curve"),
    fetch("/api/curve/metrics"),
  ]);
  if (!curveRes.ok || !metricsRes.ok) throw new Error("curve-load-failed");

  latestCurve = await curveRes.json();
  latestMetrics = await metricsRes.json();
  populateMaturityControls();
  renderDynamicText();
}

async function calculateSpread() {
  const short = Number($("spreadShort").value);
  const long = Number($("spreadLong").value);
  const error = $("spreadError");
  error.hidden = true;

  if (!(short < long)) {
    error.textContent = t("spreadInputError");
    error.hidden = false;
    return;
  }

  try {
    const response = await fetch(`/api/spread?short=${encodeURIComponent(short)}&long=${encodeURIComponent(long)}`);
    if (!response.ok) throw new Error(response.status === 422 ? "spread-input-error" : "spread-error");
    latestSpread = await response.json();
    renderSpreadResult();
  } catch (err) {
    error.textContent = err.message === "spread-input-error" ? t("spreadInputError") : t("spreadGenericError");
    error.hidden = false;
  }
}

async function loadHistory() {
  const response = await fetch("/api/curves/history?limit=180");
  if (!response.ok) throw new Error("history-load-failed");
  const payload = await response.json();
  historyCurves = payload.curves || [];
  populateHistoryControls();
  renderHistoryState();

  if (historyCurves.length >= 2) await compareHistory();
}

async function compareHistory() {
  const fromDate = $("historyFrom").value;
  const toDate = $("historyTo").value;
  const short = Number($("compareShort").value);
  const long = Number($("compareLong").value);
  const error = $("historyError");
  error.hidden = true;

  if (!fromDate || !toDate || fromDate === toDate || !(short < long)) {
    error.textContent = t("historyGenericError");
    error.hidden = false;
    return;
  }

  try {
    const params = new URLSearchParams({
      from_date: fromDate,
      to_date: toDate,
      short: String(short),
      long: String(long),
    });
    const response = await fetch(`/api/curve/compare?${params}`);
    if (!response.ok) throw new Error("history-compare-failed");
    latestComparison = await response.json();
    comparedFromCurve = historyCurves.find((curve) => curve.as_of === fromDate) || null;
    comparedToCurve = historyCurves.find((curve) => curve.as_of === toDate) || null;
    renderHistoryState();
  } catch (_) {
    error.textContent = t("historyGenericError");
    error.hidden = false;
  }
}

async function analyzeBond(event) {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const payload = Object.fromEntries([...form.entries()].map(([key, value]) => [key, Number(value)]));
  const error = $("bondError");
  error.hidden = true;

  try {
    const response = await fetch("/api/bonds/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error("bond-input-error");
    latestBondAnalytics = data;
    renderDynamicText();
  } catch (err) {
    error.textContent = err.message === "bond-input-error" ? t("bondInputError") : t("bondGenericError");
    error.hidden = false;
  }
}

document.querySelectorAll("[data-lang]").forEach((button) => {
  button.addEventListener("click", () => applyLanguage(button.dataset.lang));
});

$("spreadCalculate").addEventListener("click", calculateSpread);
$("historyCompare").addEventListener("click", compareHistory);
$("bondForm").addEventListener("submit", analyzeBond);

window.addEventListener("resize", () => {
  if (latestCurve) renderCurve(latestCurve);
  if (comparedFromCurve && comparedToCurve) renderComparisonChart(comparedFromCurve, comparedToCurve);
});

applyLanguage(currentLanguage);

async function initialize() {
  try {
    await loadCurve();
    await calculateSpread();
    await loadHistory();
  } catch (_) {
    if (!latestCurve) $("curveChart").textContent = t("curveLoadError");
  }
}

initialize();
$("bondForm").requestSubmit();
