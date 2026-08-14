import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
REVIEWER_SUBMISSION_HUB_PATH = ROOT / "docs" / "reviewer-submission-hub.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "pilot-evidence-quicklink.json"
OUTPUT_MD_PATH = ROOT / "docs" / "pilot-evidence-quicklink.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "pilot-evidence-quicklink.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _channel_url(feedback: dict[str, Any], name: str) -> str:
    for channel in feedback["feedback_channels"]:
        if channel["name"] == name:
            return channel["url"]
    raise KeyError(name)


def build_pilot_evidence_quicklink() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    submission_hub = load_json(REVIEWER_SUBMISSION_HUB_PATH)
    repo = adoption["repo"]
    actions = [
        {
            "id": "try_public_demo",
            "label": "Try the public demo",
            "time_box_minutes": 5,
            "open_url": adoption["public_demo"],
            "submit_url": _channel_url(feedback, "Demo feedback"),
            "target_metric": "external_feedback_items",
            "counts_after": "non-owner public feedback issue with permission to count",
            "evidence_to_submit": [
                "which screen or result you inspected",
                "one thing that was useful or credible",
                "one confusing or missing part",
                "permission to count this as public feedback",
            ],
        },
        {
            "id": "run_container_or_local",
            "label": "Run the container or local demo",
            "time_box_minutes": 8,
            "open_url": "https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html",
            "submit_url": f"{repo}/issues/new?template=external_run_review.md",
            "target_metric": "confirmed_external_users",
            "counts_after": "public observed-result evidence from a non-owner reviewer",
            "evidence_to_submit": [
                "command, URL, or page used",
                "environment",
                "observed result",
                "permission to count this as an external run",
            ],
        },
        {
            "id": "replay_business_data",
            "label": "Replay business-shaped data",
            "time_box_minutes": 10,
            "open_url": f"{repo}/blob/main/docs/business-data-replay-packet.md",
            "submit_url": f"{repo}/issues/new?template=business_data_replay.md",
            "target_metric": "reproducible_feedback_items",
            "counts_after": "redacted replay evidence with dataset shape, agent trace, and permission to count",
            "evidence_to_submit": [
                "command or endpoint used",
                "dataset shape and non-sensitive field names",
                "report status and finding count",
                "selected tools shown in the agent trace",
                "what the agent caught or missed",
            ],
        },
        {
            "id": "submit_business_problem",
            "label": "Submit an anonymized business problem",
            "time_box_minutes": 10,
            "open_url": f"{repo}/blob/main/docs/business-case-intake.md",
            "submit_url": _channel_url(feedback, "Business case review"),
            "target_metric": "business_case_feedback_items",
            "counts_after": "anonymized public issue with no raw production data",
            "evidence_to_submit": [
                "workflow affected",
                "data-quality failure mode",
                "why it matters operationally",
                "permission to count anonymized business-case evidence",
            ],
        },
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_pilot_evidence_quicklink.py",
        "page": "docs/pilot-evidence-quicklink.html",
        "public_url": "https://sunnnn2005.github.io/data-quality-agent/pilot-evidence-quicklink.html",
        "purpose": (
            "Give a reviewer one short public link that routes them to four countable pilot-evidence actions "
            "while preserving zero-user, zero-feedback, zero-replay, and zero-business-case baselines until public "
            "evidence exists."
        ),
        "action_count": len(actions),
        "actions": actions,
        "target_metric_count": len({action["target_metric"] for action in actions}),
        "total_evidence_fields": sum(len(action["evidence_to_submit"]) for action in actions),
        "source_submission_hub_paths": submission_hub["submission_path_count"],
        "current_counts": {
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
            "business_case_feedback_items": feedback["business_case_feedback_items"],
            "github_stars": adoption["stars"],
        },
        "resume_safe_summary": (
            "Published a CI-verified pilot evidence quicklink that gives external reviewers 4 short evidence actions, "
            "17 required evidence fields, public submission links, and explicit zero-count baselines before any outcome "
            "claim is upgraded."
        ),
        "not_claimed": [
            "external users",
            "customer feedback",
            "external reproducible replays",
            "submitted external business cases",
            "GitHub stars beyond the current public count",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    action_rows = "\n".join(
        "| {label} | {time_box_minutes} | `{target_metric}` | [Open]({open_url}) | [Submit]({submit_url}) | {counts_after} |".format(
            **action
        )
        for action in payload["actions"]
    )
    evidence_sections = "\n\n".join(
        "### {label}\n\n".format(**action)
        + "\n".join(f"- {field}" for field in action["evidence_to_submit"])
        for action in payload["actions"]
    )
    counts = "\n".join(
        f"| {key} | {value} |" for key, value in payload["current_counts"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Pilot Evidence Quicklink

{payload["purpose"]}

Public page: [{payload["public_url"]}]({payload["public_url"]})

## {payload["action_count"]} Countable Actions

| Action | Minutes | Target Metric | Open | Submit Evidence | Counting Rule |
| --- | ---: | --- | --- | --- | --- |
{action_rows}

## Evidence Fields

{evidence_sections}

## Current Counts

| Metric | Current Count |
| --- | ---: |
{counts}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def render_html(payload: dict[str, Any]) -> str:
    cards = "\n".join(
        f"""
        <article>
          <span>{action['time_box_minutes']} min</span>
          <h2>{action['label']}</h2>
          <p>Counts toward <code>{action['target_metric']}</code> only after {action['counts_after']}.</p>
          <ul>{"".join(f"<li>{field}</li>" for field in action["evidence_to_submit"])}</ul>
          <div class="card-actions">
            <a href="{action['open_url']}">Open</a>
            <a href="{action['submit_url']}">Submit evidence</a>
          </div>
        </article>
        """.strip()
        for action in payload["actions"]
    )
    counts = "\n".join(
        f"<li><code>{key}</code>: {value}</li>" for key, value in payload["current_counts"].items()
    )
    not_claimed = "\n".join(f"<li>{item}</li>" for item in payload["not_claimed"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pilot Evidence Quicklink | Data Quality Agent</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #07090d;
      --panel: #111823;
      --line: #293241;
      --text: #f8fafc;
      --muted: #a6b3c3;
      --accent: #38bdf8;
      --green: #86efac;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: radial-gradient(circle at 18% 10%, rgba(56, 189, 248, .16), transparent 28%), var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{ width: min(1080px, calc(100% - 36px)); margin: 0 auto; padding: 46px 0; }}
    header {{ min-height: 48vh; display: grid; align-items: center; }}
    .eyebrow {{ color: var(--green); font-size: 13px; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; }}
    h1 {{ font-size: clamp(42px, 8vw, 86px); line-height: .95; letter-spacing: 0; margin: 12px 0 18px; max-width: 920px; }}
    .lede {{ color: var(--muted); font-size: clamp(18px, 2vw, 22px); max-width: 780px; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }}
    article, section {{ background: rgba(17, 24, 35, .9); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
    article span {{ color: var(--green); font-weight: 900; text-transform: uppercase; }}
    h2 {{ margin: 8px 0 10px; }}
    p, li {{ color: var(--muted); }}
    code {{ color: #dbeafe; }}
    .card-actions {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }}
    a {{ align-items: center; background: var(--text); border-radius: 8px; color: #071016; display: inline-flex; font-weight: 850; min-height: 42px; padding: 0 14px; text-decoration: none; }}
    a + a {{ background: var(--accent); color: #04111a; }}
    section {{ margin-top: 16px; }}
    @media (max-width: 860px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <div class="eyebrow">Pilot evidence quicklink</div>
        <h1>One link for real feedback, runs, and business problems.</h1>
        <p class="lede">{payload["purpose"]}</p>
      </div>
    </header>
    <div class="grid">{cards}</div>
    <section>
      <h2>Current counts stay honest</h2>
      <ul>{counts}</ul>
    </section>
    <section>
      <h2>Not claimed yet</h2>
      <ul>{not_claimed}</ul>
    </section>
    <section>
      <h2>Resume-safe summary</h2>
      <p>{payload["resume_safe_summary"]}</p>
    </section>
  </main>
</body>
</html>
"""


def verify_pilot_evidence_quicklink(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["action_count"] != 4:
        raise AssertionError("pilot evidence quicklink must expose 4 short evidence actions")
    if payload["target_metric_count"] != 4:
        raise AssertionError("pilot evidence quicklink must target 4 outcome metrics")
    if payload["total_evidence_fields"] != 17:
        raise AssertionError("pilot evidence quicklink must collect 17 evidence fields")
    if payload["source_submission_hub_paths"] != 7:
        raise AssertionError("pilot evidence quicklink must be grounded in the seven-path submission hub")
    if any(value != 0 for value in payload["current_counts"].values() if isinstance(value, int)):
        raise AssertionError("pilot evidence quicklink must preserve zero-count outcome baselines")
    for required in ("external users", "customer feedback", "submitted external business cases"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"pilot evidence quicklink must not claim {required}")
    html = render_html(payload)
    for fragment in (
        "Pilot evidence quicklink",
        "Try the public demo",
        "Run the container or local demo",
        "Replay business-shaped data",
        "Submit an anonymized business problem",
        "Current counts stay honest",
        "Not claimed yet",
    ):
        if fragment not in html:
            raise AssertionError(f"pilot evidence quicklink missing HTML fragment: {fragment}")
    return {
        "pilot_evidence_quicklink_verified": True,
        "action_count": payload["action_count"],
        "total_evidence_fields": payload["total_evidence_fields"],
    }


def main() -> None:
    payload = build_pilot_evidence_quicklink()
    verify_pilot_evidence_quicklink(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
