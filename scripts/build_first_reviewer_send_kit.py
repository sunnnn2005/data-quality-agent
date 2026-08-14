import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEND_QUEUE_PATH = ROOT / "docs" / "reviewer-send-queue.json"
OUTREACH_STATUS_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
PIPELINE_PATH = ROOT / "docs" / "outcome-pipeline-board.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "first-reviewer-send-kit.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-reviewer-send-kit.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _matching_status_slot(first_send: dict[str, Any], status_board: dict[str, Any]) -> dict[str, Any]:
    target_metric = first_send["target_metric"]
    reviewer_profile = first_send["reviewer_profile"].lower()
    matches = [
        slot
        for slot in status_board["outreach_slots"]
        if slot["counts_toward"] == target_metric
        and (
            slot["reviewer_segment"].lower() in reviewer_profile
            or reviewer_profile in slot["reviewer_segment"].lower()
        )
    ]
    if len(matches) != 1:
        raise AssertionError(f"expected one matching status slot for first send, got {len(matches)}")
    return matches[0]


def build_first_reviewer_send_kit() -> dict[str, Any]:
    queue = load_json(SEND_QUEUE_PATH)
    status_board = load_json(OUTREACH_STATUS_PATH)
    pipeline = load_json(PIPELINE_PATH)

    first_send = queue["next_sends"][0]
    status_slot = _matching_status_slot(first_send, status_board)
    already_sent = status_slot["status"] != "not_sent"
    recorder_command = (
        f"Already recorded as {status_slot['status']}; do not run a duplicate recorder command for "
        f"{status_slot['slot_id']}."
        if already_sent
        else (
            "python scripts/record_reviewer_outreach_event.py "
            f"--slot-id {status_slot['slot_id']} "
            "--status sent "
            "--reviewer-contact \"<reviewer name or handle>\" "
            f"--channel-used \"{first_send['recommended_channel']}\" "
            "--note \"Sent first AI Engineer reviewer request\""
        )
    )
    sent_before = pipeline["current_baseline"]["sent_reviewer_messages"]
    sent_after = sent_before if already_sent else sent_before + 1
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_reviewer_send_kit.py",
        "purpose": (
            "Give the maintainer one concrete first send that can move the outcome pipeline from public launch "
            "toward real reviewer outreach without inflating resume outcomes."
        ),
        "selected_rank": first_send["rank"],
        "selected_metric": first_send["target_metric"],
        "selected_reviewer_profile": first_send["reviewer_profile"],
        "recommended_channel": first_send["recommended_channel"],
        "public_issue_url": first_send["public_issue_url"],
        "submission_url": first_send["submission_url"],
        "entry_url": first_send["entry_url"],
        "copy_ready_message": first_send["copy_ready_message"],
        "copy_ready_follow_up": first_send["copy_ready_follow_up"],
        "status_board_slot_id": status_slot["slot_id"],
        "source_outreach_status": status_slot["status"],
        "record_sent_command": recorder_command,
        "after_send_expected_pipeline_change": {
            "sent_reviewer_messages": {
                "before": sent_before,
                "after_recording_one_real_send": sent_after,
            },
            "claimable_resume_metric_count": {
                "before": pipeline["claimable_resume_metric_count"],
                "after_recording_one_real_send": pipeline["claimable_resume_metric_count"],
            },
        },
        "counting_boundary": (
            "Recording a sent outreach event proves distribution execution only. It does not count as an external "
            "user, accepted feedback, AI Engineer review, business validation, or GitHub star."
        ),
        "resume_status": "first_send_ready_not_outcome_evidence",
        "resume_safe_summary": (
            "Prepared one first AI Engineer reviewer send with a copy-ready message, public issue URL, and "
            "state-aware recording guidance while preserving zero claimable resume outcomes."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    expected = payload["after_send_expected_pipeline_change"]
    return f"""# First Reviewer Send Kit

This generated kit gives the first concrete reviewer send needed to move from public launch to real outreach.

## First Send

| Field | Value |
| --- | --- |
| Selected metric | `{payload["selected_metric"]}` |
| Reviewer profile | {payload["selected_reviewer_profile"]} |
| Recommended channel | {payload["recommended_channel"]} |
| Status-board slot ID | `{payload["status_board_slot_id"]}` |
| Current status | `{payload["source_outreach_status"]}` |
| Public issue | [{payload["public_issue_url"]}]({payload["public_issue_url"]}) |
| Submission URL | [{payload["submission_url"]}]({payload["submission_url"]}) |
| Entry URL | [{payload["entry_url"]}]({payload["entry_url"]}) |

## Copy-Ready Message

```text
{payload["copy_ready_message"]}
```

## Follow-Up

```text
{payload["copy_ready_follow_up"]}
```

## Record After Sending

Run this only after the message is actually sent to a real person:

```bash
{payload["record_sent_command"]}
```

## Expected Pipeline Change

| Metric | Before | After Recording One Real Send |
| --- | ---: | ---: |
| Sent reviewer messages | {expected["sent_reviewer_messages"]["before"]} | {expected["sent_reviewer_messages"]["after_recording_one_real_send"]} |
| Claimable resume metrics | {expected["claimable_resume_metric_count"]["before"]} | {expected["claimable_resume_metric_count"]["after_recording_one_real_send"]} |

## Counting Boundary

{payload["counting_boundary"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_first_reviewer_send_kit(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["selected_rank"] != 1:
        raise AssertionError("first reviewer send kit must use the highest-priority queue item")
    if payload["selected_metric"] != "ai_engineer_review_items":
        raise AssertionError("first reviewer send kit must target AI Engineer review first")
    if payload["status_board_slot_id"] != "review_slot_07":
        raise AssertionError("first reviewer send kit must map the AI Engineer send to review_slot_07")
    expected = payload["after_send_expected_pipeline_change"]
    if payload["source_outreach_status"] == "not_sent":
        if "--slot-id review_slot_07" not in payload["record_sent_command"]:
            raise AssertionError("first reviewer send kit must include the correct recorder slot id")
        if "--status sent" not in payload["record_sent_command"]:
            raise AssertionError("first reviewer send kit must record the first action as sent")
        if expected["sent_reviewer_messages"]["after_recording_one_real_send"] != expected["sent_reviewer_messages"]["before"] + 1:
            raise AssertionError("first reviewer send kit must show that one real send increments sent outreach")
    else:
        if "do not run a duplicate recorder command" not in payload["record_sent_command"]:
            raise AssertionError("first reviewer send kit must prevent duplicate sent outreach records")
        if expected["sent_reviewer_messages"]["after_recording_one_real_send"] != expected["sent_reviewer_messages"]["before"]:
            raise AssertionError("already-sent first reviewer kit must keep sent outreach stable")
    if expected["claimable_resume_metric_count"]["after_recording_one_real_send"] != 0:
        raise AssertionError("sent outreach must not become a claimable resume outcome")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in (
        "copy-ready message",
        "public issue url",
        "distribution execution only",
        "zero claimable resume outcomes",
    ):
        if phrase not in joined:
            raise AssertionError(f"first reviewer send kit missing phrase: {phrase}")
    return {
        "first_reviewer_send_kit_verified": True,
        "selected_metric": payload["selected_metric"],
        "status_board_slot_id": payload["status_board_slot_id"],
    }


def main() -> None:
    payload = build_first_reviewer_send_kit()
    verify_first_reviewer_send_kit(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps({"status": "ok", "status_board_slot_id": payload["status_board_slot_id"]}))


if __name__ == "__main__":
    main()
