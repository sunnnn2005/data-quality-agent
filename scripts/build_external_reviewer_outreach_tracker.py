import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_REVIEWER_REQUEST_PACK_PATH = ROOT / "docs" / "external-reviewer-request-pack.json"
EXTERNAL_RUN_QUICKSTART_PATH = ROOT / "docs" / "external-run-quickstart.json"
PILOT_REVIEW_TRACKER_PATH = ROOT / "docs" / "pilot-review-tracker.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "external-reviewer-outreach-tracker.json"
OUTPUT_MD_PATH = ROOT / "docs" / "external-reviewer-outreach-tracker.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_external_reviewer_outreach_tracker() -> dict[str, Any]:
    request_pack = load_json(EXTERNAL_REVIEWER_REQUEST_PACK_PATH)
    quickstart = load_json(EXTERNAL_RUN_QUICKSTART_PATH)
    pilot_tracker = load_json(PILOT_REVIEW_TRACKER_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    queue = [
        {
            "id": "classmate-demo-review",
            "target_segment": "UC Davis data science classmate or DS club member",
            "message_source": "classmate_public_demo",
            "recommended_channel": "LinkedIn DM, Discord, or in-person class message",
            "requested_action": "Try the public demo and submit one feedback issue.",
            "primary_link": quickstart["public_demo_url"],
            "secondary_link": request_pack["public_collection_issue"]["url"],
            "status": "not_contacted",
            "public_evidence_link": None,
            "counts_toward_resume": False,
            "follow_up_after_days": 4,
        },
        {
            "id": "developer-local-run",
            "target_segment": "student developer, OSS reviewer, or AI engineering peer",
            "message_source": "developer_container_smoke_run",
            "recommended_channel": "GitHub discussion, LinkedIn DM, or project channel",
            "requested_action": "Run the GHCR container or Docker Compose PostgreSQL replay and open External Run Review.",
            "primary_link": quickstart["public_url"],
            "secondary_link": quickstart["review_template"],
            "status": "not_contacted",
            "public_evidence_link": None,
            "counts_toward_resume": False,
            "follow_up_after_days": 5,
        },
        {
            "id": "mentor-postgres-replay",
            "target_segment": "mentor, recruiter, hiring manager, or data practitioner",
            "message_source": "mentor_postgres_replay",
            "recommended_channel": "LinkedIn DM or email",
            "requested_action": "Review the application evidence pack or run the PostgreSQL replay and comment on credibility.",
            "primary_link": quickstart["public_url"],
            "secondary_link": request_pack["external_run_review_template"]["url"],
            "status": "not_contacted",
            "public_evidence_link": None,
            "counts_toward_resume": False,
            "follow_up_after_days": 7,
        },
    ]
    public_counts = {
        "external_feedback_items": feedback["external_feedback_items"],
        "confirmed_external_users": feedback["confirmed_external_users"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        "business_case_feedback_items": feedback["business_case_feedback_items"],
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_external_reviewer_outreach_tracker.py",
        "purpose": (
            "Convert the external-run quickstart and reviewer request pack into a trackable outreach queue "
            "without counting private messages, sent invitations, or unverified replies as users or feedback."
        ),
        "queue_count": len(queue),
        "queue": queue,
        "status_counts": {
            "not_contacted": sum(1 for item in queue if item["status"] == "not_contacted"),
            "contacted": sum(1 for item in queue if item["status"] == "contacted"),
            "public_evidence_received": sum(1 for item in queue if item["status"] == "public_evidence_received"),
        },
        "source_message_count": len(request_pack["outreach_messages"]),
        "quickstart_review_path_count": quickstart["review_path_count"],
        "quickstart_submission_field_count": quickstart["submission_field_count"],
        "linked_pilot_review_slots": pilot_tracker["planned_review_count"],
        "public_counts": public_counts,
        "counting_rules": [
            "A sent message does not count as feedback.",
            "A private reply does not count unless the reviewer gives permission to cite it publicly.",
            "A run counts only after a public issue, review note, or External Run Review includes enough evidence.",
            "No private business data should be posted; only redacted schemas, commands, and summaries are allowed.",
        ],
        "resume_upgrade_rules": pilot_tracker["resume_upgrade_rules"],
        "not_claimed": quickstart["not_claimed"] + [
            "No outreach message has been sent yet.",
            "No contacted reviewer is claimed yet.",
        ],
        "resume_safe_summary": (
            "Published a CI-verified external reviewer outreach tracker with 3 queued reviewer segments, "
            "3 source outreach messages, the external-run quickstart, follow-up windows, public-evidence rules, "
            "and zero contacted-reviewer or feedback claims."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    queue_rows = "\n".join(
        "| {id} | {target_segment} | {status} | [{primary_link}]({primary_link}) | {follow_up_after_days} | {counts_toward_resume} |".format(
            **item
        )
        for item in payload["queue"]
    )
    status_rows = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["status_counts"].items())
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["public_counts"].items())
    rules = "\n".join(f"- {item}" for item in payload["counting_rules"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# External Reviewer Outreach Tracker

This generated tracker turns reviewer outreach into an auditable queue.

## Purpose

{payload["purpose"]}

## Queue

| ID | Target Segment | Status | Primary Link | Follow Up After Days | Counts Toward Resume |
| --- | --- | --- | --- | ---: | --- |
{queue_rows}

## Status Counts

| Status | Count |
| --- | ---: |
{status_rows}

## Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Counting Rules

{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_external_reviewer_outreach_tracker(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "queue_count": 3,
        "source_message_count": 3,
        "quickstart_review_path_count": 3,
        "quickstart_submission_field_count": 8,
        "linked_pilot_review_slots": 3,
        "not_contacted": 3,
        "contacted": 0,
        "public_evidence_received": 0,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
    }
    if payload["queue_count"] != expected["queue_count"]:
        raise AssertionError("external reviewer outreach tracker must include 3 queue entries")
    for key in ("source_message_count", "quickstart_review_path_count", "quickstart_submission_field_count"):
        if payload[key] != expected[key]:
            raise AssertionError(f"{key} expected {expected[key]!r}, got {payload[key]!r}")
    if payload["linked_pilot_review_slots"] != expected["linked_pilot_review_slots"]:
        raise AssertionError("external reviewer outreach tracker must link the 3 pilot review slots")
    for key in ("not_contacted", "contacted", "public_evidence_received"):
        if payload["status_counts"][key] != expected[key]:
            raise AssertionError(f"status {key} expected {expected[key]!r}")
    for key in ("external_feedback_items", "confirmed_external_users"):
        if payload["public_counts"][key] != expected[key]:
            raise AssertionError(f"public count {key} must remain zero before evidence")
    if any(item["counts_toward_resume"] for item in payload["queue"]):
        raise AssertionError("queued outreach must not count toward resume before public evidence")
    for item in payload["queue"]:
        if not item["primary_link"].startswith("https://"):
            raise AssertionError("queue primary links must be public HTTPS URLs")
    for required in ("No outreach message has been sent yet.", "No contacted reviewer is claimed yet."):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"external reviewer outreach tracker must preserve not-claimed signal: {required}")
    return {"external_reviewer_outreach_tracker_verified": True, **expected}


def main() -> None:
    payload = build_external_reviewer_outreach_tracker()
    verify_external_reviewer_outreach_tracker(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
