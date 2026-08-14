import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTREACH_PACK_PATH = ROOT / "docs" / "reviewer-outreach-execution-pack.json"
SHARE_KIT_PATH = ROOT / "docs" / "reviewer-share-kit.json"
RESUME_OUTCOME_METRICS_PATH = ROOT / "docs" / "resume-outcome-metrics.json"
OUTREACH_EVENTS_PATH = ROOT / "docs" / "reviewer-outreach-events.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-outreach-status-board.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def load_outreach_events(path: Path | None = None) -> list[dict[str, Any]]:
    path = OUTREACH_EVENTS_PATH if path is None else path
    if not path.exists():
        return []
    payload = load_json(path)
    events = payload.get("events", [])
    if not isinstance(events, list):
        raise AssertionError("reviewer outreach events must be a list")
    return events


def apply_outreach_events(slots: list[dict[str, Any]], events: list[dict[str, Any]]) -> None:
    slot_by_id = {slot["slot_id"]: slot for slot in slots}
    allowed_statuses = {"sent", "replied_private", "public_issue_submitted"}
    for event in events:
        slot_id = event.get("slot_id")
        if slot_id not in slot_by_id:
            raise AssertionError(f"unknown outreach slot_id: {slot_id}")
        status = event.get("status")
        if status not in allowed_statuses:
            raise AssertionError("outreach events can only record sent, replied_private, or public_issue_submitted")
        slot = slot_by_id[slot_id]
        slot["status"] = status
        slot["reviewer_contact"] = event.get("reviewer_contact")
        slot["channel_used"] = event.get("channel_used")
        slot["sent_at"] = event.get("sent_at") or slot["sent_at"]
        slot["last_event_at"] = event.get("event_at")
        slot["reply_received"] = status in {"replied_private", "public_issue_submitted"}
        slot["public_evidence_url"] = event.get("public_evidence_url")
        slot["permission_to_count"] = bool(event.get("permission_to_count", False))
        slot["no_private_data_confirmed"] = bool(event.get("no_private_data_confirmed", False))
        if status == "public_issue_submitted" and not slot["public_evidence_url"]:
            raise AssertionError("public_issue_submitted events require public_evidence_url")
        slot["next_action"] = {
            "sent": "Wait for a reply or ask the reviewer to submit public redacted evidence.",
            "replied_private": "Ask for a public redacted GitHub issue with permission to count.",
            "public_issue_submitted": "Run the external reviewer evidence gate before counting any resume outcome.",
        }[status]


def calculate_conversion_metrics(slots: list[dict[str, Any]]) -> dict[str, Any]:
    slot_count = len(slots)
    contacted_count = sum(1 for slot in slots if slot["status"] != "not_sent")
    private_reply_count = sum(1 for slot in slots if slot["status"] == "replied_private")
    public_issue_count = sum(1 for slot in slots if slot["status"] == "public_issue_submitted")
    accepted_evidence_count = sum(1 for slot in slots if slot["accepted_by_gate"])

    def rate(numerator: int, denominator: int) -> float:
        if denominator == 0:
            return 0.0
        return round(numerator / denominator, 4)

    return {
        "tracked_slot_count": slot_count,
        "contacted_count": contacted_count,
        "not_contacted_count": slot_count - contacted_count,
        "private_reply_count": private_reply_count,
        "public_issue_count": public_issue_count,
        "accepted_evidence_count": accepted_evidence_count,
        "contact_rate": rate(contacted_count, slot_count),
        "private_reply_rate_from_contacted": rate(private_reply_count, contacted_count),
        "public_issue_rate_from_contacted": rate(public_issue_count, contacted_count),
        "accepted_evidence_rate_from_public_issues": rate(accepted_evidence_count, public_issue_count),
        "remaining_contacts_to_first_public_issue": 0 if public_issue_count else 1,
        "resume_claim_status": "blocked_until_public_evidence",
    }


