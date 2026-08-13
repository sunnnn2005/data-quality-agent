import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / ".github" / "ISSUE_TEMPLATE" / "demo_feedback.md"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "feedback-intake-quality.json"
OUTPUT_MD_PATH = ROOT / "docs" / "feedback-intake-quality.md"


REQUIRED_TRY_PATHS = [
    "Public demo page",
    "Support-ticket case study",
    "CSV upload endpoint",
    "PostgreSQL Docker Compose demo",
    "LLM tool-calling route",
]
REQUIRED_SECTIONS = [
    "What did you try?",
    "What worked well?",
    "What was confusing or missing?",
    "Your environment",
    "Outcome",
]
REQUIRED_OUTCOMES = [
    "I could reproduce the verified support-ticket result.",
    "I found a bug.",
    "I have a feature request.",
    "I would use this pattern in a real data workflow.",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_feedback_intake_quality_payload() -> dict[str, Any]:
    template = TEMPLATE_PATH.read_text()
    metrics = load_json(FEEDBACK_METRICS_PATH)
    captured_fields = {
        "review_path": all(item in template for item in REQUIRED_TRY_PATHS),
        "positive_signal": "What worked well?" in template,
        "confusion_or_gap": "What was confusing or missing?" in template,
        "environment": all(item in template for item in ("OS:", "Python version:", "Command or URL used:")),
        "outcome_labels": all(item in template for item in REQUIRED_OUTCOMES),
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_feedback_intake_quality.py",
        "template_path": ".github/ISSUE_TEMPLATE/demo_feedback.md",
        "feedback_issue_template": metrics["feedback_issue_template"],
        "required_section_count": len(REQUIRED_SECTIONS),
        "required_try_path_count": len(REQUIRED_TRY_PATHS),
        "required_outcome_count": len(REQUIRED_OUTCOMES),
        "captured_field_count": sum(1 for value in captured_fields.values() if value),
        "captured_fields": captured_fields,
        "tracking_labels": metrics["tracking_labels"],
        "current_public_counts": {
            "external_feedback_items": metrics["external_feedback_items"],
            "confirmed_external_users": metrics["confirmed_external_users"],
            "reproducible_feedback_items": metrics["reproducible_feedback_items"],
            "bug_feedback_items": metrics["bug_feedback_items"],
            "feature_feedback_items": metrics["feature_feedback_items"],
        },
        "resume_safe_summary": (
            "Added a CI-verified feedback intake system that collects reviewer path, environment, "
            "reproducibility outcome, bug/feature signals, and real-workflow usefulness without "
            "claiming external users or customer feedback."
        ),
        "not_claimed": [
            "external users",
            "customer feedback",
            "production usage",
            "survey responses",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    fields = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["captured_fields"].items()
    )
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_public_counts"].items())
    labels = "\n".join(f"| {key} | `{value}` |" for key, value in payload["tracking_labels"].items())
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Feedback Intake Quality

This generated artifact verifies that the public feedback template collects useful pilot evidence while preserving honest zero-user and zero-feedback baselines.

## Intake Coverage

| Field | Captured |
| --- | --- |
{fields}

## Tracking Labels

| Metric | Label |
| --- | --- |
{labels}

## Current Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_feedback_intake_quality(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "required_section_count": 5,
        "required_try_path_count": 5,
        "required_outcome_count": 4,
        "captured_field_count": 5,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    if not all(payload["captured_fields"].values()):
        raise AssertionError("feedback intake must capture every required field group")
    if payload["current_public_counts"]["external_feedback_items"] != 0:
        raise AssertionError("feedback intake must not inflate external feedback")
    if payload["current_public_counts"]["confirmed_external_users"] != 0:
        raise AssertionError("feedback intake must not inflate confirmed users")
    for required in ("feedback", "confirmed-user", "reproducible", "bug", "enhancement"):
        if required not in payload["tracking_labels"].values():
            raise AssertionError(f"feedback intake missing tracking label {required}")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("used by customers", "production users", "collected customer feedback"):
        if forbidden in joined:
            raise AssertionError(f"feedback intake must not claim {forbidden}")
    return {"feedback_intake_quality_verified": True, **expected}


def main() -> None:
    payload = build_feedback_intake_quality_payload()
    verify_feedback_intake_quality(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
