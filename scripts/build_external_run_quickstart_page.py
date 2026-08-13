import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_RUN_PACKET_PATH = ROOT / "docs" / "external-run-evidence-packet.json"
EXTERNAL_REVIEWER_REQUEST_PACK_PATH = ROOT / "docs" / "external-reviewer-request-pack.json"
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
OUTPUT_HTML_PATH = ROOT / "docs" / "external-run-quickstart.html"
OUTPUT_JSON_PATH = ROOT / "docs" / "external-run-quickstart.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_external_run_quickstart_payload() -> dict[str, Any]:
    packet = load_json(EXTERNAL_RUN_PACKET_PATH)
    request_pack = load_json(EXTERNAL_REVIEWER_REQUEST_PACK_PATH)
    adoption = load_json(ADOPTION_METRICS_PATH)
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_external_run_quickstart_page.py",
        "page": "docs/external-run-quickstart.html",
        "public_url": "https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html",
        "public_demo_url": adoption["public_demo"],
        "repo_url": adoption["repo"],
        "container_image": adoption["container_image"]["image"],
        "collection_issue": packet["public_collection_issue"]["url"],
        "review_template": packet["external_run_review_template"]["url"],
        "review_path_count": packet["review_path_count"],
        "submission_field_count": packet["submission_field_count"],
        "upgrade_rule_count": packet["upgrade_rule_count"],
        "review_paths": packet["review_paths"],
        "submission_fields": packet["submission_fields"],
        "privacy_boundaries": packet["privacy_boundaries"],
        "current_counts": packet["current_counts"],
        "outreach_message_count": len(request_pack["outreach_messages"]),
        "resume_safe_summary": (
            "Published a GitHub Pages external-run quickstart that routes reviewers through 3 run paths, "
            "8 evidence fields, a public collection issue, a structured review template, and explicit privacy "
            "boundaries before any external-user or feedback claim can be counted."
        ),
        "not_claimed": [
            "No external reviewer run is claimed yet.",
            "No external users are claimed yet.",
            "No customer feedback is claimed yet.",
            "No private business data is requested or stored.",
        ],
    }


