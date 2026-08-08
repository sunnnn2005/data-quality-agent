def render_dashboard() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Data Quality Agent</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    body { margin: 0; background: #0d1017; color: #eef2ff; }
    main { max-width: 1180px; margin: 0 auto; padding: 40px 24px; }
    header { display: flex; justify-content: space-between; gap: 20px; align-items: flex-end; }
    h1 { margin: 0; font-size: clamp(36px, 7vw, 72px); line-height: .9; letter-spacing: 0; }
    p { color: #aab4cf; font-size: 16px; line-height: 1.6; }
    select, button { border: 1px solid #2a3142; background: #161b27; color: #f8fafc; border-radius: 8px; padding: 12px 14px; font-weight: 700; }
    button { background: #4f8cff; border-color: #4f8cff; cursor: pointer; }
    .grid { display: grid; grid-template-columns: 340px 1fr; gap: 20px; margin-top: 28px; }
    .panel { background: #121722; border: 1px solid #252c3b; border-radius: 8px; padding: 20px; }
    .score { font-size: 64px; font-weight: 900; }
    .status { display: inline-flex; padding: 6px 10px; border-radius: 999px; background: #2d3648; color: #dbeafe; font-size: 13px; font-weight: 800; }
    .finding { border-top: 1px solid #273044; padding: 16px 0; }
    .finding:first-child { border-top: 0; padding-top: 0; }
    .sev { color: #ff7a90; font-weight: 900; }
    code { background: #20283a; padding: 2px 6px; border-radius: 6px; }
    @media (max-width: 820px) { .grid, header { grid-template-columns: 1fr; display: grid; } }
  </style>
</head>
<body>
<main>
  <header>
    <div>
      <h1>Data Quality Agent</h1>
      <p>Automated schema, freshness, completeness, uniqueness, and outlier diagnosis for analytics datasets.</p>
    </div>
    <div>
      <select id="dataset"></select>
      <button id="run">Analyze</button>
    </div>
  </header>
  <section class="grid">
    <aside class="panel">
      <div class="status" id="status">WAITING</div>
      <div class="score" id="score">--</div>
      <p id="summary">Choose a dataset and run the agent.</p>
      <h3>Agent Trace</h3>
      <div id="trace"></div>
    </aside>
    <section class="panel">
      <h2>Findings</h2>
      <div id="findings"></div>
      <h2>Likely Causes</h2>
      <div id="causes"></div>
      <h2>Next Steps</h2>
      <div id="steps"></div>
    </section>
  </section>
</main>
<script>
const datasetSelect = document.querySelector("#dataset");
const runButton = document.querySelector("#run");

async function loadDatasets() {
  const response = await fetch("/datasets");
  const datasets = await response.json();
  datasetSelect.innerHTML = datasets.map(item => `<option value="${item.id}">${item.name}</option>`).join("");
}

function list(items) {
  return `<ul>${items.map(item => `<li>${item}</li>`).join("")}</ul>`;
}

async function analyze() {
  const id = datasetSelect.value;
  const response = await fetch(`/datasets/${id}/quality-report`, { method: "POST" });
  const report = await response.json();
  document.querySelector("#status").textContent = report.status;
  document.querySelector("#score").textContent = report.quality_score;
  document.querySelector("#summary").textContent = `${report.dataset.name}: ${report.row_count} rows, ${report.findings.length} findings`;
  document.querySelector("#trace").innerHTML = list(report.agent_trace);
  document.querySelector("#causes").innerHTML = list(report.likely_causes);
  document.querySelector("#steps").innerHTML = list(report.recommended_next_steps);
  document.querySelector("#findings").innerHTML = report.findings.map(finding => `
    <div class="finding">
      <div class="sev">${finding.severity}</div>
      <h3>${finding.check_name}${finding.column ? `: <code>${finding.column}</code>` : ""}</h3>
      <p>${finding.message}</p>
      <p>${finding.recommendation}</p>
    </div>
  `).join("") || "<p>No quality findings.</p>";
}

runButton.addEventListener("click", analyze);
loadDatasets().then(analyze);
</script>
</body>
</html>
"""
