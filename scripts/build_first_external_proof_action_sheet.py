import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIRST_REQUEST_PATH = ROOT / "docs" / "first-outcome-evidence-request.json"
SUBMISSION_HUB_PATH = ROOT / "docs" / "reviewer-submission-hub.json"
LIVE_PROOF_PATH = ROOT / "docs" / "resume-live-proof-snapshot.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "first-external-proof-action-sheet.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-external-proof-action-sheet.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "first-external-proof-action-sheet.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_first_external_proof_action_sheet() -> dict[str, Any]:
    first_request = load_json(FIRST_REQUEST_PATH)
    submission_hub = load_json(SUBMISSION_HUB_PATH)
    live_proof = load_json(LIVE_PROOF_PATH)
    ai_path = next(
        path for path in submission_hub["submission_paths"] if path["target_metric"] == "ai_engineer_review_items"
    )
    demo_path = next(
        path for path in submission_hub["submission_paths"] if path["target_metric"] == "external_feedback_items"
    )
    replay_path = next(
        path for path in submission_hub["submission_paths"] if path["target_metric"] == "reproducible_feedback_items"
    )
    reviewer_targets = [
        {
            "rank": 1,
            "reviewer_type": "AI/ML engineer, mentor, or advanced CS/data science peer",
            "why_this_first": "This unlocks the strongest AI Engineer Intern resume signal if the issue passes the gate.",
            "target_metric": "ai_engineer_review_items",
            "entry_url": first_request["request_page_url"],
            "submission_url": ai_path["submission_url"],
            "record_sent_command": first_request["record_sent_command"],
            "copy_ready_message": first_request["copy_ready_message"],
            "acceptance_gate": first_request["acceptance_gate"],
        },
        {
            "rank": 2,
            "reviewer_type": "Classmate or student developer who can open the public demo",
            "why_this_first": "This is the fastest path to one concrete external feedback item.",
            "target_metric": "external_feedback_items",
            "entry_url": "https://sunnnn2005.github.io/data-quality-agent/two-minute-review-card.html",
            "submission_url": demo_path["submission_url"],
            "record_sent_command": (
                'python scripts/record_reviewer_outreach_event.py --slot-id review_slot_01 --status sent '
                '--reviewer-contact "<reviewer name or handle>" --channel-used "class Discord, LinkedIn DM, or text" '
                '--note "Sent two-minute demo feedback request"'
            ),
            "copy_ready_message": (
                "Could you spend 2 minutes reviewing my Data Quality Agent demo? Open this card, inspect one "
                "result, and leave one concrete public note if you are comfortable: "
                "https://sunnnn2005.github.io/data-quality-agent/two-minute-review-card.html"
            ),
            "acceptance_gate": "A non-owner public feedback issue includes one concrete observation and permission to count.",
        },
        {
            "rank": 3,
            "reviewer_type": "Developer comfortable with Docker or local API testing",
            "why_this_first": "This can prove the project is runnable outside the owner machine.",
            "target_metric": "reproducible_feedback_items",
            "entry_url": replay_path["review_path"],
            "submission_url": replay_path["submission_url"],
            "record_sent_command": (
                'python scripts/record_reviewer_outreach_event.py --slot-id review_slot_03 --status sent '
                '--reviewer-contact "<reviewer name or handle>" --channel-used "GitHub, Discord, or LinkedIn DM" '
                '--note "Sent reproducible local replay request"'
            ),
            "copy_ready_message": (
                "Could you try a reproducible run of my Data Quality Agent and leave public redacted evidence "
                "only if it works for you? Start here: "
                "https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html"
            ),
            "acceptance_gate": (
                "A non-owner public issue includes the command or URL used, observed result, environment, and "
                "permission to count."
            ),
        },
    ]
    required_success_fields = [
        "reviewer is not the repository owner",
        "public GitHub issue URL exists",
        "issue includes explicit permission to count",
        "issue confirms no private data was posted",
        "issue has one concrete observed result",
        "external reviewer evidence gate accepts it",
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_external_proof_action_sheet.py",
        "public_url": "https://sunnnn2005.github.io/data-quality-agent/first-external-proof-action-sheet.html",
        "purpose": (
            "Turn the first resume-outcome goal into a single action sheet for getting one real, public, "
            "non-owner evidence item without inflating users, feedback, stars, or business impact."
        ),
        "priority_outcome": "first accepted external evidence item",
        "primary_target_metric": first_request["target_metric"],
        "current_accepted_external_evidence": first_request["accepted_external_evidence_count"],
        "current_github_stars": live_proof["verified_now"]["github_stars"],
        "current_confirmed_external_users": 0,
        "reviewer_target_count": len(reviewer_targets),
        "reviewer_targets": reviewer_targets,
        "required_success_field_count": len(required_success_fields),
        "required_success_fields": required_success_fields,
        "today_execution_order": [
            "Send rank 1 AI Engineer review request to one real reviewer.",
            "Record only the sent outreach event after sending it.",
            "If no response after two days, send the follow-up from first-outcome-evidence-request.md.",
            "Do not update resume outcome metrics until the public issue passes the evidence gate.",
        ],
        "resume_unlock_after_acceptance": first_request["future_resume_line"],
        "counting_boundary": (
            "This action sheet and any sent message are distribution evidence only. Resume outcome metrics stay at "
            "zero until a non-owner public GitHub issue passes the external reviewer evidence gate."
        ),
        "not_claimed": [
            "No external feedback is claimed by this action sheet.",
            "No confirmed user is claimed by this action sheet.",
            "No business impact is claimed by this action sheet.",
            "No GitHub star growth is claimed by this action sheet.",
            "No AI Engineer review is claimed until a non-owner issue passes the gate.",
        ],
        "resume_safe_summary": (
            "Published a first external proof action sheet with 3 prioritized reviewer targets, 3 copy-ready asks, "
            "6 required success fields, recorder commands, and zero upgraded resume outcomes."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    target_rows = "\n".join(
        "| {rank} | {reviewer_type} | `{target_metric}` | [Start]({entry_url}) | [Submit]({submission_url}) |".format(
            **target
        )
        for target in payload["reviewer_targets"]
    )
    message_blocks = "\n\n".join(
        "### Rank {rank}: {target_metric}\n\n```text\n{copy_ready_message}\n```\n\nRecord after sending:\n\n```bash\n{record_sent_command}\n```".format(
            **target
        )
        for target in payload["reviewer_targets"]
    )
    success_fields = "\n".join(f"- {item}" for item in payload["required_success_fields"])
    execution_order = "\n".join(f"{index}. {item}" for index, item in enumerate(payload["today_execution_order"], 1))
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# First External Proof Action Sheet

{payload["purpose"]}

Public page: [{payload["public_url"]}]({payload["public_url"]})

## Current Status

| Metric | Value |
| --- | ---: |
| Accepted external evidence | {payload["current_accepted_external_evidence"]} |
| GitHub stars | {payload["current_github_stars"]} |
| Confirmed external users | {payload["current_confirmed_external_users"]} |
| Reviewer targets | {payload["reviewer_target_count"]} |
| Required success fields | {payload["required_success_field_count"]} |

## Today Execution Order

{execution_order}

## Reviewer Targets

| Rank | Reviewer | Target Metric | Start | Submit |
| ---: | --- | --- | --- | --- |
{target_rows}

## Copy-Ready Messages

{message_blocks}

## Required Success Fields

{success_fields}

## Resume Unlock After Acceptance

Locked until evidence passes:

```text
{payload["resume_unlock_after_acceptance"]}
```

## Counting Boundary

{payload["counting_boundary"]}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def render_html(payload: dict[str, Any]) -> str:
    cards = "".join(
        f"""
        <article>
          <span>Rank {target['rank']}</span>
          <h2>{html.escape(target['target_metric'])}</h2>
          <p>{html.escape(target['reviewer_type'])}</p>
          <p>{html.escape(target['why_this_first'])}</p>
          <a href="{html.escape(target['entry_url'], quote=True)}">Start</a>
          <a href="{html.escape(target['submission_url'], quote=True)}">Submit evidence</a>
        </article>
        """
        for target in payload["reviewer_targets"]
    )
    messages = "".join(
        f"""
        <section>
          <h2>Rank {target['rank']} Message</h2>
          <pre>{html.escape(target['copy_ready_message'])}</pre>
          <h3>Record after sending</h3>
          <pre>{html.escape(target['record_sent_command'])}</pre>
        </section>
        """
        for target in payload["reviewer_targets"]
    )
    success_fields = "".join(f"<li>{html.escape(item)}</li>" for item in payload["required_success_fields"])
    execution_order = "".join(f"<li>{html.escape(item)}</li>" for item in payload["today_execution_order"])
    not_claimed = "".join(f"<li>{html.escape(item)}</li>" for item in payload["not_claimed"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>First External Proof Action Sheet</title>
  <style>
    :root {{ color-scheme: dark; --bg: #0b1020; --panel: #131b2d; --line: #2a3954; --text: #f8fafc; --muted: #aab6ca; --green: #4ade80; --cyan: #67e8f9; --pink: #fb2f78; --amber: #fbbf24; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: linear-gradient(135deg, #0b1020 0%, #111827 100%); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    main {{ width: min(1120px, calc(100% - 36px)); margin: 0 auto; padding: 48px 0 72px; }}
    h1 {{ margin: 0 0 12px; font-size: clamp(42px, 7vw, 76px); line-height: .95; letter-spacing: 0; }}
    h2 {{ margin: 0 0 12px; font-size: 23px; letter-spacing: 0; }}
    h3 {{ margin: 16px 0 8px; }}
    p, li {{ color: var(--muted); line-height: 1.55; }}
    .lede {{ max-width: 820px; font-size: 19px; }}
    .stats, .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin: 28px 0; }}
    .stat, article, section {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
    .stat strong {{ display: block; font-size: 34px; }}
    article span {{ color: var(--green); font-weight: 800; text-transform: uppercase; font-size: 13px; }}
    a {{ display: inline-block; margin: 6px 8px 0 0; color: #06111f; background: var(--cyan); border-radius: 6px; padding: 9px 12px; text-decoration: none; font-weight: 800; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; background: #080d18; border: 1px solid var(--line); border-radius: 6px; padding: 14px; color: var(--text); }}
    .locked {{ color: var(--amber); font-weight: 800; }}
  </style>
</head>
<body>
<main>
  <h1>First External Proof Action Sheet</h1>
  <p class="lede">{html.escape(payload["purpose"])}</p>
  <div class="stats">
    <div class="stat"><strong>{payload["current_accepted_external_evidence"]}</strong><span>accepted external evidence</span></div>
    <div class="stat"><strong>{payload["current_github_stars"]}</strong><span>GitHub stars</span></div>
    <div class="stat"><strong>{payload["current_confirmed_external_users"]}</strong><span>confirmed external users</span></div>
    <div class="stat"><strong>{payload["reviewer_target_count"]}</strong><span>reviewer targets</span></div>
  </div>
  <section>
    <h2>Today Execution Order</h2>
    <ol>{execution_order}</ol>
  </section>
  <div class="cards">{cards}</div>
  {messages}
  <section>
    <h2>Required Success Fields</h2>
    <ul>{success_fields}</ul>
  </section>
  <section>
    <h2>Locked Resume Line</h2>
    <p class="locked">Locked until the external reviewer evidence gate passes.</p>
    <pre>{html.escape(payload["resume_unlock_after_acceptance"])}</pre>
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


def verify_first_external_proof_action_sheet(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["current_accepted_external_evidence"] != 0:
        raise AssertionError("action sheet must not claim accepted external evidence")
    if payload["current_github_stars"] != 0:
        raise AssertionError("action sheet must preserve the current zero-star baseline")
    if payload["reviewer_target_count"] != 3:
        raise AssertionError("action sheet must expose exactly three prioritized reviewer targets")
    if payload["required_success_field_count"] != 6:
        raise AssertionError("action sheet must define six required success fields")
    if payload["primary_target_metric"] != "ai_engineer_review_items":
        raise AssertionError("first proof action sheet must prioritize the AI Engineer review metric")
    target_metrics = {target["target_metric"] for target in payload["reviewer_targets"]}
    if target_metrics != {"ai_engineer_review_items", "external_feedback_items", "reproducible_feedback_items"}:
        raise AssertionError("action sheet must cover AI review, feedback, and reproducible-run paths")
    for target in payload["reviewer_targets"]:
        if not target["entry_url"].startswith("https://"):
            raise AssertionError("reviewer target entry URLs must be public")
        if not target["submission_url"].startswith("https://github.com/"):
            raise AssertionError("reviewer target submission URLs must use public GitHub issue surfaces")
        if "record_reviewer_outreach_event.py" not in target["record_sent_command"]:
            raise AssertionError("each reviewer target must include a sent-event recorder command")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in (
        "distribution evidence only",
        "non-owner public github issue",
        "permission to count",
        "no private data",
        "no ai engineer review is claimed",
        "zero upgraded resume outcomes",
    ):
        if phrase not in joined:
            raise AssertionError(f"action sheet missing safety boundary: {phrase}")
    return {
        "first_external_proof_action_sheet_verified": True,
        "reviewer_target_count": payload["reviewer_target_count"],
        "required_success_field_count": payload["required_success_field_count"],
        "current_accepted_external_evidence": payload["current_accepted_external_evidence"],
    }


def main() -> None:
    payload = build_first_external_proof_action_sheet()
    verification = verify_first_external_proof_action_sheet(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
