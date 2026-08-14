import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PIPELINE_PATH = ROOT / "docs" / "outcome-pipeline-board.json"
SEND_QUEUE_PATH = ROOT / "docs" / "reviewer-send-queue.json"
WITNESS_PACKET_PATH = ROOT / "docs" / "outcome-witness-packet.json"
EVIDENCE_GAPS_PATH = ROOT / "docs" / "evidence-gap-diagnostics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "outcome-sprint-plan.json"
OUTPUT_MD_PATH = ROOT / "docs" / "outcome-sprint-plan.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _next_send_by_metric(queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["target_metric"]: item for item in queue["next_sends"]}


def build_outcome_sprint_plan() -> dict[str, Any]:
    pipeline = load_json(PIPELINE_PATH)
    queue = load_json(SEND_QUEUE_PATH)
    witness = load_json(WITNESS_PACKET_PATH)
    gaps = load_json(EVIDENCE_GAPS_PATH)

    sends_by_metric = _next_send_by_metric(queue)
    accepted_counts = gaps["accepted_counts"]
    sprint_days = [
        {
            "day": 1,
            "title": "Send the first AI Engineer review request",
            "target_metric": "ai_engineer_review_items",
            "current_count": accepted_counts["ai_engineer_review_items"],
            "execution_artifact": "docs/first-reviewer-send-kit.md",
            "reviewer_profile": sends_by_metric["ai_engineer_review_items"]["reviewer_profile"],
            "completion_evidence": [
                "one real reviewer contact chosen",
                "message actually sent through the recommended channel",
                "outreach event recorded with scripts/record_reviewer_outreach_event.py",
            ],
            "resume_unlock_gate": "No resume outcome changes until a non-owner AI Engineer review issue passes the evidence gate.",
        },
        {
            "day": 2,
            "title": "Collect one confirmed external run",
            "target_metric": "confirmed_external_users",
            "current_count": accepted_counts["confirmed_external_users"],
            "execution_artifact": "docs/outcome-witness-packet.md#witness_confirmed_external_users",
            "reviewer_profile": sends_by_metric["confirmed_external_users"]["reviewer_profile"],
            "completion_evidence": [
                "reviewer opened the public demo or ran the quickstart",
                "reviewer submits a public issue with observed result",
                "reviewer gives permission for the issue to count publicly",
            ],
            "resume_unlock_gate": "First claimable user metric unlocks only after accepted public issue evidence.",
        },
        {
            "day": 3,
            "title": "Collect one concrete product or README feedback item",
            "target_metric": "external_feedback_items",
            "current_count": accepted_counts["external_feedback_items"],
            "execution_artifact": "docs/reviewer-send-queue.md",
            "reviewer_profile": sends_by_metric["external_feedback_items"]["reviewer_profile"],
            "completion_evidence": [
                "reviewer names the page, command, or file inspected",
                "reviewer gives one specific useful, confusing, or broken point",
                "public issue contains no private data and grants counting permission",
            ],
            "resume_unlock_gate": "Feedback count remains zero until the external reviewer evidence gate accepts the issue.",
        },
        {
            "day": 4,
            "title": "Ask for one anonymized business data-quality scenario",
            "target_metric": "business_case_feedback_items",
            "current_count": accepted_counts["business_case_feedback_items"],
            "execution_artifact": "docs/outcome-witness-packet.md#witness_business_case_feedback_items",
            "reviewer_profile": sends_by_metric["business_case_feedback_items"]["reviewer_profile"],
            "completion_evidence": [
                "reviewer describes a real workflow problem without raw business rows",
                "issue includes impacted decision, fields involved, and expected usefulness",
                "issue grants permission to count as public business-case evidence",
            ],
            "resume_unlock_gate": "Business-problem outcome wording unlocks only after an accepted anonymized public issue.",
        },
        {
            "day": 5,
            "title": "Run the evidence gate and materialize only accepted outcomes",
            "target_metric": "all_outcome_metrics",
            "current_count": pipeline["claimable_resume_metric_count"],
            "execution_artifact": "docs/resume-claim-materializer.md",
            "reviewer_profile": "maintainer verification pass",
            "completion_evidence": [
                "scripts/update_feedback_metrics.py has been run",
                "scripts/build_external_reviewer_evidence_gate.py has been run",
                "scripts/build_resume_claim_materializer.py shows only accepted public evidence",
            ],
            "resume_unlock_gate": "Only generated materialized claims from accepted public evidence can be copied into the resume.",
        },
    ]

    target_metrics = sorted({day["target_metric"] for day in sprint_days})
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_outcome_sprint_plan.py",
        "purpose": (
            "Turn the public launch and reviewer packets into a five-day execution sprint for earning real, "
            "public, resume-countable outcome evidence."
        ),
        "sprint_day_count": len(sprint_days),
        "target_metric_count": len(target_metrics),
        "target_metrics": target_metrics,
        "current_public_counts": witness["current_public_counts"],
        "claimable_resume_metric_count": pipeline["claimable_resume_metric_count"],
        "accepted_issue_count": gaps["accepted_issue_count"],
        "sprint_days": sprint_days,
        "daily_success_rule": (
            "A day is complete only when a real non-owner action happened and the evidence can be inspected publicly "
            "or recorded in the outreach status board."
        ),
        "resume_upgrade_rule": (
            "Do not add user, feedback, business validation, AI review, or GitHub star wording to the resume until "
            "the evidence gate accepts public evidence and the resume claim materializer emits exact wording."
        ),
        "not_claimed": [
            "No external users are claimed while confirmed_external_users is zero.",
            "No external feedback is claimed while external_feedback_items is zero.",
            "No AI Engineer review is claimed while ai_engineer_review_items is zero.",
            "No business validation is claimed while business_case_feedback_items is zero.",
            "No GitHub star growth is claimed while github_stars is zero.",
        ],
        "resume_safe_summary": (
            "Published a five-day outcome sprint plan mapping 5 target metrics to real reviewer actions, public "
            "evidence gates, and zero resume upgrades until accepted non-owner evidence exists."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(
        f"| `{key}` | {value} |" for key, value in payload["current_public_counts"].items()
    )
    days = []
    for day in payload["sprint_days"]:
        evidence = "\n".join(f"- {item}" for item in day["completion_evidence"])
        days.append(
            f"""### Day {day["day"]}: {day["title"]}

- Target metric: `{day["target_metric"]}`
- Current count: {day["current_count"]}
- Execution artifact: `{day["execution_artifact"]}`
- Reviewer profile: {day["reviewer_profile"]}

Completion evidence:
{evidence}

Resume unlock gate: {day["resume_unlock_gate"]}
"""
        )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    metrics = "\n".join(f"- `{metric}`" for metric in payload["target_metrics"])
    return f"""# Outcome Sprint Plan

This generated sprint turns launch readiness into real, public, resume-countable evidence.

## Target Metrics

{metrics}

## Current Public Counts

| Metric | Count |
| --- | ---: |
{counts}

## Sprint Days

{chr(10).join(days)}
## Daily Success Rule

{payload["daily_success_rule"]}

## Resume Upgrade Rule

{payload["resume_upgrade_rule"]}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_outcome_sprint_plan(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["sprint_day_count"] != 5:
        raise AssertionError("outcome sprint plan must contain five sprint days")
    if payload["target_metric_count"] != 5:
        raise AssertionError("outcome sprint plan must target five metrics")
    if payload["claimable_resume_metric_count"] != 0:
        raise AssertionError("outcome sprint plan must not upgrade resume outcomes")
    if payload["accepted_issue_count"] != 0:
        raise AssertionError("outcome sprint plan must preserve zero accepted public evidence")
    if any(value != 0 for value in payload["current_public_counts"].values()):
        raise AssertionError("outcome sprint plan must preserve current zero public outcome counts")
    required_metrics = {
        "ai_engineer_review_items",
        "all_outcome_metrics",
        "business_case_feedback_items",
        "confirmed_external_users",
        "external_feedback_items",
    }
    if set(payload["target_metrics"]) != required_metrics:
        raise AssertionError("outcome sprint plan missing required target metrics")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in (
        "real non-owner action",
        "resume claim materializer",
        "do not add user",
        "zero resume upgrades",
    ):
        if phrase not in joined:
            raise AssertionError(f"outcome sprint plan missing phrase: {phrase}")
    return {
        "outcome_sprint_plan_verified": True,
        "sprint_day_count": payload["sprint_day_count"],
        "target_metric_count": payload["target_metric_count"],
    }


def main() -> None:
    payload = build_outcome_sprint_plan()
    verify_outcome_sprint_plan(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(verify_outcome_sprint_plan(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
