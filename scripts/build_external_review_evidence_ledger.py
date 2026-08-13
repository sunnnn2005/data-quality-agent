import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PILOT_REVIEW_TRACKER_PATH = ROOT / "docs" / "pilot-review-tracker.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "external-review-evidence-ledger.json"
OUTPUT_MD_PATH = ROOT / "docs" / "external-review-evidence-ledger.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_external_review_evidence_ledger() -> dict[str, Any]:
    tracker = load_json(PILOT_REVIEW_TRACKER_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    evidence_requirements = [
        {
            "evidence_type": "demo_feedback",
            "required_public_source": "GitHub issue created from demo_feedback.md",
            "required_labels": ["feedback"],
            "counts_toward": "external_feedback_items",
            "resume_upgrade_after": 3,
        },
        {
            "evidence_type": "confirmed_run",
            "required_public_source": "GitHub issue or reproducible note confirming the reviewer tried the demo or ran the repo",
            "required_labels": ["confirmed-user"],
            "counts_toward": "confirmed_external_users",
            "resume_upgrade_after": 1,
        },
        {
            "evidence_type": "business_case_review",
            "required_public_source": "GitHub issue created from business_case_review.md",
            "required_labels": ["business-case"],
            "counts_toward": "business_case_feedback_items",
            "resume_upgrade_after": 1,
        },
        {
            "evidence_type": "reproducible_bug",
            "required_public_source": "GitHub issue with steps, environment, expected result, and actual result",
            "required_labels": ["bug", "reproducible"],
            "counts_toward": "reproducible_feedback_items",
            "resume_upgrade_after": 1,
        },
    ]
    empty_entries: list[dict[str, Any]] = []
    public_counts = {
        "external_feedback_items": feedback["external_feedback_items"],
        "confirmed_external_users": feedback["confirmed_external_users"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        "business_case_feedback_items": feedback["business_case_feedback_items"],
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_external_review_evidence_ledger.py",
        "purpose": (
            "Define the public evidence required before pilot reviews, feedback, confirmed runs, or business-case "
            "reviews can be converted into resume outcome claims."
        ),
        "entry_count": len(empty_entries),
        "entries": empty_entries,
        "evidence_requirement_count": len(evidence_requirements),
        "evidence_requirements": evidence_requirements,
        "public_counts": public_counts,
        "linked_planned_reviews": tracker["planned_review_count"],
        "review_status_counts": tracker["status_counts"],
        "resume_upgrade_rules": tracker["resume_upgrade_rules"],
        "resume_status": "not_claimable_yet",
        "not_claimed": tracker["not_claimed"],
        "resume_safe_summary": (
            "Published a CI-verified external review evidence ledger defining 4 public evidence types, "
            "3 linked pilot review slots, and zero current evidence entries before any feedback or adoption claims."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    requirements = "\n".join(
        "| {evidence_type} | {required_public_source} | {labels} | `{counts_toward}` | {resume_upgrade_after} |".format(
            labels=", ".join(item["required_labels"]),
            **item,
        )
        for item in payload["evidence_requirements"]
    )
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["public_counts"].items())
    statuses = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["review_status_counts"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# External Review Evidence Ledger

This generated ledger defines what public proof is required before any external review can become a resume outcome.

## Purpose

{payload["purpose"]}

## Current Ledger

| Metric | Current value |
| --- | ---: |
| Evidence entries | {payload["entry_count"]} |
| Linked planned reviews | {payload["linked_planned_reviews"]} |
| Evidence requirement types | {payload["evidence_requirement_count"]} |
| Resume status | `{payload["resume_status"]}` |

## Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Pilot Review Status

| Status | Count |
| --- | ---: |
{statuses}

## Evidence Requirements

| Evidence Type | Required Public Source | Required Labels | Counts Toward | Resume Upgrade After |
| --- | --- | --- | --- | ---: |
{requirements}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_external_review_evidence_ledger(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "entry_count": 0,
        "evidence_requirement_count": 4,
        "linked_planned_reviews": 3,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
        "business_case_feedback_items": 0,
    }
    if payload["entry_count"] != expected["entry_count"]:
        raise AssertionError("external review ledger must start with zero public evidence entries")
    if payload["evidence_requirement_count"] != expected["evidence_requirement_count"]:
        raise AssertionError("external review ledger must define four evidence requirement types")
    if payload["linked_planned_reviews"] != expected["linked_planned_reviews"]:
        raise AssertionError("external review ledger must link to three planned pilot reviews")
    if payload["resume_status"] != "not_claimable_yet":
        raise AssertionError("external review ledger must not be resume-claimable before evidence")
    required_types = {item["evidence_type"] for item in payload["evidence_requirements"]}
    for required in {"demo_feedback", "confirmed_run", "business_case_review", "reproducible_bug"}:
        if required not in required_types:
            raise AssertionError(f"external review ledger missing evidence type {required}")
    counts = payload["public_counts"]
    for key in (
        "external_feedback_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
    ):
        if counts[key] != expected[key]:
            raise AssertionError(f"external review ledger must preserve zero {key}")
    if payload["review_status_counts"]["not_contacted"] != 3:
        raise AssertionError("external review ledger must preserve the three not-contacted pilot reviews")
    for required in ("external users", "customer feedback", "enterprise production usage"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"external review ledger must not claim {required}")
    return {"external_review_evidence_ledger_verified": True, **expected}


def main() -> None:
    payload = build_external_review_evidence_ledger()
    verify_external_review_evidence_ledger(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
