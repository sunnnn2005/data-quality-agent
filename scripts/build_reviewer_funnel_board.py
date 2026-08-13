import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
RESUME_READINESS_PATH = ROOT / "docs" / "resume-outcome-readiness.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-funnel-board.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-funnel-board.md"
REPO_URL = "https://github.com/sunnnn2005/data-quality-agent"
PUBLIC_DEMO_URL = "https://sunnnn2005.github.io/data-quality-agent/"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_reviewer_funnel_board_payload() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    readiness = load_json(RESUME_READINESS_PATH)
    channels = {channel["name"]: channel["url"] for channel in feedback["feedback_channels"]}
    stages = [
        {
            "id": "visit_public_demo",
            "action": "Open the public demo and inspect the support-ticket report.",
            "entry_url": PUBLIC_DEMO_URL,
            "submission_url": channels["Demo feedback"],
            "counts_toward": "external_feedback_items",
            "current_value": feedback["external_feedback_items"],
            "target_value": 3,
        },
        {
            "id": "run_local_replay",
            "action": "Run the local CSV or PostgreSQL replay and submit the result.",
            "entry_url": REPO_URL,
            "submission_url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md",
            "counts_toward": "reproducible_feedback_items",
            "current_value": feedback["reproducible_feedback_items"],
            "target_value": 2,
        },
        {
            "id": "confirm_external_use",
            "action": "Submit a confirmed-user note after trying the demo or local repo.",
            "entry_url": f"{REPO_URL}/blob/main/docs/reviewer-feedback-packet.md",
            "submission_url": channels["Demo feedback"],
            "counts_toward": "confirmed_external_users",
            "current_value": feedback["confirmed_external_users"],
            "target_value": 1,
        },
        {
            "id": "submit_business_case",
            "action": "Share an anonymized real-world data-quality case for review.",
            "entry_url": f"{REPO_URL}/blob/main/docs/business-problem-casebook.md",
            "submission_url": channels["Business case review"],
            "counts_toward": "business_case_feedback_items",
            "current_value": feedback["business_case_feedback_items"],
            "target_value": 1,
        },
    ]
    for stage in stages:
        stage["remaining_needed"] = max(0, stage["target_value"] - stage["current_value"])
        stage["status"] = "complete" if stage["remaining_needed"] == 0 else "needs_public_evidence"
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_funnel_board.py",
        "purpose": (
            "Turn public demo visits, local replays, confirmed-user notes, and business-case reviews into "
            "label-based evidence that can later upgrade resume outcomes without inflating the current baseline."
        ),
        "funnel_stage_count": len(stages),
        "funnel_stages": stages,
        "open_gap_count": sum(1 for stage in stages if stage["remaining_needed"] > 0),
        "total_remaining_evidence_items": sum(stage["remaining_needed"] for stage in stages),
        "resume_outcome_blocked_stages": readiness["blocked_stage_count"],
        "resume_outcome_claimable_stages": readiness["claimable_stage_count"],
        "current_public_counts": readiness["current_public_counts"],
        "resume_status": "evidence_collection_ready",
        "not_claimed": readiness["not_claimed"],
        "resume_safe_summary": (
            "Published a reviewer funnel board with 4 public evidence paths, 7 remaining evidence items, "
            "and explicit zero-user/zero-feedback baselines before stronger outcome claims are allowed."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {id} | {action} | [{entry_url}]({entry_url}) | [Submit]({submission_url}) | `{counts_toward}` | {current_value} | {target_value} | {remaining_needed} | `{status}` |".format(
            **stage
        )
        for stage in payload["funnel_stages"]
    )
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_public_counts"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Reviewer Funnel Board

This generated board shows how public review activity can become resume-safe evidence.

## Purpose

{payload["purpose"]}

## Funnel Stages

| Stage | Reviewer Action | Entry | Submission | Counts Toward | Current | Target | Remaining | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
{rows}

## Current Public Counts

| Metric | Current Value |
| --- | ---: |
{counts}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_reviewer_funnel_board(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["funnel_stage_count"] != 4:
        raise AssertionError("reviewer funnel board must define four public evidence paths")
    if payload["open_gap_count"] != 4:
        raise AssertionError("all four reviewer funnel paths must remain open until public evidence exists")
    if payload["total_remaining_evidence_items"] != 7:
        raise AssertionError("reviewer funnel board must require seven remaining evidence items")
    required_metrics = {
        "external_feedback_items",
        "reproducible_feedback_items",
        "confirmed_external_users",
        "business_case_feedback_items",
    }
    actual_metrics = {stage["counts_toward"] for stage in payload["funnel_stages"]}
    if actual_metrics != required_metrics:
        raise AssertionError("reviewer funnel board stages must map to every outcome evidence metric")
    if payload["current_public_counts"]["external_feedback_items"] != 0:
        raise AssertionError("reviewer funnel board must preserve zero feedback baseline")
    if payload["current_public_counts"]["confirmed_external_users"] != 0:
        raise AssertionError("reviewer funnel board must preserve zero confirmed-user baseline")
    for stage in payload["funnel_stages"]:
        if not stage["submission_url"].startswith("https://github.com/"):
            raise AssertionError("reviewer funnel submissions must use public GitHub issue URLs")
    return {
        "reviewer_funnel_board_verified": True,
        "funnel_stage_count": payload["funnel_stage_count"],
        "total_remaining_evidence_items": payload["total_remaining_evidence_items"],
    }


def main() -> None:
    payload = build_reviewer_funnel_board_payload()
    verify_reviewer_funnel_board(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
