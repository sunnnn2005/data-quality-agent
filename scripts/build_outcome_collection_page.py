import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACTION_CHECKLIST_PATH = ROOT / "docs" / "resume-outcome-action-checklist.json"
SUBMISSION_HUB_PATH = ROOT / "docs" / "reviewer-submission-hub.json"
PUBLIC_METRICS_PATH = ROOT / "docs" / "public-metrics-summary.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "outcome-collection.json"
OUTPUT_HTML_PATH = ROOT / "docs" / "outcome-collection.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_outcome_collection_payload() -> dict[str, Any]:
    checklist = load_json(ACTION_CHECKLIST_PATH)
    submission_hub = load_json(SUBMISSION_HUB_PATH)
    public_metrics = load_json(PUBLIC_METRICS_PATH)
    metrics = public_metrics["public_metrics"]
    actions = [
        {
            "id": action["id"],
            "title": action["title"],
            "target_metric": action["target_metric"],
            "current_count": action["current_count"],
            "remaining_to_claim": action["remaining_to_claim"],
            "owner_action": action["owner_action"],
            "completion_check": action["completion_check"],
            "evidence_path": action["evidence_path"],
            "status": action["status"],
        }
        for action in checklist["actions"]
    ]
    submission_paths = [
        {
            "id": path["id"],
            "target_metric": path["target_metric"],
            "minutes": path["minimum_minutes"],
            "review_url": path["review_path"],
            "submit_url": path["submission_url"],
            "counting_rule": path["counting_rule"],
        }
        for path in submission_hub["submission_paths"]
    ]
    payload = {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_outcome_collection_page.py",
        "purpose": (
            "Give external reviewers one public page for trying the project, submitting countable evidence, "
            "and seeing which outcome claims are still blocked."
        ),
        "actions": actions,
        "submission_paths": submission_paths,
        "tracked_action_count": checklist["tracked_action_count"],
        "submission_path_count": submission_hub["submission_path_count"],
        "required_evidence_field_count": submission_hub["total_required_evidence_fields"],
        "current_counts": {
            "confirmed_external_users": metrics["confirmed_external_users"],
            "external_feedback_items": metrics["external_feedback_items"],
            "github_stars": metrics["stars"],
            "github_forks": metrics["forks"],
            "passing_tests": metrics["test_count"],
        },
        "not_claimed": [
            "No external users are claimed while confirmed_external_users is zero.",
            "No customer feedback is claimed while external_feedback_items is zero.",
            "No GitHub star growth is claimed while stars is zero.",
            "Do not post raw customer data, secrets, private emails, addresses, API keys, or production rows.",
        ],
        "resume_safe_summary": (
            f"Published a public outcome collection page with {checklist['tracked_action_count']} next actions, "
            f"{submission_hub['submission_path_count']} submission paths, "
            f"{submission_hub['total_required_evidence_fields']} required evidence fields, "
            f"{metrics['confirmed_external_users']} confirmed users, "
            f"{metrics['external_feedback_items']} feedback items, and {metrics['stars']} GitHub stars."
        ),
    }
    return payload


