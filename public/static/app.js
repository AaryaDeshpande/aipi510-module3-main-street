"use strict";

(() => {
  const $ = id => document.getElementById(id);
  const state = {data: null, geo: null, industry: "2382", county: "55025", metric: "establishments", sort: "establishments", allCounties: false, predictionToken: 0};
  const STORAGE_KEY = "main-street-research-shortlist-v1";
  const finite = value => typeof value === "number" && Number.isFinite(value);
  const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const count = value => finite(value) ? new Intl.NumberFormat("en-US", {maximumFractionDigits: 0}).format(value) : "Unavailable";
  const decimal = value => finite(value) ? new Intl.NumberFormat("en-US", {maximumFractionDigits: 1}).format(value) : "Unavailable";
  const errorCount = value => finite(value) ? value.toFixed(2) : "Unavailable";
  const percent = value => finite(value) ? `${value > 0 ? "+" : ""}${value.toFixed(1)}%` : "Unavailable";
  const money = value => !finite(value) ? "Unavailable" : new Intl.NumberFormat("en-US", {style: "currency", currency: "USD", notation: "compact", maximumFractionDigits: 1}).format(value);
  const growthClass = value => finite(value) && value < 0 ? "growth-negative" : finite(value) && value > 0 ? "growth-positive" : "";
  const metricFormat = (value, metric = state.metric) => metric === "growth_pct" ? percent(value) : metric === "annual_payroll" ? money(value) : count(value);
  const industry = code => state.data.industries.find(item => String(item.code) === String(code));
  const county = fips => state.data.counties.find(item => String(item.fips) === String(fips));
  const currentRow = () => state.data.rows.find(row => String(row.county_fips) === state.county && String(row.industry) === state.industry);
  const metricLabel = metric => ({establishments: "Business locations", growth_pct: "Year-over-year growth", annual_payroll: "Annual payroll"}[metric]);
  const rowName = row => row.county_name || county(row.county_fips)?.name || row.county_fips;

  async function getJSON(url, options) {
    const response = await fetch(url, options);
    let body;
    try { body = await response.json(); } catch { throw new Error("The service returned an unreadable response. Please try again."); }
    if (!response.ok) throw new Error(body.error || `The request could not finish (${response.status}).`);
    return body;
  }

  function readSaved() {
    try {
      const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      return Array.isArray(value) ? value.filter(item => item && typeof item.county_fips === "string" && typeof item.industry === "string").slice(0, 100) : [];
    } catch { return []; }
  }
  function writeSaved(items) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(items)); return true; }
    catch { $("app-status").textContent = "This browser could not save your shortlist. You can still explore the data."; $("app-status").hidden = false; return false; }
  }
  const savedKey = item => `${item.county_fips}:${item.industry}`;

  function setSelection(next) {
    Object.assign(state, next);
    state.predictionToken += 1;
    $("prediction-result").replaceChildren();
    $("industry-select").value = state.industry;
    $("county-select").value = state.county;
    render();
  }

  function renderCounty() {
    const row = currentRow(), category = industry(state.industry);
    $("county-heading").textContent = county(state.county)?.name || state.county;
    $("county-category").textContent = category?.name || state.industry;
    $("county-metrics").innerHTML = `<div class="stat"><strong>${count(row?.establishments)}</strong><span>business locations · ${state.data.latest_year}</span></div><div class="stat"><strong class="${growthClass(row?.growth_pct)}">${percent(row?.growth_pct)}</strong><span>change from ${state.data.latest_year - 1}</span></div><div class="stat"><strong>${count(row?.employment)}</strong><span>reported employees</span></div>`;
    const history = (row?.history || []).filter(item => finite(item.year) && finite(item.establishments)).sort((a, b) => a.year - b.year);
    $("trend-range").textContent = history.length ? `${history[0].year}–${history[history.length - 1].year}` : "No matched history";
    drawHistory(history);
    const notes = [];
    if (!row) notes.push("This county–category pair has no eligible record in the frozen snapshot.");
    else {
      notes.push(`Annual payroll: ${money(row.annual_payroll)}.`);
      if (!finite(row.employment) || !finite(row.annual_payroll)) notes.push("Unavailable values are left blank in exports.");
      const flags = [row.employment_flag && `employment ${row.employment_flag}`, row.payroll_flag && `payroll ${row.payroll_flag}`].filter(Boolean);
      if (flags.length) notes.push(`Source flags: ${flags.join("; ")}. See source definitions.`);
    }
    $("county-data-note").textContent = notes.join(" ");
    const saved = readSaved().some(item => savedKey(item) === `${state.county}:${state.industry}`);
    $("save-selection").textContent = saved ? "Saved to research shortlist" : "Save to research shortlist";
    $("save-selection").classList.toggle("saved", saved);
    $("save-selection").disabled = !row || saved;
    $("predict-button").disabled = !row || !finite(row.establishments) || !finite(row.previous_establishments);
    $("predict-button").textContent = "Run estimate for this selection";
    $("interview-category").textContent = `${category?.name || state.industry} · ${county(state.county)?.name || state.county}`;
    $("workflow-hypothesis").textContent = category?.workflow_hypothesis || "Some owners may spend time on repeated quoting, scheduling, follow-up, or recordkeeping. Ask which workflow is expensive before choosing a solution.";
  }

  function drawHistory(history) {
    if (!history.length) { $("history-chart").innerHTML = '<p class="small muted">A comparable historical series is unavailable for this selection.</p>'; return; }
    const low = Math.min(...history.map(item => item.establishments)), high = Math.max(...history.map(item => item.establishments));
    const range = high - low || Math.max(1, high * .1);
    const xy = (item, index) => [24 + index * 252 / Math.max(1, history.length - 1), 72 - (item.establishments - low) * 37 / range];
    const parts = []; let segment = [];
    history.forEach((item, i) => {
      if (i && item.year !== history[i - 1].year + 1) { if (segment.length) parts.push(segment); segment = []; }
      segment.push(xy(item, i));
    });
    if (segment.length) parts.push(segment);
    $("history-chart").innerHTML = `<svg viewBox="0 0 300 110" role="img" aria-label="${esc(history.map(item => `${item.year}: ${item.establishments} locations`).join('; '))}"><line x1="20" y1="79" x2="280" y2="79" stroke="#dbe5db"/>${parts.map(points => `<polyline points="${points.map(point => point.join(',')).join(' ')}" fill="none" stroke="#247c6d" stroke-width="2.4"/>`).join("")}${history.map((item, i) => { const [x, y] = xy(item, i); return `<circle cx="${x}" cy="${y}" r="3.5" fill="#247c6d"/><text class="chart-value" x="${x}" y="${y - 11}" text-anchor="middle">${count(item.establishments)}</text><text class="chart-year" x="${x}" y="101" text-anchor="middle">${item.year}</text>`; }).join("")}</svg>`;
  }

  function colorScale(rows) {
    const unknown = "#e1e5df";
    if (state.metric === "growth_pct") {
      const colors = ["#bb775b", "#dfb69b", "#eef0df", "#8bbda5", "#237c6e"], bounds = [-10, -2, 2, 10];
      return {color: value => !finite(value) ? unknown : colors[bounds.filter(bound => value > bound).length], bins: colors.map((color, i) => ({color, label: ["≤ −10%", "−10% to −2%", "−2% to +2%", "+2% to +10%", "> +10%"][i]})), unknown};
    }
    const values = rows.map(row => row[state.metric]).filter(finite).sort((a, b) => a - b);
    const colors = ["#e7eee0", "#c1d9bb", "#8bbb9a", "#4d987d", "#176854"];
    if (!values.length) return {color: () => unknown, bins: [], unknown};
    const bounds = [.2, .4, .6, .8].map(p => values[Math.min(values.length - 1, Math.floor((values.length - 1) * p))]);
    return {color: value => !finite(value) ? unknown : colors[bounds.filter(bound => value > bound).length], bins: colors.map((color, i) => ({color, label: i === 0 ? `≤ ${metricFormat(bounds[0])}` : i === 4 ? `> ${metricFormat(bounds[3])}` : `${metricFormat(bounds[i - 1])}–${metricFormat(bounds[i])}`})), unknown};
  }

  function featureFips(feature) { return String(feature.properties?.GEOID || feature.properties?.geoid || feature.id || ""); }
  function geometryPolygons(geometry) { return geometry?.type === "Polygon" ? [geometry.coordinates] : geometry?.type === "MultiPolygon" ? geometry.coordinates : []; }
  function drawMap() {
    const rows = state.data.rows.filter(row => String(row.industry) === state.industry);
    const rowsByFips = new Map(rows.map(row => [String(row.county_fips), row]));
    const scale = colorScale(rows);
    $("map-industry-kicker").textContent = industry(state.industry)?.name || state.industry;
    $("map-heading").textContent = metricLabel(state.metric);
    $("map-year").textContent = state.metric === "growth_pct" ? `${state.data.latest_year - 1}–${state.data.latest_year}` : `${state.data.latest_year} snapshot`;
    $("map-legend").innerHTML = [...scale.bins, {color: scale.unknown, label: "Unavailable"}].map(bin => `<span class="legend-item"><i class="legend-chip" style="background:${bin.color}" aria-hidden="true"></i>${esc(bin.label)}</span>`).join("");
    $("map-caption").textContent = state.metric === "growth_pct" ? "Change in reported business locations between consecutive years. A small starting count can produce a large percentage change." : state.metric === "annual_payroll" ? "Total reported annual payroll in US dollars. Colors group counties by their position in this category's distribution; payroll is a measure of scale." : "Colors group counties by their position in this category's distribution. Each establishment is one business location with paid employees.";
    const svg = $("county-map"); svg.replaceChildren();
    if (!state.geo?.features?.length) { const text = document.createElementNS("http://www.w3.org/2000/svg", "text"); text.setAttribute("x", "295"); text.setAttribute("y", "235"); text.setAttribute("text-anchor", "middle"); text.textContent = "Map unavailable. Use the county menu."; svg.append(text); return; }
    const features = state.geo.features.filter(feature => featureFips(feature).startsWith("55"));
    const coords = features.flatMap(feature => geometryPolygons(feature.geometry).flatMap(poly => poly.flat())).filter(point => Array.isArray(point) && finite(point[0]) && finite(point[1]));
    if (!coords.length) return;
    const c = Math.cos(44 * Math.PI / 180), xs = coords.map(point => point[0] * c), ys = coords.map(point => point[1]);
    const minX = xs.reduce((a, b) => Math.min(a, b), Infinity), maxX = xs.reduce((a, b) => Math.max(a, b), -Infinity), minY = ys.reduce((a, b) => Math.min(a, b), Infinity), maxY = ys.reduce((a, b) => Math.max(a, b), -Infinity);
    const factor = Math.min(520 / (maxX - minX), 466 / (maxY - minY));
    const offsetX = (590 - (maxX - minX) * factor) / 2, offsetY = (530 - (maxY - minY) * factor) / 2;
    const project = point => [(point[0] * c - minX) * factor + offsetX, (maxY - point[1]) * factor + offsetY];
    let selectedFeature;
    for (const feature of features) {
      const fips = featureFips(feature), row = rowsByFips.get(fips), name = county(fips)?.name || feature.properties?.NAME || fips;
      const pathData = geometryPolygons(feature.geometry).map(poly => poly.map(ring => ring.map((point, i) => { const [x, y] = project(point); return `${i ? "L" : "M"}${x.toFixed(2)},${y.toFixed(2)}`; }).join(" ") + " Z").join(" ")).join(" ");
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", pathData); path.setAttribute("fill-rule", "evenodd"); path.setAttribute("fill", scale.color(row?.[state.metric])); path.setAttribute("class", `county-shape${fips === state.county ? " selected" : ""}`); path.setAttribute("tabindex", "0"); path.setAttribute("role", "button"); path.setAttribute("aria-pressed", String(fips === state.county)); path.setAttribute("aria-label", `${name}, ${metricLabel(state.metric)}: ${metricFormat(row?.[state.metric])}`);
      path.addEventListener("click", () => setSelection({county: fips}));
      path.addEventListener("keydown", event => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); setSelection({county: fips}); $("county-select").focus(); } });
      path.addEventListener("pointermove", event => { const tooltip = $("map-tooltip"), box = $("map-stage").getBoundingClientRect(); tooltip.textContent = `${name} · ${metricFormat(row?.[state.metric])}`; tooltip.hidden = false; tooltip.style.left = `${Math.min(Math.max(8, event.clientX - box.left + 10), Math.max(8, box.width - 215))}px`; tooltip.style.top = `${Math.max(4, event.clientY - box.top - 45)}px`; });
      path.addEventListener("pointerleave", () => { $("map-tooltip").hidden = true; });
      svg.append(path);
      if (fips === state.county) selectedFeature = {feature, path, name};
    }
    if (selectedFeature) {
      svg.append(selectedFeature.path);
      const biggest = geometryPolygons(selectedFeature.feature.geometry).sort((a, b) => (b[0]?.length || 0) - (a[0]?.length || 0))[0]?.[0];
      if (biggest?.length) {
        const points = biggest.map(project), tx = (Math.min(...points.map(p => p[0])) + Math.max(...points.map(p => p[0]))) / 2, ty = (Math.min(...points.map(p => p[1])) + Math.max(...points.map(p => p[1]))) / 2;
        const label = document.createElementNS("http://www.w3.org/2000/svg", "text"); label.setAttribute("x", tx.toFixed(1)); label.setAttribute("y", ty.toFixed(1)); label.setAttribute("class", "map-label"); label.textContent = selectedFeature.name.replace(/ County$/, ""); svg.append(label);
      }
    }
    $("map-tooltip").hidden = true;
  }

  function renderComparison() {
    const rows = state.data.rows.filter(row => String(row.industry) === state.industry).sort((a, b) => (finite(b[state.sort]) ? b[state.sort] : -Infinity) - (finite(a[state.sort]) ? a[state.sort] : -Infinity) || rowName(a).localeCompare(rowName(b)));
    $("comparison-description").textContent = `${industry(state.industry)?.name || state.industry} · ${state.data.latest_year} snapshot. ${state.allCounties ? "All available county records." : "First 8 county records in the selected order."}`;
    $("comparison-body").innerHTML = rows.slice(0, state.allCounties ? rows.length : 8).map(row => `<tr class="${String(row.county_fips) === state.county ? "selected-row" : ""}"><td><button class="county-link" type="button" data-county="${esc(row.county_fips)}">${esc(rowName(row).replace(/ County$/, ""))}</button></td><td class="number">${count(row.establishments)}</td><td class="number ${growthClass(row.growth_pct)}">${percent(row.growth_pct)}</td><td class="number">${money(row.annual_payroll)}</td></tr>`).join("") || '<tr><td colspan="4">No county records are available.</td></tr>';
    $("comparison-body").querySelectorAll("[data-county]").forEach(button => button.addEventListener("click", () => setSelection({county: button.dataset.county})));
    $("show-counties").textContent = state.allCounties ? "Show first 8 counties" : `Show all ${rows.length} available counties`;
    $("show-counties").hidden = rows.length <= 8;
    $("local-heading").textContent = `Within ${county(state.county)?.name || state.county}`;
    const local = state.data.rows.filter(row => String(row.county_fips) === state.county).sort((a, b) => (b.establishments || 0) - (a.establishments || 0));
    const largest = Math.max(1, ...local.map(row => row.establishments || 0));
    $("local-industries").innerHTML = local.map(row => `<div class="industry-bar-row${String(row.industry) === state.industry ? " active" : ""}"><button class="industry-link" type="button" data-industry="${esc(row.industry)}">${esc(industry(row.industry)?.name || row.industry)}</button><strong>${count(row.establishments)}</strong><div class="industry-track" aria-hidden="true"><div class="industry-fill" style="width:${finite(row.establishments) ? Math.max(1, row.establishments / largest * 100) : 0}%"></div></div></div>`).join("") || '<p class="small muted">No eligible categories are available for this county.</p>';
    $("local-industries").querySelectorAll("[data-industry]").forEach(button => button.addEventListener("click", () => setSelection({industry: button.dataset.industry})));
  }

  function renderShortlist() {
    const items = readSaved(); $("saved-count").textContent = items.length; $("export-shortlist").disabled = !items.length;
    if (!items.length) { $("shortlist-content").innerHTML = '<p class="empty-state">Your shortlist is empty. Start with a category and county above.</p>'; return; }
    $("shortlist-content").innerHTML = `<div class="table-wrap"><table><thead><tr><th scope="col">Market to investigate</th><th scope="col" class="number">Year</th><th scope="col" class="number">Locations</th><th scope="col" class="number">Change</th><th scope="col"><span class="sr-only">Actions</span></th></tr></thead><tbody>${items.map(item => `<tr><td><strong>${esc(item.county_name)}</strong><span>${esc(item.industry_name)}</span></td><td class="number">${esc(item.year)}</td><td class="number">${count(item.establishments)}</td><td class="number ${growthClass(item.growth_pct)}">${percent(item.growth_pct)}</td><td class="number"><button class="remove-button" type="button" data-remove="${esc(savedKey(item))}" aria-label="Remove ${esc(item.industry_name)} in ${esc(item.county_name)}">Remove</button></td></tr>`).join("")}</tbody></table></div>`;
    $("shortlist-content").querySelectorAll("[data-remove]").forEach(button => button.addEventListener("click", () => { if (writeSaved(readSaved().filter(item => savedKey(item) !== button.dataset.remove))) { renderShortlist(); if (state.data) renderCounty(); } }));
  }

  function populateMethod() {
    const model = state.data.model || {}, testYear = model.test_target_year || 2023;
    $("forecast-description").textContent = `Use the ${state.data.latest_year} snapshot to estimate ${model.forecast_year || state.data.latest_year + 1} business locations for the selected category. This is a dated historical estimate; current demand requires fresh validation.`;
    $("backtest-metrics").innerHTML = `<div class="backtest-cell"><strong>${errorCount(model.test?.mae)}</strong><span>model MAE · ${testYear} US test</span><small>locations of average error</small></div><div class="backtest-cell"><strong>${errorCount(model.baseline_test?.mae)}</strong><span>no-change baseline MAE</span><small>same held-out cases</small></div>`;
    const localErrors = finite(model.wisconsin_test?.mae) && finite(model.wisconsin_baseline_test?.mae) ? ` Wisconsin subset: model MAE ${errorCount(model.wisconsin_test.mae)}; no-change MAE ${errorCount(model.wisconsin_baseline_test.mae)}${finite(model.wisconsin_test_rows) ? ` (${count(model.wisconsin_test_rows)} cases)` : ""}.` : "";
    $("backtest-interpretation").textContent = (model.model_beats_baseline === false ? "The no-change baseline was more accurate on the final test. Keep that result in view when interpreting the model estimate." : model.model_beats_baseline === true ? "The model had lower held-out MAE than the no-change baseline. This result is specific to the recorded period and evaluated cases." : "Inspect the saved evaluation to compare the model with the no-change baseline.") + localErrors;
    $("model-method").textContent = `Model: ${model.selected_model || "See metadata"}. Training predicts ${model.training_target_year || 2021}; validation predicts ${model.validation_target_year || 2022}; final testing predicts ${testYear}. Each prediction uses information available in its input period. The public estimate applies the saved model to the latest frozen snapshot.`;
    const limits = state.data.limitations || ["Published data are historical and can contain disclosure protection or missing values.", "Market scale and growth do not establish owner profits, customer demand, or a specific sales opportunity."];
    $("limitations").innerHTML = `<ul>${limits.map(limit => `<li>${esc(typeof limit === "string" ? limit : limit.description || JSON.stringify(limit))}</li>`).join("")}</ul>`;
    $("source-links").innerHTML = (state.data.sources || []).filter(source => /^https:\/\//.test(source.url || "")).map(source => `<li><a href="${esc(source.url)}" target="_blank" rel="noopener noreferrer">${esc(source.name || source.url)}</a></li>`).join("");
  }

  function render() { renderCounty(); drawMap(); renderComparison(); renderShortlist(); }

  async function predict() {
    const row = currentRow(); if (!row || !finite(row.establishments) || !finite(row.previous_establishments)) return;
    const token = ++state.predictionToken; $("predict-button").disabled = true; $("predict-button").textContent = "Running saved model…"; $("prediction-result").replaceChildren();
    try {
      const result = await getJSON("/predict", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({industry: state.industry, establishments: row.establishments, previous_establishments: row.previous_establishments})});
      if (token !== state.predictionToken) return;
      if (!finite(result.prediction) || !finite(result.baseline)) throw new Error("The service returned an incomplete estimate.");
      $("prediction-result").innerHTML = `<div class="prediction-values"><div><strong>${decimal(result.prediction)}</strong><span>model estimate · ${esc(result.target_year)}</span></div><div><strong>${decimal(result.baseline)}</strong><span>no-change estimate</span></div></div><p>${esc(result.notice || `Historical estimate using data through ${result.as_of_year}.`)}</p>`;
    } catch (error) { if (token === state.predictionToken) { const p = document.createElement("p"); p.className = "prediction-error"; p.textContent = error.message; $("prediction-result").replaceChildren(p); } }
    finally { if (token === state.predictionToken) { $("predict-button").disabled = false; $("predict-button").textContent = "Run estimate for this selection"; } }
  }

  function exportShortlist() {
    const items = readSaved(); if (!items.length) return;
    const headers = ["county_fips", "county_name", "industry", "industry_name", "year", "establishments", "previous_establishments", "growth_pct", "employment", "annual_payroll", "employment_flag", "payroll_flag", "saved_at", "purpose"];
    const csvCell = value => { const raw = value === null || value === undefined ? "" : typeof value === "number" ? String(value) : String(value).replace(/^[=+\-@]/, "'$&"); return `"${raw.replace(/"/g, '""')}"`; };
    const text = "\uFEFF" + [headers.map(csvCell).join(","), ...items.map(item => headers.map(key => csvCell(key === "purpose" ? "Research shortlist; demand and buyer fit unverified" : item[key])).join(","))].join("\r\n");
    const link = document.createElement("a"), url = URL.createObjectURL(new Blob([text], {type: "text/csv;charset=utf-8"})); link.href = url; link.download = "main-street-research-shortlist.csv"; document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async function load() {
    $("app-status").className = "status"; $("app-status").hidden = false; $("app-status").textContent = "Loading the business data and county map…"; $("retry").hidden = true;
    try {
      const [dataResult, geoResult] = await Promise.allSettled([getJSON("/api/data"), getJSON("/api/geo")]);
      if (dataResult.status !== "fulfilled") throw dataResult.reason;
      const data = dataResult.value;
      if (!Array.isArray(data.rows) || !Array.isArray(data.industries) || !Array.isArray(data.counties) || !data.industries.length || !data.counties.length) throw new Error("The data snapshot is incomplete. Please check the service and try again.");
      state.data = data; state.geo = geoResult.status === "fulfilled" ? geoResult.value : null;
      state.industry = data.industries.some(item => String(item.code) === state.industry) ? state.industry : String(data.industries[0].code);
      state.county = data.counties.some(item => String(item.fips) === state.county) ? state.county : String(data.counties[0].fips);
      $("industry-select").innerHTML = data.industries.map(item => `<option value="${esc(item.code)}">${esc(item.name)}</option>`).join("");
      $("county-select").innerHTML = [...data.counties].sort((a, b) => a.name.localeCompare(b.name)).map(item => `<option value="${esc(item.fips)}">${esc(item.name)}</option>`).join("");
      $("snapshot-label").textContent = `${data.latest_year} Census business snapshot`;
      $("industry-description").textContent = "Ten selected service categories, using consistent industry definitions.";
      populateMethod(); setSelection({});
      ["explorer", "comparisons", "research-next"].forEach(id => { $(id).hidden = false; });
      if (!state.geo) { $("app-status").textContent = "The map geometry could not load. County menus, comparisons, and the research shortlist remain available."; }
      else $("app-status").hidden = true;
    } catch (error) { $("app-status").className = "status error"; $("app-status").textContent = `The explorer could not load: ${error.message}`; $("retry").hidden = false; }
  }

  $("industry-select").addEventListener("change", event => setSelection({industry: event.target.value, allCounties: false}));
  $("county-select").addEventListener("change", event => setSelection({county: event.target.value}));
  $("map-metric").addEventListener("change", event => { state.metric = event.target.value; drawMap(); });
  $("comparison-sort").addEventListener("change", event => { state.sort = event.target.value; renderComparison(); });
  $("show-counties").addEventListener("click", () => { state.allCounties = !state.allCounties; renderComparison(); });
  $("save-selection").addEventListener("click", () => {
    const row = currentRow(); if (!row) return;
    const items = readSaved(); if (items.some(item => savedKey(item) === `${state.county}:${state.industry}`)) return;
    if (writeSaved([...items, {county_fips: state.county, county_name: rowName(row), industry: state.industry, industry_name: industry(state.industry)?.name || state.industry, year: state.data.latest_year, establishments: row.establishments, previous_establishments: row.previous_establishments, growth_pct: row.growth_pct, employment: row.employment, annual_payroll: row.annual_payroll, employment_flag: row.employment_flag, payroll_flag: row.payroll_flag, saved_at: new Date().toISOString()}])) { renderShortlist(); renderCounty(); }
  });
  $("predict-button").addEventListener("click", predict);
  $("export-shortlist").addEventListener("click", exportShortlist);
  $("retry").addEventListener("click", load);
  renderShortlist(); load();
})();
