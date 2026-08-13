import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
REVIEWER_FUNNEL_PATH = ROOT / "docs" / "reviewer-funnel-board.json"
REVIEWER_INVITATION_KIT_PATH = ROOT / "docs" / "reviewer-invitation-kit.json"
RESUME_TRACTION_PROOF_PATH = ROOT / "docs" / "resume-traction-proof.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-action-queue.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-action-queue.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _task(
    *,
    task_id: str,
    reviewer_segment: str,
    counts_toward: str,
    entry_url: str,
    submission_url: str,
    message_template: str,
    required_public_evidence: list[str],
    claimable_when: str,
) -> dict[str, Any]:
    return {
        "id": task_id,
        "reviewer_segment": reviewer_segment,
        "status": "not_contacted",
        "counts_toward": counts_toward,
        "entry_url": entry_url,
        "submission_url": submission_url,
        "message_template": message_template,
        "required_public_evidence": required_public_evidence,
        "privacy_boundary": (
            "Do not share raw customer data, secrets, private emails, addresses, API keys, or production rows. "
            "Use redacted screenshots, public demo links, synthetic CSVs, or short summaries only."
        ),
        "permission_to_count": (
            "Reviewer must give explicit permission for the public GitHub issue to be counted as project feedback or usage evidence."
        ),
        "claimable_when": claimable_when,
    }


