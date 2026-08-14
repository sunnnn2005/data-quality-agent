import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEND_QUEUE_PATH = ROOT / "docs" / "reviewer-send-queue.json"
OUTREACH_EVENTS_PATH = ROOT / "docs" / "reviewer-outreach-events.json"
ACCEPTED_EVIDENCE_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
FIRST_OUTCOME_REQUEST_PATH = ROOT / "docs" / "first-outcome-evidence-request.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "outcome-launch-day-tracker.json"
OUTPUT_MD_PATH = ROOT / "docs" / "outcome-launch-day-tracker.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _status_slot_id(queue_slot_id: str) -> str:
    parts = queue_slot_id.split("_")
    if len(parts) < 2 or not parts[1].isdigit():
        raise AssertionError(f"cannot map queue slot id to status slot id: {queue_slot_id}")
    return f"review_slot_{parts[1]}"


def _record_command(item: dict[str, Any]) -> str:
    return (
        "python scripts/record_reviewer_outreach_event.py "
        f"--slot-id {_status_slot_id(item['slot_id'])} "
        "--status sent "
        '--reviewer-contact "<reviewer name or handle>" '
        f"--channel-used \"{item['recommended_channel']}\" "
        f"--note \"Sent {item['target_metric']} request\""
    )


def _launch_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "rank": item["rank"],
        "queue_slot_id": item["slot_id"],
        "status_board_slot_id": _status_slot_id(item["slot_id"]),
        "target_metric": item["target_metric"],
        "reviewer_profile": item["reviewer_profile"],
        "who_to_choose": item["who_to_choose"],
        "recommended_channel": item["recommended_channel"],
        "public_issue_url": item["public_issue_url"],
        "submission_url": item["submission_url"],
        "copy_ready_message": item["copy_ready_message"],
        "record_sent_command": _record_command(item),
        "after_send_counts_as": "outreach_execution_only",
        "resume_countable_now": False,
        "resume_unlock_condition": item["counts_only_after"],
    }


