import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROUTER_PATH = ROOT / "docs" / "reviewer-quickstart-router.json"
CHECKLIST_PATH = ROOT / "docs" / "evidence-acceptance-checklist.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "first-external-review-card.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-external-review-card.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "first-external-review-card.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_first_external_review_card() -> dict[str, Any]:
    router = load_json(ROUTER_PATH)
    checklist = load_json(CHECKLIST_PATH)
    routes_by_metric = {route["target_metric"]: route for route in router["routes"]}
    priority_metrics = [
        "ai_engineer_review_items",
        "confirmed_external_users",
        "external_feedback_items",
    ]
    primary_routes = [routes_by_metric[metric] for metric in priority_metrics]
    acceptance_items = checklist["acceptance_items"]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_external_review_card.py",
        "purpose": (
            "Create a shareable one-page reviewer card that converts a first external reviewer into public, "
            "permissioned evidence without claiming users, feedback, or stars before they exist."
        ),
        "public_url": "https://sunnnn2005.github.io/data-quality-agent/first-external-review-card.html",
        "primary_routes": primary_routes,
        "all_route_count": router["route_count"],
        "target_metrics": priority_metrics,
        "current_counts": {
            metric: checklist["current_public_counts"][metric] for metric in priority_metrics
        },
        "blocked_outcome_count": len(acceptance_items),
        "fastest_path_minutes": 5,
        "ai_engineer_path_minutes": 12,
        "counting_rule": router["manual_counting_rule"],
        "success_definition": (
            "One non-owner public GitHub issue with permission, no private data, and enough detail to pass the "
            "external reviewer evidence gate."
        ),
        "copy_ready_message": (
            "Could you spend 5-12 minutes reviewing my Data Quality Agent project? "
            "This page lets you choose the fastest feedback path, an AI Engineer architecture review, or a "
            "confirmed-use note: https://sunnnn2005.github.io/data-quality-agent/first-external-review-card.html. "
            "Please submit only public, non-private evidence if you are comfortable."
        ),
        "resume_safe_summary": (
            "Published a one-page external review card routing reviewers to 3 public evidence paths and preserving "
            "zero user, feedback, AI-review, and star claims until a non-owner public issue passes the evidence gate."
        ),
        "not_claimed": [
            "accepted external review",
            "confirmed external user",
            "external feedback",
            "GitHub stars",
            "production adoption",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    route_rows = "\n".join(
        "| {label} | `{target_metric}` | {best_for} | [Submit]({submission_url}) |".format(
            **route
        )
        for route in payload["primary_routes"]
    )
    count_rows = "\n".join(
        f"| `{metric}` | {count} |" for metric, count in payload["current_counts"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# First External Review Card

This generated card is the shortest shareable path for earning the first external evidence item.

## Public URL

[{payload["public_url"]}]({payload["public_url"]})

## Copy-Ready Message

```text
{payload["copy_ready_message"]}
```

## Primary Review Paths

| Reviewer Situation | Target Metric | Best For | Submit Evidence |
| --- | --- | --- | --- |
{route_rows}

## Current Counts

| Metric | Current Count |
| --- | ---: |
{count_rows}

## Success Definition

{payload["success_definition"]}

## Counting Rule

{payload["counting_rule"]}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def render_html(payload: dict[str, Any]) -> str:
    cards = "\n".join(
        f"""
        <article class="path">
          <p class="metric">{html.escape(route["target_metric"])}</p>
          <h2>{html.escape(route["label"])}</h2>
          <p>{html.escape(route["best_for"])}</p>
          <a class="button" href="{html.escape(route["submission_url"])}">Submit public evidence</a>
        </article>
        """
        for route in payload["primary_routes"]
    )
    count_items = "\n".join(
        f"<li><span>{html.escape(metric)}</span><strong>{count}</strong></li>"
        for metric, count in payload["current_counts"].items()
    )
    message = html.escape(payload["copy_ready_message"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>First External Review Card</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #071017;
      --panel: #111a24;
      --panel-2: #172333;
      --text: #f6f8fb;
      --muted: #aab6c7;
      --line: #283548;
      --accent: #5eead4;
      --accent-2: #8ab4ff;
      --warn: #ffd166;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(135deg, #071017 0%, #111827 58%, #0f172a 100%);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{
      width: min(1120px, calc(100% - 40px));
      margin: 0 auto;
      padding: 52px 0;
    }}
    .hero {{
      display: grid;
      gap: 28px;
      grid-template-columns: minmax(0, 1.1fr) minmax(300px, .9fr);
      min-height: 58vh;
      align-items: center;
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 13px;
      font-weight: 850;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    h1 {{
      font-size: clamp(44px, 7vw, 84px);
      line-height: .96;
      letter-spacing: 0;
      margin: 12px 0 18px;
    }}
    .lede {{
      color: var(--muted);
      font-size: clamp(18px, 2vw, 23px);
      max-width: 760px;
      margin: 0;
    }}
    .copy {{
      background: rgba(255, 255, 255, .06);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }}
    .copy p {{
      color: var(--muted);
      margin: 0 0 12px;
    }}
    .copy pre {{
      background: #050a10;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: #dbeafe;
      margin: 0;
      overflow-x: auto;
      padding: 14px;
      white-space: pre-wrap;
      font: 13px/1.5 ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }}
    .paths {{
      display: grid;
      gap: 14px;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      margin: 36px 0;
    }}
    .path {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
      min-height: 260px;
      display: flex;
      flex-direction: column;
    }}
    .metric {{
      color: var(--accent-2);
      font-size: 12px;
      font-weight: 850;
      margin: 0 0 12px;
      text-transform: uppercase;
    }}
    h2 {{
      font-size: 28px;
      letter-spacing: 0;
      line-height: 1.05;
      margin: 0 0 12px;
    }}
    .path p:not(.metric) {{
      color: var(--muted);
      margin: 0 0 20px;
    }}
    .button {{
      align-items: center;
      background: var(--accent);
      border-radius: 8px;
      color: #05201b;
      display: inline-flex;
      font-weight: 850;
      justify-content: center;
      margin-top: auto;
      min-height: 44px;
      padding: 0 16px;
      text-decoration: none;
    }}
    .evidence {{
      display: grid;
      gap: 18px;
      grid-template-columns: minmax(0, .8fr) minmax(0, 1.2fr);
      border-top: 1px solid var(--line);
      padding-top: 32px;
    }}
    .counts {{
      background: var(--panel-2);
      border: 1px solid var(--line);
      border-radius: 8px;
      margin: 0;
      padding: 18px;
    }}
    .counts li {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      padding: 10px 0;
      border-bottom: 1px solid rgba(255, 255, 255, .08);
      color: var(--muted);
    }}
    .counts li:last-child {{ border-bottom: 0; }}
    .counts strong {{ color: var(--text); }}
    .rule {{
      background: rgba(255, 209, 102, .08);
      border: 1px solid rgba(255, 209, 102, .32);
      border-radius: 8px;
      padding: 18px;
    }}
    .rule h2 {{ color: var(--warn); }}
    .rule p {{ color: var(--muted); margin: 0 0 12px; }}
    @media (max-width: 860px) {{
      .hero, .paths, .evidence {{ grid-template-columns: 1fr; }}
      main {{ width: min(100% - 28px, 1120px); padding: 34px 0; }}
      .path {{ min-height: 0; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div>
        <p class="eyebrow">External evidence request</p>
        <h1>Review Data Quality Agent in 5-12 minutes</h1>
        <p class="lede">Choose one public feedback path. A resume outcome counts only after a non-owner GitHub issue includes permission and no private data.</p>
      </div>
      <aside class="copy">
        <p>Copy this message to a classmate, mentor, or engineer.</p>
        <pre>{message}</pre>
      </aside>
    </section>
    <section class="paths" aria-label="review paths">
      {cards}
    </section>
    <section class="evidence">
      <ul class="counts" aria-label="current outcome counts">
        {count_items}
      </ul>
      <div class="rule">
        <h2>Counting rule</h2>
        <p>{html.escape(payload["counting_rule"])}</p>
        <p><strong>Success:</strong> {html.escape(payload["success_definition"])}</p>
        <p>{html.escape(payload["resume_safe_summary"])}</p>
      </div>
    </section>
  </main>
</body>
</html>
"""


def verify_first_external_review_card(payload: dict[str, Any]) -> dict[str, Any]:
    if len(payload["primary_routes"]) != 3:
        raise AssertionError("first external review card must expose exactly three primary paths")
    if payload["current_counts"] != {
        "ai_engineer_review_items": 0,
        "confirmed_external_users": 0,
        "external_feedback_items": 0,
    }:
        raise AssertionError("first external review card must preserve zero external outcome claims")
    if "non-owner public GitHub issue" not in payload["counting_rule"]:
        raise AssertionError("first external review card must require public non-owner evidence")
    if "5-12 minutes" not in payload["copy_ready_message"]:
        raise AssertionError("first external review card must be easy to send")
    if "production adoption" not in payload["not_claimed"]:
        raise AssertionError("first external review card must avoid adoption claims")
    for route in payload["primary_routes"]:
        if not route["submission_url"].startswith("https://github.com/"):
            raise AssertionError("review evidence must be submitted on public GitHub")
    return {
        "first_external_review_card_verified": True,
        "primary_route_count": len(payload["primary_routes"]),
        "blocked_outcome_count": payload["blocked_outcome_count"],
        "current_counts": payload["current_counts"],
    }


def main() -> None:
    payload = build_first_external_review_card()
    verify_first_external_review_card(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps({"status": "ok", "output": str(OUTPUT_HTML_PATH)}))


if __name__ == "__main__":
    main()
