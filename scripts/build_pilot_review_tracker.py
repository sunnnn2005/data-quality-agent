import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PILOT_PLAN_PATH = ROOT / "docs" / "pilot-program-plan.json"
PILOT_OUTREACH_PATH = ROOT / "docs" / "pilot-outreach-kit.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "pilot-review-tracker.json"
OUTPUT_MD_PATH = ROOT / "docs" / "pilot-review-tracker.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_pilot_review_tracker_payload() -> dict[str, Any]:
    plan = load_json(PILOT_PLAN_PATH)
    outreach = load_json(PILOT_OUTREACH_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    segments = plan["participant_segments"]
    review_paths = plan["review_paths"]
    planned_reviews = [
        {
            "id": "student-review-1",
            "segment": "student_reviewers",
            "target_source": segments[0]["source"],
            "requested_action": segments[0]["requested_action"],
            "primary_review_path": review_paths["quick_demo"],
            "secondary_review_path": review_paths["feedback_issue"],
            "status": "not_contacted",
            "public_evidence_link": None,
            "counts_toward_resume": False,
            "next_step": "Send a short demo-review request to one UC Davis classmate or club member.",
        },
        {
            "id": "developer-review-1",
            "segment": "developer_reviewers",
            "target_source": segments[1]["source"],
            "requested_action": segments[1]["requested_action"],
            "primary_review_path": review_paths["github_repo"],
            "secondary_review_path": review_paths["bug_report"],
            "status": "not_contacted",
            "public_evidence_link": None,
            "counts_toward_resume": False,
            "next_step": "Ask one student developer to run the repo locally or inspect the API contract.",
        },
        {
            "id": "career-review-1",
            "segment": "career_reviewers",
            "target_source": segments[2]["source"],
            "requested_action": segments[2]["requested_action"],
            "primary_review_path": review_paths["application_evidence_pack"],
            "secondary_review_path": review_paths["business_case_review"],
            "status": "not_contacted",
            "public_evidence_link": None,
            "counts_toward_resume": False,
            "next_step": "Ask one mentor, recruiter, or hiring manager to review the evidence pack.",
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
        "generated_by": "scripts/build_pilot_review_tracker.py",
        "purpose": (
            "Track planned pilot review requests, public evidence links, and resume-safe status without counting "
            "private messages or unverified compliments as users or feedback."
        ),
        "planned_review_count": len(planned_reviews),
        "planned_reviews": planned_reviews,
        "status_counts": {
            "not_contacted": sum(1 for item in planned_reviews if item["status"] == "not_contacted"),
            "contacted": sum(1 for item in planned_reviews if item["status"] == "contacted"),
            "feedback_received": sum(1 for item in planned_reviews if item["status"] == "feedback_received"),
        },
        "public_counts": public_counts,
        "resume_upgrade_rules": [
            {
                "signal": "public pilot feedback",
                "current_value": public_counts["external_feedback_items"],
                "minimum_before_claim": plan["success_thresholds"]["minimum_feedback_items_before_resume_claim"],
                "required_evidence": "public GitHub issue labeled feedback",
                "resume_status": "not_claimable_yet",
            },
            {
                "signal": "external reviewer tried the project",
                "current_value": public_counts["confirmed_external_users"],
                "minimum_before_claim": plan["success_thresholds"]["minimum_confirmed_users_before_user_claim"],
                "required_evidence": "public issue or note labeled confirmed-user",
                "resume_status": "not_claimable_yet",
            },
            {
                "signal": "real-world business case feedback",
                "current_value": public_counts["business_case_feedback_items"],
                "minimum_before_claim": 1,
                "required_evidence": "public issue using the business-case template",
                "resume_status": "not_claimable_yet",
            },
        ],
        "tracking_rules": outreach["tracking_rules"],
        "not_claimed": outreach["not_claimed"],
        "resume_safe_summary": (
            "Published a CI-verified pilot review tracker with 3 planned reviewer segments, public evidence links, "
            "status counts, and resume-upgrade rules while preserving zero verified feedback and user claims."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    review_rows = "\n".join(
        "| {id} | {segment} | {status} | [{primary_review_path}]({primary_review_path}) | {counts_toward_resume} | {next_step} |".format(
            **item
        )
        for item in payload["planned_reviews"]
    )
    status_rows = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["status_counts"].items())
    count_rows = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["public_counts"].items())
    upgrade_rows = "\n".join(
        "| {signal} | {current_value} | {minimum_before_claim} | {required_evidence} | `{resume_status}` |".format(
            **item
        )
        for item in payload["resume_upgrade_rules"]
    )
    tracking_rules = "\n".join(f"- {item}" for item in payload["tracking_rules"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Pilot Review Tracker

This generated tracker turns the pilot plan into an auditable review pipeline.

## Purpose

{payload["purpose"]}

## Planned Reviews

| ID | Segment | Status | Primary Review Path | Counts Toward Resume | Next Step |
| --- | --- | --- | --- | --- | --- |
{review_rows}

## Status Counts

| Status | Count |
| --- | ---: |
{status_rows}

## Public Counts

| Metric | Current value |
| --- | ---: |
{count_rows}

## Resume Upgrade Rules

| Signal | Current Value | Minimum Before Claim | Required Evidence | Status |
| --- | ---: | ---: | --- | --- |
{upgrade_rows}

## Tracking Rules

{tracking_rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_pilot_review_tracker(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "planned_review_count": 3,
        "not_contacted_count": 3,
        "contacted_count": 0,
        "feedback_received_count": 0,
        "resume_upgrade_rule_count": 3,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "business_case_feedback_items": 0,
    }
    if payload["planned_review_count"] != expected["planned_review_count"]:
        raise AssertionError("pilot review tracker must include three planned reviews")
    statuses = payload["status_counts"]
    if statuses["not_contacted"] != expected["not_contacted_count"]:
        raise AssertionError("pilot review tracker must start with three not-contacted reviews")
    if statuses["contacted"] != expected["contacted_count"]:
        raise AssertionError("pilot review tracker must not count contacts before outreach happens")
    if statuses["feedback_received"] != expected["feedback_received_count"]:
        raise AssertionError("pilot review tracker must not count feedback before public evidence exists")
    if len(payload["resume_upgrade_rules"]) != expected["resume_upgrade_rule_count"]:
        raise AssertionError("pilot review tracker must include three resume-upgrade rules")
    counts = payload["public_counts"]
    for key in ("external_feedback_items", "confirmed_external_users", "business_case_feedback_items"):
        if counts[key] != expected[key]:
            raise AssertionError(f"pilot review tracker must preserve zero {key}")
    if any(item["counts_toward_resume"] for item in payload["planned_reviews"]):
        raise AssertionError("planned reviews must not count toward resume before public evidence is linked")
    if not all(rule["resume_status"] == "not_claimable_yet" for rule in payload["resume_upgrade_rules"]):
        raise AssertionError("resume-upgrade rules must remain not claimable before evidence")
    for required in ("external users", "customer feedback", "enterprise production usage"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"pilot review tracker must not claim {required}")
    return {"pilot_review_tracker_verified": True, **expected}


def main() -> None:
    payload = build_pilot_review_tracker_payload()
    verify_pilot_review_tracker(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
