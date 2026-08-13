import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AI_READINESS_PATH = ROOT / "docs" / "ai-engineer-readiness.json"
APPLICATION_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
TEMPLATE_PATH = ROOT / ".github" / "ISSUE_TEMPLATE" / "ai_engineer_review.md"
OUTPUT_JSON_PATH = ROOT / "docs" / "ai-engineer-review-intake.json"
OUTPUT_MD_PATH = ROOT / "docs" / "ai-engineer-review-intake.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_ai_engineer_review_intake() -> dict[str, Any]:
    readiness = load_json(AI_READINESS_PATH)
    application_pack = load_json(APPLICATION_PACK_PATH)
    template_text = TEMPLATE_PATH.read_text()
    review_paths = {
        "ai_engineer_readiness": application_pack["application_links"]["ai_engineer_readiness"],
        "agent_capability_matrix": application_pack["application_links"]["agent_capability_matrix"],
        "openapi_contract": application_pack["application_links"]["api_contract"],
        "business_replay_demo": application_pack["application_links"]["business_replay_demo"],
        "real_model_evidence_capture": application_pack["application_links"]["real_model_evidence_capture"],
        "review_issue_template": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md",
    }
    review_questions = [
        "Does the LLM tool calling path choose tools based on evidence rather than following a fixed workflow?",
        "Are tool results fed back into the model before the final answer?",
        "Is the output structured enough for another API or reviewer to verify?",
        "Are guardrails, redaction, and read-only database boundaries visible?",
        "Would this project credibly support an AI Engineer Intern interview discussion?",
        "What single improvement would make the project more convincing?",
    ]
    countable_conditions = [
        "Issue is created by a non-owner reviewer.",
        "Issue uses ai_engineer_review.md or includes equivalent answers.",
        "Reviewer grants permission to count the public issue.",
        "Review includes at least one inspected path or command.",
        "Review does not include private customer data, secrets, or raw business rows.",
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_ai_engineer_review_intake.py",
        "purpose": "Collect public, permissioned reviewer feedback specifically about AI Engineer readiness.",
        "template": str(TEMPLATE_PATH.relative_to(ROOT)),
        "review_path_count": len(review_paths),
        "review_paths": review_paths,
        "review_question_count": len(review_questions),
        "review_questions": review_questions,
        "countable_condition_count": len(countable_conditions),
        "countable_conditions": countable_conditions,
        "implemented_ai_signals": readiness["implemented_signal_count"],
        "partial_ai_signals": readiness["partial_signal_count"],
        "not_claimed_ai_signals": readiness["not_claimed_signal_count"],
        "template_checks": {
            "has_permission_checkbox": "You may count this public issue" in template_text,
            "has_not_count_checkbox": "Do not count this issue publicly" in template_text,
            "asks_strongest_signal": "What was strongest?" in template_text,
            "asks_missing_signal": "What was not credible enough yet?" in template_text,
            "mentions_tool_calling": "LLM tool calling" in template_text,
        },
        "current_counts": {
            "accepted_ai_engineer_reviews": 0,
            "external_ai_feedback_items": 0,
        },
        "resume_status": "review_intake_ready_not_claimable",
        "resume_safe_summary": (
            "Published an AI Engineer review intake path with 6 review paths, 6 reviewer questions, "
            "5 countable-evidence conditions, and an explicit zero-review baseline."
        ),
        "not_claimed": [
            "AI Engineer reviewers have not submitted accepted public feedback yet.",
            "No external AI Engineer feedback count is claimed yet.",
            "No production AI deployment is claimed.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    paths = "\n".join(f"- {key.replace('_', ' ').title()}: [{url}]({url})" for key, url in payload["review_paths"].items())
    questions = "\n".join(f"{index}. {question}" for index, question in enumerate(payload["review_questions"], 1))
    conditions = "\n".join(f"- {condition}" for condition in payload["countable_conditions"])
    checks = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["template_checks"].items())
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_counts"].items())
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# AI Engineer Review Intake

This generated artifact gives external reviewers a focused way to judge whether the project demonstrates AI Engineer Intern readiness.

## Purpose

{payload["purpose"]}

## Review Paths

{paths}

## Review Questions

{questions}

## Countable Evidence Conditions

{conditions}

## Template Checks

| Check | Passed |
| --- | --- |
{checks}

## Current Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_ai_engineer_review_intake(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["review_path_count"] != 6:
        raise AssertionError("AI Engineer review intake must expose 6 review paths")
    if payload["review_question_count"] != 6:
        raise AssertionError("AI Engineer review intake must define 6 review questions")
    if payload["countable_condition_count"] != 5:
        raise AssertionError("AI Engineer review intake must define 5 countable conditions")
    if not all(payload["template_checks"].values()):
        raise AssertionError("AI Engineer review template is missing required fields")
    if payload["implemented_ai_signals"] != 8:
        raise AssertionError("AI Engineer review intake must reflect 8 implemented AI signals")
    if payload["current_counts"] != {"accepted_ai_engineer_reviews": 0, "external_ai_feedback_items": 0}:
        raise AssertionError("AI Engineer review intake must preserve zero review baseline")
    if payload["resume_status"] != "review_intake_ready_not_claimable":
        raise AssertionError("AI Engineer review intake must not be claimable as feedback yet")
    joined = json.dumps(payload, sort_keys=True).lower()
    required_groups = [
        ("tool calling", "tool-calling"),
        ("structured",),
        ("guardrails",),
        ("permission",),
        ("non-owner",),
    ]
    for group in required_groups:
        if not any(required in joined for required in group):
            raise AssertionError(f"AI Engineer review intake missing required concept: {group[0]}")
    for forbidden in ("submitted accepted public feedback", "external ai engineer feedback count is claimed"):
        if forbidden not in joined:
            raise AssertionError(f"AI Engineer review intake must block claim: {forbidden}")
    return {
        "ai_engineer_review_intake_verified": True,
        "review_path_count": payload["review_path_count"],
        "review_question_count": payload["review_question_count"],
        "countable_condition_count": payload["countable_condition_count"],
    }


def main() -> None:
    payload = build_ai_engineer_review_intake()
    verify_ai_engineer_review_intake(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
