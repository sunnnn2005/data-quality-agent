import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
REVIEWER_ACTION_QUEUE_PATH = ROOT / "docs" / "reviewer-action-queue.json"
REVIEWER_SUBMISSION_HUB_PATH = ROOT / "docs" / "reviewer-submission-hub.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "first-10-reviewer-sprint.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-10-reviewer-sprint.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _slot(
    *,
    slot_id: str,
    reviewer_profile: str,
    ask: str,
    target_metric: str,
    source_task_id: str,
    entry_url: str,
    submission_url: str,
    acceptance_evidence: list[str],
) -> dict[str, Any]:
    return {
        "id": slot_id,
        "reviewer_profile": reviewer_profile,
        "status": "not_sent",
        "ask": ask,
        "target_metric": target_metric,
        "source_task_id": source_task_id,
        "entry_url": entry_url,
        "submission_url": submission_url,
        "acceptance_evidence": acceptance_evidence,
        "counts_only_after": (
            "A non-owner public GitHub issue passes the external reviewer evidence gate, includes explicit permission "
            "to count the evidence, and contains no private data."
        ),
    }


def build_first_10_reviewer_sprint() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    queue = load_json(REVIEWER_ACTION_QUEUE_PATH)
    hub = load_json(REVIEWER_SUBMISSION_HUB_PATH)
    tasks = {task["id"]: task for task in queue["tasks"]}
    paths = {path["target_metric"]: path for path in hub["submission_paths"]}

    slots = [
        _slot(
            slot_id="slot_01_ds_peer_demo",
            reviewer_profile="UC Davis data science peer",
            ask="Try the public demo and report one confusing or useful workflow detail.",
            target_metric="external_feedback_items",
            source_task_id="review_uc_davis_ds_peer_demo",
            entry_url=tasks["review_uc_davis_ds_peer_demo"]["entry_url"],
            submission_url=tasks["review_uc_davis_ds_peer_demo"]["submission_url"],
            acceptance_evidence=["demo path tried", "specific feedback", "permission to count publicly"],
        ),
        _slot(
            slot_id="slot_02_swe_peer_demo",
            reviewer_profile="student software engineer peer",
            ask="Review setup clarity, README flow, and whether the project looks runnable.",
            target_metric="external_feedback_items",
            source_task_id="review_student_swe_peer_demo",
            entry_url=tasks["review_student_swe_peer_demo"]["entry_url"],
            submission_url=tasks["review_student_swe_peer_demo"]["submission_url"],
            acceptance_evidence=["reviewed URL", "engineering feedback", "permission to count publicly"],
        ),
        _slot(
            slot_id="slot_03_local_replay",
            reviewer_profile="engineer comfortable with Docker or local setup",
            ask="Run the local replay path and confirm whether the report is reproducible.",
            target_metric="reproducible_feedback_items",
            source_task_id="review_local_replay_engineer",
            entry_url=tasks["review_local_replay_engineer"]["entry_url"],
            submission_url=tasks["review_local_replay_engineer"]["submission_url"],
            acceptance_evidence=["command or URL used", "observed result", "environment summary"],
        ),
        _slot(
            slot_id="slot_04_confirmed_use",
            reviewer_profile="reviewer who opened the demo or ran the repo",
            ask="Confirm the exact path used and whether the result was understandable.",
            target_metric="confirmed_external_users",
            source_task_id="review_confirmed_external_use",
            entry_url=tasks["review_confirmed_external_use"]["entry_url"],
            submission_url=tasks["review_confirmed_external_use"]["submission_url"],
            acceptance_evidence=["path used", "observed result", "permission to count as external use"],
        ),
        _slot(
            slot_id="slot_05_data_analyst_case",
            reviewer_profile="data analyst or analytics student",
            ask="Submit one anonymized data-quality problem this agent should handle.",
            target_metric="business_case_feedback_items",
            source_task_id="review_data_analyst_business_case",
            entry_url=tasks["review_data_analyst_business_case"]["entry_url"],
            submission_url=tasks["review_data_analyst_business_case"]["submission_url"],
            acceptance_evidence=["anonymized workflow", "data-quality problem", "business impact"],
        ),
        _slot(
            slot_id="slot_06_operator_case",
            reviewer_profile="small-business operator or operations teammate",
            ask="Describe one workflow where bad data would cause a wrong operational decision.",
            target_metric="business_case_feedback_items",
            source_task_id="review_operator_business_case",
            entry_url=tasks["review_operator_business_case"]["entry_url"],
            submission_url=tasks["review_operator_business_case"]["submission_url"],
            acceptance_evidence=["workflow affected", "decision risk", "permission to count anonymized case"],
        ),
        _slot(
            slot_id="slot_07_ai_engineer_review",
            reviewer_profile="AI engineer, mentor, or ML systems reviewer",
            ask="Inspect the LLM tool-calling loop, guardrails, and evidence trail for AI Engineer credibility.",
            target_metric="ai_engineer_review_items",
            source_task_id="review_ai_engineer_agent_readiness",
            entry_url=tasks["review_ai_engineer_agent_readiness"]["entry_url"],
            submission_url=tasks["review_ai_engineer_agent_readiness"]["submission_url"],
            acceptance_evidence=["inspected implementation path", "AI-agent signal feedback", "permission to count publicly"],
        ),
        _slot(
            slot_id="slot_08_open_source_review",
            reviewer_profile="open-source maintainer or GitHub contributor",
            ask="Review whether a first-time contributor can understand and run the project.",
            target_metric="external_feedback_items",
            source_task_id="review_open_source_maintainer",
            entry_url=tasks["review_open_source_maintainer"]["entry_url"],
            submission_url=tasks["review_open_source_maintainer"]["submission_url"],
            acceptance_evidence=["contributor-readiness feedback", "suggested improvement", "permission to count publicly"],
        ),
        _slot(
            slot_id="slot_09_public_star_if_useful",
            reviewer_profile="reviewer who finds the repo useful enough to save",
            ask="Star or fork only if the project is genuinely useful; no traded or fake engagement.",
            target_metric="github_stars",
            source_task_id="star_or_fork_if_useful",
            entry_url="https://github.com/sunnnn2005/data-quality-agent",
            submission_url=paths["github_stars"]["submission_url"],
            acceptance_evidence=["public GitHub star count above zero", "no paid or traded engagement"],
        ),
        _slot(
            slot_id="slot_10_second_replay",
            reviewer_profile="second technical reviewer for independent reproducibility",
            ask="Run either the public demo or local replay and submit an independent observed result.",
            target_metric="reproducible_feedback_items",
            source_task_id="confirm_external_run",
            entry_url=paths["confirmed_external_users"]["review_path"],
            submission_url=paths["confirmed_external_users"]["submission_url"],
            acceptance_evidence=["independent run path", "observed result", "permission to count public run evidence"],
        ),
    ]

    target_counts: dict[str, int] = {}
    for slot in slots:
        target_counts[slot["target_metric"]] = target_counts.get(slot["target_metric"], 0) + 1

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_10_reviewer_sprint.py",
        "purpose": (
            "Turn the zero-user and zero-feedback baseline into a 10-slot reviewer sprint that can produce "
            "resume-safe public evidence without inflating current outcomes."
        ),
        "sprint_name": "first_10_external_reviewer_sprint",
        "slot_count": len(slots),
        "not_sent_count": sum(1 for slot in slots if slot["status"] == "not_sent"),
        "completed_count": 0,
        "target_metric_count": len(target_counts),
        "target_counts": target_counts,
        "current_counts": {
            "confirmed_external_users": feedback["confirmed_external_users"],
            "external_feedback_items": feedback["external_feedback_items"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
            "business_case_feedback_items": feedback["business_case_feedback_items"],
            "ai_engineer_review_items": feedback["ai_engineer_review_items"],
            "github_stars": 0,
        },
        "slots": slots,
        "success_thresholds": [
            "1 accepted confirmed external user issue",
            "3 accepted external feedback issues",
            "1 accepted reproducible run issue",
            "1 accepted anonymized business case",
            "1 accepted AI Engineer review issue",
            "1 organic public GitHub star or fork",
        ],
        "blocked_resume_claims": [
            "users",
            "customer feedback",
            "business impact",
            "AI Engineer external review",
            "GitHub star growth",
        ],
        "resume_status": "first_10_sprint_ready_not_claimable",
        "resume_safe_summary": (
            f"Published a CI-verified first-10 reviewer sprint with {len(slots)} public evidence slots, "
            f"{len(target_counts)} target metrics, zero sent outreach, and zero upgraded outcome claims."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    current_counts = "\n".join(
        f"| {key} | {value} |" for key, value in payload["current_counts"].items()
    )
    target_counts = "\n".join(
        f"| {key} | {value} |" for key, value in sorted(payload["target_counts"].items())
    )
    slots = "\n\n".join(
        "\n".join(
            [
                f"### {slot['id']}",
                "",
                f"- Reviewer profile: {slot['reviewer_profile']}",
                f"- Status: `{slot['status']}`",
                f"- Target metric: `{slot['target_metric']}`",
                f"- Source task: `{slot['source_task_id']}`",
                f"- Entry: [{slot['entry_url']}]({slot['entry_url']})",
                f"- Submit evidence: [{slot['submission_url']}]({slot['submission_url']})",
                f"- Ask: {slot['ask']}",
                f"- Counts only after: {slot['counts_only_after']}",
                "",
                "Acceptance evidence:",
                *[f"- {item}" for item in slot["acceptance_evidence"]],
            ]
        )
        for slot in payload["slots"]
    )
    thresholds = "\n".join(f"- {item}" for item in payload["success_thresholds"])
    blocked = "\n".join(f"- {item}" for item in payload["blocked_resume_claims"])
    return f"""# First 10 Reviewer Sprint

This generated sprint converts the project traction goal into 10 concrete external-review slots.

## Purpose

{payload["purpose"]}

## Current Counts

| Metric | Current Count |
| --- | ---: |
{current_counts}

## Target Slot Mix

| Metric | Slots |
| --- | ---: |
{target_counts}

## Reviewer Slots

{slots}

## Success Thresholds

{thresholds}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Still Blocked

{blocked}
"""


def verify_first_10_reviewer_sprint(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["slot_count"] != 10:
        raise AssertionError("first reviewer sprint must contain 10 reviewer slots")
    if payload["not_sent_count"] != 10:
        raise AssertionError("first reviewer sprint must preserve a zero-sent baseline")
    if payload["completed_count"] != 0:
        raise AssertionError("first reviewer sprint must not claim completed reviewers")
    if payload["target_metric_count"] != 6:
        raise AssertionError("first reviewer sprint must target six outcome metrics")
    if payload["resume_status"] != "first_10_sprint_ready_not_claimable":
        raise AssertionError("first reviewer sprint must keep resume outcomes not claimable")
    if any(value != 0 for value in payload["current_counts"].values()):
        raise AssertionError("first reviewer sprint must not claim existing outcomes")

    expected_metrics = {
        "external_feedback_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "github_stars",
    }
    if set(payload["target_counts"]) != expected_metrics:
        raise AssertionError("first reviewer sprint must cover all resume outcome metrics")

    slot_ids = {slot["id"] for slot in payload["slots"]}
    if len(slot_ids) != payload["slot_count"]:
        raise AssertionError("first reviewer sprint slot IDs must be unique")
    for slot in payload["slots"]:
        if slot["status"] != "not_sent":
            raise AssertionError("first reviewer sprint must not mark outreach as sent")
        if "permission" not in slot["counts_only_after"].lower():
            raise AssertionError("first reviewer sprint must require permission to count evidence")
        if not slot["submission_url"].startswith("https://github.com/sunnnn2005/data-quality-agent"):
            raise AssertionError("first reviewer sprint must submit evidence to public GitHub surfaces")
        if len(slot["acceptance_evidence"]) < 2:
            raise AssertionError("first reviewer sprint slots must define acceptance evidence")

    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("active users", "production users", "customer traction", "completed_count: 1"):
        if forbidden in joined:
            raise AssertionError(f"first reviewer sprint must not claim {forbidden}")
    return {
        "first_10_reviewer_sprint_verified": True,
        "slot_count": payload["slot_count"],
        "target_metric_count": payload["target_metric_count"],
        "not_sent_count": payload["not_sent_count"],
    }


def main() -> None:
    payload = build_first_10_reviewer_sprint()
    verify_first_10_reviewer_sprint(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))


if __name__ == "__main__":
    main()
