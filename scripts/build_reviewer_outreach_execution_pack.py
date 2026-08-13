import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REVIEWER_ACTION_QUEUE_PATH = ROOT / "docs" / "reviewer-action-queue.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-outreach-execution-pack.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-outreach-execution-pack.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _subject(task: dict[str, Any]) -> str:
    segment = task["reviewer_segment"].replace("UC Davis", "UC Davis")
    return f"Could you review my Data Quality Agent project? ({segment})"


def _send_channel(task: dict[str, Any]) -> str:
    segment = task["reviewer_segment"].lower()
    if "uc davis" in segment or "student" in segment:
        return "LinkedIn, class Discord, club Slack, or direct message"
    if "open-source" in segment:
        return "GitHub discussion, maintainer DM, or project community channel"
    if "operator" in segment or "analyst" in segment:
        return "LinkedIn or email to someone who has seen messy CSV, support, sales, or operations data"
    return "LinkedIn, email, or mentor message"


def _personalization(task: dict[str, Any]) -> list[str]:
    return [
        f"Name the reviewer segment: {task['reviewer_segment']}.",
        "Mention that the project is public and starts from a zero-feedback baseline.",
        f"Ask them to use this entry path: {task['entry_url']}.",
        "Ask them not to share private data and to submit only public, redacted evidence.",
    ]


def _ready_message(task: dict[str, Any]) -> str:
    return (
        f"Hi {{name}}, I am trying to make my Data Quality Agent project credible for AI Engineer and SWE internship applications. "
        f"{task['message_template']} If you are comfortable with it, please submit the review here: {task['submission_url']} "
        "and include the sentence 'I give permission for this public issue to be counted as project review evidence.' "
        "Please do not include raw customer data, secrets, private emails, addresses, API keys, or production rows. Thank you."
    )


def _follow_up(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "after_days": 4,
        "status_before_follow_up": "sent_no_response",
        "message": (
            f"Quick follow-up on my Data Quality Agent review request. No pressure, but if you have 8-15 minutes, "
            f"the entry point is {task['entry_url']} and the public evidence form is {task['submission_url']}. "
            "A short redacted comment is enough."
        ),
    }