def build_reviewer_action_queue() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    funnel = load_json(REVIEWER_FUNNEL_PATH)
    invitation = load_json(REVIEWER_INVITATION_KIT_PATH)
    traction = load_json(RESUME_TRACTION_PROOF_PATH)
    stages = {stage["id"]: stage for stage in funnel["funnel_stages"]}
    invitation_by_target = {item["target"]: item for item in invitation["invitation_targets"]}

    tasks = [
        _task(
            task_id="review_uc_davis_ds_peer_demo",
            reviewer_segment="UC Davis data science peer",
            counts_toward=stages["visit_public_demo"]["counts_toward"],
            entry_url=stages["visit_public_demo"]["entry_url"],
            submission_url=stages["visit_public_demo"]["submission_url"],
            message_template=invitation_by_target["classmate_quick_demo"]["message"],
            required_public_evidence=[
                "Public GitHub issue with demo path tried",
                "One concrete confusing, useful, or broken behavior",
                "Permission to count the issue as external feedback",
            ],
            claimable_when="Counts only after a public GitHub issue is accepted by the evidence gate.",
        ),
        _task(
            task_id="review_student_swe_peer_demo",
            reviewer_segment="student software engineer peer",
            counts_toward=stages["visit_public_demo"]["counts_toward"],
            entry_url=stages["visit_public_demo"]["entry_url"],
            submission_url=stages["visit_public_demo"]["submission_url"],
            message_template=invitation_by_target["club_or_discord_batch"]["message"],
            required_public_evidence=[
                "Public GitHub issue with reviewed URL",
                "Specific product or engineering feedback",
                "Permission to count the issue as external feedback",
            ],
            claimable_when="Counts toward feedback only after the issue names a reviewed project surface.",
        ),
        _task(
            task_id="review_local_replay_engineer",
            reviewer_segment="engineer comfortable with Docker or local setup",
            counts_toward=stages["run_local_replay"]["counts_toward"],
            entry_url=stages["run_local_replay"]["entry_url"],
            submission_url=stages["run_local_replay"]["submission_url"],
            message_template=invitation_by_target["technical_friend_local_replay"]["message"],
            required_public_evidence=[
                "Command or run path used",
                "Redacted result summary",
                "Whether the run was reproducible",
            ],
            claimable_when="Counts as reproducible feedback only after the reviewer confirms a local or container replay.",
        ),
        _task(
            task_id="review_confirmed_external_use",
            reviewer_segment="reviewer who tried demo or local repo",
            counts_toward=stages["confirm_external_use"]["counts_toward"],
            entry_url=stages["confirm_external_use"]["entry_url"],
            submission_url=stages["confirm_external_use"]["submission_url"],
            message_template=invitation_by_target["confirmed_use_note"]["message"],
            required_public_evidence=[
                "Public confirmation of demo or repo usage",
                "Path used",
                "Permission to count as confirmed external use",
            ],
            claimable_when="Counts as external use only after public confirmation names the path used.",
        ),
        _task(
            task_id="review_data_analyst_business_case",
            reviewer_segment="data analyst or analytics student",
            counts_toward=stages["submit_business_case"]["counts_toward"],
            entry_url=stages["submit_business_case"]["entry_url"],
            submission_url=stages["submit_business_case"]["submission_url"],
            message_template=invitation_by_target["data_practitioner_business_case"]["message"],
            required_public_evidence=[
                "Anonymized business-data quality problem",
                "Expected business impact",
                "No private rows or sensitive fields",
            ],
            claimable_when="Counts as a business case only after it includes an anonymized problem and impact description.",
        ),
        _task(
            task_id="review_operator_business_case",
            reviewer_segment="small-business operator or operations teammate",
            counts_toward=stages["submit_business_case"]["counts_toward"],
            entry_url=stages["submit_business_case"]["entry_url"],
            submission_url=stages["submit_business_case"]["submission_url"],
            message_template=invitation_by_target["data_practitioner_business_case"]["message"],
            required_public_evidence=[
                "Workflow affected by data-quality failure",
                "What decision would be wrong if the data is bad",
                "Permission to count the anonymized case as business feedback",
            ],
            claimable_when="Counts only when a real workflow impact is described without exposing private data.",
        ),
        _task(
            task_id="review_ai_engineer_agent_readiness",
            reviewer_segment="AI engineer, mentor, or ML systems reviewer",
            counts_toward="ai_engineer_review_items",
            entry_url=invitation_by_target["mentor_ai_engineer_review"]["entry_url"],
            submission_url=invitation_by_target["mentor_ai_engineer_review"]["submission_url"],
            message_template=invitation_by_target["mentor_ai_engineer_review"]["message"],
            required_public_evidence=[
                "Inspected LLM tool-calling or agent-readiness path",
                "Concrete AI Engineer credibility feedback",
                "Permission to count as AI Engineer review evidence",
            ],
            claimable_when="Counts as AI Engineer review evidence only after the reviewer names an inspected path.",
        ),
        _task(
            task_id="review_open_source_maintainer",
            reviewer_segment="open-source maintainer or GitHub contributor",
            counts_toward=stages["visit_public_demo"]["counts_toward"],
            entry_url=stages["visit_public_demo"]["entry_url"],
            submission_url=stages["visit_public_demo"]["submission_url"],
            message_template=(
                "Could you review whether this repo is understandable for an outside contributor? "
                "I am especially looking for feedback on README clarity, issue templates, evidence artifacts, "
                "and whether a first-time contributor could run the project."
            ),
            required_public_evidence=[
                "Public issue with contributor-readiness feedback",
                "One suggested improvement for README, setup, tests, or issue templates",
                "Permission to count the issue as external feedback",
            ],
            claimable_when="Counts as feedback only after the issue gives contributor-facing evidence.",
        ),
    ]

    evidence_goals = sorted({task["counts_toward"] for task in tasks})
    status_counts = {
        "not_contacted": sum(1 for task in tasks if task["status"] == "not_contacted"),
        "contacted": 0,
        "completed": 0,
    }

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_action_queue.py",
        "purpose": (
            "Turn the zero-user, zero-feedback baseline into a concrete public reviewer action queue "
            "without claiming any reviewer has been contacted or completed."
        ),
        "baseline": {
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
            "business_case_feedback_items": feedback["business_case_feedback_items"],
            "ai_engineer_review_items": feedback["ai_engineer_review_items"],
            "stars": traction["public_counts"]["stars"],
        },
        "queue_count": len(tasks),
        "not_contacted_count": status_counts["not_contacted"],
        "evidence_goal_count": len(evidence_goals),
        "evidence_goals": evidence_goals,
        "status_counts": status_counts,
        "tasks": tasks,
        "blocked_resume_claims": [
            "active users",
            "customer feedback",
            "enterprise production usage",
            "earned GitHub stars beyond the current public count",
            "completed external reviews",
        ],
        "resume_status": "outreach_queue_ready_not_claimable",
        "resume_safe_summary": (
            f"Published a CI-verified reviewer action queue with {len(tasks)} concrete outreach tasks mapped to "
            f"{len(evidence_goals)} evidence goals and zero contacted or completed reviewers."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    baseline = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["baseline"].items())
    goals = "\n".join(f"- `{goal}`" for goal in payload["evidence_goals"])
    tasks = "\n\n".join(
        "\n".join(
            [
                f"### {task['id']}",
                "",
                f"- Reviewer segment: {task['reviewer_segment']}",
                f"- Status: `{task['status']}`",
                f"- Counts toward: `{task['counts_toward']}`",
                f"- Entry: [{task['entry_url']}]({task['entry_url']})",
                f"- Submission: [{task['submission_url']}]({task['submission_url']})",
                f"- Claimable when: {task['claimable_when']}",
                "",
                task["message_template"],
                "",
                "Required public evidence:",
                *[f"- {item}" for item in task["required_public_evidence"]],
                "",
                f"Privacy boundary: {task['privacy_boundary']}",
                "",
                f"Permission rule: {task['permission_to_count']}",
            ]
        )
        for task in payload["tasks"]
    )
    blocked = "\n".join(f"- {item}" for item in payload["blocked_resume_claims"])
    return f"""# Reviewer Action Queue

This generated queue turns reviewer outreach into public, countable evidence tasks.

## Purpose

{payload["purpose"]}

## Baseline

| Metric | Current value |
| --- | ---: |
{baseline}

## Evidence Goals

{goals}

## Tasks

{tasks}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Blocked Resume Claims

{blocked}
"""


