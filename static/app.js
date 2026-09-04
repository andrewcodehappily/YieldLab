const $ = (id) => document.getElementById(id);

const TRANSLATIONS = {
  "zh-Hant": {
    eyebrow: "固定收益研究實驗室",
    lede: "探索殖利率曲線、利差與債券風險，不需要一台大得像小鋼琴的彭博終端機鍵盤。",
    apiDocs: "API 文件 ↗",
    navDashboard: "總覽",
    navCurve: "曲線",
    navBacktest: "回測",
    navRisk: "風險",
    routeDashboardEyebrow: "RESEARCH TERMINAL",
    routeDashboardTitle: "研究總覽",
    routeDashboardLede: "固定收益、殖利率曲線、事件回測與風險分析的研究工作台。",
    routeCurveEyebrow: "CURVE RESEARCH",
    routeCurveTitle: "殖利率曲線研究",
    routeCurveLede: "分析期限結構、歷史曲線、參數化擬合與利率因子。",
    routeBacktestEyebrow: "BACKTEST LAB",
    routeBacktestTitle: "歷史回測",
    routeBacktestLede: "用日頻 ACM 與 FRED 2s10s 驗證倒掛解除後的市場行為。",
    routeRiskEyebrow: "RISK ENGINE",
    routeRiskTitle: "風險與投資組合",
    routeRiskLede: "建立利率情境、重新定價債券組合並分析 DV01、Duration 與 Convexity。",
    moduleCurveEyebrow: "CURVE RESEARCH",
    moduleCurveTitle: "殖利率曲線研究",
    moduleCurveDesc: "利差、歷史曲線、NS/NSS 擬合與 PCA 因子。",
    moduleBacktestEyebrow: "EVENT STUDY",
    moduleBacktestTitle: "歷史回測",
    moduleBacktestDesc: "ACM / FRED 日頻倒掛解除與 S&P 500 事件研究。",
    moduleRiskEyebrow: "RISK ENGINE",
    moduleRiskTitle: "風險與投資組合",
    moduleRiskDesc: "情境衝擊、債券風險與投資組合重新定價。",
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
    scenarioLab: "情境實驗室",
    scenarioTitle: "扭曲整條殖利率曲線",
    scenarioHint: "平移 + 節點插值",
    presetScenario: "預設情境",
    parallelShock: "全曲線平移（bp）",
    shock2Y: "2年衝擊（bp）",
    shock10Y: "10年衝擊（bp）",
    shock30Y: "30年衝擊（bp）",
    applyScenario: "套用情境",
    baseCurve: "原始曲線",
    shockedCurve: "衝擊後曲線",
    scenarioChartAria: "利率情境衝擊曲線圖",
    scenarioMovement: "曲線動態",
    baseTwoTen: "原始 2s10s",
    shockedTwoTen: "衝擊後 2s10s",
    twoTenChange: "2s10s 變化",
    customScenario: "自訂情境",
    presetParallelUp100: "全曲線 +100 bp",
    presetParallelDown100: "全曲線 −100 bp",
    presetBullSteepener: "牛市陡峭化",
    presetBullFlattener: "牛市平坦化",
    presetBearSteepener: "熊市陡峭化",
    presetBearFlattener: "熊市平坦化",
    scenarioGenericError: "利率情境暫時無法計算。",
    portfolioLab: "投資組合實驗室",
    portfolioStressTitle: "把整個債券組合丟進壓力測試",
    exactRepricing: "逐筆現金流重新定價",
    addPosition: "＋ 新增部位",
    runStressTest: "執行壓力測試",
    positionName: "名稱",
    marketValueBefore: "衝擊前市值",
    marketValueAfter: "衝擊後市值",
    portfolioPnl: "損益",
    portfolioDv01: "組合 DV01",
    portfolioDuration: "加權修正存續期間",
    portfolioConvexity: "加權凸性",
    shockApplied: "衝擊",
    yieldBeforeAfter: "殖利率 前 → 後",
    remove: "移除",
    portfolioGenericError: "投資組合壓力測試失敗，請檢查部位資料。",
    modelLab: "曲線模型實驗室",
    modelTitle: "Nelson–Siegel / Svensson 曲線擬合",
    modelHint: "只在觀測期限範圍內插值",
    curveModel: "曲線模型",
    fitCurve: "重新擬合",
    queryMaturity: "查詢期限（年）",
    queryYield: "查詢擬合殖利率",
    forwardStart: "Forward 起點（年）",
    forwardEnd: "Forward 終點（年）",
    calculateForward: "計算 Forward",
    observedCurve: "Treasury 觀測點",
    fittedCurve: "擬合曲線",
    fitChartAria: "殖利率曲線模型擬合圖",
    fitRmse: "擬合 RMSE",
    fittedYield: "擬合殖利率",
    forwardRate: "近似 Forward Rate",
    modelParameters: "模型參數",
    forwardApproximation: "Forward Rate 將擬合後的 Treasury par-yield 曲線視為連續複利零息曲線，只是研究用近似，不是完整 coupon bootstrap。",
    modelGenericError: "曲線模型暫時無法計算，請檢查期限或稍後再試。",
    factorLab: "PCA 因子實驗室",
    factorTitle: "Level / Slope / Curvature",
    factorChartAria: "PCA 因子 loading 圖",
    factorShockChartAria: "PCA 因子衝擊曲線圖",
    factorWindow: (days, start, end) => `${days} 個交易日 · ${start} → ${end}`,
    factorScore: (score, sigma) => `最新 ${score} bp · ${sigma}σ`,
    levelShock: "Level 衝擊（σ）",
    slopeShock: "Slope 衝擊（σ）",
    curvatureShock: "Curvature 衝擊（σ）",
    applyFactorShock: "套用 PCA 衝擊",
    factorStressPortfolio: "用此因子衝擊壓力測試組合",
    factorShockedCurve: "PCA 衝擊後曲線",
    factorGenericError: "PCA 因子分析暫時無法完成。",
    marketHistoryLab: "市場歷史實驗室",
    marketHistoryTitle: "S&P 500 與倒掛條件",
    marketFormulaAria: "ACM 倒掛條件：長期限預期平均短率減短期限預期平均短率，小於短期限期限溢酬減長期限期限溢酬",
    fredFormulaHint: "10年期殖利率 − 2年期殖利率為負",
    marketFrequency: "資料頻率",
    frequencyDaily: "日頻",
    frequencyMonthly: "月頻",
    marketDefinition: "倒掛定義",
    definitionAcm: "ACM 分解",
    definitionFred: "FRED 10Y−2Y",
    marketT1: "短端 T₁",
    marketT2: "長端 T₂",
    marketStartDate: "起始日期",
    marketEndDate: "結束日期",
    marketApply: "更新圖表",
    marketZoomAll: "全部",
    marketZoom10Y: "10年",
    marketZoom5Y: "5年",
    marketZoom2Y: "2年",
    marketZoom1Y: "1年",
    zoomForMarkers: "縮到 15 年內才顯示 +6 個月線",
    previousEvent: "← 上一個事件",
    nextEvent: "下一個事件 →",
    nonInverted: "未倒掛",
    invertedPeriod: "倒掛",
    unavailableData: "無利率資料",
    sixMonthsLater: "+6 個月",
    expectedPathDifference: "預期短率平均差",
    termPremiumThreshold: "期限溢酬門檻",
    acmFittedSpread: "ACM 擬合殖利率差",
    fredSpread: "FRED 10Y−2Y",
    marketCurrentState: "最新狀態",
    marketStateInverted: "倒掛",
    marketStateNormal: "未倒掛",
    marketChartAria: "S&P 500 與倒掛區間圖",
    eventStudyTitle: "倒掛結束後 6 個月事件研究",
    dailyObservationNote: "日頻 S&P 500",
    monthlyObservationNote: "月頻 S&P 500",
    eventCount: "倒掛結束事件",
    completedSamples: (done, total) => `已完成 ${done} / ${total} 個 6 個月樣本`,
    negativeSixMonthRate: "6 個月後負報酬比例",
    medianSixMonthReturn: "6 個月中位報酬",
    worstSixMonthReturn: "最差 6 個月報酬",
    worstSixMonthDrawdown: "最差 6 個月內最大回撤",
    eventEndDay: "倒掛結束日",
    eventEndMonth: "倒掛結束月",
    eventSixMonth: "+6 個月",
    eventSixMonthReturn: "6 個月報酬",
    eventMaxDrawdown: "期間最大回撤",
    eventDrawdownDay: "最深回撤日",
    eventDrawdownMonth: "最深回撤月",
    incompleteSample: "尚未滿 6 個月",
    noEvents: "這個區間沒有倒掛結束事件。",
    marketMethodologyDaily: "日頻 ACM：紅色交易日滿足 Eavg(T₂)−Eavg(T₁) < L(T₁)−L(T₂)。倒掛結束是第一個由倒掛切回未倒掛的日頻觀測；+6 個月使用六個日曆月後第一個 S&P 500 交易日。",
    marketMethodologyMonthly: "月頻 ACM：紅色月份滿足 Eavg(T₂)−Eavg(T₁) < L(T₁)−L(T₂)。倒掛結束是第一個由倒掛切回未倒掛的月份，並比較 +6 個月的 S&P 500。",
    marketMethodologyFred: "FRED 日頻 2s10s：T10Y2Y < 0 為倒掛；第一個由負值恢復到 0 或正值的日頻觀測視為倒掛結束，+6 個月使用六個日曆月後第一個 S&P 500 交易日。",
    marketSource: (sp500, rates) => `S&P 500：${sp500} · 利率資料：${rates}`,
    marketGenericError: "市場歷史資料暫時無法載入，或選擇的期限／日期區間無效。",
    footer: "YieldLab v1.0 · Fixed-Income Research Terminal",
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
    navDashboard: "Dashboard",
    navCurve: "Curve",
    navBacktest: "Backtest",
    navRisk: "Risk",
    routeDashboardEyebrow: "RESEARCH TERMINAL",
    routeDashboardTitle: "Research Dashboard",
    routeDashboardLede: "A focused workspace for fixed income, curve research, event studies, and risk analytics.",
    routeCurveEyebrow: "CURVE RESEARCH",
    routeCurveTitle: "Yield Curve Research",
    routeCurveLede: "Study term structure, historical curves, parametric fits, and rate factors.",
    routeBacktestEyebrow: "BACKTEST LAB",
    routeBacktestTitle: "Historical Backtest",
    routeBacktestLede: "Test post-inversion market behavior with daily ACM and FRED 2s10s data.",
    routeRiskEyebrow: "RISK ENGINE",
    routeRiskTitle: "Risk & Portfolio",
    routeRiskLede: "Build rate scenarios, reprice bond portfolios, and analyze DV01, duration, and convexity.",
    moduleCurveEyebrow: "CURVE RESEARCH",
    moduleCurveTitle: "Yield Curve Research",
    moduleCurveDesc: "Spreads, curve history, NS/NSS fitting, and PCA factors.",
    moduleBacktestEyebrow: "EVENT STUDY",
    moduleBacktestTitle: "Historical Backtest",
    moduleBacktestDesc: "Daily ACM / FRED inversion ends with S&P 500 event studies.",
    moduleRiskEyebrow: "RISK ENGINE",
    moduleRiskTitle: "Risk & Portfolio",
    moduleRiskDesc: "Scenario shocks, bond analytics, and full portfolio repricing.",
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
    scenarioLab: "SCENARIO LAB",
    scenarioTitle: "Twist the entire yield curve",
    scenarioHint: "Parallel shift + anchor interpolation",
    presetScenario: "Preset scenario",
    parallelShock: "Parallel shift (bp)",
    shock2Y: "2Y shock (bp)",
    shock10Y: "10Y shock (bp)",
    shock30Y: "30Y shock (bp)",
    applyScenario: "Apply scenario",
    baseCurve: "Base curve",
    shockedCurve: "Shocked curve",
    scenarioChartAria: "Interest-rate scenario shock chart",
    scenarioMovement: "Curve movement",
    baseTwoTen: "Base 2s10s",
    shockedTwoTen: "Shocked 2s10s",
    twoTenChange: "2s10s change",
    customScenario: "Custom scenario",
    presetParallelUp100: "Parallel +100 bp",
    presetParallelDown100: "Parallel −100 bp",
    presetBullSteepener: "Bull steepener",
    presetBullFlattener: "Bull flattener",
    presetBearSteepener: "Bear steepener",
    presetBearFlattener: "Bear flattener",
    scenarioGenericError: "The interest-rate scenario is temporarily unavailable.",
    portfolioLab: "PORTFOLIO LAB",
    portfolioStressTitle: "Throw the bond portfolio into a stress test",
    exactRepricing: "Exact cash-flow repricing",
    addPosition: "+ Add position",
    runStressTest: "Run stress test",
    positionName: "Name",
    marketValueBefore: "Market value before",
    marketValueAfter: "Market value after",
    portfolioPnl: "P/L",
    portfolioDv01: "Portfolio DV01",
    portfolioDuration: "Weighted modified duration",
    portfolioConvexity: "Weighted convexity",
    shockApplied: "Shock",
    yieldBeforeAfter: "Yield before → after",
    remove: "Remove",
    portfolioGenericError: "Portfolio stress test failed. Please check the position data.",
    modelLab: "CURVE MODEL LAB",
    modelTitle: "Nelson–Siegel / Svensson curve fitting",
    modelHint: "Interpolation only inside the observed maturity range",
    curveModel: "Curve model",
    fitCurve: "Refit curve",
    queryMaturity: "Query maturity (years)",
    queryYield: "Query fitted yield",
    forwardStart: "Forward start (years)",
    forwardEnd: "Forward end (years)",
    calculateForward: "Calculate forward",
    observedCurve: "Treasury observations",
    fittedCurve: "Fitted curve",
    fitChartAria: "Yield-curve model fit chart",
    fitRmse: "Fit RMSE",
    fittedYield: "Fitted yield",
    forwardRate: "Approx. forward rate",
    modelParameters: "Model parameters",
    forwardApproximation: "The forward-rate view treats the fitted Treasury par-yield curve as a continuously compounded zero curve. It is a research approximation, not a full coupon bootstrap.",
    modelGenericError: "Curve modelling is temporarily unavailable. Check the maturity inputs or try again later.",
    factorLab: "PCA FACTOR LAB",
    factorTitle: "Level / Slope / Curvature",
    factorChartAria: "PCA factor loading chart",
    factorShockChartAria: "PCA factor shock curve chart",
    factorWindow: (days, start, end) => `${days} trading days · ${start} → ${end}`,
    factorScore: (score, sigma) => `Latest ${score} bp · ${sigma}σ`,
    levelShock: "Level shock (σ)",
    slopeShock: "Slope shock (σ)",
    curvatureShock: "Curvature shock (σ)",
    applyFactorShock: "Apply PCA shock",
    factorStressPortfolio: "Stress portfolio with this factor shock",
    factorShockedCurve: "PCA-shocked curve",
    factorGenericError: "PCA factor analysis is temporarily unavailable.",
    marketHistoryLab: "MARKET HISTORY LAB",
    marketHistoryTitle: "S&P 500 and inversion regimes",
    marketFormulaAria: "ACM inversion condition: the difference in expected average short rates is below the reverse difference in term premia",
    fredFormulaHint: "10-year yield minus 2-year yield is negative",
    marketFrequency: "Data frequency",
    frequencyDaily: "Daily",
    frequencyMonthly: "Monthly",
    marketDefinition: "Inversion definition",
    definitionAcm: "ACM decomposition",
    definitionFred: "FRED 10Y−2Y",
    marketT1: "Short end T₁",
    marketT2: "Long end T₂",
    marketStartDate: "Start date",
    marketEndDate: "End date",
    marketApply: "Update chart",
    marketZoomAll: "All",
    marketZoom10Y: "10Y",
    marketZoom5Y: "5Y",
    marketZoom2Y: "2Y",
    marketZoom1Y: "1Y",
    zoomForMarkers: "Zoom to 15 years or less to show +6-month lines",
    previousEvent: "← Previous event",
    nextEvent: "Next event →",
    nonInverted: "Not inverted",
    invertedPeriod: "Inverted",
    unavailableData: "No rate data",
    sixMonthsLater: "+6 months",
    expectedPathDifference: "Expected-rate path difference",
    termPremiumThreshold: "Term-premium threshold",
    acmFittedSpread: "ACM fitted-yield spread",
    fredSpread: "FRED 10Y−2Y",
    marketCurrentState: "Latest state",
    marketStateInverted: "Inverted",
    marketStateNormal: "Not inverted",
    marketChartAria: "S&P 500 with inversion regimes",
    eventStudyTitle: "Six-month post-inversion-end event study",
    dailyObservationNote: "Daily S&P 500",
    monthlyObservationNote: "Monthly S&P 500",
    eventCount: "Inversion-end events",
    completedSamples: (done, total) => `${done} / ${total} completed six-month samples`,
    negativeSixMonthRate: "Negative six-month return rate",
    medianSixMonthReturn: "Median six-month return",
    worstSixMonthReturn: "Worst six-month return",
    worstSixMonthDrawdown: "Worst max drawdown within six months",
    eventEndDay: "Inversion end date",
    eventEndMonth: "Inversion end month",
    eventSixMonth: "+6 months",
    eventSixMonthReturn: "Six-month return",
    eventMaxDrawdown: "Max drawdown",
    eventDrawdownDay: "Deepest drawdown date",
    eventDrawdownMonth: "Deepest drawdown month",
    incompleteSample: "Not six months old yet",
    noEvents: "No inversion-end event occurs in this window.",
    marketMethodologyDaily: "Daily ACM: red trading days satisfy Eavg(T₂)−Eavg(T₁) < L(T₁)−L(T₂). The inversion ends on the first daily observation that returns from inverted to non-inverted; +6 months uses the first S&P 500 trading day on or after six calendar months later.",
    marketMethodologyMonthly: "Monthly ACM: red months satisfy Eavg(T₂)−Eavg(T₁) < L(T₁)−L(T₂). The inversion ends on the first month that returns from inverted to non-inverted and is compared with S&P 500 six months later.",
    marketMethodologyFred: "FRED daily 2s10s: T10Y2Y < 0 is inverted. The inversion ends on the first daily observation that returns to zero or positive; +6 months uses the first S&P 500 trading day on or after six calendar months later.",
    marketSource: (sp500, rates) => `S&P 500: ${sp500} · Rates: ${rates}`,
    marketGenericError: "Market history is unavailable, or the selected maturity/date range is invalid.",
    footer: "YieldLab v1.0 · Fixed-Income Research Terminal",
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
let scenarioPresets = [];
let latestScenarioResult = null;
let scenarioShockedCurve = null;
let latestPortfolioResult = null;
let latestCurveFit = null;
let latestFittedYieldQuote = null;
let latestForwardQuote = null;
let pcaAnalysis = null;
let factorShockResult = null;
let factorShockedCurve = null;
let marketHistory = null;
let marketEventCatalog = [];
let marketEventCatalogKey = "";
let marketFocusedEventIndex = -1;
let currentPage = resolvePage();

function resolvePage() {
  const path = window.location.pathname.replace(/\/+$/, "") || "/";
  if (path === "/" || path === "/dashboard") return "dashboard";
  if (path === "/curve") return "curve";
  if (path === "/backtest") return "backtest";
  if (path === "/risk") return "risk";
  return "dashboard";
}

function t(key) {
  return TRANSLATIONS[currentLanguage][key];
}

function applyRouteLayout() {
  currentPage = resolvePage();
  const routeCopy = {
    dashboard: ["routeDashboardEyebrow", "routeDashboardTitle", "routeDashboardLede", "/"],
    curve: ["routeCurveEyebrow", "routeCurveTitle", "routeCurveLede", "/curve"],
    backtest: ["routeBacktestEyebrow", "routeBacktestTitle", "routeBacktestLede", "/backtest"],
    risk: ["routeRiskEyebrow", "routeRiskTitle", "routeRiskLede", "/risk"],
  };
  const [eyebrowKey, titleKey, ledeKey, routePath] = routeCopy[currentPage];
  $("routeEyebrow").textContent = t(eyebrowKey);
  $("routeTitle").textContent = t(titleKey);
  $("routeLede").textContent = t(ledeKey);
  $("routePath").textContent = routePath;
  document.title = `YieldLab · ${t(titleKey)}`;

  document.querySelectorAll("[data-pages]").forEach((element) => {
    const pages = element.dataset.pages.split(/\s+/).filter(Boolean);
    element.hidden = !pages.includes(currentPage);
  });
  document.querySelectorAll("[data-route-link]").forEach((link) => {
    const active = link.dataset.routeLink === currentPage;
    link.classList.toggle("active", active);
    if (active) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
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

  applyRouteLayout();
  renderDynamicText();
  renderSpreadResult();
  renderHistoryState();
  populateScenarioPresetOptions();
  renderScenarioState();
  renderPortfolioResult();
  refreshPortfolioRowLabels();
  renderModelState();
  renderFactorState();
  if ($("marketFrequency")) syncMarketModeControls();
  renderMarketHistory();
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

function fmtPercent(value, digits = 2) {
  if (value === null || value === undefined || !Number.isFinite(Number(value))) return t("noData");
  const number = Number(value);
  return `${number > 0 ? "+" : ""}${number.toFixed(digits)}%`;
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

function scenarioPresetLabel(key) {
  const keys = {
    parallel_up_100: "presetParallelUp100",
    parallel_down_100: "presetParallelDown100",
    bull_steepener: "presetBullSteepener",
    bull_flattener: "presetBullFlattener",
    bear_steepener: "presetBearSteepener",
    bear_flattener: "presetBearFlattener",
  };
  return keys[key] ? t(keys[key]) : key;
}

function fmtMoney(value) {
  if (value === null || value === undefined || !Number.isFinite(Number(value))) return t("noData");
  return new Intl.NumberFormat(currentLanguage === "zh-Hant" ? "zh-TW" : "en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  }).format(Number(value));
}

function setSignedClass(element, value) {
  element.classList.toggle("positive", value > 0);
  element.classList.toggle("negative", value < 0);
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

function renderComparisonChart(fromCurve, toCurve, hostId = "compareChart") {
  const host = $(hostId);
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

function renderFitChart(result) {
  const host = $("fitChart");
  if (!host || !result) return;

  const width = Math.max(host.clientWidth || 900, 520);
  const height = 390;
  const margin = { top: 28, right: 26, bottom: 50, left: 54 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;
  const fitted = result.points;
  const observed = result.points.filter((point) => point.observed_yield_pct !== null);
  const maturities = fitted.map((point) => point.maturity_years);
  const yields = fitted.map((point) => point.fitted_yield_pct).concat(observed.map((point) => point.observed_yield_pct));
  const minMaturity = Math.min(...maturities);
  const maxMaturity = Math.max(...maturities);
  const minLog = Math.log(minMaturity);
  const maxLog = Math.log(maxMaturity);
  const yMinRaw = Math.min(...yields);
  const yMaxRaw = Math.max(...yields);
  const pad = Math.max((yMaxRaw - yMinRaw) * 0.25, 0.15);
  const yMin = Math.floor((yMinRaw - pad) * 10) / 10;
  const yMax = Math.ceil((yMaxRaw + pad) * 10) / 10;
  const x = (maturity) => margin.left + ((Math.log(maturity) - minLog) / (maxLog - minLog || 1)) * innerW;
  const y = (value) => margin.top + ((yMax - value) / (yMax - yMin || 1)) * innerH;

  const grid = Array.from({ length: 5 }, (_, i) => {
    const value = yMax - ((yMax - yMin) * i) / 4;
    const yy = y(value);
    return `<line class="grid" x1="${margin.left}" x2="${margin.left + innerW}" y1="${yy}" y2="${yy}"/><text x="8" y="${yy + 4}">${value.toFixed(2)}%</text>`;
  }).join("");

  const fitLine = fitted.map((point) => `${x(point.maturity_years)},${y(point.fitted_yield_pct)}`).join(" ");
  const labelMap = new Map((latestCurve?.points || []).map((point) => [Number(point.maturity_years.toFixed(12)), point.label]));
  const dots = observed.map((point) => `
    <circle class="fit-observed-point" cx="${x(point.maturity_years)}" cy="${y(point.observed_yield_pct)}" r="5">
      <title>${labelMap.get(Number(point.maturity_years.toFixed(12))) || point.maturity_years}: ${point.observed_yield_pct.toFixed(2)}%</title>
    </circle>`).join("");
  const labels = observed.map((point) => `<text text-anchor="middle" x="${x(point.maturity_years)}" y="${height - 14}">${labelMap.get(Number(point.maturity_years.toFixed(12))) || `${point.maturity_years.toFixed(1)}Y`}</text>`).join("");

  host.innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-hidden="true">
      ${grid}
      <polyline class="model-fit-line" points="${fitLine}"/>
      ${dots}
      ${labels}
    </svg>`;
}

function renderModelState() {
  if (latestCurveFit) {
    $("fitRmse").textContent = `${latestCurveFit.rmse_bp.toFixed(2)} bp`;
    $("modelParameters").textContent = Object.entries(latestCurveFit.parameters)
      .map(([key, value]) => `${key}=${Number(value).toFixed(4)}`)
      .join(" · ");
    renderFitChart(latestCurveFit);
  }
  if (latestFittedYieldQuote) {
    $("fittedYieldValue").textContent = `${latestFittedYieldQuote.fitted_yield_pct.toFixed(3)}%`;
    $("fittedYieldMaturity").textContent = `${latestFittedYieldQuote.maturity_years.toFixed(2)} ${t("yearSuffix")}`;
  }
  if (latestForwardQuote) {
    $("forwardRateValue").textContent = `${latestForwardQuote.forward_rate_pct.toFixed(3)}%`;
    $("forwardWindow").textContent = `${latestForwardQuote.start_years.toFixed(2)}Y → ${latestForwardQuote.end_years.toFixed(2)}Y`;
  }
}

async function loadCurveFit() {
  const error = $("modelError");
  error.hidden = true;
  try {
    const model = $("curveModel").value;
    const response = await fetch(`/api/curve/fit?model=${encodeURIComponent(model)}&grid_points=140`);
    if (!response.ok) throw new Error("fit-failed");
    latestCurveFit = await response.json();
    renderModelState();
  } catch (_) {
    error.textContent = t("modelGenericError");
    error.hidden = false;
  }
}

async function queryFittedYield() {
  const error = $("modelError");
  error.hidden = true;
  try {
    const model = $("curveModel").value;
    const maturity = Number($("fitMaturity").value);
    const response = await fetch(`/api/curve/fitted-yield?model=${encodeURIComponent(model)}&maturity=${encodeURIComponent(maturity)}`);
    if (!response.ok) throw new Error("fitted-yield-failed");
    latestFittedYieldQuote = await response.json();
    renderModelState();
  } catch (_) {
    error.textContent = t("modelGenericError");
    error.hidden = false;
  }
}

async function calculateForwardRate() {
  const error = $("modelError");
  error.hidden = true;
  try {
    const model = $("curveModel").value;
    const start = Number($("forwardStart").value);
    const end = Number($("forwardEnd").value);
    if (!(start > 0 && end > start && end <= 30)) throw new Error("forward-input");
    const response = await fetch(`/api/curve/forward?model=${encodeURIComponent(model)}&start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`);
    if (!response.ok) throw new Error("forward-failed");
    latestForwardQuote = await response.json();
    renderModelState();
  } catch (_) {
    error.textContent = t("modelGenericError");
    error.hidden = false;
  }
}

function renderFactorChart(analysis) {
  const host = $("factorChart");
  if (!host || !analysis?.loadings?.length) return;
  const width = Math.max(host.clientWidth || 900, 520);
  const height = 390;
  const margin = { top: 28, right: 26, bottom: 50, left: 54 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;
  const points = analysis.loadings;
  const minLog = Math.log(Math.min(...points.map((point) => point.maturity_years)));
  const maxLog = Math.log(Math.max(...points.map((point) => point.maturity_years)));
  const allValues = points.flatMap((point) => [point.level, point.slope, point.curvature]);
  const maxAbs = Math.max(...allValues.map((value) => Math.abs(value)), 0.1) * 1.15;
  const x = (maturity) => margin.left + ((Math.log(maturity) - minLog) / (maxLog - minLog || 1)) * innerW;
  const y = (value) => margin.top + ((maxAbs - value) / (2 * maxAbs)) * innerH;
  const zeroY = y(0);
  const line = (key) => points.map((point) => `${x(point.maturity_years)},${y(point[key])}`).join(" ");
  const labels = points.map((point) => `<text text-anchor="middle" x="${x(point.maturity_years)}" y="${height - 14}">${point.label}</text>`).join("");

  host.innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-hidden="true">
      <line class="grid factor-zero" x1="${margin.left}" x2="${margin.left + innerW}" y1="${zeroY}" y2="${zeroY}"/>
      <text x="8" y="${zeroY + 4}">0</text>
      <polyline class="factor-line factor-level" points="${line("level")}"/>
      <polyline class="factor-line factor-slope" points="${line("slope")}"/>
      <polyline class="factor-line factor-curvature" points="${line("curvature")}"/>
      ${labels}
    </svg>`;
}

function renderFactorState() {
  if (pcaAnalysis) {
    $("factorWindow").textContent = t("factorWindow")(pcaAnalysis.trading_days, pcaAnalysis.start_date, pcaAnalysis.end_date);
    const factors = Object.fromEntries(pcaAnalysis.factors.map((factor) => [factor.name, factor]));
    for (const name of ["level", "slope", "curvature"]) {
      const factor = factors[name];
      if (!factor) continue;
      $(`${name}Variance`).textContent = `${factor.explained_variance_pct.toFixed(1)}%`;
      $(`${name}Score`).textContent = t("factorScore")(factor.latest_score_bp.toFixed(2), factor.latest_sigma.toFixed(2));
      $(`${name}Bar`).style.width = `${Math.min(100, factor.explained_variance_pct)}%`;
    }
    renderFactorChart(pcaAnalysis);
  }
  if (factorShockResult && latestCurve && factorShockedCurve) {
    renderComparisonChart(latestCurve, factorShockedCurve, "factorShockChart");
  }
}

async function loadPca() {
  const error = $("factorError");
  error.hidden = true;
  try {
    const response = await fetch("/api/factors/pca?limit=180");
    if (!response.ok) throw new Error("pca-failed");
    pcaAnalysis = await response.json();
    renderFactorState();
  } catch (_) {
    error.textContent = t("factorGenericError");
    error.hidden = false;
  }
}

function factorShockRequest() {
  return {
    level_sigma: Number($("levelSigma").value || 0),
    slope_sigma: Number($("slopeSigma").value || 0),
    curvature_sigma: Number($("curvatureSigma").value || 0),
  };
}

async function applyPcaFactorShock() {
  const error = $("factorError");
  error.hidden = true;
  try {
    const response = await fetch("/api/factors/shock?limit=180", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(factorShockRequest()),
    });
    if (!response.ok) throw new Error("factor-shock-failed");
    factorShockResult = await response.json();
    const shock = factorShockResult.shock_result;
    factorShockedCurve = {
      as_of: shock.as_of,
      source: factorShockResult.scenario.name,
      points: shock.points.map((point) => ({
        maturity_years: point.maturity_years,
        label: point.label,
        yield_pct: point.shocked_yield_pct,
      })),
    };
    renderFactorState();
  } catch (_) {
    error.textContent = t("factorGenericError");
    error.hidden = false;
  }
}

function populateMarketMaturityControls() {
  const t1 = $("marketT1");
  const t2 = $("marketT2");
  if (!t1 || !t2) return;
  t1.innerHTML = Array.from({ length: 9 }, (_, index) => {
    const maturity = index + 1;
    return `<option value="${maturity}">${maturity}Y</option>`;
  }).join("");
  t2.innerHTML = Array.from({ length: 9 }, (_, index) => {
    const maturity = index + 2;
    return `<option value="${maturity}">${maturity}Y</option>`;
  }).join("");
  t1.value = "2";
  t2.value = "10";
  $("marketFrequency").value = "daily";
  $("marketInversionMode").value = "acm";
  const currentDate = new Date().toISOString().slice(0, 10);
  if (!$("marketEndDate").value) $("marketEndDate").value = currentDate;
  if (!$("marketStartDate").value) $("marketStartDate").value = shiftDateMonths($("marketEndDate").value, -120);
  syncMarketModeControls();
}

function syncMarketModeControls() {
  const frequency = $("marketFrequency").value;
  const mode = $("marketInversionMode").value;
  const isFred = frequency === "daily" && mode === "fred_2s10s";
  $("marketInversionMode").disabled = frequency !== "daily";
  if (frequency !== "daily") $("marketInversionMode").value = "acm";
  $("marketT1").disabled = isFred;
  $("marketT2").disabled = isFred;
  if (isFred) {
    $("marketT1").value = "2";
    $("marketT2").value = "10";
  }
  $("marketAcmFormula").hidden = isFred;
  $("marketFredFormula").hidden = !isFred;
  $("marketExpectedCard").hidden = isFred;
  $("marketPremiumCard").hidden = isFred;
  $("marketSpreadLabel").textContent = isFred ? t("fredSpread") : t("acmFittedSpread");
  $("marketObservationNote").textContent = frequency === "daily" ? t("dailyObservationNote") : t("monthlyObservationNote");
  $("marketEventEndHeader").textContent = frequency === "daily" ? t("eventEndDay") : t("eventEndMonth");
  $("marketDrawdownDateHeader").textContent = frequency === "daily" ? t("eventDrawdownDay") : t("eventDrawdownMonth");
  $("marketMethodologyText").textContent = isFred
    ? t("marketMethodologyFred")
    : frequency === "daily"
      ? t("marketMethodologyDaily")
      : t("marketMethodologyMonthly");
}

function shiftMonth(month, delta) {
  const [year, monthNumber] = month.split("-").map(Number);
  const date = new Date(Date.UTC(year, monthNumber - 1 + delta, 1));
  return `${date.getUTCFullYear()}-${String(date.getUTCMonth() + 1).padStart(2, "0")}`;
}

function shiftDateMonths(dateText, delta) {
  const [year, month, day] = dateText.split("-").map(Number);
  const target = new Date(Date.UTC(year, month - 1 + delta, 1));
  const targetYear = target.getUTCFullYear();
  const targetMonth = target.getUTCMonth();
  const lastDay = new Date(Date.UTC(targetYear, targetMonth + 1, 0)).getUTCDate();
  const result = new Date(Date.UTC(targetYear, targetMonth, Math.min(day, lastDay)));
  return result.toISOString().slice(0, 10);
}

function marketRegime(point) {
  if (point.inverted === null || point.inverted === undefined) return "unavailable";
  return point.inverted ? "inverted" : "normal";
}

function renderMarketEventStudy() {
  if (!marketHistory) return;
  const summary = marketHistory.event_summary;
  const events = marketHistory.events || [];
  $("eventCount").textContent = String(summary.event_count);
  $("eventCompleted").textContent = t("completedSamples")(summary.completed_event_count, summary.event_count);
  $("eventNegativeRate").textContent = summary.negative_return_pct === null ? t("noData") : `${summary.negative_return_pct.toFixed(1)}%`;
  $("eventMedianReturn").textContent = fmtPercent(summary.median_return_pct);
  $("eventWorstReturn").textContent = fmtPercent(summary.worst_return_pct);
  $("eventWorstDrawdown").textContent = fmtPercent(summary.worst_max_drawdown_pct);
  setSignedClass($("eventMedianReturn"), summary.median_return_pct || 0);
  setSignedClass($("eventWorstReturn"), summary.worst_return_pct || 0);
  setSignedClass($("eventWorstDrawdown"), summary.worst_max_drawdown_pct || 0);

  const tbody = $("marketEventRows");
  if (!events.length) {
    tbody.innerHTML = `<tr><td colspan="5" class="market-event-empty">${t("noEvents")}</td></tr>`;
    return;
  }
  tbody.innerHTML = events.map((event) => {
    const eventKey = marketHistory.frequency === "daily"
      ? event.inversion_end_date
      : event.inversion_end_date.slice(0, 7);
    if (!event.completed) {
      return `<tr data-event-end="${eventKey}"><td>${event.inversion_end_date}</td><td colspan="4" class="market-event-incomplete">${t("incompleteSample")}</td></tr>`;
    }
    const returnClass = event.six_month_return_pct > 0 ? "positive" : event.six_month_return_pct < 0 ? "negative" : "";
    return `<tr data-event-end="${eventKey}">
      <td>${event.inversion_end_date}</td>
      <td>${event.six_month_date}</td>
      <td class="${returnClass}">${fmtPercent(event.six_month_return_pct)}</td>
      <td class="negative">${fmtPercent(event.max_drawdown_pct)}</td>
      <td>${event.max_drawdown_date}</td>
    </tr>`;
  }).join("");
}

function renderMarketHistory() {
  const host = $("marketChart");
  if (!host || !marketHistory?.points?.length) return;
  syncMarketModeControls();

  const points = marketHistory.points;
  const width = Math.max(host.clientWidth || 1040, 620);
  const height = 430;
  const margin = { top: 24, right: 22, bottom: 46, left: 66 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;

  const timestamps = points.map((point) => Date.parse(`${point.date}T00:00:00Z`));
  const minTime = timestamps[0];
  const maxTime = timestamps[timestamps.length - 1];
  const prices = points.map((point) => point.sp500_close);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const count = points.length;
  const spanDays = Math.max((maxTime - minTime) / 86400000, 1);
  const useLogScale = spanDays > 365.25 * 15;
  const minLog = Math.log10(minPrice);
  const maxLog = Math.log10(maxPrice);
  const linearPad = Math.max((maxPrice - minPrice) * 0.06, 1);
  const linearMin = Math.max(0, minPrice - linearPad);
  const linearMax = maxPrice + linearPad;

  const x = (timestamp) => margin.left + ((timestamp - minTime) / (maxTime - minTime || 1)) * innerW;
  const y = (price) => useLogScale
    ? margin.top + ((maxLog - Math.log10(price)) / (maxLog - minLog || 1)) * innerH
    : margin.top + ((linearMax - price) / (linearMax - linearMin || 1)) * innerH;

  const segments = [];
  let segmentStart = 0;
  let segmentStatus = marketRegime(points[0]);
  for (let index = 1; index <= points.length; index += 1) {
    const status = index < points.length ? marketRegime(points[index]) : null;
    if (status !== segmentStatus) {
      segments.push({ start: segmentStart, end: index - 1, status: segmentStatus });
      segmentStart = index;
      segmentStatus = status;
    }
  }

  const regimeRects = segments.map((segment) => {
    const startTime = timestamps[segment.start];
    const endTime = timestamps[segment.end];
    const leftTime = segment.start === 0 ? minTime : (timestamps[segment.start - 1] + startTime) / 2;
    const rightTime = segment.end === points.length - 1 ? maxTime : (endTime + timestamps[segment.end + 1]) / 2;
    const left = x(leftTime);
    const right = x(rightTime);
    return `<rect class="market-regime market-regime-${segment.status}" x="${left}" y="${margin.top}" width="${Math.max(right - left, 0.5)}" height="${innerH}"/>`;
  }).join("");

  const logCandidates = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000];
  const yTickValues = useLogScale
    ? logCandidates.filter((value) => value >= minPrice * 0.9 && value <= maxPrice * 1.1)
    : Array.from({ length: 5 }, (_, index) => linearMin + ((linearMax - linearMin) * index) / 4);
  const yTicks = yTickValues.map((value) => {
    const yy = y(value);
    const label = new Intl.NumberFormat(currentLanguage === "zh-Hant" ? "zh-TW" : "en-US", {
      maximumFractionDigits: value < 100 ? 1 : 0,
    }).format(value);
    return `<line class="market-grid" x1="${margin.left}" x2="${margin.left + innerW}" y1="${yy}" y2="${yy}"/><text x="8" y="${yy + 4}">${label}</text>`;
  }).join("");
  const desiredTickCount = spanDays <= 180 ? 8 : 12;
  const tickStep = Math.max(1, Math.floor((count - 1) / Math.max(desiredTickCount - 1, 1)));
  const tickIndexes = [];
  for (let index = 0; index < count; index += tickStep) tickIndexes.push(index);
  if (tickIndexes[tickIndexes.length - 1] !== count - 1) tickIndexes.push(count - 1);
  const xTicks = tickIndexes.map((index) => {
    const point = points[index];
    const xx = x(timestamps[index]);
    const label = spanDays <= 180
      ? point.date
      : spanDays <= 365.25 * 3
        ? point.date.slice(0, 7)
        : point.date.slice(0, 4);
    return `<line class="market-year-grid" x1="${xx}" x2="${xx}" y1="${margin.top}" y2="${margin.top + innerH}"/><text text-anchor="middle" x="${xx}" y="${height - 14}">${label}</text>`;
  }).join("");

  const showEventMarkers = spanDays <= 365.25 * 15;
  document.querySelectorAll(".market-event-marker-legend").forEach((element) => {
    element.hidden = !showEventMarkers;
  });
  $("marketMarkerHint").hidden = showEventMarkers;
  const eventLines = showEventMarkers ? (marketHistory.events || []).map((event) => {
    const sixTime = event.six_month_date ? Date.parse(`${event.six_month_date}T00:00:00Z`) : null;
    if (sixTime === null || sixTime < minTime || sixTime > maxTime) return "";
    const xx = x(sixTime);
    return `<line class="market-event-six" x1="${xx}" x2="${xx}" y1="${margin.top}" y2="${margin.top + innerH}"><title>${t("sixMonthsLater")}: ${event.six_month_date} · ${fmtPercent(event.six_month_return_pct)}</title></line>`;
  }).join("") : "";

  const line = points.map((point, index) => `${x(timestamps[index])},${y(point.sp500_close)}`).join(" ");
  const hoverStep = count <= 36 ? 1 : Math.max(1, Math.round(count / 80));
  const hoverPoints = points.map((point, index) => {
    if (index % hoverStep !== 0 && index !== points.length - 1) return "";
    let componentText = t("unavailableData");
    if (point.inverted !== null && point.inverted !== undefined) {
      componentText = marketHistory.mode === "fred_2s10s"
        ? `FRED 2s10s ${fmtBpUnit(point.fitted_yield_spread_bp)}`
        : `EΔ ${point.expected_path_difference_bp.toFixed(1)} bp · Lgap ${point.term_premium_threshold_bp.toFixed(1)} bp · ACM ΔY ${point.fitted_yield_spread_bp.toFixed(1)} bp`;
    }
    return `<circle class="market-hover-point" cx="${x(timestamps[index])}" cy="${y(point.sp500_close)}" r="7"><title>${point.date} · S&P 500 ${point.sp500_close.toFixed(2)} · ${componentText}</title></circle>`;
  }).join("");

  host.innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-hidden="true">
      <g class="market-regimes">${regimeRects}</g>
      ${yTicks}
      ${xTicks}
      ${eventLines}
      <polyline class="market-sp500-line" points="${line}"/>
      ${hoverPoints}
    </svg>`;

  const valid = points.filter((point) => point.inverted !== null && point.inverted !== undefined);
  const latest = valid[valid.length - 1];
  if (latest) {
    $("marketExpectedDiff").textContent = fmtBpUnit(latest.expected_path_difference_bp);
    $("marketPremiumGap").textContent = fmtBpUnit(latest.term_premium_threshold_bp);
    $("marketFittedSpread").textContent = fmtBpUnit(latest.fitted_yield_spread_bp);
    $("marketCurrentState").textContent = latest.inverted ? t("marketStateInverted") : t("marketStateNormal");
    $("marketLatestDate").textContent = latest.date;
    setSignedClass($("marketFittedSpread"), latest.fitted_yield_spread_bp);
    $("marketCurrentState").classList.toggle("negative", latest.inverted);
    $("marketCurrentState").classList.toggle("positive", !latest.inverted);
  }

  $("marketRangePill").textContent = marketHistory.frequency === "daily"
    ? `${marketHistory.start_date} → ${marketHistory.end_date}`
    : `${marketHistory.start_date.slice(0, 7)} → ${marketHistory.end_date.slice(0, 7)}`;
  $("marketSource").textContent = t("marketSource")(marketHistory.sp500_source, marketHistory.rates_source);
  renderMarketEventStudy();
}

async function ensureMarketEventCatalog(t1, t2) {
  const frequency = $("marketFrequency").value;
  const mode = frequency === "daily" ? $("marketInversionMode").value : "acm";
  const key = `${frequency}:${mode}:${t1}:${t2}`;
  if (marketEventCatalogKey === key && marketEventCatalog.length) {
    updateMarketEventNav();
    return;
  }

  try {
    let response;
    if (frequency === "daily") {
      const params = new URLSearchParams({ t1: String(t1), t2: String(t2), mode });
      response = await fetch(`/api/market/sp500-inversions/daily/events?${params}`);
    } else {
      const params = new URLSearchParams({
        t1: String(t1),
        t2: String(t2),
        start_month: "1961-06",
        end_month: new Date().toISOString().slice(0, 7),
      });
      response = await fetch(`/api/market/sp500-inversions?${params}`);
    }
    if (!response.ok) throw new Error("event-catalog-failed");
    const payload = await response.json();
    marketEventCatalog = payload.events || [];
    marketEventCatalogKey = key;
    const visibleLatest = marketHistory?.events?.at(-1)?.inversion_end_date;
    const normalizedVisible = frequency === "daily" ? visibleLatest : visibleLatest?.slice(0, 7);
    const matchedIndex = normalizedVisible
      ? marketEventCatalog.findIndex((event) => {
          const keyDate = frequency === "daily" ? event.inversion_end_date : event.inversion_end_date.slice(0, 7);
          return keyDate === normalizedVisible;
        })
      : -1;
    marketFocusedEventIndex = matchedIndex >= 0 ? matchedIndex : marketEventCatalog.length - 1;
  } catch (_) {
    marketEventCatalog = marketHistory?.events || [];
    marketEventCatalogKey = key;
    marketFocusedEventIndex = marketEventCatalog.length - 1;
  }
  updateMarketEventNav();
}

function updateMarketEventNav() {
  const prev = $("marketPrevEvent");
  const next = $("marketNextEvent");
  if (!prev || !next) return;
  const hasEvents = marketEventCatalog.length > 0;
  prev.disabled = !hasEvents || marketFocusedEventIndex <= 0;
  next.disabled = !hasEvents || marketFocusedEventIndex >= marketEventCatalog.length - 1;
}

async function focusMarketEvent(delta) {
  if (!marketEventCatalog.length) {
    await ensureMarketEventCatalog(Number($("marketT1").value), Number($("marketT2").value));
  }
  if (!marketEventCatalog.length) return;
  const baseIndex = marketFocusedEventIndex < 0 ? marketEventCatalog.length - 1 : marketFocusedEventIndex;
  const targetIndex = Math.min(Math.max(baseIndex + delta, 0), marketEventCatalog.length - 1);
  marketFocusedEventIndex = targetIndex;
  const frequency = $("marketFrequency").value;
  const endKey = frequency === "daily"
    ? marketEventCatalog[targetIndex].inversion_end_date
    : marketEventCatalog[targetIndex].inversion_end_date.slice(0, 7);
  await zoomToMarketEvent(endKey);
  updateMarketEventNav();
}

async function loadMarketHistory() {
  const error = $("marketError");
  if (!error) return;
  error.hidden = true;
  syncMarketModeControls();
  const frequency = $("marketFrequency").value;
  const mode = frequency === "daily" ? $("marketInversionMode").value : "acm";
  const t1 = Number($("marketT1").value);
  const t2 = Number($("marketT2").value);
  const startDate = $("marketStartDate").value;
  const endDate = $("marketEndDate").value;
  if (!(t1 >= 1 && t2 <= 10 && t1 < t2 && /^\d{4}-\d{2}-\d{2}$/.test(startDate) && /^\d{4}-\d{2}-\d{2}$/.test(endDate) && startDate <= endDate)) {
    error.textContent = t("marketGenericError");
    error.hidden = false;
    return;
  }

  try {
    let response;
    if (frequency === "daily") {
      const params = new URLSearchParams({
        t1: String(t1),
        t2: String(t2),
        mode,
        start_date: startDate,
        end_date: endDate,
      });
      response = await fetch(`/api/market/sp500-inversions/daily?${params}`);
    } else {
      const params = new URLSearchParams({
        t1: String(t1),
        t2: String(t2),
        start_month: startDate.slice(0, 7),
        end_month: endDate.slice(0, 7),
      });
      response = await fetch(`/api/market/sp500-inversions?${params}`);
    }
    if (!response.ok) throw new Error("market-history-failed");
    marketHistory = await response.json();
    await ensureMarketEventCatalog(t1, t2);
    renderMarketHistory();
  } catch (_) {
    error.textContent = t("marketGenericError");
    error.hidden = false;
  }
}

async function setMarketWindow(months) {
  const currentDate = new Date().toISOString().slice(0, 10);
  const end = $("marketEndDate").value || currentDate;
  $("marketEndDate").value = end;
  $("marketStartDate").value = months === "all"
    ? "1950-01-03"
    : shiftDateMonths(end, -Number(months));
  await loadMarketHistory();
}

async function zoomToMarketEvent(endKey) {
  const frequency = $("marketFrequency").value;
  const catalogIndex = marketEventCatalog.findIndex((event) => {
    const keyDate = frequency === "daily" ? event.inversion_end_date : event.inversion_end_date.slice(0, 7);
    return keyDate === endKey;
  });
  if (catalogIndex >= 0) marketFocusedEventIndex = catalogIndex;
  const currentDate = new Date().toISOString().slice(0, 10);
  const endDate = frequency === "daily" ? endKey : `${endKey}-01`;
  $("marketStartDate").value = shiftDateMonths(endDate, -3);
  $("marketEndDate").value = [shiftDateMonths(endDate, 9), currentDate].sort()[0];
  await loadMarketHistory();
  updateMarketEventNav();
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

function populateScenarioPresetOptions() {
  const select = $("scenarioPreset");
  if (!select) return;
  const previous = select.value || "custom";
  const options = [
    `<option value="custom">${t("customScenario")}</option>`,
    ...scenarioPresets.map((preset) => `<option value="${preset.key}">${scenarioPresetLabel(preset.key)}</option>`),
  ];
  select.innerHTML = options.join("");
  select.value = [...select.options].some((option) => option.value === previous) ? previous : "custom";
}

function interpolateScenarioShock(scenario, maturity) {
  const anchors = [...(scenario.shocks || [])].sort((a, b) => a.maturity_years - b.maturity_years);
  if (!anchors.length) return Number(scenario.parallel_bp || 0);

  let shaped = 0;
  if (maturity <= anchors[0].maturity_years) {
    shaped = anchors[0].shock_bp;
  } else if (maturity >= anchors[anchors.length - 1].maturity_years) {
    shaped = anchors[anchors.length - 1].shock_bp;
  } else {
    for (let i = 0; i < anchors.length - 1; i += 1) {
      const left = anchors[i];
      const right = anchors[i + 1];
      if (left.maturity_years <= maturity && maturity <= right.maturity_years) {
        const weight = (maturity - left.maturity_years) / (right.maturity_years - left.maturity_years);
        shaped = left.shock_bp + weight * (right.shock_bp - left.shock_bp);
        break;
      }
    }
  }
  return Number(scenario.parallel_bp || 0) + Number(shaped || 0);
}

function setScenarioControlsFromPreset(key) {
  if (key === "custom") return;
  const preset = scenarioPresets.find((item) => item.key === key);
  if (!preset) return;
  const scenario = preset.scenario;
  $("parallelShock").value = Number(scenario.parallel_bp || 0);
  $("shock2Y").value = interpolateScenarioShock({ ...scenario, parallel_bp: 0 }, 2);
  $("shock10Y").value = interpolateScenarioShock({ ...scenario, parallel_bp: 0 }, 10);
  $("shock30Y").value = interpolateScenarioShock({ ...scenario, parallel_bp: 0 }, 30);
}

function scenarioFromControls() {
  const key = $("scenarioPreset").value;
  const preset = scenarioPresets.find((item) => item.key === key);
  if (key !== "custom" && preset) return JSON.parse(JSON.stringify(preset.scenario));

  return {
    name: "custom",
    parallel_bp: Number($("parallelShock").value || 0),
    shocks: [
      { maturity_years: 2, shock_bp: Number($("shock2Y").value || 0) },
      { maturity_years: 10, shock_bp: Number($("shock10Y").value || 0) },
      { maturity_years: 30, shock_bp: Number($("shock30Y").value || 0) },
    ],
  };
}

async function loadScenarioPresets() {
  const response = await fetch("/api/scenarios/presets");
  if (!response.ok) throw new Error("scenario-presets-failed");
  scenarioPresets = await response.json();
  populateScenarioPresetOptions();
}

function renderScenarioState() {
  if (!latestScenarioResult || !latestCurve || !scenarioShockedCurve) return;
  renderComparisonChart(latestCurve, scenarioShockedCurve, "scenarioChart");
  $("scenarioMovement").textContent = latestScenarioResult.movement
    ? translateMovement(latestScenarioResult.movement)
    : t("noData");
  $("scenarioBaseSpread").textContent = fmtBpUnit(latestScenarioResult.base_two_ten_spread_bp);
  $("scenarioShockedSpread").textContent = fmtBpUnit(latestScenarioResult.shocked_two_ten_spread_bp);
  $("scenarioSpreadChange").textContent = fmtBpUnit(latestScenarioResult.two_ten_spread_change_bp);
  setSignedClass($("scenarioSpreadChange"), latestScenarioResult.two_ten_spread_change_bp || 0);
}

async function applyScenario() {
  if (!latestCurve) return;
  const error = $("scenarioError");
  error.hidden = true;
  try {
    const response = await fetch("/api/scenarios/curve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(scenarioFromControls()),
    });
    if (!response.ok) throw new Error("scenario-failed");
    latestScenarioResult = await response.json();
    scenarioShockedCurve = {
      as_of: latestScenarioResult.as_of,
      source: latestScenarioResult.scenario_name,
      points: latestScenarioResult.points.map((point) => ({
        maturity_years: point.maturity_years,
        label: point.label,
        yield_pct: point.shocked_yield_pct,
      })),
    };
    renderScenarioState();
  } catch (_) {
    error.textContent = t("scenarioGenericError");
    error.hidden = false;
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function yieldAtMaturity(maturity) {
  if (!latestCurve) return null;
  const point = latestCurve.points.find((item) => Math.abs(item.maturity_years - maturity) < 1e-9);
  return point ? point.yield_pct : null;
}

function addPortfolioRow(position = {}) {
  const tbody = $("portfolioBody");
  const row = document.createElement("tr");
  const frequency = Number(position.payments_per_year || 2);
  row.innerHTML = `
    <td><input class="position-name" type="text" value="${escapeHtml(position.name || `Bond ${tbody.children.length + 1}`)}"></td>
    <td><input class="position-face" type="number" min="0.01" step="1000" value="${Number(position.face_value || 100000)}"></td>
    <td><input class="position-coupon" type="number" min="0" step="0.01" value="${Number(position.coupon_rate_pct ?? 4.5)}"></td>
    <td><input class="position-ytm" type="number" step="0.01" value="${Number(position.yield_to_maturity_pct ?? 4.5)}"></td>
    <td><input class="position-maturity" type="number" min="0.083333" step="0.5" value="${Number(position.maturity_years || 10)}"></td>
    <td><select class="position-frequency">
      ${[1, 2, 4, 12].map((item) => `<option value="${item}" ${item === frequency ? "selected" : ""}>${item}</option>`).join("")}
    </select></td>
    <td><button type="button" class="remove-position secondary-button" data-i18n-dynamic="remove">${t("remove")}</button></td>`;
  tbody.appendChild(row);
}

function refreshPortfolioRowLabels() {
  document.querySelectorAll("[data-i18n-dynamic='remove']").forEach((button) => {
    button.textContent = t("remove");
  });
}

function seedPortfolio() {
  if ($("portfolioBody").children.length || !latestCurve) return;
  const samples = [
    { name: "2Y Treasury", maturity: 2, face: 100000 },
    { name: "10Y Treasury", maturity: 10, face: 250000 },
    { name: "30Y Treasury", maturity: 30, face: 100000 },
  ];
  samples.forEach((sample) => {
    const ytm = yieldAtMaturity(sample.maturity) ?? 4.5;
    addPortfolioRow({
      name: sample.name,
      face_value: sample.face,
      coupon_rate_pct: ytm,
      yield_to_maturity_pct: ytm,
      maturity_years: sample.maturity,
      payments_per_year: 2,
    });
  });
}

function readPortfolioPositions() {
  return [...$("portfolioBody").querySelectorAll("tr")].map((row, index) => ({
    name: row.querySelector(".position-name").value.trim() || `Bond ${index + 1}`,
    face_value: Number(row.querySelector(".position-face").value),
    coupon_rate_pct: Number(row.querySelector(".position-coupon").value),
    yield_to_maturity_pct: Number(row.querySelector(".position-ytm").value),
    maturity_years: Number(row.querySelector(".position-maturity").value),
    payments_per_year: Number(row.querySelector(".position-frequency").value),
  }));
}

function renderPortfolioResult() {
  if (!latestPortfolioResult) return;
  $("portfolioBefore").textContent = fmtMoney(latestPortfolioResult.market_value_before);
  $("portfolioAfter").textContent = fmtMoney(latestPortfolioResult.market_value_after);
  $("portfolioPnl").textContent = fmtMoney(latestPortfolioResult.pnl);
  $("portfolioPnlPct").textContent = `${latestPortfolioResult.pnl_pct > 0 ? "+" : ""}${latestPortfolioResult.pnl_pct.toFixed(3)}%`;
  $("portfolioDv01").textContent = fmtMoney(latestPortfolioResult.dv01);
  $("portfolioDuration").textContent = `${latestPortfolioResult.weighted_modified_duration.toFixed(3)} ${t("yearSuffix")}`;
  $("portfolioConvexity").textContent = latestPortfolioResult.weighted_convexity.toFixed(3);
  setSignedClass($("portfolioPnl"), latestPortfolioResult.pnl);
  setSignedClass($("portfolioPnlPct"), latestPortfolioResult.pnl_pct);

  $("portfolioResults").innerHTML = latestPortfolioResult.positions.map((position) => `
    <tr>
      <td>${escapeHtml(position.name)}</td>
      <td>${fmtBpUnit(position.shock_bp)}</td>
      <td>${position.base_yield_pct.toFixed(2)}% → ${position.shocked_yield_pct.toFixed(2)}%</td>
      <td>${fmtMoney(position.market_value_before)}</td>
      <td>${fmtMoney(position.market_value_after)}</td>
      <td class="${position.pnl > 0 ? "positive" : position.pnl < 0 ? "negative" : ""}">${fmtMoney(position.pnl)} (${position.pnl_pct > 0 ? "+" : ""}${position.pnl_pct.toFixed(2)}%)</td>
    </tr>`).join("");
}

async function stressPortfolio(scenario = null) {
  const error = $("portfolioError");
  error.hidden = true;
  try {
    const positions = readPortfolioPositions();
    if (!positions.length) throw new Error("empty-portfolio");
    const response = await fetch("/api/portfolio/stress", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ positions, scenario: scenario || scenarioFromControls() }),
    });
    if (!response.ok) throw new Error("portfolio-failed");
    latestPortfolioResult = await response.json();
    renderPortfolioResult();
  } catch (_) {
    error.textContent = t("portfolioGenericError");
    error.hidden = false;
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
$("marketApply").addEventListener("click", loadMarketHistory);
$("marketFrequency").addEventListener("change", async () => {
  syncMarketModeControls();
  marketEventCatalog = [];
  marketEventCatalogKey = "";
  await loadMarketHistory();
});
$("marketInversionMode").addEventListener("change", async () => {
  syncMarketModeControls();
  marketEventCatalog = [];
  marketEventCatalogKey = "";
  await loadMarketHistory();
});
$("marketPrevEvent").addEventListener("click", () => focusMarketEvent(-1));
$("marketNextEvent").addEventListener("click", () => focusMarketEvent(1));
document.querySelectorAll("[data-market-window]").forEach((button) => {
  button.addEventListener("click", () => setMarketWindow(button.dataset.marketWindow));
});
$("marketEventRows").addEventListener("click", (event) => {
  const row = event.target.closest("tr[data-event-end]");
  if (row) zoomToMarketEvent(row.dataset.eventEnd);
});
$("fitCurve").addEventListener("click", loadCurveFit);
$("queryFittedYield").addEventListener("click", queryFittedYield);
$("calculateForward").addEventListener("click", calculateForwardRate);
$("curveModel").addEventListener("change", async () => {
  latestFittedYieldQuote = null;
  latestForwardQuote = null;
  await loadCurveFit();
  await queryFittedYield();
  await calculateForwardRate();
});
$("applyFactorShock").addEventListener("click", applyPcaFactorShock);
$("factorStressPortfolio").addEventListener("click", async () => {
  if (!factorShockResult) await applyPcaFactorShock();
  if (factorShockResult) await stressPortfolio(factorShockResult.scenario);
});
$("applyScenario").addEventListener("click", async () => {
  await applyScenario();
  if (latestPortfolioResult) await stressPortfolio();
});
$("stressPortfolio").addEventListener("click", () => stressPortfolio());
$("addPosition").addEventListener("click", () => addPortfolioRow());
$("portfolioBody").addEventListener("click", (event) => {
  const button = event.target.closest(".remove-position");
  if (!button) return;
  button.closest("tr").remove();
});
$("scenarioPreset").addEventListener("change", async (event) => {
  setScenarioControlsFromPreset(event.target.value);
  await applyScenario();
  if (latestPortfolioResult) await stressPortfolio();
});
["parallelShock", "shock2Y", "shock10Y", "shock30Y"].forEach((id) => {
  $(id).addEventListener("input", () => {
    $("scenarioPreset").value = "custom";
  });
});
$("bondForm").addEventListener("submit", analyzeBond);

window.addEventListener("resize", () => {
  if ((currentPage === "dashboard" || currentPage === "curve") && latestCurve) renderCurve(latestCurve);
  if (currentPage === "curve" && comparedFromCurve && comparedToCurve) renderComparisonChart(comparedFromCurve, comparedToCurve);
  if (currentPage === "curve" && latestCurveFit) renderFitChart(latestCurveFit);
  if (currentPage === "curve" && pcaAnalysis) renderFactorChart(pcaAnalysis);
  if (currentPage === "curve" && latestCurve && factorShockedCurve) renderComparisonChart(latestCurve, factorShockedCurve, "factorShockChart");
  if (currentPage === "risk" && latestCurve && scenarioShockedCurve) renderComparisonChart(latestCurve, scenarioShockedCurve, "scenarioChart");
  if (currentPage === "backtest" && marketHistory) renderMarketHistory();
});

applyLanguage(currentLanguage);

async function initialize() {
  try {
    if (currentPage === "dashboard") {
      await loadCurve();
      return;
    }

    if (currentPage === "curve") {
      await loadCurve();
      await Promise.all([loadCurveFit(), loadPca(), calculateSpread(), loadHistory()]);
      await Promise.all([queryFittedYield(), calculateForwardRate(), applyPcaFactorShock()]);
      return;
    }

    if (currentPage === "backtest") {
      populateMarketMaturityControls();
      await loadMarketHistory();
      return;
    }

    if (currentPage === "risk") {
      await loadCurve();
      seedPortfolio();
      await loadScenarioPresets();
      await applyScenario();
      await stressPortfolio();
      $("bondForm").requestSubmit();
    }
  } catch (_) {
    const visibleCurve = !$("curveChart")?.closest("[data-pages]")?.hidden;
    if (visibleCurve && !latestCurve) $("curveChart").textContent = t("curveLoadError");
  }
}

initialize();
