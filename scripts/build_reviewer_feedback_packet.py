import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTCOME_UPGRADE_PATH = ROOT / "docs" / "outcome-upgrade-playbook.json"
PILOT_REVIEW_TRACKER_PATH = ROOT / "docs" / "pilot-review-tracker.json"
APPLICATION_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-feedback-packet.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-feedback-packet.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_reviewer_feedback_packet() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    upgrade = load_json(OUTCOME_UPGRADE_PATH)
    tracker = load_json(PILOT_REVIEW_TRACKER_PATH)
    application_pack = load_json(APPLICATION_PACK_PATH)
    links = application_pack["application_links"]
    feedback_channels = {item["name"]: item["url"] for item in feedback["feedback_channels"]}
    reviewer_tasks = [
        {
            "id": "quick_demo_review",
            "audience": "classmate_or_student_developer",
            "time_box_minutes": 8,
            "path": links["demo"],
            "ask": "Open the public demo, read the support-ticket result, and report what is unclear or convincing.",
            "counts_toward": "external_feedback_items",
            "submission_url": feedback_channels["Demo feedback"],
        },
        {
            "id": "local_repo_review",
            "audience": "student_developer_or_open_source_reviewer",
            "time_box_minutes": 15,
            "path": links["github_repo"],
            "ask": "Run or inspect the repo, then confirm whether the setup and agent evidence trail are reproducible.",
            "counts_toward": "confirmed_external_users",
            "submission_url": feedback_channels["Demo feedback"],
        },
        {
            "id": "business_case_review",
            "audience": "mentor_recruiter_or_data_practitioner",
            "time_box_minutes": 12,
            "path": f"{links['github_repo']}/blob/main/docs/business-case-intake.md",
            "ask": "Review whether the project maps to a realistic data-quality failure and submit an anonymized business-case note.",
            "counts_toward": "business_case_feedback_items",
            "submission_url": feedback_channels["Business case review"],
        },
    ]
    evidence_questions = [
        "Which path did you try: public demo, local repo, API docs, or business-case review?",
        "Could you reproduce or understand the support-ticket data-quality failure?",
        "What is the strongest AI-agent signal in the project?",
        "What was confusing, missing, or not credible enough for an internship reviewer?",
        "Would you classify your note as feedback, confirmed run, reproducible issue, feature request, or business-case review?",
    ]
    conversion_paths = [
        {"metric": "external_feedback_items", "label": "feedback", "threshold": 3},
        {"metric": "confirmed_external_users", "label": "confirmed-user", "threshold": 1},
        {"metric": "reproducible_feedback_items", "label": "reproducible", "threshold": 1},
        {"metric": "business_case_feedback_items", "label": "business-case", "threshold": 1},
    ]
    current_counts = {
        "external_feedback_items": feedback["external_feedback_items"],
        "confirmed_external_users": feedback["confirmed_external_users"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        "business_case_feedback_items": feedback["business_case_feedback_items"],
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_feedback_packet.py",
        "purpose": (
            "Give reviewers a short, public, metric-aware path for trying the project and submitting evidence that "
            "can later upgrade resume outcomes without inflating the current baseline."
        ),
        "reviewer_task_count": len(reviewer_tasks),
        "reviewer_tasks": reviewer_tasks,
        "evidence_question_count": len(evidence_questions),
        "evidence_questions": evidence_questions,
        "conversion_path_count": len(conversion_paths),
        "conversion_paths": conversion_paths,
        "current_public_counts": current_counts,
        "linked_upgrade_rules": [rule["id"] for rule in upgrade["upgrade_rules"]],
        "planned_review_slots": tracker["planned_review_count"],
        "resume_status": "collection_ready_not_claimable",
        "not_claimed": upgrade["forbidden_until_proven"],
        "resume_safe_summary": (
            "Published a CI-verified reviewer feedback packet with 3 task paths, 5 evidence questions, "
            "4 metric conversion paths, and zero current feedback/adoption counts."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    tasks = "\n".join(
        "| {id} | {audience} | {time_box_minutes} | [{path}]({path}) | `{counts_toward}` | [Submit]({submission_url}) |".format(
            **task
        )
        for task in payload["reviewer_tasks"]
    )
    questions = "\n".join(f"{index}. {question}" for index, question in enumerate(payload["evidence_questions"], 1))
    paths = "\n".join(
        "| {metric} | `{label}` | {threshold} |".format(**path) for path in payload["conversion_paths"]
    )
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_public_counts"].items()
    )
    rules = "\n".join(f"- `{rule}`" for rule in payload["linked_upgrade_rules"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Reviewer Feedback Packet

This generated packet gives external reviewers a short path to try the project and submit public evidence.

## Purpose

{payload["purpose"]}

## Reviewer Tasks

| Task | Audience | Minutes | Path | Counts Toward | Submission |
| --- | --- | ---: | --- | --- | --- |
{tasks}

## Evidence Questions

{questions}

## Metric Conversion Paths

| Metric | Required Label | Upgrade Threshold |
| --- | --- | ---: |
{paths}

## Current Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Linked Upgrade Rules

{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_reviewer_feedback_packet(payload: dict[str, Any]) -> dict[str, Any]:
    expected_counts = {
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
        "business_case_feedback_items": 0,
    }
    if payload["reviewer_task_count"] != 3:
        raise AssertionError("reviewer feedback packet must define three reviewer tasks")
    if payload["evidence_question_count"] != 5:
        raise AssertionError("reviewer feedback packet must define five evidence questions")
    if payload["conversion_path_count"] != 4:
        raise AssertionError("reviewer feedback packet must define four metric conversion paths")
    if payload["current_public_counts"] != expected_counts:
        raise AssertionError("reviewer feedback packet must preserve zero public feedback baseline")
    if payload["planned_review_slots"] != 3:
        raise AssertionError("reviewer feedback packet must link three planned review slots")
    if payload["resume_status"] != "collection_ready_not_claimable":
        raise AssertionError("reviewer feedback packet must not be resume-claimable as feedback yet")
    required_metrics = set(expected_counts)
    actual_metrics = {path["metric"] for path in payload["conversion_paths"]}
    if actual_metrics != required_metrics:
        raise AssertionError("reviewer feedback packet conversion paths must match feedback metrics")
    required_upgrade_rules = {
        "first_confirmed_external_run",
        "pilot_feedback_signal",
        "reproducible_bug_signal",
        "business_case_signal",
        "github_interest_signal",
    }
    if set(payload["linked_upgrade_rules"]) != required_upgrade_rules:
        raise AssertionError("reviewer feedback packet must link every outcome upgrade rule")
    for task in payload["reviewer_tasks"]:
        if not task["submission_url"].startswith("https://github.com/"):
            raise AssertionError("reviewer task submissions must use public GitHub issue links")
    for required in ("external users", "customer feedback", "enterprise production usage"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"reviewer feedback packet must not claim {required}")
    return {
        "reviewer_feedback_packet_verified": True,
        "reviewer_task_count": payload["reviewer_task_count"],
        "evidence_question_count": payload["evidence_question_count"],
        "conversion_path_count": payload["conversion_path_count"],
    }


def main() -> None:
    payload = build_reviewer_feedback_packet()
    verify_reviewer_feedback_packet(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
