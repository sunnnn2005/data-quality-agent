import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_LAUNCH_PATH = ROOT / "docs" / "public-launch-broadcast.json"
OUTREACH_STATUS_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
ACCEPTED_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
GITHUB_PUBLIC_STATS_PATH = ROOT / "docs" / "github-public-stats-snapshot.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "outcome-pipeline-board.json"
OUTPUT_MD_PATH = ROOT / "docs" / "outcome-pipeline-board.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _stage_status(stage: str, count: int, goal: int) -> dict[str, Any]:
    return {
        "stage": stage,
        "current_count": count,
        "target_count": goal,
        "complete": count >= goal,
    }


def build_outcome_pipeline_board() -> dict[str, Any]:
    public_launch = load_json(PUBLIC_LAUNCH_PATH)
    outreach = load_json(OUTREACH_STATUS_PATH)
    accepted = load_json(ACCEPTED_ROLLUP_PATH)
    adoption = load_json(ADOPTION_METRICS_PATH)
    github_public_stats = load_json(GITHUB_PUBLIC_STATS_PATH) if GITHUB_PUBLIC_STATS_PATH.exists() else {}

    published_broadcasts = public_launch["published_broadcast_count"]
    sent_messages = outreach["sent_count"]
    public_issues = outreach["public_issue_submitted_count"]
    accepted_issues = accepted["accepted_issue_count"]
    stars = github_public_stats.get("public_stats", {}).get("stars", adoption["stars"])

    stages = [
        _stage_status("public_launch_published", published_broadcasts, 1),
        _stage_status("real_reviewer_messages_sent", sent_messages, 3),
        _stage_status("public_reviewer_issues_submitted", public_issues, 1),
        _stage_status("accepted_external_evidence", accepted_issues, 1),
        _stage_status("github_stars", stars, 5),
    ]

    metric_paths = [
        {
            "resume_metric": "confirmed_external_users",
            "current_count": accepted["accepted_counts"]["confirmed_external_users"],
            "resume_claimable": False,
            "first_resume_threshold": 1,
            "next_action": "Send the public launch link to one real reviewer and ask them to open the demo or run the quickstart.",
            "evidence_required": "A non-owner public GitHub issue with permission to count and no private data.",
        },
        {
            "resume_metric": "external_feedback_items",
            "current_count": accepted["accepted_counts"]["external_feedback_items"],
            "resume_claimable": False,
            "first_resume_threshold": 1,
            "next_action": "Ask a data or SWE peer to submit one concrete usability, correctness, or README feedback item.",
            "evidence_required": "A public issue containing the feedback, reviewer permission, and enough context to reproduce the concern.",
        },
        {
            "resume_metric": "ai_engineer_review_items",
            "current_count": accepted["accepted_counts"]["ai_engineer_review_items"],
            "resume_claimable": False,
            "first_resume_threshold": 1,
            "next_action": "Route one AI/ML systems reviewer to issue #26 and ask them to inspect the agent loop, tools, guardrails, and evaluation docs.",
            "evidence_required": "A public AI Engineer review issue that names inspected files or commands and gives permission to count.",
        },
        {
            "resume_metric": "business_case_feedback_items",
            "current_count": accepted["accepted_counts"]["business_case_feedback_items"],
            "resume_claimable": False,
            "first_resume_threshold": 1,
            "next_action": "Ask a student org, small business, or operations peer whether the support-ticket demo maps to a real data quality pain.",
            "evidence_required": "A redacted business-context issue with impact, fields involved, and permission to count.",
        },
        {
            "resume_metric": "github_stars",
            "current_count": stars,
            "resume_claimable": False,
            "first_resume_threshold": 5,
            "next_action": "Share the demo and README with reviewers only after asking for real use or feedback, not empty stars.",
            "evidence_required": "Public GitHub star count from docs/github-public-stats-snapshot.json, not private messages or self-claims.",
        },
    ]

    for path in metric_paths:
        path["resume_claimable"] = path["current_count"] >= path["first_resume_threshold"]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_outcome_pipeline_board.py",
        "purpose": (
            "Connect public launch, reviewer outreach, public evidence, accepted evidence, and resume-safe "
            "outcome claims in one execution board."
        ),
        "pipeline_stage_count": len(stages),
        "complete_stage_count": sum(1 for stage in stages if stage["complete"]),
        "resume_metric_count": len(metric_paths),
        "claimable_resume_metric_count": sum(1 for path in metric_paths if path["resume_claimable"]),
        "current_baseline": {
            "published_public_broadcasts": published_broadcasts,
            "sent_reviewer_messages": sent_messages,
            "public_reviewer_issues_submitted": public_issues,
            "accepted_external_evidence_items": accepted_issues,
            "github_stars": stars,
        },
        "pipeline_stages": stages,
        "resume_metric_paths": metric_paths,
        "blocked_resume_claims": [
            path["resume_metric"] for path in metric_paths if not path["resume_claimable"]
        ],
        "next_best_actions": [
            "Send three real reviewer messages using the reviewer send queue.",
            "Record each sent message with scripts/record_reviewer_outreach_event.py.",
            "Ask reviewers to submit public, redacted GitHub issues through the reviewer submission hub.",
            "Regenerate docs/github-public-stats-snapshot.json before claiming any GitHub star count.",
            "Run the external reviewer evidence gate before changing any resume outcome number.",
        ],
        "resume_status": "distribution_started_outcomes_not_claimable",
        "resume_safe_summary": (
            "Built a CI-verified outcome pipeline board connecting 1 public launch broadcast to reviewer "
            "outreach, public evidence, accepted evidence, and resume claim thresholds while preserving "
            "zero claimable resume outcomes."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    stages = "\n".join(
        f"| `{item['stage']}` | {item['current_count']} | {item['target_count']} | {item['complete']} |"
        for item in payload["pipeline_stages"]
    )
    metrics = "\n".join(
        "| `{resume_metric}` | {current_count} | {first_resume_threshold} | {resume_claimable} | {next_action} |".format(
            **item
        )
        for item in payload["resume_metric_paths"]
    )
    actions = "\n".join(f"- {item}" for item in payload["next_best_actions"])
    blocked = "\n".join(f"- `{item}`" for item in payload["blocked_resume_claims"])
    baseline = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["current_baseline"].items()
    )
    return f"""# Outcome Pipeline Board

This generated board connects distribution activity to resume-safe outcome claims.

## Current Baseline

| Metric | Count |
| --- | ---: |
{baseline}

## Pipeline Stages

| Stage | Current | Target | Complete |
| --- | ---: | ---: | --- |
{stages}

## Resume Metric Paths

| Metric | Current | First Resume Threshold | Claimable | Next Action |
| --- | ---: | ---: | --- | --- |
{metrics}

## Blocked Resume Claims

{blocked}

## Next Best Actions

{actions}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_outcome_pipeline_board(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["pipeline_stage_count"] != 5:
        raise AssertionError("outcome pipeline board must track five pipeline stages")
    if payload["resume_metric_count"] != 5:
        raise AssertionError("outcome pipeline board must track five resume outcome paths")
    if payload["complete_stage_count"] != 1:
        raise AssertionError("only the public launch stage should be complete at the current baseline")
    if payload["claimable_resume_metric_count"] != 0:
        raise AssertionError("no resume outcome metric should be claimable at the current baseline")
    baseline = payload["current_baseline"]
    if baseline["published_public_broadcasts"] != 1:
        raise AssertionError("outcome pipeline board must include the one published public broadcast")
    if baseline["sent_reviewer_messages"] < 0:
        raise AssertionError("outcome pipeline board sent reviewer messages cannot be negative")
    for key in (
        "public_reviewer_issues_submitted",
        "accepted_external_evidence_items",
        "github_stars",
    ):
        if baseline[key] != 0:
            raise AssertionError(f"outcome pipeline board must preserve zero baseline for {key}")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in (
        "record_reviewer_outreach_event.py",
        "reviewer submission hub",
        "external reviewer evidence gate",
        "zero claimable resume outcomes",
    ):
        if phrase not in joined:
            raise AssertionError(f"outcome pipeline board missing phrase: {phrase}")
    return {
        "outcome_pipeline_board_verified": True,
        "pipeline_stage_count": payload["pipeline_stage_count"],
        "claimable_resume_metric_count": payload["claimable_resume_metric_count"],
    }


def main() -> None:
    payload = build_outcome_pipeline_board()
    verify_outcome_pipeline_board(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps({"status": "ok", "pipeline_stage_count": payload["pipeline_stage_count"]}))


if __name__ == "__main__":
    main()
