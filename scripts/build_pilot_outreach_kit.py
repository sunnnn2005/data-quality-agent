import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
APPLICATION_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "pilot-outreach-kit.json"
OUTPUT_MD_PATH = ROOT / "docs" / "pilot-outreach-kit.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_pilot_outreach_kit_payload() -> dict[str, Any]:
    application_pack = load_json(APPLICATION_PACK_PATH)
    feedback_metrics = load_json(FEEDBACK_METRICS_PATH)
    links = application_pack["application_links"]
    feedback_channels = {item["name"]: item["url"] for item in feedback_metrics["feedback_channels"]}
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_pilot_outreach_kit.py",
        "goal": (
            "Collect real public feedback from people who try the demo, read the scorecard, or run the project locally, "
            "without claiming adoption until feedback is linked to public evidence."
        ),
        "target_audiences": [
            "UC Davis data science classmates",
            "data science or AI club members",
            "student developers interested in LLM agents",
            "technical recruiters or hiring managers reviewing internship projects",
        ],
        "review_paths": {
            "quick_demo": links["demo"],
            "github_repo": links["github_repo"],
            "pilot_feedback_tracker": "https://github.com/sunnnn2005/data-quality-agent/issues/16",
            "public_review_request": "https://github.com/sunnnn2005/data-quality-agent/issues/17",
            "application_evidence_pack": f"{links['github_repo']}/blob/main/docs/application-evidence-pack.md",
            "live_scorecard": links["live_scorecard"],
            "feedback_issue": feedback_channels["Demo feedback"],
            "bug_report": feedback_channels["Bug report"],
            "feature_request": feedback_channels["Feature request"],
            "business_case_review": feedback_channels["Business case review"],
        },
        "outreach_messages": [
            {
                "channel": "linkedin_or_email",
                "audience": "recruiter_or_hiring_manager",
                "message": (
                    "Hi, I built a public LLM data-quality agent project that analyzes CSV and read-only PostgreSQL business data. "
                    "It includes a live demo, container image, OpenAPI contract, CI-verified scorecard, and an evidence pack that keeps user and feedback claims honest. "
                    "If helpful, I would appreciate any feedback on whether this project demonstrates enough AI engineering depth for internship roles."
                ),
            },
            {
                "channel": "discord_slack_or_club",
                "audience": "student_developer",
                "message": (
                    "I am testing a data-quality LLM agent project for internship applications. "
                    "Could you try the public demo or skim the scorecard and leave one GitHub issue with anything confusing, useful, or broken? "
                    "I am tracking feedback publicly instead of claiming users without evidence."
                ),
            },
            {
                "channel": "github_issue_or_readme",
                "audience": "open_source_reviewer",
                "message": (
                    "Review request: does this repo make the LLM agent behavior, safety boundaries, evidence trail, and not-claimed adoption metrics clear enough? "
                    "Please use the demo feedback, bug report, or feature request template so the feedback can be reproduced and counted honestly."
                ),
            },
        ],
        "success_metrics": {
            "external_feedback_items": feedback_metrics["external_feedback_items"],
            "confirmed_external_users": feedback_metrics["confirmed_external_users"],
            "reproducible_feedback_items": feedback_metrics["reproducible_feedback_items"],
            "target_first_feedback_items": 3,
            "target_confirmed_external_users": 1,
        },
        "tracking_rules": [
            "Only count feedback that is linked from a public GitHub issue or reproducible external note.",
            "Only count a user after they explicitly confirm they tried the demo or ran the project.",
            "Do not count private compliments, application submissions, or self-testing as external users.",
            "Keep stars, users, and feedback as zero until public metrics prove otherwise.",
        ],
        "not_claimed": application_pack["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    audiences = "\n".join(f"- {item}" for item in payload["target_audiences"])
    paths = "\n".join(f"- {key.replace('_', ' ').title()}: [{url}]({url})" for key, url in payload["review_paths"].items())
    messages = "\n\n".join(
        f"### {item['channel']} -> {item['audience']}\n\n{item['message']}" for item in payload["outreach_messages"]
    )
    metrics = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["success_metrics"].items())
    rules = "\n".join(f"- {item}" for item in payload["tracking_rules"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Pilot Outreach Kit

This generated kit helps collect real public feedback without inflating adoption claims.

## Goal

{payload["goal"]}

## Target Audiences

{audiences}

## Review Paths

{paths}

## Outreach Messages

{messages}

## Success Metrics

| Metric | Current / Target |
| --- | ---: |
{metrics}

## Tracking Rules

{rules}

## Not Claimed

{not_claimed}
"""


def verify_pilot_outreach_kit(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "target_audience_count": 4,
        "review_path_count": 10,
        "outreach_message_count": 3,
        "tracking_rule_count": 4,
        "current_external_feedback_items": 0,
        "current_confirmed_external_users": 0,
    }
    if len(payload["target_audiences"]) != expected["target_audience_count"]:
        raise AssertionError("pilot outreach kit must include four target audiences")
    if len(payload["review_paths"]) != expected["review_path_count"]:
        raise AssertionError("pilot outreach kit must include ten review paths")
    if len(payload["outreach_messages"]) != expected["outreach_message_count"]:
        raise AssertionError("pilot outreach kit must include three outreach messages")
    if len(payload["tracking_rules"]) != expected["tracking_rule_count"]:
        raise AssertionError("pilot outreach kit must include four tracking rules")
    metrics = payload["success_metrics"]
    if metrics["external_feedback_items"] != expected["current_external_feedback_items"]:
        raise AssertionError("pilot outreach kit must preserve current feedback baseline")
    if metrics["confirmed_external_users"] != expected["current_confirmed_external_users"]:
        raise AssertionError("pilot outreach kit must preserve current user baseline")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("existing users", "customer traction", "production deployment"):
        if forbidden in joined:
            raise AssertionError(f"pilot outreach kit must not claim {forbidden}")
    for required in ("external users", "customer feedback", "enterprise production usage"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"pilot outreach kit must not claim {required}")
    return {"pilot_outreach_kit_verified": True, **expected}


def main() -> None:
    payload = build_pilot_outreach_kit_payload()
    verify_pilot_outreach_kit(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