def verify_reviewer_action_queue(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "queue_count": 8,
        "not_contacted_count": 8,
        "evidence_goal_count": 5,
        "completed_count": 0,
        "contacted_count": 0,
    }
    if payload["queue_count"] != expected["queue_count"]:
        raise AssertionError("reviewer action queue must include eight outreach tasks")
    if payload["not_contacted_count"] != expected["not_contacted_count"]:
        raise AssertionError("reviewer action queue must preserve not-contacted baseline")
    if payload["evidence_goal_count"] != expected["evidence_goal_count"]:
        raise AssertionError("reviewer action queue must cover five evidence goals")
    if payload["status_counts"]["completed"] != expected["completed_count"]:
        raise AssertionError("reviewer action queue must not claim completed reviews")
    if payload["status_counts"]["contacted"] != expected["contacted_count"]:
        raise AssertionError("reviewer action queue must not claim contacted reviewers")
    if payload["resume_status"] != "outreach_queue_ready_not_claimable":
        raise AssertionError("reviewer action queue must keep resume status not-claimable")
    required_goals = {
        "external_feedback_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
    }
    if set(payload["evidence_goals"]) != required_goals:
        raise AssertionError("reviewer action queue must map to the tracked feedback metrics")
    for value in payload["baseline"].values():
        if value != 0:
            raise AssertionError("reviewer action queue must start from the zero evidence baseline")
    ids = {task["id"] for task in payload["tasks"]}
    if len(ids) != expected["queue_count"]:
        raise AssertionError("reviewer action queue task IDs must be unique")
    for task in payload["tasks"]:
        if task["status"] != "not_contacted":
            raise AssertionError("reviewer action queue must not imply outreach has happened")
        if not task["submission_url"].startswith("https://github.com/sunnnn2005/data-quality-agent/"):
            raise AssertionError("reviewer action queue submissions must go to public GitHub evidence")
        if "permission" not in task["permission_to_count"].lower():
            raise AssertionError("reviewer action queue must require permission to count evidence")
        if "raw customer data" not in task["privacy_boundary"].lower():
            raise AssertionError("reviewer action queue must include private-data boundaries")
        if not task["required_public_evidence"]:
            raise AssertionError("reviewer action queue tasks must list required public evidence")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("active users: 1", "customer traction", "production adoption", "completed reviewers: 1"):
        if forbidden in joined:
            raise AssertionError(f"reviewer action queue must not claim {forbidden}")
    for blocked in ("active users", "customer feedback", "enterprise production usage"):
        if blocked not in payload["blocked_resume_claims"]:
            raise AssertionError(f"reviewer action queue must block {blocked}")
    return {"reviewer_action_queue_verified": True, **expected}


def main() -> None:
    payload = build_reviewer_action_queue()
    verify_reviewer_action_queue(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
