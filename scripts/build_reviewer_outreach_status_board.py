import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTREACH_PACK_PATH = ROOT / "docs" / "reviewer-outreach-execution-pack.json"
SHARE_KIT_PATH = ROOT / "docs" / "reviewer-share-kit.json"
RESUME_OUTCOME_METRICS_PATH = ROOT / "docs" / "resume-outcome-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-outreach-status-board.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_reviewer_outreach_status_board() -> dict[str, Any]:
    outreach = load_json(OUTREACH_PACK_PATH)
    share_kit = load_json(SHARE_KIT_PATH)
    outcome_metrics = load_json(RESUME_OUTCOME_METRICS_PATH)

    stages = [
        {
            "status": "not_sent",
            "meaning": "The outreach slot exists, but no real reviewer has been contacted.",
            "resume_countable": False,
        },
        {
            "status": "sent",
            "meaning": "A message was actually sent to a real reviewer.",
            "resume_countable": False,
        },
        {
            "status": "replied_private",
            "meaning": "The reviewer replied privately; private replies are notes only and do not count as public evidence.",
            "resume_countable": False,
        },
        {
            "status": "public_issue_submitted",
            "meaning": "A reviewer submitted a public, redacted GitHub issue with permission to count it.",
            "resume_countable": False,
        },
        {
            "status": "accepted_evidence",
            "meaning": "A non-owner public GitHub issue passed the evidence gate and can update outcome metrics.",
            "resume_countable": True,
        },
    ]

    slots = []
    for index, item in enumerate(outreach["outreach_items"], start=1):
        slots.append(
            {
                "slot_id": f"review_slot_{index:02d}",
                "source_outreach_id": item["id"],
                "reviewer_segment": item["reviewer_segment"],
                "channel": item["channel"],
                "counts_toward": item["counts_toward"],
                "status": "not_sent",
                "sent_at": None,
                "reply_received": False,
                "public_evidence_url": None,
                "accepted_by_gate": False,
                "next_action": "Send manually only after choosing a real reviewer.",
                "resume_counting_rule": (
                    "Does not count until a non-owner public GitHub issue passes the evidence gate."
                ),
                "privacy_boundary": item["privacy_boundary"],
            }
        )

    tracked_counts = {item["metric"]: item["current_count"] for item in outcome_metrics["tracked_outcomes"]}
    current_counts = {
        "external_feedback_items": tracked_counts["external_feedback_items"],
        "confirmed_external_users": tracked_counts["confirmed_external_users"],
        "reproducible_feedback_items": tracked_counts["reproducible_feedback_items"],
        "business_case_feedback_items": tracked_counts["business_case_feedback_items"],
        "ai_engineer_review_items": tracked_counts["ai_engineer_review_items"],
    }

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_outreach_status_board.py",
        "purpose": (
            "Track real reviewer outreach from planned to sent, replied, public issue, and accepted evidence "
            "without converting private outreach into resume claims."
        ),
        "source_outreach_item_count": outreach["outreach_item_count"],
        "source_share_channel_count": share_kit["share_channel_count"],
        "status_stage_count": len(stages),
        "outreach_slot_count": len(slots),
        "not_sent_count": len(slots),
        "sent_count": 0,
        "reply_count": 0,
        "accepted_evidence_count": 0,
        "resume_upgrade_count": 0,
        "current_outcome_counts": current_counts,
        "status_stages": stages,
        "outreach_slots": slots,
        "resume_upgrade_rules": [
            "No resume outcome is upgraded until a public issue URL exists.",
            "Private replies are useful notes but never public evidence.",
            "Evidence must include permission to count the reviewer submission publicly.",
            "Self-authored issues and owner-authored planning issues are excluded.",
            "Accepted evidence updates resume-outcome-metrics only after the evidence gate passes.",
        ],
        "manual_update_schema": {
            "slot_id": "review_slot_01",
            "sent_at": "ISO-8601 timestamp after the message is actually sent",
            "public_evidence_url": "Public GitHub issue URL, if submitted",
            "external_author": "Non-owner reviewer identity or public GitHub handle",
            "permission_to_count": "Required before counting",
            "no_private_data": "Required before counting",
            "evidence_gate_status": "pending | accepted | rejected",
        },
        "resume_status": "tracking_ready_not_claimable",
        "resume_safe_summary": (
            f"Published a CI-verified outreach status board tracking {len(slots)} reviewer slots across "
            f"{len(stages)} status stages, {len(current_counts)} evidence goals, and zero sent, replied, "
            "accepted-evidence, or resume-upgrade claims."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    stages = "\n".join(
        f"| `{stage['status']}` | {stage['meaning']} | {stage['resume_countable']} |"
        for stage in payload["status_stages"]
    )
    slots = "\n".join(
        f"| {slot['slot_id']} | {slot['reviewer_segment']} | `{slot['counts_toward']}` | `{slot['status']}` |"
        for slot in payload["outreach_slots"]
    )
    rules = "\n".join(f"- {rule}" for rule in payload["resume_upgrade_rules"])
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_outcome_counts"].items())
    return f"""# Reviewer Outreach Status Board

This generated board tracks reviewer outreach execution without claiming results that have not happened.

## Purpose

{payload["purpose"]}

## Status Stages

| Stage | Meaning | Resume Countable |
| --- | --- | --- |
{stages}

## Outreach Slots

| Slot | Reviewer Segment | Counts Toward | Status |
| --- | --- | --- | --- |
{slots}

## Current Outcome Counts

| Metric | Count |
| --- | ---: |
{counts}

## Resume Upgrade Rules

{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_reviewer_outreach_status_board(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "source_outreach_item_count": 8,
        "source_share_channel_count": 5,
        "status_stage_count": 5,
        "outreach_slot_count": 8,
        "not_sent_count": 8,
        "sent_count": 0,
        "reply_count": 0,
        "accepted_evidence_count": 0,
        "resume_upgrade_count": 0,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    if payload.get("resume_status") != "tracking_ready_not_claimable":
        raise AssertionError("status board must not be resume-claimable as usage evidence")
    if len(payload.get("status_stages", [])) != expected["status_stage_count"]:
        raise AssertionError("status board must include five status stages")
    if len(payload.get("outreach_slots", [])) != expected["outreach_slot_count"]:
        raise AssertionError("status board must include eight reviewer slots")
    for value in payload.get("current_outcome_counts", {}).values():
        if value != 0:
            raise AssertionError("status board must preserve zero current outcome counts")
    for slot in payload["outreach_slots"]:
        if slot["status"] != "not_sent":
            raise AssertionError("status board must start every outreach slot as not_sent")
        if slot["sent_at"] is not None:
            raise AssertionError("status board must not fabricate sent timestamps")
        if slot["reply_received"] is not False:
            raise AssertionError("status board must not fabricate reviewer replies")
        if slot["public_evidence_url"] is not None:
            raise AssertionError("status board must not fabricate public evidence URLs")
        if slot["accepted_by_gate"] is not False:
            raise AssertionError("status board must not fabricate accepted evidence")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in (
        "non-owner public github issue",
        "permission",
        "self-authored",
        "private replies",
        "evidence gate",
    ):
        if required not in joined:
            raise AssertionError(f"status board must include {required}")
    if "replied_private" not in {stage["status"] for stage in payload["status_stages"]}:
        raise AssertionError("status board must distinguish private replies from public evidence")
    return {"reviewer_outreach_status_board_verified": True, **expected}


def main() -> None:
    payload = build_reviewer_outreach_status_board()
    verify_reviewer_outreach_status_board(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps({"status": "ok", "output": str(OUTPUT_JSON_PATH), "outreach_slot_count": payload["outreach_slot_count"]}))


if __name__ == "__main__":
    main()
