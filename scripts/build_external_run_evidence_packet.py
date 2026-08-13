import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNNABLE_RELEASE_PATH = ROOT / "docs" / "runnable-release-packet.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "external-run-evidence-packet.json"
OUTPUT_MD_PATH = ROOT / "docs" / "external-run-evidence-packet.md"
PUBLIC_COLLECTION_ISSUE_URL = "https://github.com/sunnnn2005/data-quality-agent/issues/18"
EXTERNAL_RUN_REVIEW_TEMPLATE_URL = (
    "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_external_run_evidence_packet() -> dict[str, Any]:
    runnable = load_json(RUNNABLE_RELEASE_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    feedback_url = feedback["feedback_issue_template"]
    review_paths = [
        {
            "id": "public_demo_review",
            "surface": "public_demo",
            "time_box_minutes": 8,
            "required_evidence": [
                "public demo URL opened",
                "support-ticket finding inspected",
                "one useful or confusing point written by reviewer",
            ],
            "counts_toward_after_public_issue": "external_feedback_items",
        },
        {
            "id": "container_smoke_run",
            "surface": "ghcr_container",
            "time_box_minutes": 12,
            "command": "docker run --rm -p 8000:8000 ghcr.io/sunnnn2005/data-quality-agent:latest",
            "required_evidence": [
                "host OS and Docker version",
                "health endpoint response",
                "quality-report endpoint response status",
            ],
            "counts_toward_after_public_issue": "confirmed_external_users",
        },
        {
            "id": "postgres_replay_run",
            "surface": "docker_compose_business_demo",
            "time_box_minutes": 15,
            "command": "docker compose up --build",
            "required_evidence": [
                "compose command completed",
                "PostgreSQL support-ticket route called",
                "agent-report fallback or model-backed status captured",
            ],
            "counts_toward_after_public_issue": "reproducible_feedback_items",
        },
    ]
    submission_fields = [
        {"name": "reviewer_role", "required": True, "example": "student developer, data analyst, recruiter, mentor"},
        {"name": "path_tried", "required": True, "example": "public_demo_review or container_smoke_run"},
        {"name": "environment", "required": True, "example": "macOS 15, Docker Desktop 4.x, Chrome"},
        {"name": "commands_or_urls_used", "required": True, "example": "docker compose up --build"},
        {"name": "observed_result", "required": True, "example": "health returned ok and support-ticket report loaded"},
        {"name": "usefulness_score_1_to_5", "required": True, "example": "4"},
        {"name": "main_feedback", "required": True, "example": "setup was clear, but report explanation could be shorter"},
        {"name": "permission_to_count_publicly", "required": True, "example": "yes"},
    ]
    upgrade_rules = [
        {
            "claim": "tried by an external reviewer",
            "metric": "confirmed_external_users",
            "minimum_public_count": 1,
            "required_label": "confirmed-user",
        },
        {
            "claim": "collected external feedback",
            "metric": "external_feedback_items",
            "minimum_public_count": 3,
            "required_label": "feedback",
        },
        {
            "claim": "validated through reproducible local replay",
            "metric": "reproducible_feedback_items",
            "minimum_public_count": 1,
            "required_label": "reproducible",
        },
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_external_run_evidence_packet.py",
        "purpose": (
            "Turn external reviewer runs into public, resume-safe evidence by requiring commands, environment, "
            "observed results, and permission before any user or feedback claim is counted."
        ),
        "input_artifacts": {
            "runnable_release_packet": "docs/runnable-release-packet.json",
            "feedback_metrics": "docs/feedback-metrics.json",
        },
        "review_path_count": len(review_paths),
        "review_paths": review_paths,
        "submission_url": feedback_url,
        "external_run_review_template": {
            "path": ".github/ISSUE_TEMPLATE/external_run_review.md",
            "url": EXTERNAL_RUN_REVIEW_TEMPLATE_URL,
            "purpose": "Structured issue template for one reviewer run when a separate issue is easier than commenting on issue #18.",
        },
        "public_collection_issue": {
            "number": 18,
            "url": PUBLIC_COLLECTION_ISSUE_URL,
            "purpose": "Public issue where external reviewers can comment with run evidence using the packet template.",
            "counting_status": "collection_open_not_counted_yet",
        },
        "submission_field_count": len(submission_fields),
        "submission_fields": submission_fields,
        "upgrade_rule_count": len(upgrade_rules),
        "upgrade_rules": upgrade_rules,
        "current_counts": {
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        },
        "runnable_surface_count": len(runnable["runnable_surfaces"]),
        "acceptance_check_count": len(runnable["acceptance_checks"]),
        "privacy_boundaries": [
            "Do not ask reviewers to upload private business data.",
            "Do not store raw reviewer datasets in this repository.",
            "Ask for anonymized field names, command output summaries, and screenshots only when safe.",
            "Count only public GitHub issues where the reviewer gave permission to count the run.",
        ],
        "not_claimed": [
            "No external reviewer run is claimed yet.",
            "No external users are claimed yet.",
            "No customer feedback is claimed yet.",
            "No enterprise deployment is claimed yet.",
        ],
        "resume_safe_summary": (
            "Published an external-run evidence packet and public collection issue defining 3 reviewer run paths, "
            "8 required submission fields, 3 resume-upgrade rules, and privacy boundaries for converting future "
            "reviewer runs into public evidence."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    paths = "\n".join(
        (
            f"| {path['id']} | {path['surface']} | {path['time_box_minutes']} | "
            f"`{path.get('command', '-')}` | `{path['counts_toward_after_public_issue']}` |"
        )
        for path in payload["review_paths"]
    )
    fields = "\n".join(
        "| {name} | {required} | {example} |".format(**field) for field in payload["submission_fields"]
    )
    rules = "\n".join(
        "| {claim} | `{metric}` | {minimum_public_count} | `{required_label}` |".format(**rule)
        for rule in payload["upgrade_rules"]
    )
    counts = "\n".join(
        f"| {metric.replace('_', ' ').title()} | {value} |" for metric, value in payload["current_counts"].items()
    )
    boundaries = "\n".join(f"- {item}" for item in payload["privacy_boundaries"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# External Run Evidence Packet

This generated packet defines how an outside reviewer can run the project and submit evidence that is safe to count later.

## Purpose

{payload["purpose"]}

## Reviewer Run Paths

| Path | Surface | Minutes | Command | Counts Toward After Public Issue |
| --- | --- | ---: | --- | --- |
{paths}

Submission URL: [{payload["submission_url"]}]({payload["submission_url"]})

External run review template: [{payload["external_run_review_template"]["url"]}]({payload["external_run_review_template"]["url"]})

Public collection issue: [#{payload["public_collection_issue"]["number"]}]({payload["public_collection_issue"]["url"]})

Counting status: `{payload["public_collection_issue"]["counting_status"]}`

## Required Submission Fields

| Field | Required | Example |
| --- | --- | --- |
{fields}

## Resume Upgrade Rules

| Future Claim | Metric | Minimum Public Count | Required Label |
| --- | --- | ---: | --- |
{rules}

## Current Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Privacy Boundaries

{boundaries}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_external_run_evidence_packet(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["review_path_count"] != 3:
        raise AssertionError("external run evidence packet must define 3 reviewer run paths")
    if payload["submission_field_count"] != 8:
        raise AssertionError("external run evidence packet must define 8 submission fields")
    if payload["upgrade_rule_count"] != 3:
        raise AssertionError("external run evidence packet must define 3 upgrade rules")
    if payload["runnable_surface_count"] != 3:
        raise AssertionError("external run evidence packet must link 3 runnable surfaces")
    if payload["acceptance_check_count"] != 4:
        raise AssertionError("external run evidence packet must link 4 acceptance checks")
    if payload["public_collection_issue"]["url"] != PUBLIC_COLLECTION_ISSUE_URL:
        raise AssertionError("external run evidence packet must link the public collection issue")
    if payload["external_run_review_template"]["url"] != EXTERNAL_RUN_REVIEW_TEMPLATE_URL:
        raise AssertionError("external run evidence packet must link the external run review template")
    if payload["public_collection_issue"]["counting_status"] != "collection_open_not_counted_yet":
        raise AssertionError("external run evidence packet must keep collection open but uncounted")
    commands = " ".join(path.get("command", "") for path in payload["review_paths"])
    if "docker run" not in commands or "docker compose up --build" not in commands:
        raise AssertionError("external run evidence packet must include container and compose commands")
    required_fields = {field["name"] for field in payload["submission_fields"] if field["required"]}
    expected_fields = {
        "reviewer_role",
        "path_tried",
        "environment",
        "commands_or_urls_used",
        "observed_result",
        "usefulness_score_1_to_5",
        "main_feedback",
        "permission_to_count_publicly",
    }
    if required_fields != expected_fields:
        raise AssertionError("external run evidence packet submission fields changed")
    expected_counts = {
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
    }
    if payload["current_counts"] != expected_counts:
        raise AssertionError("external run evidence packet must preserve zero external-run baseline")
    labels = {rule["required_label"] for rule in payload["upgrade_rules"]}
    if labels != {"feedback", "confirmed-user", "reproducible"}:
        raise AssertionError("external run evidence packet must map to public feedback labels")
    for forbidden in ("No external reviewer run", "No external users", "No customer feedback", "No enterprise deployment"):
        if not any(item.startswith(forbidden) for item in payload["not_claimed"]):
            raise AssertionError(f"external run evidence packet must include not-claimed text for {forbidden}")
    return {
        "external_run_evidence_packet_verified": True,
        "review_path_count": payload["review_path_count"],
        "submission_field_count": payload["submission_field_count"],
        "upgrade_rule_count": payload["upgrade_rule_count"],
    }


def main() -> None:
    payload = build_external_run_evidence_packet()
    verify_external_run_evidence_packet(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
