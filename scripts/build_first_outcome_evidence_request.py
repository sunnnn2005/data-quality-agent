import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "docs" / "first-reviewer-handoff.json"
AI_REVIEWER_CARD_PATH = ROOT / "docs" / "ai-engineer-reviewer-card.json"
OUTCOME_INTAKE_PATH = ROOT / "docs" / "public-outcome-intake-dashboard.json"
ACCEPTED_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "first-outcome-evidence-request.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-outcome-evidence-request.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "first-outcome-evidence-request.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_first_outcome_evidence_request() -> dict[str, Any]:
    handoff = load_json(HANDOFF_PATH)
    reviewer_card = load_json(AI_REVIEWER_CARD_PATH)
    outcome_intake = load_json(OUTCOME_INTAKE_PATH)
    accepted_rollup = load_json(ACCEPTED_ROLLUP_PATH)

    target_path = next(
        path
        for path in outcome_intake["blocked_intake_paths"]
        if path["metric"] == handoff["target_metric"]
    )

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_outcome_evidence_request.py",
        "purpose": (
            "Create one public, sendable request for the first resume-countable external outcome: "
            "an AI Engineer review submitted by a non-owner reviewer through a public GitHub issue."
        ),
        "request_page_url": "https://sunnnn2005.github.io/data-quality-agent/first-outcome-evidence-request.html",
        "target_metric": handoff["target_metric"],
        "current_count": handoff["current_count"],
        "required_count": handoff["required_count"],
        "remaining_to_unlock": target_path["remaining"],
        "accepted_external_evidence_count": accepted_rollup["accepted_issue_count"],
        "reviewer_profile": handoff["reviewer_profile"],
        "recommended_channel": handoff["recommended_channel"],
        "who_to_choose": handoff["who_to_choose"],
        "review_minutes": reviewer_card["review_minutes"],
        "entry_url": handoff["entry_url"],
        "submission_url": handoff["submission_url"],
        "public_tracking_issue_url": handoff["public_issue_url"],
        "copy_ready_message": handoff["copy_ready_message"],
        "copy_ready_follow_up": handoff["copy_ready_follow_up"],
        "inspection_targets": reviewer_card["inspection_targets"],
        "review_prompts": reviewer_card["review_prompts"],
        "required_public_fields": handoff["required_public_fields"],
        "acceptance_gate": handoff["evidence_gate"],
        "manual_acceptance_rule": handoff["manual_acceptance_rule"],
        "record_sent_command": handoff["record_sent_command"],
        "future_resume_line": handoff["future_resume_line"],
        "resume_status": "first_external_outcome_request_ready_not_claimable",
        "counting_boundary": (
            "This request page is not evidence by itself. The outcome becomes resume-countable only after a "
            "non-owner public GitHub issue includes permission to count, no private data, inspected paths, and "
            "passes the external reviewer evidence gate."
        ),
        "not_claimed": [
            "No AI Engineer review has been accepted yet.",
            "No reviewer message is recorded as sent yet.",
            "No external user, customer feedback, business impact, production deployment, or GitHub star is claimed.",
            "The future resume line is locked until the public evidence gate passes.",
        ],
        "resume_safe_summary": (
            "Published a first outcome evidence request for one AI Engineer reviewer, with 6 inspection targets, "
            "5 review prompts, public submission links, required evidence fields, and a locked future resume line "
            "while preserving 0 accepted external evidence."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    targets = "\n".join(
        f"- `{item['path']}`: {item['reason']}" for item in payload["inspection_targets"]
    )
    prompts = "\n".join(f"- {item}" for item in payload["review_prompts"])
    fields = "\n".join(f"- {item}" for item in payload["required_public_fields"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# First Outcome Evidence Request

{payload["purpose"]}

Public page: [{payload["request_page_url"]}]({payload["request_page_url"]})

## Current Status

| Metric | Value |
| --- | --- |
| Target metric | `{payload["target_metric"]}` |
| Current count | {payload["current_count"]} |
| Required count | {payload["required_count"]} |
| Remaining to unlock | {payload["remaining_to_unlock"]} |
| Accepted external evidence | {payload["accepted_external_evidence_count"]} |
| Resume status | `{payload["resume_status"]}` |

## Who To Ask

- Reviewer profile: {payload["reviewer_profile"]}
- Recommended channel: {payload["recommended_channel"]}
- Who to choose: {payload["who_to_choose"]}
- Time requested: {payload["review_minutes"]} minutes

## Reviewer Links

- Start page: [{payload["entry_url"]}]({payload["entry_url"]})
- Submission form: [{payload["submission_url"]}]({payload["submission_url"]})
- Public tracking issue: [{payload["public_tracking_issue_url"]}]({payload["public_tracking_issue_url"]})

## Copy-Ready Message

```text
{payload["copy_ready_message"]}
```

## Follow-Up

```text
{payload["copy_ready_follow_up"]}
```

## Inspection Targets

{targets}

## Review Prompts

{prompts}

## Required Public Evidence Fields

{fields}

## Record After Sending

Run only after sending this to a real reviewer:

```bash
{payload["record_sent_command"]}
```

## Acceptance Gate

{payload["acceptance_gate"]}

Manual rule: {payload["manual_acceptance_rule"]}

## Future Resume Line

Locked until evidence passes:

```text
{payload["future_resume_line"]}
```

## Counting Boundary

{payload["counting_boundary"]}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def render_html(payload: dict[str, Any]) -> str:
    targets = "".join(
        f"<li><strong>{html.escape(item['path'])}</strong><span>{html.escape(item['reason'])}</span></li>"
        for item in payload["inspection_targets"]
    )
    prompts = "".join(f"<li>{html.escape(item)}</li>" for item in payload["review_prompts"])
    fields = "".join(f"<li>{html.escape(item)}</li>" for item in payload["required_public_fields"])
    not_claimed = "".join(f"<li>{html.escape(item)}</li>" for item in payload["not_claimed"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>First Outcome Evidence Request</title>
  <style>
    :root {{ color-scheme: dark; --bg: #0c1017; --panel: #151c26; --line: #2f3948; --text: #f7f9fc; --muted: #aeb8c8; --blue: #67d4ff; --pink: #ff2d6f; --green: #42d392; --amber: #ffd166; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 46px 20px 70px; }}
    h1 {{ margin: 0 0 10px; font-size: 46px; letter-spacing: 0; }}
    h2 {{ font-size: 22px; margin: 0 0 14px; letter-spacing: 0; }}
    p, li, span {{ color: var(--muted); line-height: 1.55; }}
    .lede {{ max-width: 820px; font-size: 18px; }}
    .stats, .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; }}
    .stats {{ margin: 28px 0 34px; }}
    .stat, section {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
    .stat strong {{ display: block; font-size: 30px; color: var(--text); }}
    section {{ margin-top: 16px; }}
    a {{ color: var(--blue); font-weight: 800; }}
    .button {{ display: inline-block; margin: 8px 10px 0 0; background: var(--pink); color: white; text-decoration: none; padding: 10px 14px; border-radius: 6px; }}
    code, pre {{ white-space: pre-wrap; color: var(--text); background: #0a0e14; border-radius: 6px; }}
    pre {{ padding: 14px; overflow-x: auto; }}
    li strong {{ display: block; color: var(--text); }}
    .locked {{ color: var(--amber); font-weight: 800; }}
  </style>
</head>
<body>
<main>
  <h1>First Outcome Evidence Request</h1>
  <p class="lede">A single sendable request for the first public, resume-countable external outcome: an AI Engineer review of the Data Quality Agent's tool-calling loop, guardrails, and evidence trail.</p>
  <div class="stats">
    <div class="stat"><strong>{payload["current_count"]}/{payload["required_count"]}</strong><span>accepted AI Engineer reviews</span></div>
    <div class="stat"><strong>{payload["remaining_to_unlock"]}</strong><span>remaining to unlock</span></div>
    <div class="stat"><strong>{payload["review_minutes"]}</strong><span>minutes requested</span></div>
    <div class="stat"><strong>{payload["accepted_external_evidence_count"]}</strong><span>accepted external evidence</span></div>
  </div>
  <section>
    <h2>Send This Review Request</h2>
    <p>{html.escape(payload["who_to_choose"])}</p>
    <a class="button" href="{html.escape(payload["entry_url"], quote=True)}">Open reviewer start page</a>
    <a class="button" href="{html.escape(payload["submission_url"], quote=True)}">Submit public review</a>
    <a href="{html.escape(payload["public_tracking_issue_url"], quote=True)}">Public tracking issue</a>
  </section>
  <section>
    <h2>Copy-Ready Message</h2>
    <pre>{html.escape(payload["copy_ready_message"])}</pre>
  </section>
  <section>
    <h2>Inspection Targets</h2>
    <ul>{targets}</ul>
  </section>
  <section>
    <h2>Review Prompts</h2>
    <ul>{prompts}</ul>
  </section>
  <section>
    <h2>Required Public Evidence</h2>
    <ul>{fields}</ul>
  </section>
  <section>
    <h2>Locked Resume Line</h2>
    <p class="locked">Locked until the public evidence gate passes.</p>
    <pre>{html.escape(payload["future_resume_line"])}</pre>
  </section>
  <section>
    <h2>Counting Boundary</h2>
    <p>{html.escape(payload["counting_boundary"])}</p>
    <h2>Not Claimed</h2>
    <ul>{not_claimed}</ul>
  </section>
</main>
</body>
</html>
"""


def verify_first_outcome_evidence_request(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["target_metric"] != "ai_engineer_review_items":
        raise AssertionError("first outcome request must target the AI Engineer review metric")
    if payload["current_count"] != 0 or payload["accepted_external_evidence_count"] != 0:
        raise AssertionError("first outcome request must preserve zero accepted external evidence")
    if payload["required_count"] != 1 or payload["remaining_to_unlock"] != 1:
        raise AssertionError("first outcome request must require exactly one accepted AI Engineer review")
    if payload["review_minutes"] < 8:
        raise AssertionError("first outcome request must give reviewers enough time to inspect evidence")
    if len(payload["inspection_targets"]) != 6:
        raise AssertionError("first outcome request must expose six inspection targets")
    if len(payload["review_prompts"]) != 5:
        raise AssertionError("first outcome request must expose five review prompts")
    if not payload["submission_url"].startswith("https://github.com/"):
        raise AssertionError("first outcome request must route to a public GitHub submission URL")
    if "{name}" not in payload["copy_ready_message"]:
        raise AssertionError("copy-ready message must preserve the recipient placeholder")
    if "--slot-id review_slot_07" not in payload["record_sent_command"]:
        raise AssertionError("first outcome request must include the review_slot_07 recorder command")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in (
        "non-owner public github issue",
        "permission to count",
        "not evidence by itself",
        "no ai engineer review has been accepted yet",
        "future resume line is locked",
    ):
        if phrase not in joined:
            raise AssertionError(f"first outcome request missing boundary: {phrase}")
    return {
        "first_outcome_evidence_request_verified": True,
        "target_metric": payload["target_metric"],
        "current_count": payload["current_count"],
        "required_count": payload["required_count"],
    }


def main() -> None:
    payload = build_first_outcome_evidence_request()
    verify_first_outcome_evidence_request(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(verify_first_outcome_evidence_request(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
