import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEND_QUEUE_PATH = ROOT / "docs" / "reviewer-send-queue.json"
FIRST_SEND_PATH = ROOT / "docs" / "first-reviewer-send-kit.json"
OUTREACH_STATUS_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "real-reviewer-outreach-playbook.json"
OUTPUT_MD_PATH = ROOT / "docs" / "real-reviewer-outreach-playbook.md"


CONTACT_POOLS = [
    {
        "pool": "UC Davis technical mentor",
        "best_metric": "ai_engineer_review_items",
        "who_to_find": "TA, professor office-hour contact, AI/ML club officer, or advanced CS/data science student",
        "why_it_matters": "This is the strongest first evidence for an AI Engineer Intern resume because the reviewer can inspect architecture, tool calling, and guardrails.",
        "suggested_channel": "LinkedIn, email, Discord, or in-person follow-up",
    },
    {
        "pool": "Student developer peer",
        "best_metric": "confirmed_external_users",
        "who_to_find": "classmate or hackathon peer who can open the public demo and submit a short public run issue",
        "why_it_matters": "One confirmed non-owner run turns the project from only self-published into externally tried.",
        "suggested_channel": "class Discord, club Slack, or direct message",
    },
    {
        "pool": "Developer comfortable with Docker",
        "best_metric": "reproducible_feedback_items",
        "who_to_find": "peer who can run docker compose or inspect the local PostgreSQL replay path",
        "why_it_matters": "Reproducible run evidence is stronger than a casual demo view and supports engineering credibility.",
        "suggested_channel": "GitHub, Discord, or direct message",
    },
    {
        "pool": "Operations or spreadsheet-heavy user",
        "best_metric": "business_case_feedback_items",
        "who_to_find": "student org treasurer, tutoring coordinator, small-business operator, or anyone who has cleaned messy CSVs",
        "why_it_matters": "Business-case feedback is the closest honest substitute for enterprise impact before a real company pilot exists.",
        "suggested_channel": "email, LinkedIn, or in-person ask",
    },
    {
        "pool": "General product reviewer",
        "best_metric": "external_feedback_items",
        "who_to_find": "friend, classmate, or club member who can say what was useful, confusing, or broken",
        "why_it_matters": "Specific product feedback creates a real iteration loop without pretending there are users yet.",
        "suggested_channel": "direct message or class group",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _send_by_metric(send_queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["target_metric"]: item for item in send_queue["next_sends"]}


def _status_slot_for_metric(status_board: dict[str, Any], metric: str) -> dict[str, Any]:
    matches = [slot for slot in status_board["outreach_slots"] if slot["counts_toward"] == metric]
    if metric == "external_feedback_items":
        matches = [slot for slot in matches if slot["reviewer_segment"] == "UC Davis data science peer"]
    if metric == "business_case_feedback_items":
        matches = [slot for slot in matches if slot["reviewer_segment"] == "data analyst or analytics student"]
    if len(matches) != 1:
        raise AssertionError(f"expected one outreach status slot for {metric}, got {len(matches)}")
    return matches[0]


def _outreach_step(
    pool: dict[str, Any],
    send_by_metric: dict[str, dict[str, Any]],
    status_board: dict[str, Any],
    rank: int,
) -> dict[str, Any]:
    metric = pool["best_metric"]
    send = send_by_metric[metric]
    status_slot = _status_slot_for_metric(status_board, metric)
    recorder_command = (
        "python scripts/record_reviewer_outreach_event.py "
        f"--slot-id {status_slot['slot_id']} "
        "--status sent "
        "--reviewer-contact \"<private label or public handle>\" "
        f"--channel-used \"{pool['suggested_channel']}\" "
        f"--note \"Sent {metric} reviewer ask from real outreach playbook\""
    )
    return {
        "rank": rank,
        "contact_pool": pool["pool"],
        "target_metric": metric,
        "who_to_find": pool["who_to_find"],
        "why_it_matters": pool["why_it_matters"],
        "suggested_channel": pool["suggested_channel"],
        "status_board_slot_id": status_slot["slot_id"],
        "public_issue_url": send["public_issue_url"],
        "submission_url": send["submission_url"],
        "copy_ready_message": send["copy_ready_message"],
        "record_after_real_send": recorder_command,
        "counts_only_after": send["counts_only_after"],
        "resume_outcome_after_send": False,
    }


def build_real_reviewer_outreach_playbook() -> dict[str, Any]:
    send_queue = load_json(SEND_QUEUE_PATH)
    first_send = load_json(FIRST_SEND_PATH)
    status_board = load_json(OUTREACH_STATUS_PATH)
    send_by_metric = _send_by_metric(send_queue)
    missing = [pool["best_metric"] for pool in CONTACT_POOLS if pool["best_metric"] not in send_by_metric]
    if missing:
        raise AssertionError(f"reviewer send queue missing metrics: {missing}")

    steps = [_outreach_step(pool, send_by_metric, status_board, rank) for rank, pool in enumerate(CONTACT_POOLS, start=1)]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_real_reviewer_outreach_playbook.py",
        "purpose": (
            "Turn the zero-outcome baseline into a concrete manual outreach plan for getting real, non-owner, "
            "permissioned public evidence that can eventually unlock stronger resume claims."
        ),
        "current_baseline": {
            "accepted_public_evidence": 0,
            "external_feedback_items": 0,
            "confirmed_external_users": 0,
            "ai_engineer_review_items": 0,
            "github_stars_claimable": 0,
        },
        "first_action": {
            "metric": first_send["selected_metric"],
            "slot_id": first_send["status_board_slot_id"],
            "reviewer_profile": first_send["selected_reviewer_profile"],
            "record_command": first_send["record_sent_command"],
        },
        "contact_pool_count": len(CONTACT_POOLS),
        "outreach_step_count": len(steps),
        "outreach_steps": steps,
        "counting_policy": (
            "A sent message is only distribution evidence. Resume outcomes increase only when a non-owner public "
            "GitHub issue includes permission to count, contains no private data, and passes the evidence gate."
        ),
        "today_completion_definition": [
            "Choose one real person from the first contact pool.",
            "Send the copy-ready message outside the repo.",
            "Record only the sent event with scripts/record_reviewer_outreach_event.py.",
            "Do not change user, feedback, star, or business-impact counts until public evidence is accepted.",
        ],
        "resume_safe_summary": (
            "Added a real reviewer outreach playbook with 5 contact pools, 5 evidence targets, copy-ready asks, "
            "recording commands, and strict counting boundaries for converting future external reviews into "
            "resume-safe outcome claims."
        ),
        "not_claimed": [
            "message sent",
            "external user",
            "external feedback",
            "AI Engineer review",
            "business pilot",
            "GitHub star growth",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    steps = []
    for item in payload["outreach_steps"]:
        steps.append(
            f"""### {item["rank"]}. {item["contact_pool"]}

- Target metric: `{item["target_metric"]}`
- Who to find: {item["who_to_find"]}
- Suggested channel: {item["suggested_channel"]}
- Status-board slot: `{item["status_board_slot_id"]}`
- Why it matters: {item["why_it_matters"]}
- Public issue: [{item["public_issue_url"]}]({item["public_issue_url"]})
- Submission URL: [{item["submission_url"]}]({item["submission_url"]})

Copy-ready message:

```text
{item["copy_ready_message"]}
```

Record after a real send:

```bash
{item["record_after_real_send"]}
```

Counting rule: {item["counts_only_after"]}
"""
        )

    completion = "\n".join(f"- {item}" for item in payload["today_completion_definition"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Real Reviewer Outreach Playbook

{payload["purpose"]}

## Current Baseline

| Metric | Count |
| --- | ---: |
| Accepted public evidence | {payload["current_baseline"]["accepted_public_evidence"]} |
| External feedback items | {payload["current_baseline"]["external_feedback_items"]} |
| Confirmed external users | {payload["current_baseline"]["confirmed_external_users"]} |
| AI Engineer review items | {payload["current_baseline"]["ai_engineer_review_items"]} |
| GitHub stars claimable | {payload["current_baseline"]["github_stars_claimable"]} |

## First Action

- Metric: `{payload["first_action"]["metric"]}`
- Slot: `{payload["first_action"]["slot_id"]}`
- Reviewer profile: {payload["first_action"]["reviewer_profile"]}

```bash
{payload["first_action"]["record_command"]}
```

## Today Completion Definition

{completion}

## Outreach Steps

{chr(10).join(steps)}
## Counting Policy

{payload["counting_policy"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_real_reviewer_outreach_playbook(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["contact_pool_count"] != 5:
        raise AssertionError("real reviewer outreach playbook must define five contact pools")
    if payload["outreach_step_count"] != 5:
        raise AssertionError("real reviewer outreach playbook must define five outreach steps")
    if payload["first_action"]["metric"] != "ai_engineer_review_items":
        raise AssertionError("first real outreach action must target AI Engineer review")
    if payload["first_action"]["slot_id"] != "review_slot_07":
        raise AssertionError("first real outreach action must record against review_slot_07")
    expected_slots = {
        "ai_engineer_review_items": "review_slot_07",
        "confirmed_external_users": "review_slot_04",
        "reproducible_feedback_items": "review_slot_03",
        "business_case_feedback_items": "review_slot_05",
        "external_feedback_items": "review_slot_01",
    }
    for key, value in payload["current_baseline"].items():
        if value != 0:
            raise AssertionError(f"{key} must stay at zero until accepted public evidence exists")
    metrics = {item["target_metric"] for item in payload["outreach_steps"]}
    required = {
        "ai_engineer_review_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "external_feedback_items",
    }
    if metrics != required:
        raise AssertionError(f"real reviewer outreach metrics mismatch: {sorted(metrics)}")
    for item in payload["outreach_steps"]:
        if item["status_board_slot_id"] != expected_slots[item["target_metric"]]:
            raise AssertionError(f"{item['target_metric']} mapped to wrong status-board slot")
        if item["resume_outcome_after_send"] is not False:
            raise AssertionError("sent outreach must not be treated as a resume outcome")
        if "--status sent" not in item["record_after_real_send"]:
            raise AssertionError("each outreach step must provide a sent-event recorder command")
        if f"--slot-id {item['status_board_slot_id']}" not in item["record_after_real_send"]:
            raise AssertionError("each recorder command must use the status-board slot id")
        if "permission" not in item["counts_only_after"].lower():
            raise AssertionError("each outreach step must preserve permission-based counting")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in ("non-owner public github issue", "no private data", "evidence gate"):
        if phrase not in joined:
            raise AssertionError(f"real reviewer outreach playbook missing boundary phrase: {phrase}")
    return {
        "real_reviewer_outreach_playbook_verified": True,
        "outreach_step_count": payload["outreach_step_count"],
    }


def main() -> None:
    payload = build_real_reviewer_outreach_playbook()
    verify_real_reviewer_outreach_playbook(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps({"status": "ok", "outreach_step_count": payload["outreach_step_count"]}))


if __name__ == "__main__":
    main()
