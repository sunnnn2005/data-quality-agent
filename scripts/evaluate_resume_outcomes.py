import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONVERSION_BOARD_PATH = ROOT / "docs" / "pilot-conversion-board.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-outcome-readiness.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-outcome-readiness.md"


METRIC_SOURCES = {
    "confirmed_external_feedback": ("feedback", "external_feedback_items"),
    "confirmed_external_users": ("feedback", "confirmed_external_users"),
    "business_case_validated": ("feedback", "business_case_feedback_items"),
    "reproducible_replay_confirmed": ("feedback", "reproducible_feedback_items"),
    "github_interest_signal": ("adoption", "stars"),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_resume_outcome_readiness_payload(
    conversion_board_path: Path = CONVERSION_BOARD_PATH,
    feedback_metrics_path: Path = FEEDBACK_METRICS_PATH,
    adoption_metrics_path: Path = ADOPTION_METRICS_PATH,
) -> dict[str, Any]:
    conversion = load_json(conversion_board_path)
    feedback = load_json(feedback_metrics_path)
    adoption = load_json(adoption_metrics_path)
    stages = [_evaluate_stage(stage, feedback, adoption) for stage in conversion["stages"]]
    claimable = [stage for stage in stages if stage["resume_claim_allowed"]]
    blocked = [stage for stage in stages if not stage["resume_claim_allowed"]]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/evaluate_resume_outcomes.py",
        "purpose": (
            "Evaluate which public outcome signals are currently safe to use on a resume and exactly what evidence "
            "is still missing for stronger claims such as feedback, confirmed use, business-case validation, replay "
            "evidence, or GitHub interest."
        ),
        "stage_count": len(stages),
        "claimable_stage_count": len(claimable),
        "blocked_stage_count": len(blocked),
        "stages": stages,
        "claimable_resume_lines": [stage["resume_safe_wording"] for stage in claimable if stage["resume_safe_wording"]],
        "missing_evidence": [
            {
                "stage": stage["stage"],
                "current_value": stage["current_value"],
                "minimum_to_claim": stage["minimum_to_claim"],
                "remaining_needed": stage["remaining_needed"],
                "evidence_required": stage["evidence_required"],
            }
            for stage in blocked
        ],
        "current_public_counts": {
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "business_case_feedback_items": feedback["business_case_feedback_items"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
            "stars": adoption["stars"],
            "forks": adoption["forks"],
        },
        "not_claimed": conversion["not_claimed"],
        "next_best_actions": [
            "Ask 3 reviewers to submit public demo feedback issues with reproducible context.",
            "Ask 1 reviewer to run the local Docker/PostgreSQL or CSV replay and label the issue confirmed-user.",
            "Collect 1 anonymized business-case review with permission boundaries before claiming real-world validation.",
            "Collect 2 reproducible replay issues with command, schema summary, status, and finding count.",
            "Share the public demo/repo ethically; count stars only from GitHub's public metric.",
        ],
        "resume_safe_summary": (
            f"{len(claimable)} resume-safe readiness signals are currently claimable; "
            f"{len(blocked)} stronger outcome claims remain blocked until public evidence reaches the defined thresholds."
        ),
    }


def _evaluate_stage(stage: dict[str, Any], feedback: dict[str, Any], adoption: dict[str, Any]) -> dict[str, Any]:
    current_value = _resolve_current_value(stage, feedback, adoption)
    minimum = int(stage["minimum_to_claim"])
    remaining = max(0, minimum - current_value)
    allowed = current_value >= minimum and bool(stage.get("resume_safe_wording"))
    return {
        **stage,
        "current_value": current_value,
        "resume_claim_allowed": allowed,
        "remaining_needed": remaining,
        "evidence_status": "claimable" if allowed else "blocked_until_public_evidence",
    }


def _resolve_current_value(stage: dict[str, Any], feedback: dict[str, Any], adoption: dict[str, Any]) -> int:
    source = METRIC_SOURCES.get(stage["stage"])
    if source is None:
        return int(stage["current_value"])
    source_name, metric_name = source
    payload = feedback if source_name == "feedback" else adoption
    return int(payload.get(metric_name, 0))


def render_markdown(payload: dict[str, Any]) -> str:
    stage_rows = "\n".join(
        "| {stage} | {current_value} | {minimum_to_claim} | {remaining_needed} | `{evidence_status}` | {evidence_required} |".format(
            **stage
        )
        for stage in payload["stages"]
    )
    claimable = "\n".join(f"- {line}" for line in payload["claimable_resume_lines"])
    missing = "\n".join(
        "| {stage} | {current_value} | {minimum_to_claim} | {remaining_needed} | {evidence_required} |".format(
            **item
        )
        for item in payload["missing_evidence"]
    )
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_public_counts"].items()
    )
    actions = "\n".join(f"- {item}" for item in payload["next_best_actions"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Resume Outcome Readiness

This generated artifact tells you which outcome claims are safe for the resume right now.

## Purpose

{payload["purpose"]}

## Stage Readiness

| Stage | Current Value | Minimum To Claim | Remaining Needed | Status | Evidence Required |
| --- | ---: | ---: | ---: | --- | --- |
{stage_rows}

## Claimable Resume Lines

{claimable}

## Missing Evidence

| Stage | Current Value | Minimum To Claim | Remaining Needed | Evidence Required |
| --- | ---: | ---: | ---: | --- |
{missing}

## Current Public Counts

| Metric | Current Value |
| --- | ---: |
{counts}

## Next Best Actions

{actions}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_resume_outcome_readiness(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "stage_count": 6,
        "claimable_stage_count": 2,
        "blocked_stage_count": 4,
        "confirmed_external_users": 0,
        "external_feedback_items": 0,
        "business_case_feedback_items": 0,
        "reproducible_feedback_items": 0,
    }
    if payload["stage_count"] != expected["stage_count"]:
        raise AssertionError("resume outcome readiness must evaluate six stages")
    if payload["claimable_stage_count"] != expected["claimable_stage_count"]:
        raise AssertionError("resume outcome readiness must keep two current readiness claims")
    if payload["blocked_stage_count"] != expected["blocked_stage_count"]:
        raise AssertionError("resume outcome readiness must block four stronger outcome claims")
    counts = payload["current_public_counts"]
    for key in (
        "confirmed_external_users",
        "external_feedback_items",
        "business_case_feedback_items",
        "reproducible_feedback_items",
    ):
        if counts[key] != expected[key]:
            raise AssertionError(f"{key} must remain zero until public evidence exists")
    missing = {item["stage"]: item for item in payload["missing_evidence"]}
    expected_remaining = {
        "confirmed_external_feedback": 3,
        "confirmed_external_users": 1,
        "business_case_validated": 1,
        "reproducible_replay_confirmed": 2,
    }
    for stage, remaining in expected_remaining.items():
        if missing[stage]["remaining_needed"] != remaining:
            raise AssertionError(f"{stage} remaining_needed expected {remaining}")
    for required in ("external users", "customer feedback", "validated business impact", "production adoption"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"resume outcome readiness must not claim {required}")
    return {"resume_outcome_readiness_verified": True, **expected}


def write_outputs(payload: dict[str, Any]) -> None:
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate resume-safe outcome readiness from public evidence metrics.")
    parser.add_argument("--check", action="store_true", help="Verify the generated payload without writing files.")
    args = parser.parse_args()
    payload = build_resume_outcome_readiness_payload()
    verify_resume_outcome_readiness(payload)
    if not args.check:
        write_outputs(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
