import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / ".github" / "ISSUE_TEMPLATE" / "business_case_review.md"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "business-case-intake.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-case-intake.md"


REQUIRED_SECTIONS = [
    "Business context",
    "Data-quality problem",
    "Fields involved",
    "Tried path",
    "Outcome",
    "Permission",
]
REQUIRED_CONTEXT_FIELDS = [
    "Industry or team:",
    "Workflow affected:",
    "Data source type:",
]
REQUIRED_TRY_PATHS = [
    "Public demo page",
    "CSV upload endpoint",
    "PostgreSQL Docker Compose demo",
    "LLM tool-calling route",
    "I only reviewed the repository/docs",
]
REQUIRED_OUTCOMES = [
    "The agent found a relevant issue.",
    "The deterministic checks found a relevant issue.",
    "The report missed an important business rule.",
    "The suggested owner handoff/action was useful.",
    "I would need another integration before using this pattern.",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_business_case_intake_payload() -> dict[str, Any]:
    template = TEMPLATE_PATH.read_text()
    metrics = load_json(FEEDBACK_METRICS_PATH)
    captured_fields = {
        "business_context": all(item in template for item in REQUIRED_CONTEXT_FIELDS),
        "data_quality_problem": "What broke, looked suspicious, or slowed the workflow?" in template,
        "field_scope": "List only non-sensitive field names or anonymized examples." in template,
        "try_path": all(item in template for item in REQUIRED_TRY_PATHS),
        "outcome_signals": all(item in template for item in REQUIRED_OUTCOMES),
        "permission_boundary": all(
            item in template
            for item in (
                "This can be counted as anonymized public business-case feedback.",
                "Do not quote my organization, name, or raw data.",
            )
        ),
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_case_intake.py",
        "template_path": ".github/ISSUE_TEMPLATE/business_case_review.md",
        "business_case_issue_template": (
            "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md"
        ),
        "required_section_count": len(REQUIRED_SECTIONS),
        "required_context_field_count": len(REQUIRED_CONTEXT_FIELDS),
        "required_try_path_count": len(REQUIRED_TRY_PATHS),
        "required_outcome_count": len(REQUIRED_OUTCOMES),
        "captured_field_count": sum(1 for value in captured_fields.values() if value),
        "captured_fields": captured_fields,
        "tracking_label": metrics["tracking_labels"]["business_case_feedback_items"],
        "current_public_counts": {
            "business_case_feedback_items": metrics["business_case_feedback_items"],
            "external_feedback_items": metrics["external_feedback_items"],
            "confirmed_external_users": metrics["confirmed_external_users"],
        },
        "resume_upgrade_rule": {
            "signal": "anonymized public business-case feedback",
            "current_value": metrics["business_case_feedback_items"],
            "minimum_before_claim": 1,
            "evidence_required": "public GitHub issue using the business-case template and business-case label",
            "resume_status": "not_claimable_yet"
            if metrics["business_case_feedback_items"] == 0
            else "claimable_with_linked_evidence",
        },
        "resume_safe_summary": (
            "Published a CI-verified business-case intake path for collecting anonymized real-world "
            "data-quality problems, business context, tried route, outcome signal, and permission boundaries "
            "without claiming any submitted external business cases yet."
        ),
        "not_claimed": [
            "submitted external business cases",
            "customer feedback",
            "enterprise production usage",
            "raw customer data",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    fields = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["captured_fields"].items()
    )
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["current_public_counts"].items()
    )
    rule = payload["resume_upgrade_rule"]
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Business Case Intake

This generated artifact verifies that the project has a public path for collecting anonymized real-world data-quality problems while preserving honest zero-case and zero-user baselines.

## Intake Coverage

| Field | Captured |
| --- | --- |
{fields}

## Current Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Resume Upgrade Rule

| Signal | Current value | Minimum before claim | Evidence required | Status |
| --- | ---: | ---: | --- | --- |
| {rule["signal"]} | {rule["current_value"]} | {rule["minimum_before_claim"]} | {rule["evidence_required"]} | `{rule["resume_status"]}` |

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_business_case_intake(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "required_section_count": 6,
        "required_context_field_count": 3,
        "required_try_path_count": 5,
        "required_outcome_count": 5,
        "captured_field_count": 6,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    if not all(payload["captured_fields"].values()):
        raise AssertionError("business case intake must capture every required field group")
    if payload["tracking_label"] != "business-case":
        raise AssertionError("business case intake must use the business-case tracking label")
    counts = payload["current_public_counts"]
    if counts["business_case_feedback_items"] != 0:
        raise AssertionError("business case intake must not inflate submitted business-case feedback")
    if counts["confirmed_external_users"] != 0:
        raise AssertionError("business case intake must preserve the zero-user baseline")
    if payload["resume_upgrade_rule"]["resume_status"] != "not_claimable_yet":
        raise AssertionError("business case intake must not be resume-claimable before public evidence")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("real customers used", "enterprise adoption", "production customers"):
        if forbidden in joined:
            raise AssertionError(f"business case intake must not claim {forbidden}")
    return {"business_case_intake_verified": True, **expected}


def main() -> None:
    payload = build_business_case_intake_payload()
    verify_business_case_intake(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