def render_html(payload: dict[str, Any]) -> str:
    paths = "\n".join(
        f"""
        <article class=\"card\">
          <strong>{item['id'].replace('_', ' ')}</strong>
          <h2>{item['surface'].replace('_', ' ').title()}</h2>
          <p>Time box: {item['time_box_minutes']} minutes.</p>
          <p>Counts toward: <code>{item['counts_toward_after_public_issue']}</code> only after public evidence and permission.</p>
          {f"<pre><code>{item['command']}</code></pre>" if item.get('command') else ""}
          <ul>
            {"".join(f"<li>{evidence}</li>" for evidence in item["required_evidence"])}
          </ul>
        </article>
        """
        for item in payload["review_paths"]
    )
    fields = "\n".join(
        f"<li><code>{item['name']}</code> - example: {item['example']}</li>"
        for item in payload["submission_fields"]
    )
    privacy = "\n".join(f"<li>{item}</li>" for item in payload["privacy_boundaries"])
    counts = "\n".join(
        f"<li><code>{key}</code>: {value}</li>" for key, value in payload["current_counts"].items()
    )
    not_claimed = "\n".join(f"<li>{item}</li>" for item in payload["not_claimed"])
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>External Run Quickstart | Data Quality Agent</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #070b10;
      --panel: #111923;
      --panel-2: #182434;
      --text: #f8fafc;
      --muted: #aab6c7;
      --line: #293548;
      --accent: #5eead4;
      --accent-2: #93c5fd;
      --warn: #fbbf24;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(135deg, rgba(94, 234, 212, .10), transparent 34%), var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif;
      line-height: 1.5;
    }}
    a {{ color: inherit; }}
    .shell {{ width: min(1100px, calc(100% - 36px)); margin: 0 auto; padding: 44px 0; }}
    header {{ min-height: 54vh; display: grid; align-items: center; }}
    .eyebrow {{ color: var(--accent); font-size: 13px; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; }}
    h1 {{ font-size: clamp(40px, 7vw, 82px); letter-spacing: 0; line-height: .96; margin: 12px 0 18px; max-width: 920px; }}
    .lede {{ color: var(--muted); font-size: clamp(18px, 2vw, 22px); max-width: 800px; margin: 0 0 24px; }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 12px; }}
    .button {{ align-items: center; background: var(--text); border-radius: 8px; color: #071016; display: inline-flex; font-weight: 850; min-height: 46px; padding: 0 16px; text-decoration: none; }}
    .button.feedback {{ background: var(--accent); color: #06201b; }}
    .button.secondary {{ background: rgba(255, 255, 255, .07); border: 1px solid var(--line); color: var(--text); }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }}
    .card, .panel {{ background: rgba(17, 25, 35, .92); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
    .card strong {{ color: var(--accent); display: block; font-size: 13px; margin-bottom: 10px; text-transform: uppercase; }}
    .card h2, .panel h2 {{ margin: 0 0 10px; }}
    .card p, .card li, .panel li, .panel p {{ color: var(--muted); }}
    .panel {{ margin: 16px 0; }}
    pre {{ background: #05080c; border: 1px solid var(--line); border-radius: 8px; overflow: auto; padding: 12px; }}
    code {{ color: #dbeafe; }}
    .warning {{ border-color: rgba(251, 191, 36, .45); }}
    .warning strong {{ color: var(--warn); }}
    footer {{ border-top: 1px solid var(--line); color: var(--muted); margin-top: 42px; padding-top: 22px; }}
    @media (max-width: 860px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main class=\"shell\">
    <header>
      <div>
        <div class=\"eyebrow\">External run quickstart</div>
        <h1>Run it, leave evidence, keep the claim honest.</h1>
        <p class=\"lede\">
          Choose one path below, record what happened, then comment on the public collection issue or open the
          structured External Run Review template. A run only counts after public permission is given.
        </p>
        <div class=\"actions\">
          <a class=\"button feedback\" href=\"{payload['review_template']}\">Open External Run Review</a>
          <a class=\"button\" href=\"{payload['collection_issue']}\">Comment on Issue #18</a>
          <a class=\"button secondary\" href=\"{payload['public_demo_url']}\">Open Public Demo</a>
          <a class=\"button secondary\" href=\"{payload['repo_url']}\">Open Repository</a>
        </div>
      </div>
    </header>

    <section class=\"grid\" aria-label=\"External run paths\">
      {paths}
    </section>

    <section class=\"panel\">
      <h2>Required evidence fields</h2>
      <p>These {payload['submission_field_count']} fields make the result countable without asking for private data.</p>
      <ul>{fields}</ul>
    </section>

    <section class=\"panel warning\">
      <strong>Privacy boundary</strong>
      <h2>No private business data</h2>
      <ul>{privacy}</ul>
    </section>

    <section class=\"panel\">
      <h2>Current public counts</h2>
      <p>These stay at zero until a reviewer leaves public evidence and permission.</p>
      <ul>{counts}</ul>
    </section>

    <section class=\"panel\">
      <h2>Not claimed yet</h2>
      <ul>{not_claimed}</ul>
    </section>

    <section class=\"panel\">
      <h2>Resume-safe summary</h2>
      <p>{payload['resume_safe_summary']}</p>
    </section>

    <footer>
      Generated by <code>{payload['generated_by']}</code>. Container image:
      <code>{payload['container_image']}</code>.
    </footer>
  </main>
</body>
</html>
"""


def verify_external_run_quickstart_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["review_path_count"] != 3:
        raise AssertionError("external run quickstart must expose 3 review paths")
    if payload["submission_field_count"] != 8:
        raise AssertionError("external run quickstart must preserve 8 evidence fields")
    if payload["upgrade_rule_count"] != 3:
        raise AssertionError("external run quickstart must preserve 3 upgrade rules")
    if not payload["collection_issue"].endswith("/issues/18"):
        raise AssertionError("external run quickstart must link public issue #18")
    if not payload["review_template"].endswith("template=external_run_review.md"):
        raise AssertionError("external run quickstart must link the external run review template")
    if payload["current_counts"].get("confirmed_external_users") != 0:
        raise AssertionError("external run quickstart must preserve zero confirmed-user baseline")
    if "No private business data is requested or stored." not in payload["not_claimed"]:
        raise AssertionError("external run quickstart must not request private business data")

    html = render_html(payload)
    required_fragments = [
        "External run quickstart",
        "Open External Run Review",
        "Comment on Issue #18",
        "docker run --rm -p 8000:8000 ghcr.io/sunnnn2005/data-quality-agent:latest",
        "docker compose up --build",
        "permission_to_count_publicly",
        "No private business data",
        "confirmed_external_users",
        "No external reviewer run is claimed yet.",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in html]
    if missing:
        raise AssertionError(f"external run quickstart page missing fragments: {missing}")
    return {
        "external_run_quickstart_verified": True,
        "review_path_count": payload["review_path_count"],
        "submission_field_count": payload["submission_field_count"],
        "upgrade_rule_count": payload["upgrade_rule_count"],
    }


def main() -> None:
    payload = build_external_run_quickstart_payload()
    verify_external_run_quickstart_payload(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