def build_outcome_launch_day_tracker() -> dict[str, Any]:
    queue = load_json(SEND_QUEUE_PATH)
    events = load_json(OUTREACH_EVENTS_PATH)
    accepted = load_json(ACCEPTED_EVIDENCE_PATH)
    first_request = load_json(FIRST_OUTCOME_REQUEST_PATH)

    launch_items = [_launch_item(item) for item in queue["next_sends"]]
    accepted_counts = accepted["accepted_counts"]
    first_metric = first_request["target_metric"]
    first_remaining = max(0, first_request["required_count"] - accepted_counts.get(first_metric, 0))

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_outcome_launch_day_tracker.py",
        "purpose": (
            "Turn the public outcome evidence system into a day-of-execution tracker for collecting the first "
            "real resume-countable external result without inflating outreach into user, feedback, or star claims."
        ),
        "launch_day_goal": (
            "Send the first five reviewer requests, record only messages that were actually sent, and wait for "
            "public non-owner GitHub issues before upgrading any resume outcome."
        ),
        "first_resume_unlock": {
            "target_metric": first_metric,
            "current_count": accepted_counts.get(first_metric, 0),
            "required_count": first_request["required_count"],
            "remaining_to_unlock": first_remaining,
            "future_resume_line": first_request["future_resume_line"],
            "request_page_url": first_request["request_page_url"],
        },
        "baseline": {
            "planned_send_count": queue["queue_count"],
            "recorded_outreach_event_count": len(events.get("events", [])),
            "sent_count": queue["sent_count"],
            "accepted_external_evidence_count": accepted["accepted_issue_count"],
            "github_stars_claimed": 0,
            "resume_outcome_claimable_now": False,
        },
        "launch_items": launch_items,
        "post_send_rules": [
            "Record a sent event only after a real message is sent to a real reviewer.",
            "A sent event is distribution evidence, not usage, feedback, business impact, or a star.",
            "Ask reviewers to submit public redacted GitHub issues through the linked templates.",
            "Count a resume outcome only after a non-owner public issue passes the evidence gate.",
            "Do not include private data, customer rows, secrets, private emails, addresses, or API keys.",
        ],
        "resume_safe_summary": (
            f"Published a launch-day outcome tracker with {len(launch_items)} concrete reviewer sends, "
            f"{len(events.get('events', []))} recorded outreach events, {accepted['accepted_issue_count']} accepted "
            "external evidence items, and explicit rules preventing outreach from being counted as users or feedback."
        ),
        "not_claimed": [
            "No outreach is claimed as sent unless it is recorded in reviewer-outreach-events.json.",
            "No external users, feedback, business impact, production deployment, or GitHub stars are claimed.",
            "No resume line is unlocked until accepted evidence count for its metric reaches the threshold.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    baseline = payload["baseline"]
    first = payload["first_resume_unlock"]
    lines = [
        "# Outcome Launch Day Tracker",
        "",
        payload["purpose"],
        "",
        "## Launch Day Goal",
        "",
        payload["launch_day_goal"],
        "",
        "## Current Baseline",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Planned sends | {baseline['planned_send_count']} |",
        f"| Recorded outreach events | {baseline['recorded_outreach_event_count']} |",
        f"| Sent count | {baseline['sent_count']} |",
        f"| Accepted external evidence | {baseline['accepted_external_evidence_count']} |",
        f"| Resume outcome claimable now | {baseline['resume_outcome_claimable_now']} |",
        "",
        "## First Resume Unlock",
        "",
        f"- Target metric: `{first['target_metric']}`",
        f"- Current count: {first['current_count']}",
        f"- Required count: {first['required_count']}",
        f"- Remaining to unlock: {first['remaining_to_unlock']}",
        f"- Request page: [{first['request_page_url']}]({first['request_page_url']})",
        f"- Locked future line: {first['future_resume_line']}",
        "",
        "## Send These Today",
        "",
    ]
    for item in payload["launch_items"]:
        lines.extend(
            [
                f"### {item['rank']}. {item['queue_slot_id']}",
                "",
                f"- Target metric: `{item['target_metric']}`",
                f"- Reviewer profile: {item['reviewer_profile']}",
                f"- Who to choose: {item['who_to_choose']}",
                f"- Channel: {item['recommended_channel']}",
                f"- Public issue: [{item['public_issue_url']}]({item['public_issue_url']})",
                f"- Submission URL: [{item['submission_url']}]({item['submission_url']})",
                f"- After send counts as: `{item['after_send_counts_as']}`",
                f"- Resume countable now: `{item['resume_countable_now']}`",
                "",
                "Copy-ready message:",
                "",
                "```text",
                item["copy_ready_message"],
                "```",
                "",
                "Record after sending:",
                "",
                "```bash",
                item["record_sent_command"],
                "```",
                "",
            ]
        )
    lines.extend(
        [
            "## Post-Send Rules",
            "",
            *[f"- {rule}" for rule in payload["post_send_rules"]],
            "",
            "## Resume-Safe Summary",
            "",
            payload["resume_safe_summary"],
            "",
            "## Not Claimed",
            "",
            *[f"- {item}" for item in payload["not_claimed"]],
            "",
        ]
    )
    return "\n".join(lines)


def verify_outcome_launch_day_tracker(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["baseline"]["planned_send_count"] != 5:
        raise AssertionError("launch day tracker must keep the first five sends visible")
    if payload["baseline"]["accepted_external_evidence_count"] != 0:
        raise AssertionError("launch day tracker must not claim accepted external evidence")
    if payload["baseline"]["resume_outcome_claimable_now"] is not False:
        raise AssertionError("launch day tracker must keep resume outcomes locked at baseline")
    if payload["first_resume_unlock"]["target_metric"] != "ai_engineer_review_items":
        raise AssertionError("first unlock must remain AI Engineer review evidence")
    if payload["first_resume_unlock"]["remaining_to_unlock"] != 1:
        raise AssertionError("first unlock must require one external evidence item")
    if len(payload["launch_items"]) != 5:
        raise AssertionError("launch day tracker must expose five launch items")
    for item in payload["launch_items"]:
        if "--status sent" not in item["record_sent_command"]:
            raise AssertionError("each launch item must include a sent recorder command")
        if item["after_send_counts_as"] != "outreach_execution_only":
            raise AssertionError("sent outreach must be separated from outcome evidence")
        if item["resume_countable_now"] is not False:
            raise AssertionError("launch items are not immediately resume-countable")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in (
        "real resume-countable external result",
        "public non-owner github issues",
        "outreach from being counted as users or feedback",
        "no external users",
    ):
        if phrase not in joined:
            raise AssertionError(f"launch day tracker missing phrase: {phrase}")
    return {
        "outcome_launch_day_tracker_verified": True,
        "launch_item_count": len(payload["launch_items"]),
        "accepted_external_evidence_count": payload["baseline"]["accepted_external_evidence_count"],
    }


def main() -> None:
    payload = build_outcome_launch_day_tracker()
    verify_outcome_launch_day_tracker(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(
        json.dumps(
            {
                "outcome_launch_day_tracker_verified": True,
                "launch_item_count": len(payload["launch_items"]),
                "accepted_external_evidence_count": payload["baseline"]["accepted_external_evidence_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
