import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUSINESS_RESOLUTION_BRIEF_PATH = ROOT / "docs" / "business-resolution-brief.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "business-resolution-review-request.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-resolution-review-request.md"
REVIEW_ISSUE_URL = "https://github.com/sunnnn2005/data-quality-agent/issues/30"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_business_resolution_review_request() -> dict[str, Any]:
    brief = load_json(BUSINESS_RESOLUTION_BRIEF_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    counts = brief["detected_signal_counts"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_resolution_review_request.py",
        "review_issue": REVIEW_ISSUE_URL,
        "source_brief": "docs/business-resolution-brief.md",
        "review_goal": (
            "Collect non-owner public review on whether the support-operations business-resolution brief "
            "looks realistic, useful, and specific enough for a real data or operations workflow."
        ),
        "review_questions": [
            "Does this support-operations data-quality scenario look realistic?",
            "Are the 5 findings mapped to the right business risks?",
            "Are the 3 high-priority actions useful and specific enough?",
            "Are the 4 owner handoffs believable for a real data/ops team?",
            "What would make this more useful for a real analyst, data engineer, or operations team?",
        ],
        "evidence_gate": {
            "counts_only_if": [
                "reviewer is not the repository owner",
                "reviewer comments publicly on issue #30 or submits a linked public review issue",
                "reviewer gives explicit permission to count the review publicly",
                "review contains no private company data, customer names, emails, secrets, or raw production rows",
            ],
            "self_authored_issue_counts_as_feedback": False,
            "current_external_feedback_items": feedback["external_feedback_items"],
            "current_business_case_feedback_items": feedback["business_case_feedback_items"],
            "current_confirmed_external_users": feedback["confirmed_external_users"],
        },
        "brief_signal_counts": {
            "findings": counts["findings"],
            "business_risk_areas": counts["business_risk_areas"],
            "high_priority_actions": counts["high_priority_actions"],
            "owner_handoffs": counts["owner_handoffs"],
        },
        "resume_safe_progress": (
            "Opened a public business-resolution review request for an anonymized support-operations data-quality "
            "case, with explicit evidence gates before any external feedback or business validation claim can count."
        ),
        "not_claimed": [
            "external reviewer feedback from issue creation alone",
            "customer adoption",
            "production deployment",
            "business impact validated by a company",
            "GitHub stars gained",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    questions = "\n".join(f"{index}. {item}" for index, item in enumerate(payload["review_questions"], start=1))
    gates = "\n".join(f"- {item}" for item in payload["evidence_gate"]["counts_only_if"])
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["brief_signal_counts"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    gate = payload["evidence_gate"]
    return f"""# Business Resolution Review Request

This generated artifact turns the business-resolution brief into a public external-review entrypoint. It does not count the self-authored issue as feedback.

## Review Issue

[{payload["review_issue"]}]({payload["review_issue"]})

## Review Goal

{payload["review_goal"]}

## Review Questions

{questions}

## Brief Signal Counts

| Signal | Count |
| --- | ---: |
{counts}

## Evidence Gate

Counts only if:

{gates}

| Current metric | Value |
| --- | ---: |
| External feedback items | {gate["current_external_feedback_items"]} |
| Business-case feedback items | {gate["current_business_case_feedback_items"]} |
| Confirmed external users | {gate["current_confirmed_external_users"]} |
| Self-authored issue counts as feedback | `{gate["self_authored_issue_counts_as_feedback"]}` |

## Resume-Safe Progress

{payload["resume_safe_progress"]}

## Not Claimed

{not_claimed}
"""


def verify_business_resolution_review_request(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["review_issue"] != REVIEW_ISSUE_URL:
        raise AssertionError("business resolution review request must link issue #30")
    if len(payload["review_questions"]) != 5:
        raise AssertionError("business resolution review request must ask 5 focused questions")
    counts = payload["brief_signal_counts"]
    expected_counts = {
        "findings": 5,
        "business_risk_areas": 4,
        "high_priority_actions": 3,
        "owner_handoffs": 4,
    }
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {counts.get(key)!r}")
    gate = payload["evidence_gate"]
    if gate["self_authored_issue_counts_as_feedback"] is not False:
        raise AssertionError("self-authored issue must not count as feedback")
    if gate["current_external_feedback_items"] != 0 or gate["current_confirmed_external_users"] != 0:
        raise AssertionError("review request must preserve zero external feedback/user baseline")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("explicit permission", "no private company data", "not the repository owner"):
        if required not in joined:
            raise AssertionError(f"business resolution review request missing gate: {required}")
    not_claimed = {item.lower() for item in payload["not_claimed"]}
    for forbidden in ("customer adoption", "production deployment", "github stars gained"):
        if forbidden not in not_claimed:
            raise AssertionError(f"business resolution review request must not claim {forbidden}")
    return {"business_resolution_review_request_verified": True, **expected_counts}


def main() -> None:
    payload = build_business_resolution_review_request()
    verify_business_resolution_review_request(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
