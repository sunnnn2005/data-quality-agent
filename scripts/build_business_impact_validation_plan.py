import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUSINESS_IMPACT_PATH = ROOT / "docs" / "business-impact.json"
BUSINESS_PROBLEM_CASEBOOK_PATH = ROOT / "docs" / "business-problem-casebook.json"
BUSINESS_RESOLUTION_BRIEF_PATH = ROOT / "docs" / "business-resolution-brief.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "business-impact-validation-plan.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-impact-validation-plan.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_business_impact_validation_plan() -> dict[str, Any]:
    impact = load_json(BUSINESS_IMPACT_PATH)
    casebook = load_json(BUSINESS_PROBLEM_CASEBOOK_PATH)
    resolution = load_json(BUSINESS_RESOLUTION_BRIEF_PATH)

    validation_metrics = [
        {
            "metric": "defects_found_per_dataset",
            "current_demo_value": impact["finding_count"],
            "target_for_first_external_case": ">= 1 confirmed issue on an anonymized non-owner dataset",
            "evidence_required": "public business-case issue with anonymized row/field summary and permission to count",
            "resume_upgrade_after_evidence": "Validated the agent on a non-owner data-quality case and surfaced confirmed defects before reporting consumption.",
        },
        {
            "metric": "owner_handoffs_created",
            "current_demo_value": impact["owner_handoff_count"],
            "target_for_first_external_case": ">= 1 reviewer-confirmed owner or workflow handoff",
            "evidence_required": "reviewer confirms at least one suggested owner/action maps to their workflow",
            "resume_upgrade_after_evidence": "Mapped data-quality findings to reviewer-confirmed operational handoffs.",
        },
        {
            "metric": "manual_review_minutes_estimated",
            "current_demo_value": None,
            "target_for_first_external_case": "reviewer-provided before/after estimate",
            "evidence_required": "reviewer reports approximate manual check time and whether the report changed their triage path",
            "resume_upgrade_after_evidence": "Collected reviewer-estimated manual review time for a real anonymized workflow.",
        },
        {
            "metric": "dashboard_risk_prevented",
            "current_demo_value": impact["business_risk_area_count"],
            "target_for_first_external_case": ">= 1 reviewer-confirmed dashboard, report, or workflow risk",
            "evidence_required": "reviewer states which business workflow, decision, or report would have been affected by the detected issue",
            "resume_upgrade_after_evidence": "Linked confirmed data-quality findings to a concrete downstream decision risk.",
        },
        {
            "metric": "false_positive_review",
            "current_demo_value": None,
            "target_for_first_external_case": "reviewer labels at least one finding as useful, noisy, or incorrect",
            "evidence_required": "public feedback issue separates useful findings from false positives",
            "resume_upgrade_after_evidence": "Used reviewer feedback to calibrate data-quality findings and reduce noisy recommendations.",
        },
    ]

    first_pilot_protocol = [
        {
            "step": "Collect an anonymized CSV or table schema",
            "done_when": "The reviewer confirms there is no private data, secrets, or customer identifiers.",
        },
        {
            "step": "Run the deterministic checks and LLM-agent report",
            "done_when": "The run produces findings, evidence, recommendations, and limitations.",
        },
        {
            "step": "Ask the reviewer to label findings",
            "done_when": "The reviewer marks each key finding as useful, noisy, incorrect, or needs context.",
        },
        {
            "step": "Map findings to a workflow decision",
            "done_when": "At least one detected issue is tied to a dashboard, report, owner, or operational process.",
        },
        {
            "step": "Submit public redacted evidence",
            "done_when": "A non-owner public GitHub issue includes permission to count and no sensitive data.",
        },
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_impact_validation_plan.py",
        "purpose": (
            "Define how a reviewer can turn the current anonymized business demo into externally validated, "
            "resume-safe business impact evidence without fabricating users, ROI, or production adoption."
        ),
        "source_artifacts": [
            "docs/business-impact.json",
            "docs/business-problem-casebook.json",
            "docs/business-resolution-brief.json",
        ],
        "current_demo_baseline": {
            "dataset_id": impact["dataset_id"],
            "quality_score": impact["quality_score"],
            "status": impact["status"],
            "findings": impact["finding_count"],
            "business_risk_areas": impact["business_risk_area_count"],
            "owner_handoffs": impact["owner_handoff_count"],
            "high_priority_actions": impact["high_priority_action_count"],
            "casebook_cases": casebook["business_case_count"],
            "resolution_steps": len(resolution["resolution_steps"]),
            "external_validated_business_cases": 0,
        },
        "validation_metric_count": len(validation_metrics),
        "validation_metrics": validation_metrics,
        "pilot_step_count": len(first_pilot_protocol),
        "first_pilot_protocol": first_pilot_protocol,
        "minimum_resume_upgrade_gate": {
            "required_public_issues": 1,
            "required_non_owner_author": True,
            "requires_permission_to_count": True,
            "requires_no_sensitive_data": True,
            "requires_business_workflow_mapping": True,
            "current_accepted_business_cases": 0,
            "resume_claim_allowed": False,
        },
        "resume_safe_now": (
            "Built a CI-verified business-impact validation plan mapping 5 measurable pilot metrics to public "
            "evidence requirements, while preserving a zero external-business-case baseline."
        ),
        "future_resume_lines_after_evidence": [
            metric["resume_upgrade_after_evidence"] for metric in validation_metrics
        ],
        "not_claimed": [
            "validated business impact",
            "production adoption",
            "external business users",
            "revenue saved",
            "manual time saved",
            "customer dataset",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    baseline = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["current_demo_baseline"].items()
    )
    metrics = "\n".join(
        "| {metric} | {current_demo_value} | {target_for_first_external_case} | {evidence_required} |".format(
            **metric
        )
        for metric in payload["validation_metrics"]
    )
    protocol = "\n".join(
        f"| {index} | {step['step']} | {step['done_when']} |"
        for index, step in enumerate(payload["first_pilot_protocol"], start=1)
    )
    gate = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["minimum_resume_upgrade_gate"].items()
    )
    future_lines = "\n".join(f"- {line}" for line in payload["future_resume_lines_after_evidence"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Business Impact Validation Plan

This generated plan defines how the project can earn real business-impact evidence from an external reviewer.

## Purpose

{payload["purpose"]}

## Current Demo Baseline

| Metric | Value |
| --- | ---: |
{baseline}

## Validation Metrics

| Metric | Current Demo Value | First External Target | Evidence Required |
| --- | ---: | --- | --- |
{metrics}

## First Pilot Protocol

| Step | Action | Done When |
| ---: | --- | --- |
{protocol}

## Minimum Resume Upgrade Gate

| Rule | Value |
| --- | --- |
{gate}

## Resume-Safe Now

{payload["resume_safe_now"]}

## Future Resume Lines After Evidence

{future_lines}

## Not Claimed

{not_claimed}
"""


def verify_business_impact_validation_plan(payload: dict[str, Any]) -> dict[str, Any]:
    baseline = payload["current_demo_baseline"]
    expected_baseline = {
        "quality_score": 24,
        "status": "FAIL",
        "findings": 5,
        "business_risk_areas": 4,
        "owner_handoffs": 4,
        "high_priority_actions": 3,
        "casebook_cases": 1,
        "resolution_steps": 4,
        "external_validated_business_cases": 0,
    }
    for key, expected in expected_baseline.items():
        if baseline.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {baseline.get(key)!r}")
    if payload["validation_metric_count"] != 5:
        raise AssertionError("business impact validation plan must define five validation metrics")
    if payload["pilot_step_count"] != 5:
        raise AssertionError("business impact validation plan must define five pilot steps")
    gate = payload["minimum_resume_upgrade_gate"]
    if gate["resume_claim_allowed"] is not False or gate["current_accepted_business_cases"] != 0:
        raise AssertionError("business impact validation plan must not unlock resume claims without evidence")
    if len(payload["future_resume_lines_after_evidence"]) != payload["validation_metric_count"]:
        raise AssertionError("each validation metric must map to a future resume line")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in (
        "non-owner",
        "permission to count",
        "no sensitive data",
        "business workflow",
        "public github issue",
    ):
        if required not in joined:
            raise AssertionError(f"business impact validation plan must include {required}")
    for not_claimed in (
        "validated business impact",
        "production adoption",
        "external business users",
        "revenue saved",
        "manual time saved",
        "customer dataset",
    ):
        if not_claimed not in payload["not_claimed"]:
            raise AssertionError(f"business impact validation plan must not claim {not_claimed}")
    return {
        "business_impact_validation_plan_verified": True,
        "validation_metric_count": payload["validation_metric_count"],
        "pilot_step_count": payload["pilot_step_count"],
        "external_validated_business_cases": baseline["external_validated_business_cases"],
    }


def main() -> None:
    payload = build_business_impact_validation_plan()
    verify_business_impact_validation_plan(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
