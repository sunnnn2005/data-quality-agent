import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_REVIEWER_CALL_PATH = ROOT / "docs" / "public-reviewer-call.json"
REVIEWER_SUBMISSION_HUB_PATH = ROOT / "docs" / "reviewer-submission-hub.json"
REVIEWER_OUTREACH_EXECUTION_PACK_PATH = ROOT / "docs" / "reviewer-outreach-execution-pack.json"
RESUME_OUTCOME_METRICS_PATH = ROOT / "docs" / "resume-outcome-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-share-kit.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-share-kit.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _submission_url(hub: dict[str, Any], path_id: str) -> str:
    for path in hub["submission_paths"]:
        if path["id"] == path_id:
            return path["submission_url"]
    raise KeyError(path_id)


def build_reviewer_share_kit() -> dict[str, Any]:
    public_call = load_json(PUBLIC_REVIEWER_CALL_PATH)
    hub = load_json(REVIEWER_SUBMISSION_HUB_PATH)
    outreach = load_json(REVIEWER_OUTREACH_EXECUTION_PACK_PATH)
    outcome_metrics = load_json(RESUME_OUTCOME_METRICS_PATH)
    repo = "https://github.com/sunnnn2005/data-quality-agent"
    issue_url = public_call["public_call_issue"]
    demo_url = "https://sunnnn2005.github.io/data-quality-agent/"
    current_counts = {
        item["metric"]: item["current_count"]
        for item in outcome_metrics["tracked_outcomes"]
        if item["metric"]
        in {
            "confirmed_external_users",
            "external_feedback_items",
            "business_case_feedback_items",
            "ai_engineer_review_items",
            "github_stars",
        }
    }
    share_messages = [
        {
            "channel": "linkedin_dm",
            "audience": "AI Engineer, SWE, or data engineer peer",
            "message": (
                "Hi {name}, I am collecting public review evidence for my Data Quality Agent project. "
                f"The public call is {issue_url}. If you have 8-15 minutes, could you inspect the LLM tool-calling loop, "
                f"read-only business-data path, or public demo at {demo_url}? Please do not include private data. "
                "If you are comfortable, include permission for the public issue to be counted as review evidence."
            ),
            "call_to_action_url": issue_url,
            "evidence_submission_url": _submission_url(hub, "submit_ai_engineer_review"),
            "counts_toward": "ai_engineer_review_items",
        },
        {
            "channel": "email_or_mentor",
            "audience": "mentor, TA, professor, or technical reviewer",
            "message": (
                "Hi {name}, I am trying to make this project credible for AI Engineer internship applications. "
                f"Would you be willing to review the public call at {issue_url} and leave one GitHub issue with concrete feedback? "
                "Please avoid private data, raw customer rows, or secrets. If you are comfortable, include permission for the "
                "public issue to be counted as project review evidence."
            ),
            "call_to_action_url": issue_url,
            "evidence_submission_url": _submission_url(hub, "try_public_demo"),
            "counts_toward": "external_feedback_items",
        },
        {
            "channel": "class_discord_or_slack",
            "audience": "student developer or data science club channel",
            "message": (
                "I am collecting public review evidence for a Data Quality Agent project. "
                f"Public call: {issue_url}. If anyone can try the demo or run the repo, please leave a public GitHub issue "
                "with what worked, what broke, and permission to count the issue as review evidence. Do not include private data."
            ),
            "call_to_action_url": issue_url,
            "evidence_submission_url": _submission_url(hub, "confirm_external_run"),
            "counts_toward": "confirmed_external_users",
        },
        {
            "channel": "github_discussion_or_issue_comment",
            "audience": "open-source reviewer or first-time contributor",
            "message": (
                f"Review request: {issue_url}. I am looking for public feedback on whether the repo is runnable, "
                "whether the LLM-agent evidence is clear, and where the contributor path is confusing. "
                "Please keep private data out of the issue and include permission if the public review can be counted."
            ),
            "call_to_action_url": issue_url,
            "evidence_submission_url": _submission_url(hub, "submit_reproducible_issue"),
            "counts_toward": "reproducible_feedback_items",
        },
        {
            "channel": "resume_portfolio_link",
            "audience": "recruiter or hiring manager opening the resume",
            "message": (
                "For reviewers: this project keeps outcome claims evidence-backed. "
                f"The public reviewer call is {issue_url}, the demo is {demo_url}, and feedback should avoid private data. "
                "Permission is required before any public issue is counted toward resume outcome metrics."
            ),
            "call_to_action_url": issue_url,
            "evidence_submission_url": _submission_url(hub, "submit_business_case"),
            "counts_toward": "business_case_feedback_items",
        },
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_share_kit.py",
        "purpose": (
            "Package the public reviewer call into copy-ready sharing messages so real reviewers can try the project "
            "and submit public evidence without upgrading any resume outcome claim prematurely."
        ),
        "public_call_issue": issue_url,
        "share_channel_count": len(share_messages),
        "ready_message_count": len(share_messages),
        "linked_submission_paths": hub["submission_path_count"],
        "linked_public_call_segments": public_call["reviewer_segment_count"],
        "required_evidence_fields": hub["total_required_evidence_fields"],
        "outreach_tasks_linked": outreach["outreach_item_count"],
        "send_status_counts": {"not_sent": len(share_messages), "sent": 0, "completed": 0},
        "current_counts": current_counts,
        "share_messages": share_messages,
        "manual_execution_rules": [
            "Do not mark a message as sent until it has actually been sent by the maintainer.",
            "Does not count private replies, private DMs, or private email reactions as public outcome evidence.",
            "Does not count self-authored issues, vague reactions, or fake GitHub engagement.",
            "Counts only public, non-owner GitHub issues with explicit permission and no private data.",
            "Keep all user, feedback, business-impact, AI-review, and star claims blocked while accepted counts are zero.",
        ],
        "resume_status": "share_ready_not_claimable",
        "resume_safe_summary": (
            "Published a CI-verified reviewer share kit with 5 copy-ready messages, 5 share channels, issue #19, "
            "6 submission paths, and zero sent or completed outreach claimed."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    message_rows = "\n".join(
        "| {channel} | {audience} | `{counts_toward}` | [Call]({call_to_action_url}) | [Submit]({evidence_submission_url}) |".format(
            **message
        )
        for message in payload["share_messages"]
    )
    messages = "\n\n".join(
        "### {channel}\n\nAudience: {audience}\n\n```text\n{message}\n```\n\nSubmission: {evidence_submission_url}".format(
            **message
        )
        for message in payload["share_messages"]
    )
    rules = "\n".join(f"- {rule}" for rule in payload["manual_execution_rules"])
    counts = "\n".join(f"| {key} | {value} |" for key, value in payload["current_counts"].items())
    return f"""# Reviewer Share Kit

This generated kit turns the public reviewer call into copy-ready outreach text.

## Purpose

{payload["purpose"]}

## Public Call

[{payload["public_call_issue"]}]({payload["public_call_issue"]})

## Share Channels

| Channel | Audience | Counts Toward | Public Call | Evidence Form |
| --- | --- | --- | --- | --- |
{message_rows}

## Copy-Ready Messages

{messages}

## Current Counts

| Outcome | Current Count |
| --- | ---: |
{counts}

## Send Status

| Status | Count |
| --- | ---: |
| not_sent | {payload["send_status_counts"]["not_sent"]} |
| sent | {payload["send_status_counts"]["sent"]} |
| completed | {payload["send_status_counts"]["completed"]} |

## Manual Execution Rules

{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_reviewer_share_kit(payload: dict[str, Any]) -> dict[str, Any]:
    expected_counts = {
        "share_channel_count": 5,
        "ready_message_count": 5,
        "linked_submission_paths": 6,
        "linked_public_call_segments": 3,
        "required_evidence_fields": 23,
        "outreach_tasks_linked": 8,
    }
    for key, expected in expected_counts.items():
        if payload[key] != expected:
            raise AssertionError(f"{key} must be {expected}")
    if payload["public_call_issue"] != "https://github.com/sunnnn2005/data-quality-agent/issues/19":
        raise AssertionError("reviewer share kit must point to issue #19")
    if payload["send_status_counts"] != {"not_sent": 5, "sent": 0, "completed": 0}:
        raise AssertionError("reviewer share kit must not claim sent or completed outreach")
    for key, value in payload["current_counts"].items():
        if value != 0:
            raise AssertionError(f"{key} must remain zero until accepted evidence exists")
    for message in payload["share_messages"]:
        text = json.dumps(message, sort_keys=True).lower()
        if "permission" not in text:
            raise AssertionError("every share message must ask for permission")
        if "private data" not in text:
            raise AssertionError("every share message must warn against private data")
        if "https://github.com/sunnnn2005/data-quality-agent" not in text:
            raise AssertionError("every share message must link public GitHub evidence")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("does not count private replies", "self-authored", "fake github engagement", "not_sent"):
        if required not in joined:
            raise AssertionError(f"reviewer share kit missing boundary: {required}")
    if payload["resume_status"] != "share_ready_not_claimable":
        raise AssertionError("reviewer share kit must remain share-ready but not claimable")
    return {
        "reviewer_share_kit_verified": True,
        "share_channel_count": payload["share_channel_count"],
        "ready_message_count": payload["ready_message_count"],
        "linked_submission_paths": payload["linked_submission_paths"],
        "required_evidence_fields": payload["required_evidence_fields"],
    }


def main() -> None:
    payload = build_reviewer_share_kit()
    verify_reviewer_share_kit(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
