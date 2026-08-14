import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REVIEW_CARD_PATH = ROOT / "docs" / "first-external-review-card.json"
QUICKLINK_PATH = ROOT / "docs" / "pilot-evidence-quicklink.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "two-minute-review-card.json"
OUTPUT_MD_PATH = ROOT / "docs" / "two-minute-review-card.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "two-minute-review-card.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_two_minute_review_card() -> dict[str, Any]:
    review_card = load_json(REVIEW_CARD_PATH)
    quicklink = load_json(QUICKLINK_PATH)
    demo_route = next(
        route for route in review_card["primary_routes"] if route["target_metric"] == "external_feedback_items"
    )
    ai_route = next(
        route for route in review_card["primary_routes"] if route["target_metric"] == "ai_engineer_review_items"
    )

    micro_steps = [
        {
            "step": 1,
            "label": "Open the public demo",
            "action": "Open the hosted demo and inspect the support-ticket data-quality result.",
            "url": "https://sunnnn2005.github.io/data-quality-agent/",
            "counts_as_outcome": False,
        },
        {
            "step": 2,
            "label": "Pick one useful or confusing detail",
            "action": "Choose one concrete observation about the report, agent behavior, guardrails, or UI.",
            "url": review_card["public_url"],
            "counts_as_outcome": False,
        },
        {
            "step": 3,
            "label": "Submit public evidence",
            "action": "Open the feedback issue template and include permission/no-private-data checks.",
            "url": demo_route["submission_url"],
            "counts_as_outcome": False,
        },
    ]
    required_evidence = [
        "what page, command, or route was reviewed",
        "one concrete observed result",
        "one useful, confusing, or missing detail",
        "permission to count publicly",
        "confirmation that no private data was posted",
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_two_minute_review_card.py",
        "public_url": "https://sunnnn2005.github.io/data-quality-agent/two-minute-review-card.html",
        "purpose": (
            "Give a busy reviewer the shortest safe path to produce the first countable public feedback item "
            "without inflating users, stars, or adoption."
        ),
        "time_budget_minutes": 2,
        "micro_step_count": len(micro_steps),
        "micro_steps": micro_steps,
        "primary_feedback_url": demo_route["submission_url"],
        "ai_engineer_review_url": ai_route["submission_url"],
        "fallback_evidence_hub": quicklink["public_url"],
        "required_evidence_count": len(required_evidence),
        "required_evidence": required_evidence,
        "current_counts": review_card["current_counts"],
        "success_definition": (
            "One non-owner GitHub issue that includes a concrete observation, explicit permission to count, "
            "and no private data."
        ),
        "copy_ready_message": (
            "Could you spend 2 minutes reviewing my Data Quality Agent demo? "
            "Open this card, inspect one result, and leave one concrete public note if you are comfortable: "
            "https://sunnnn2005.github.io/data-quality-agent/two-minute-review-card.html"
        ),
        "resume_safe_summary": (
            "Published a two-minute external review card with 3 micro-steps, 5 required evidence fields, "
            "and zero outcome upgrades until a non-owner public issue passes the evidence gate."
        ),
        "not_claimed": [
            "external feedback",
            "confirmed external user",
            "GitHub stars",
            "production adoption",
            "business impact validated by a company",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    steps = "\n".join(
        f"{step['step']}. [{step['label']}]({step['url']}) - {step['action']} "
        f"`counts_as_outcome={step['counts_as_outcome']}`"
        for step in payload["micro_steps"]
    )
    evidence = "\n".join(f"- {item}" for item in payload["required_evidence"])
    counts = "\n".join(f"| `{metric}` | {count} |" for metric, count in payload["current_counts"].items())
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Two-Minute Review Card

{payload["purpose"]}

Public card: [{payload["public_url"]}]({payload["public_url"]})

## Copy-Ready Message

```text
{payload["copy_ready_message"]}
```

## Micro-Steps

{steps}

## Required Evidence

{evidence}

## Current Counts

| Metric | Count |
| --- | ---: |
{counts}

## Success Definition

{payload["success_definition"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def render_html(payload: dict[str, Any]) -> str:
    cards = "\n".join(
        f"""
        <article>
          <span>Step {step['step']}</span>
          <h2>{html.escape(step['label'])}</h2>
          <p>{html.escape(step['action'])}</p>
          <a href="{html.escape(step['url'])}">Open</a>
        </article>
        """
        for step in payload["micro_steps"]
    )
    evidence = "".join(f"<li>{html.escape(item)}</li>" for item in payload["required_evidence"])
    counts = "".join(
        f"<li><span>{html.escape(metric)}</span><strong>{count}</strong></li>"
        for metric, count in payload["current_counts"].items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Two-Minute Review Card</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #08111f;
      --panel: #101b2b;
      --line: #243247;
      --text: #f7fafc;
      --muted: #a9b6c8;
      --accent: #5eead4;
      --accent2: #facc15;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: radial-gradient(circle at 20% 10%, rgba(94, 234, 212, .16), transparent 32%),
        linear-gradient(135deg, #08111f 0%, #121827 100%);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{
      width: min(1040px, calc(100% - 36px));
      margin: 0 auto;
      padding: 52px 0;
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 13px;
      font-weight: 850;
      text-transform: uppercase;
    }}
    h1 {{
      font-size: clamp(46px, 8vw, 88px);
      line-height: .95;
      letter-spacing: 0;
      margin: 10px 0 18px;
      max-width: 880px;
    }}
    .lede {{
      color: var(--muted);
      font-size: 21px;
      max-width: 760px;
    }}
    .steps {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin: 36px 0;
    }}
    article, .panel {{
      background: rgba(16, 27, 43, .88);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 22px;
    }}
    article span {{
      color: var(--accent2);
      font-weight: 850;
      text-transform: uppercase;
      font-size: 12px;
    }}
    h2 {{
      font-size: 26px;
      letter-spacing: 0;
      margin: 10px 0;
    }}
    p, li {{
      color: var(--muted);
    }}
    a {{
      color: #06121f;
      background: var(--accent);
      display: inline-flex;
      border-radius: 8px;
      font-weight: 850;
      margin-top: 10px;
      padding: 10px 14px;
      text-decoration: none;
    }}
    .grid {{
      display: grid;
      gap: 14px;
      grid-template-columns: 1fr 1fr;
    }}
    ul {{
      padding-left: 20px;
    }}
    .counts {{
      list-style: none;
      padding: 0;
    }}
    .counts li {{
      border-bottom: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
    }}
    code {{
      color: var(--accent);
    }}
    @media (max-width: 760px) {{
      .steps, .grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="eyebrow">Fastest honest evidence path</div>
    <h1>Review Data Quality Agent in 2 minutes</h1>
    <p class="lede">{html.escape(payload["purpose"])}</p>
    <section class="steps">{cards}</section>
    <section class="grid">
      <div class="panel">
        <h2>Required evidence</h2>
        <ul>{evidence}</ul>
      </div>
      <div class="panel">
        <h2>Current counts</h2>
        <ul class="counts">{counts}</ul>
        <p>Success: {html.escape(payload["success_definition"])}</p>
      </div>
    </section>
  </main>
</body>
</html>
"""


def verify_two_minute_review_card(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["time_budget_minutes"] != 2:
        raise AssertionError("two-minute review card must keep the time budget at two minutes")
    if payload["micro_step_count"] != 3:
        raise AssertionError("two-minute review card must define three micro-steps")
    if payload["required_evidence_count"] != 5:
        raise AssertionError("two-minute review card must define five required evidence fields")
    if any(step["counts_as_outcome"] for step in payload["micro_steps"]):
        raise AssertionError("micro-steps must not count as outcomes before public evidence is submitted")
    if any(count != 0 for count in payload["current_counts"].values()):
        raise AssertionError("two-minute review card must preserve zero current outcome counts")
    if "non-owner GitHub issue" not in payload["success_definition"]:
        raise AssertionError("two-minute review card must require non-owner public evidence")
    if "production adoption" not in payload["not_claimed"]:
        raise AssertionError("two-minute review card must not claim production adoption")
    return {
        "two_minute_review_card_verified": True,
        "micro_step_count": payload["micro_step_count"],
        "required_evidence_count": payload["required_evidence_count"],
        "current_count_sum": sum(payload["current_counts"].values()),
    }


def main() -> None:
    payload = build_two_minute_review_card()
    verify_two_minute_review_card(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
