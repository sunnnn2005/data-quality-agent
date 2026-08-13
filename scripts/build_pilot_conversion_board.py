import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PILOT_REVIEW_TRACKER_PATH = ROOT / "docs" / "pilot-review-tracker.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "pilot-conversion-board.json"
OUTPUT_MD_PATH = ROOT / "docs" / "pilot-conversion-board.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_pilot_conversion_board_payload() -> dict[str, Any]:
    tracker = load_json(PILOT_REVIEW_TRACKER_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    stages = [
        {
            "stage": "public_demo_available",
            "current_value": 1,
            "minimum_to_claim": 1,
            "evidence_required": "GitHub Pages demo, README link, and public evidence health check",
            "resume_claim_allowed": True,
            "resume_safe_wording": "Published a public demo and evidence-backed documentation for a data-quality LLM agent.",
        },
        {
            "stage": "pilot_outreach_ready",
            "current_value": tracker["planned_review_count"],
            "minimum_to_claim": 3,
            "evidence_required": "CI-verified planned reviewer segments and public feedback entrypoints",
            "resume_claim_allowed": True,
            "resume_safe_wording": "Built a pilot feedback pipeline with three reviewer segments and public evidence rules.",
        },
        {
            "stage": "confirmed_external_feedback",
            "current_value": feedback["external_feedback_items"],
            "minimum_to_claim": 3,
            "evidence_required": "Public GitHub issues labeled feedback with reproducible context",
            "resume_claim_allowed": False,
            "resume_safe_wording": None,
        },
        {
            "stage": "confirmed_external_users",
            "current_value": feedback["confirmed_external_users"],
            "minimum_to_claim": 1,
            "evidence_required": "Public issue or replay note labeled confirmed-user",
            "resume_claim_allowed": False,
            "resume_safe_wording": None,
        },
        {
            "stage": "business_case_validated",
            "current_value": feedback["business_case_feedback_items"],
            "minimum_to_claim": 1,
            "evidence_required": "Public business-case review issue with anonymized workflow and permission boundary",
            "resume_claim_allowed": False,
            "resume_safe_wording": None,
        },
        {
            "stage": "reproducible_replay_confirmed",
            "current_value": feedback["reproducible_feedback_items"],
            "minimum_to_claim": 2,
            "evidence_required": "Public replay issues with commands, non-sensitive schema, status, and finding count",
            "resume_claim_allowed": False,
            "resume_safe_wording": None,
        },
    ]
    claimable = [stage for stage in stages if stage["resume_claim_allowed"]]
    blocked = [stage for stage in stages if not stage["resume_claim_allowed"]]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_pilot_conversion_board.py",
        "purpose": (
            "Convert public pilot evidence into resume-safe outcome claims only after explicit, auditable thresholds "
            "are met. This board prevents private messages, planned outreach, or unverified compliments from being "
            "counted as users, feedback, or business impact."
        ),
        "stage_count": len(stages),
        "claimable_stage_count": len(claimable),
        "blocked_stage_count": len(blocked),
        "stages": stages,
        "current_resume_safe_claims": [stage["resume_safe_wording"] for stage in claimable],
        "blocked_resume_claims": [
            {
                "stage": stage["stage"],
                "current_value": stage["current_value"],
                "minimum_to_claim": stage["minimum_to_claim"],
                "evidence_required": stage["evidence_required"],
            }
            for stage in blocked
        ],
        "not_claimed": [
            "external users",
            "customer feedback",
            "validated business impact",
            "production adoption",
            "GitHub stars beyond the current public count",
        ],
        "resume_safe_summary": (
            "Added a CI-verified pilot conversion board that separates two claimable readiness signals from four "
            "blocked outcome claims until public feedback, confirmed users, business-case reviews, or reproducible "
            "replay evidence exist."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    stage_rows = "\n".join(
        "| {stage} | {current_value} | {minimum_to_claim} | {evidence_required} | `{resume_claim_allowed}` |".format(
            **stage
        )
        for stage in payload["stages"]
    )
    claimable = "\n".join(f"- {claim}" for claim in payload["current_resume_safe_claims"])
    blocked = "\n".join(
        "| {stage} | {current_value} | {minimum_to_claim} | {evidence_required} |".format(**stage)
        for stage in payload["blocked_resume_claims"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Pilot Conversion Board

This generated board defines when pilot evidence becomes resume-safe outcome language.

## Purpose

{payload["purpose"]}

## Conversion Stages

| Stage | Current Value | Minimum To Claim | Evidence Required | Resume Claim Allowed |
| --- | ---: | ---: | --- | --- |
{stage_rows}

## Current Resume-Safe Claims

{claimable}

## Blocked Outcome Claims

| Stage | Current Value | Minimum To Claim | Evidence Required |
| --- | ---: | ---: | --- |
{blocked}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_pilot_conversion_board(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "stage_count": 6,
        "claimable_stage_count": 2,
        "blocked_stage_count": 4,
        "confirmed_external_feedback": 0,
        "confirmed_external_users": 0,
        "business_case_validated": 0,
        "reproducible_replay_confirmed": 0,
    }
    if payload["stage_count"] != expected["stage_count"]:
        raise AssertionError("pilot conversion board must define six conversion stages")
    if payload["claimable_stage_count"] != expected["claimable_stage_count"]:
        raise AssertionError("pilot conversion board must expose two readiness claims")
    if payload["blocked_stage_count"] != expected["blocked_stage_count"]:
        raise AssertionError("pilot conversion board must block four outcome claims")
    stages = {stage["stage"]: stage for stage in payload["stages"]}
    for key in (
        "confirmed_external_feedback",
        "confirmed_external_users",
        "business_case_validated",
        "reproducible_replay_confirmed",
    ):
        if stages[key]["current_value"] != expected[key]:
            raise AssertionError(f"{key} must remain zero until public evidence exists")
        if stages[key]["resume_claim_allowed"]:
            raise AssertionError(f"{key} must not be resume-claimable yet")
    if len(payload["blocked_resume_claims"]) != expected["blocked_stage_count"]:
        raise AssertionError("blocked outcome claims must be listed explicitly")
    for required in ("external users", "customer feedback", "validated business impact", "production adoption"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"pilot conversion board must not claim {required}")
    return {"pilot_conversion_board_verified": True, **expected}


def main() -> None:
    payload = build_pilot_conversion_board_payload()
    verify_pilot_conversion_board(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