def build_next_unlocks(current_counts: dict[str, int], slots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    slot_by_metric: dict[str, list[dict[str, Any]]] = {}
    for slot in slots:
        slot_by_metric.setdefault(slot["counts_toward"], []).append(slot)

    targets = {
        "external_feedback_items": {
            "target": 1,
            "resume_line_after_unlock": "Received first public non-owner product feedback issue for the demo.",
        },
        "confirmed_external_users": {
            "target": 1,
            "resume_line_after_unlock": "Recorded first permissioned external user trying the public demo or local replay.",
        },
        "reproducible_feedback_items": {
            "target": 1,
            "resume_line_after_unlock": "Received first reproducible local/Docker replay from a non-owner reviewer.",
        },
        "business_case_feedback_items": {
            "target": 1,
            "resume_line_after_unlock": "Validated the agent against a first anonymized real-world data-quality case.",
        },
        "ai_engineer_review_items": {
            "target": 1,
            "resume_line_after_unlock": "Received first public AI Engineer review of agent design, tools, and evidence quality.",
        },
    }
    unlocks = []
    for metric, config in targets.items():
        current = current_counts.get(metric, 0)
        candidate_slots = slot_by_metric.get(metric, [])
        unlocks.append(
            {
                "metric": metric,
                "current_count": current,
                "target_count": config["target"],
                "remaining_needed": max(0, config["target"] - current),
                "candidate_slots": [slot["slot_id"] for slot in candidate_slots],
                "next_manual_action": (
                    "Ask one listed reviewer slot to submit a public redacted GitHub issue with permission to count."
                    if current < config["target"]
                    else "Run the evidence gate and update resume outcome metrics."
                ),
                "resume_line_after_unlock": config["resume_line_after_unlock"],
                "claimable_now": current >= config["target"],
            }
        )
    return unlocks


def build_reviewer_outreach_status_board() -> dict[str, Any]:
    outreach = load_json(OUTREACH_PACK_PATH)
    share_kit = load_json(SHARE_KIT_PATH)
    outcome_metrics = load_json(RESUME_OUTCOME_METRICS_PATH)
    events = load_outreach_events()

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
                "reviewer_contact": None,
                "channel_used": None,
                "sent_at": None,
                "last_event_at": None,
                "reply_received": False,
                "public_evidence_url": None,
                "permission_to_count": False,
                "no_private_data_confirmed": False,
                "accepted_by_gate": False,
                "next_action": "Send manually only after choosing a real reviewer.",
                "resume_counting_rule": (
                    "Does not count until a non-owner public GitHub issue passes the evidence gate."
                ),
                "privacy_boundary": item["privacy_boundary"],
            }
        )
    apply_outreach_events(slots, events)

    tracked_counts = {item["metric"]: item["current_count"] for item in outcome_metrics["tracked_outcomes"]}
    current_counts = {
        "external_feedback_items": tracked_counts["external_feedback_items"],
        "confirmed_external_users": tracked_counts["confirmed_external_users"],
        "reproducible_feedback_items": tracked_counts["reproducible_feedback_items"],
        "business_case_feedback_items": tracked_counts["business_case_feedback_items"],
        "ai_engineer_review_items": tracked_counts["ai_engineer_review_items"],
    }
    conversion_metrics = calculate_conversion_metrics(slots)
    next_unlocks = build_next_unlocks(current_counts, slots)

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
        "recorded_event_count": len(events),
        "not_sent_count": sum(1 for slot in slots if slot["status"] == "not_sent"),
        "sent_count": sum(1 for slot in slots if slot["status"] == "sent"),
        "reply_count": sum(1 for slot in slots if slot["reply_received"]),
        "public_issue_submitted_count": sum(1 for slot in slots if slot["status"] == "public_issue_submitted"),
        "accepted_evidence_count": 0,
        "resume_upgrade_count": 0,
        "conversion_metrics": conversion_metrics,
        "next_resume_unlocks": next_unlocks,
        "next_resume_unlock_count": len(next_unlocks),
        "blocked_unlock_count": sum(1 for unlock in next_unlocks if not unlock["claimable_now"]),
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
            f"{len(stages)} status stages, {len(current_counts)} evidence goals, {len(events)} recorded outreach "
            f"events, {conversion_metrics['contact_rate']:.0%} contact-to-slot coverage, and zero accepted-evidence "
            "or resume-upgrade claims."
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
    conversion_rows = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["conversion_metrics"].items()
    )
    unlock_rows = "\n".join(
        "| {metric} | {current_count} | {target_count} | {remaining_needed} | {slots} | {claimable_now} |".format(
            metric=unlock["metric"],
            current_count=unlock["current_count"],
            target_count=unlock["target_count"],
            remaining_needed=unlock["remaining_needed"],
            slots=", ".join(unlock["candidate_slots"]),
            claimable_now=unlock["claimable_now"],
        )
        for unlock in payload["next_resume_unlocks"]
    )
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