def build_reviewer_outreach_execution_pack() -> dict[str, Any]:
    queue = load_json(REVIEWER_ACTION_QUEUE_PATH)
    outreach_items = []
    for index, task in enumerate(queue["tasks"], start=1):
        outreach_items.append(
            {
                "id": f"outreach_{index:02d}_{task['id']}",
                "source_task_id": task["id"],
                "reviewer_segment": task["reviewer_segment"],
                "send_status": "not_sent",
                "counts_toward": task["counts_toward"],
                "channel": _send_channel(task),
                "subject": _subject(task),
                "ready_to_send_message": _ready_message(task),
                "personalization_checklist": _personalization(task),
                "entry_url": task["entry_url"],
                "submission_url": task["submission_url"],
                "evidence_acceptance_checklist": task["required_public_evidence"],
                "follow_up": _follow_up(task),
                "privacy_boundary": task["privacy_boundary"],
                "permission_to_count": task["permission_to_count"],
                "status_update_rule": (
                    "Move from not_sent to sent only after the message is actually sent. "
                    "Move to completed only after a public GitHub issue passes the evidence gate."
                ),
            }
        )

    evidence_goals = sorted({item["counts_toward"] for item in outreach_items})
    send_status_counts = {
        "not_sent": sum(1 for item in outreach_items if item["send_status"] == "not_sent"),
        "sent": 0,
        "completed": 0,
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_outreach_execution_pack.py",
        "purpose": (
            "Convert the reviewer action queue into ready-to-send outreach messages, follow-up rules, "
            "and evidence checklists while preserving the zero-sent and zero-completed baseline."
        ),
        "source_queue": {
            "queue_count": queue["queue_count"],
            "evidence_goal_count": queue["evidence_goal_count"],
            "not_contacted_count": queue["not_contacted_count"],
            "resume_status": queue["resume_status"],
        },
        "outreach_item_count": len(outreach_items),
        "ready_message_count": len(outreach_items),
        "follow_up_rule_count": len(outreach_items),
        "evidence_goal_count": len(evidence_goals),
        "evidence_goals": evidence_goals,
        "send_status_counts": send_status_counts,
        "outreach_items": outreach_items,
        "manual_execution_rules": [
            "Do not mark a message as sent until it is actually sent to a real reviewer.",
            "Do not count private replies as public evidence.",
            "Do not count self-authored planning issues as external evidence.",
            "Do not ask reviewers to upload raw private business data.",
            "Do not write users, feedback, or business impact on a resume until a public issue passes the evidence gate.",
        ],
        "resume_status": "ready_to_send_not_claimable",
        "resume_safe_summary": (
            f"Published a CI-verified outreach execution pack with {len(outreach_items)} ready-to-send reviewer messages, "
            f"{len(outreach_items)} follow-up rules, {len(evidence_goals)} evidence goals, and zero sent or completed outreach claimed."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    source = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["source_queue"].items())
    goals = "\n".join(f"- `{goal}`" for goal in payload["evidence_goals"])
    rules = "\n".join(f"- {rule}" for rule in payload["manual_execution_rules"])
    items = "\n\n".join(
        "\n".join(
            [
                f"### {item['id']}",
                "",
                f"- Segment: {item['reviewer_segment']}",
                f"- Channel: {item['channel']}",
                f"- Status: `{item['send_status']}`",
                f"- Counts toward: `{item['counts_toward']}`",
                f"- Entry: [{item['entry_url']}]({item['entry_url']})",
                f"- Submission: [{item['submission_url']}]({item['submission_url']})",
                f"- Subject: {item['subject']}",
                "",
                "Message:",
                "",
                item["ready_to_send_message"],
                "",
                "Personalization checklist:",
                *[f"- {check}" for check in item["personalization_checklist"]],
                "",
                "Evidence acceptance checklist:",
                *[f"- {check}" for check in item["evidence_acceptance_checklist"]],
                "",
                f"Follow-up after {item['follow_up']['after_days']} days:",
                "",
                item["follow_up"]["message"],
                "",
                f"Status update rule: {item['status_update_rule']}",
            ]
        )
        for item in payload["outreach_items"]
    )
    return f"""# Reviewer Outreach Execution Pack

This generated pack turns the reviewer action queue into messages that can be sent manually.

## Purpose

{payload["purpose"]}

## Source Queue

| Field | Value |
| --- | ---: |
{source}

## Evidence Goals

{goals}

## Outreach Items

{items}

## Manual Execution Rules

{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_reviewer_outreach_execution_pack(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "outreach_item_count": 8,
        "ready_message_count": 8,
        "follow_up_rule_count": 8,
        "evidence_goal_count": 5,
        "not_sent_count": 8,
        "sent_count": 0,
        "completed_count": 0,
    }
    if payload["outreach_item_count"] != expected["outreach_item_count"]:
        raise AssertionError("outreach execution pack must include eight outreach items")
    if payload["ready_message_count"] != expected["ready_message_count"]:
        raise AssertionError("outreach execution pack must include eight ready messages")
    if payload["follow_up_rule_count"] != expected["follow_up_rule_count"]:
        raise AssertionError("outreach execution pack must include eight follow-up rules")
    if payload["evidence_goal_count"] != expected["evidence_goal_count"]:
        raise AssertionError("outreach execution pack must cover five evidence goals")
    if payload["send_status_counts"]["not_sent"] != expected["not_sent_count"]:
        raise AssertionError("outreach execution pack must preserve not-sent baseline")
    if payload["send_status_counts"]["sent"] != expected["sent_count"]:
        raise AssertionError("outreach execution pack must not claim sent outreach")
    if payload["send_status_counts"]["completed"] != expected["completed_count"]:
        raise AssertionError("outreach execution pack must not claim completed outreach")
    if payload["resume_status"] != "ready_to_send_not_claimable":
        raise AssertionError("outreach execution pack must not be resume-claimable as usage evidence")
    ids = {item["id"] for item in payload["outreach_items"]}
    if len(ids) != expected["outreach_item_count"]:
        raise AssertionError("outreach execution pack item IDs must be unique")
    required_goals = {
        "external_feedback_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
    }
    if set(payload["evidence_goals"]) != required_goals:
        raise AssertionError("outreach execution pack must map to tracked evidence goals")
    for item in payload["outreach_items"]:
        if item["send_status"] != "not_sent":
            raise AssertionError("outreach execution pack must not imply outreach has been sent")
        if "{name}" not in item["ready_to_send_message"]:
            raise AssertionError("ready messages must keep a manual personalization placeholder")
        if "permission" not in item["ready_to_send_message"].lower():
            raise AssertionError("ready messages must request permission to count public evidence")
        if "raw customer data" not in item["ready_to_send_message"].lower():
            raise AssertionError("ready messages must include private-data boundaries")
        if not item["submission_url"].startswith("https://github.com/sunnnn2005/data-quality-agent/"):
            raise AssertionError("outreach evidence must submit to public GitHub URLs")
        if item["follow_up"]["after_days"] != 4:
            raise AssertionError("outreach execution pack must use a deterministic follow-up delay")
        if "completed only after a public GitHub issue passes the evidence gate" not in item["status_update_rule"]:
            raise AssertionError("status rules must depend on public evidence gate completion")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("sent outreach: 1", "completed outreach: 1", "active users: 1", "customer traction"):
        if forbidden in joined:
            raise AssertionError(f"outreach execution pack must not claim {forbidden}")
    return {"reviewer_outreach_execution_pack_verified": True, **expected}


def main() -> None:
    payload = build_reviewer_outreach_execution_pack()
    verify_reviewer_outreach_execution_pack(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
