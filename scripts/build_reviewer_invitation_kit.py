import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
REVIEWER_FUNNEL_PATH = ROOT / "docs" / "reviewer-funnel-board.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-invitation-kit.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-invitation-kit.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_reviewer_invitation_kit_payload() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    funnel = load_json(REVIEWER_FUNNEL_PATH)
    stages = {stage["id"]: stage for stage in funnel["funnel_stages"]}
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_invitation_kit.py",
        "purpose": (
            "Provide copy-ready invitations that route real reviewers into public GitHub evidence, "
            "so feedback and usage claims can be upgraded only after public proof exists."
        ),
        "current_baseline": {
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
            "business_case_feedback_items": feedback["business_case_feedback_items"],
        },
        "invitation_targets": [
            {
                "target": "classmate_quick_demo",
                "audience": "UC Davis classmate or student developer",
                "minutes": 8,
                "funnel_stage": "visit_public_demo",
                "counts_toward": stages["visit_public_demo"]["counts_toward"],
                "entry_url": stages["visit_public_demo"]["entry_url"],
                "submission_url": stages["visit_public_demo"]["submission_url"],
                "message": (
                    "Could you spend 8 minutes trying my public Data Quality Agent demo and leave one GitHub issue "
                    "with anything confusing, useful, or broken? I am tracking feedback publicly instead of claiming users without proof."
                ),
            },
            {
                "target": "technical_friend_local_replay",
                "audience": "student developer comfortable with local setup",
                "minutes": 15,
                "funnel_stage": "run_local_replay",
                "counts_toward": stages["run_local_replay"]["counts_toward"],
                "entry_url": stages["run_local_replay"]["entry_url"],
                "submission_url": stages["run_local_replay"]["submission_url"],
                "message": (
                    "Could you clone my Data Quality Agent repo, run the local replay path, and submit whether the result was reproducible? "
                    "Please avoid raw private data; a short redacted run summary is enough."
                ),
            },
            {
                "target": "mentor_ai_engineer_review",
                "audience": "mentor, engineer, or AI/data practitioner",
                "minutes": 12,
                "funnel_stage": "confirm_external_use",
                "counts_toward": stages["confirm_external_use"]["counts_toward"],
                "entry_url": stages["confirm_external_use"]["entry_url"],
                "submission_url": stages["confirm_external_use"]["submission_url"],
                "message": (
                    "I am improving this project for AI Engineer internship applications. Could you review whether the tool-calling agent, "
                    "safety boundaries, and evidence trail look credible, then leave a public note if you tried the demo or repo?"
                ),
            },
            {
                "target": "data_practitioner_business_case",
                "audience": "data analyst, operations teammate, or small-business operator",
                "minutes": 12,
                "funnel_stage": "submit_business_case",
                "counts_toward": stages["submit_business_case"]["counts_toward"],
                "entry_url": stages["submit_business_case"]["entry_url"],
                "submission_url": stages["submit_business_case"]["submission_url"],
                "message": (
                    "Do you have an anonymized data-quality problem this project should handle, such as duplicate IDs, stale exports, "
                    "missing routing fields, or suspicious numeric values? A public business-case issue with no raw data would help me test real usefulness."
                ),
            },
            {
                "target": "club_or_discord_batch",
                "audience": "data science club, Discord, or Slack group",
                "minutes": 10,
                "funnel_stage": "visit_public_demo",
                "counts_toward": stages["visit_public_demo"]["counts_toward"],
                "entry_url": stages["visit_public_demo"]["entry_url"],
                "submission_url": stages["visit_public_demo"]["submission_url"],
                "message": (
                    "I am collecting public review evidence for a data-quality LLM agent project. If anyone can try the demo, "
                    "please leave one GitHub issue with what worked, what broke, or what would make it more useful for real data workflows."
                ),
            },
        ],
        "success_thresholds": {
            "first_feedback": 1,
            "resume_feedback_signal": 3,
            "confirmed_external_user_signal": 1,
            "business_case_signal": 1,
        },
        "counting_rules": [
            "Count only public GitHub issues or reproducible public notes.",
            "Count confirmed users only when the reviewer states they tried the demo or ran the repo.",
            "Do not count private messages, self-tests, application submissions, or unverifiable compliments.",
            "Do not collect raw customer data, secrets, addresses, emails, or production rows.",
        ],
        "not_claimed": funnel["not_claimed"],
        "resume_safe_summary": (
            "Published 5 copy-ready reviewer invitations tied to 4 public evidence paths and explicit zero-feedback baselines."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    baseline = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_baseline"].items())
    invitations = "\n\n".join(
        "\n".join(
            [
                f"### {item['target']} -> {item['audience']}",
                "",
                f"- Minutes: {item['minutes']}",
                f"- Funnel stage: `{item['funnel_stage']}`",
                f"- Counts toward: `{item['counts_toward']}`",
                f"- Entry: [{item['entry_url']}]({item['entry_url']})",
                f"- Submission: [{item['submission_url']}]({item['submission_url']})",
                "",
                item["message"],
            ]
        )
        for item in payload["invitation_targets"]
    )
    thresholds = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["success_thresholds"].items()
    )
    rules = "\n".join(f"- {rule}" for rule in payload["counting_rules"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Reviewer Invitation Kit

This generated kit gives copy-ready messages for collecting public review evidence.

## Purpose

{payload["purpose"]}

## Current Baseline

| Metric | Current value |
| --- | ---: |
{baseline}

## Invitations

{invitations}

## Success Thresholds

| Threshold | Value |
| --- | ---: |
{thresholds}

## Counting Rules

{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_reviewer_invitation_kit(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "invitation_count": 5,
        "distinct_funnel_stages": 4,
        "counting_rule_count": 4,
        "current_external_feedback_items": 0,
        "current_confirmed_external_users": 0,
    }
    if len(payload["invitation_targets"]) != expected["invitation_count"]:
        raise AssertionError("reviewer invitation kit must include five copy-ready invitations")
    stages = {item["funnel_stage"] for item in payload["invitation_targets"]}
    if len(stages) != expected["distinct_funnel_stages"]:
        raise AssertionError("reviewer invitation kit must cover four funnel stages")
    if len(payload["counting_rules"]) != expected["counting_rule_count"]:
        raise AssertionError("reviewer invitation kit must include four counting rules")
    baseline = payload["current_baseline"]
    if baseline["external_feedback_items"] != expected["current_external_feedback_items"]:
        raise AssertionError("reviewer invitation kit must preserve current feedback baseline")
    if baseline["confirmed_external_users"] != expected["current_confirmed_external_users"]:
        raise AssertionError("reviewer invitation kit must preserve current user baseline")
    for item in payload["invitation_targets"]:
        if not item["entry_url"].startswith("https://"):
            raise AssertionError("reviewer invitations must use public entry URLs")
        if "github.com/sunnnn2005/data-quality-agent/issues/new" not in item["submission_url"]:
            raise AssertionError("reviewer invitations must submit to public GitHub issue templates")
        if item["counts_toward"] not in {
            "external_feedback_items",
            "confirmed_external_users",
            "reproducible_feedback_items",
            "business_case_feedback_items",
        }:
            raise AssertionError("reviewer invitations must map to tracked feedback metrics")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("existing users", "customer traction", "production deployment", "paid users"):
        if forbidden in joined:
            raise AssertionError(f"reviewer invitation kit must not claim {forbidden}")
    return {"reviewer_invitation_kit_verified": True, **expected}


def main() -> None:
    payload = build_reviewer_invitation_kit_payload()
    verify_reviewer_invitation_kit(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