## Recorded Events

| Metric | Count |
| --- | ---: |
| Recorded outreach events | {payload["recorded_event_count"]} |
| Sent messages | {payload["sent_count"]} |
| Replies or public submissions | {payload["reply_count"]} |
| Public issues submitted | {payload["public_issue_submitted_count"]} |
| Accepted evidence | {payload["accepted_evidence_count"]} |

## Conversion Metrics

| Metric | Value |
| --- | ---: |
{conversion_rows}

## Next Resume Unlocks

| Metric | Current | Target | Remaining | Candidate Slots | Claimable Now |
| --- | ---: | ---: | ---: | --- | --- |
{unlock_rows}

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
        "source_outreach_item_count": 9,
        "source_share_channel_count": 5,
        "status_stage_count": 5,
        "outreach_slot_count": 9,
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
        raise AssertionError("status board must include nine reviewer slots")
    conversion = payload.get("conversion_metrics", {})
    expected_conversion = {
        "tracked_slot_count": expected["outreach_slot_count"],
        "accepted_evidence_count": 0,
        "resume_claim_status": "blocked_until_public_evidence",
    }
    for key, value in expected_conversion.items():
        if conversion.get(key) != value:
            raise AssertionError(f"conversion metric {key} expected {value!r}, got {conversion.get(key)!r}")
    if conversion.get("contacted_count", 0) > expected["outreach_slot_count"]:
        raise AssertionError("conversion metrics cannot contact more reviewers than tracked slots")
    if conversion.get("public_issue_count", 0) > conversion.get("contacted_count", 0):
        raise AssertionError("conversion metrics cannot submit more public issues than contacted reviewers")
    if payload.get("next_resume_unlock_count") != 5:
        raise AssertionError("status board must identify five next resume unlocks")
    if payload.get("blocked_unlock_count") != len(payload.get("next_resume_unlocks", [])):
        raise AssertionError("all resume unlocks must remain blocked until evidence exists")
    for value in payload.get("current_outcome_counts", {}).values():
        if value != 0:
            raise AssertionError("status board must preserve zero current outcome counts")
    counted_statuses = {"not_sent", "sent", "replied_private", "public_issue_submitted"}
    if payload["not_sent_count"] + payload["sent_count"] + sum(
        1 for slot in payload["outreach_slots"] if slot["status"] in {"replied_private", "public_issue_submitted"}
    ) != expected["outreach_slot_count"]:
        raise AssertionError("status board slot status counts must cover every outreach slot")
    for slot in payload["outreach_slots"]:
        if slot["status"] not in counted_statuses:
            raise AssertionError("status board contains an unsupported outreach status")
        if slot["status"] == "not_sent" and slot["sent_at"] is not None:
            raise AssertionError("status board must not fabricate sent timestamps")
        if slot["status"] == "not_sent" and slot["reply_received"] is not False:
            raise AssertionError("status board must not fabricate reviewer replies")
        if slot["status"] != "public_issue_submitted" and slot["public_evidence_url"] is not None:
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
        "blocked_until_public_evidence",
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
