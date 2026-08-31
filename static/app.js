const $ = (id) => document.getElementById(id);

function fmtBp(value) {
  if (value === null || value === undefined) return "n/a";
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(1)}`;
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

async function loadCurve() {
  const [curveRes, metricsRes] = await Promise.all([
    fetch("/api/curve"),
    fetch("/api/curve/metrics"),
  ]);
  if (!curveRes.ok || !metricsRes.ok) throw new Error("Unable to load curve data");

  const curve = await curveRes.json();
  const metrics = await metricsRes.json();

  $("twoTen").textContent = fmtBp(metrics.two_ten_spread_bp);
  $("fiveThirty").textContent = fmtBp(metrics.five_thirty_spread_bp);
  $("frontBack").textContent = fmtBp(metrics.front_back_spread_bp);
  $("shape").textContent = metrics.shape;
  $("curveSource").textContent = curve.source;
  $("asOf").textContent = `as of ${curve.as_of}`;
  renderCurve(curve);
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
    if (!response.ok) {
      const detail = Array.isArray(data.detail) ? data.detail.map((item) => item.msg).join("; ") : (data.detail || "Bond analysis failed");
      throw new Error(detail);
    }

    $("price").textContent = `$${data.price.toFixed(2)}`;
    $("macaulay").textContent = `${data.macaulay_duration.toFixed(3)} y`;
    $("modified").textContent = `${data.modified_duration.toFixed(3)} y`;
    $("convexity").textContent = data.convexity.toFixed(3);
    $("dv01").textContent = `$${data.dv01.toFixed(4)}`;
  } catch (err) {
    error.textContent = err.message;
    error.hidden = false;
  }
}

$("bondForm").addEventListener("submit", analyzeBond);
window.addEventListener("resize", () => loadCurve().catch(() => {}));

loadCurve().catch((err) => {
  $("curveChart").textContent = err.message;
});
$("bondForm").requestSubmit();