def render_html(payload: dict[str, Any]) -> str:
    action_cards = "\n".join(
        f"""
        <article class="card">
          <div class="tag">{action["target_metric"]}</div>
          <h3>{action["title"]}</h3>
          <p>{action["owner_action"]}</p>
          <p><strong>Done when:</strong> {action["completion_check"]}</p>
          <a href="{action["evidence_path"]}">Evidence path</a>
        </article>
        """
        for action in payload["actions"]
    )
    submission_cards = "\n".join(
        f"""
        <article class="path">
          <div>
            <span>{path["minutes"]} min</span>
            <h3>{path["id"].replace("_", " ").title()}</h3>
            <p>{path["counting_rule"]}</p>
          </div>
          <div class="path-actions">
            <a class="button secondary" href="{path["review_url"]}">Review</a>
            <a class="button" href="{path["submit_url"]}">Submit Evidence</a>
          </div>
        </article>
        """
        for path in payload["submission_paths"]
    )
    counts = payload["current_counts"]
    not_claimed = "\n".join(f"<li>{item}</li>" for item in payload["not_claimed"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Data Quality Agent Outcome Collection</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0b0f14;
      --panel: #121821;
      --panel-2: #182131;
      --text: #f6f8fb;
      --muted: #a9b5c9;
      --line: #2b3548;
      --accent: #5eead4;
      --accent-2: #8ab4ff;
      --warn: #ffd166;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at 16% 4%, rgba(94, 234, 212, .16), transparent 28rem),
        radial-gradient(circle at 88% 0%, rgba(138, 180, 255, .16), transparent 30rem),
        var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    a {{ color: inherit; }}
    .shell {{ width: min(1120px, calc(100% - 40px)); margin: 0 auto; padding: 48px 0; }}
    header {{ display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(280px, .9fr); gap: 28px; align-items: center; min-height: 64vh; }}
    .eyebrow {{ color: var(--accent); font-size: 13px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }}
    h1 {{ font-size: clamp(42px, 7vw, 78px); letter-spacing: 0; line-height: .95; margin: 14px 0 18px; }}
    .lede {{ color: var(--muted); font-size: clamp(18px, 2.2vw, 23px); max-width: 760px; margin: 0 0 24px; }}
    .actions, .path-actions {{ display: flex; flex-wrap: wrap; gap: 10px; }}
    .button {{ align-items: center; background: var(--accent); border: 1px solid rgba(255,255,255,.12); border-radius: 8px; color: #061f1b; display: inline-flex; font-weight: 800; min-height: 42px; padding: 0 14px; text-decoration: none; }}
    .button.secondary {{ background: rgba(255,255,255,.07); color: var(--text); }}
    .metrics {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .metric, .card, .path, .guardrail {{ background: rgba(18, 24, 33, .9); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
    .metric strong {{ display: block; font-size: 34px; line-height: 1; margin-bottom: 6px; }}
    .metric span, .card p, .path p, .guardrail li {{ color: var(--muted); }}
    section {{ border-top: 1px solid var(--line); padding: 42px 0; }}
    h2 {{ font-size: clamp(28px, 4vw, 42px); letter-spacing: 0; line-height: 1; margin: 0 0 16px; }}
    .section-copy {{ color: var(--muted); max-width: 840px; margin: 0 0 22px; font-size: 17px; }}
    .cards {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; }}
    .card h3, .path h3 {{ margin: 8px 0; font-size: 18px; }}
    .tag, .path span {{ color: var(--warn); font-size: 12px; font-weight: 900; text-transform: uppercase; }}
    .paths {{ display: grid; gap: 12px; }}
    .path {{ display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 16px; align-items: center; }}
    .guardrail ul {{ margin: 0; padding-left: 18px; }}
    footer {{ color: var(--muted); border-top: 1px solid var(--line); padding: 28px 0 0; }}
    @media (max-width: 860px) {{
      header, .path {{ grid-template-columns: 1fr; }}
      .cards, .metrics {{ grid-template-columns: 1fr; }}
      .shell {{ width: min(100% - 28px, 1120px); padding: 28px 0; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <header>
      <div>
        <div class="eyebrow">Public outcome collection</div>
        <h1>Turn reviews into resume-safe evidence</h1>
        <p class="lede">
          This page gives reviewers one public path to try Data Quality Agent, submit evidence, and help convert
          currently blocked outcome claims into verified resume signals.
        </p>
        <div class="actions">
          <a class="button" href="review.html">Start 8-minute review</a>
          <a class="button secondary" href="reviewer-submission-hub.md">Submission hub</a>
          <a class="button secondary" href="resume-outcome-action-checklist.md">Action checklist</a>
          <a class="button secondary" href="public-metrics-summary.md">Public metrics</a>
        </div>
      </div>
      <div class="metrics" aria-label="Current outcome counts">
        <div class="metric"><strong>{counts["confirmed_external_users"]}</strong><span>confirmed external users</span></div>
        <div class="metric"><strong>{counts["external_feedback_items"]}</strong><span>public feedback items</span></div>
        <div class="metric"><strong>{counts["github_stars"]}</strong><span>public GitHub stars</span></div>
        <div class="metric"><strong>{counts["passing_tests"]}</strong><span>passing tests</span></div>
      </div>
    </header>

    <section>
      <h2>Next Outcome Actions</h2>
      <p class="section-copy">{payload["purpose"]}</p>
      <div class="cards">{action_cards}
      </div>
    </section>

    <section>
      <h2>Submit Evidence</h2>
      <p class="section-copy">
        Countable evidence must be public, non-owner, permissioned, and free of raw private data.
      </p>
      <div class="paths">{submission_cards}
      </div>
    </section>

    <section>
      <h2>Counting Boundaries</h2>
      <div class="guardrail">
        <ul>{not_claimed}</ul>
      </div>
    </section>

    <footer>
      Generated by <code>{payload["generated_by"]}</code>. {payload["resume_safe_summary"]}
    </footer>
  </main>
</body>
</html>
"""


def verify_outcome_collection_payload(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "tracked_action_count": 5,
        "submission_path_count": 6,
        "required_evidence_field_count": 23,
        "confirmed_external_users": 0,
        "external_feedback_items": 0,
        "github_stars": 0,
        "passing_tests": 147,
    }
    if payload["tracked_action_count"] != expected["tracked_action_count"]:
        raise AssertionError("outcome collection page must expose five next actions")
    if payload["submission_path_count"] != expected["submission_path_count"]:
        raise AssertionError("outcome collection page must expose six submission paths")
    if payload["required_evidence_field_count"] != expected["required_evidence_field_count"]:
        raise AssertionError("outcome collection page must preserve 23 evidence fields")
    counts = payload["current_counts"]
    for key in ("confirmed_external_users", "external_feedback_items", "github_stars", "passing_tests"):
        if counts[key] != expected[key]:
            raise AssertionError(f"{key} expected {expected[key]!r}, got {counts[key]!r}")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("permission", "public", "raw customer data", "github stars"):
        if required not in joined:
            raise AssertionError(f"outcome collection page missing boundary: {required}")
    return {"outcome_collection_page_verified": True, **expected}


def main() -> None:
    payload = build_outcome_collection_payload()
    verify_outcome_collection_payload(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
