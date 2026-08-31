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
    footer: "YieldLab v0.1 · 讓利率風險少一點神祕，多一點可以直接點。",
    noData: "無資料",
    shapeNormal: "正常",
    shapeFlat: "平坦",
    shapeInverted: "倒掛",
    treasurySource: "美國財政部",
    builtInDemo: "YieldLab 內建示範資料",
    demoUnavailable: "YieldLab 示範資料（美國財政部資料來源暫時無法使用）",
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
    footer: "YieldLab v0.1 · making interest-rate risk less mysterious and more clickable.",
    noData: "n/a",
    shapeNormal: "Normal",
    shapeFlat: "Flat",
    shapeInverted: "Inverted",
    treasurySource: "U.S. Department of the Treasury",
    builtInDemo: "YieldLab built-in demo data",
    demoUnavailable: "YieldLab demo data (Treasury feed unavailable)",
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
}

function fmtBp(value) {
  if (value === null || value === undefined) return t("noData");
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(1)}`;
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
  };
  return keys[source] ? t(keys[source]) : source;
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

  const tickCount = 5;
  const grid = Array.from({ length: tickCount }, (_, i) => {
    const value = yMax - ((yMax - yMin) * i) / (tickCount - 1);
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

async function loadCurve() {
  const [curveRes, metricsRes] = await Promise.all([
    fetch("/api/curve"),
    fetch("/api/curve/metrics"),
  ]);
  if (!curveRes.ok || !metricsRes.ok) throw new Error("curve-load-failed");

  latestCurve = await curveRes.json();
  latestMetrics = await metricsRes.json();
  renderDynamicText();
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
    latestBondAnalytics = await response.json();
    if (!response.ok) throw new Error("bond-input-error");
    renderDynamicText();
  } catch (err) {
    error.textContent = err.message === "bond-input-error" ? t("bondInputError") : t("bondGenericError");
    error.hidden = false;
  }
}

document.querySelectorAll("[data-lang]").forEach((button) => {
  button.addEventListener("click", () => applyLanguage(button.dataset.lang));
});

$("bondForm").addEventListener("submit", analyzeBond);
window.addEventListener("resize", () => {
  if (latestCurve) renderCurve(latestCurve);
});

applyLanguage(currentLanguage);
loadCurve().catch(() => {
  $("curveChart").textContent = t("curveLoadError");
});
$("bondForm").requestSubmit();
