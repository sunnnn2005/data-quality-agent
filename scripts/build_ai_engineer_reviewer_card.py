import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AI_REVIEW_INTAKE_PATH = ROOT / "docs" / "ai-engineer-review-intake.json"
QUICKSTART_ROUTER_PATH = ROOT / "docs" / "reviewer-quickstart-router.json"
OUTCOME_BADGES_PATH = ROOT / "docs" / "outcome-badges.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "ai-engineer-reviewer-card.json"
OUTPUT_MD_PATH = ROOT / "docs" / "ai-engineer-reviewer-card.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_ai_engineer_reviewer_card() -> dict[str, Any]:
    intake = load_json(AI_REVIEW_INTAKE_PATH)
    router = load_json(QUICKSTART_ROUTER_PATH)
    badges = load_json(OUTCOME_BADGES_PATH)
    ai_route = next(route for route in router["routes"] if route["id"] == "ai_engineer_review")
    badge_by_id = {badge["id"]: badge for badge in badges["badges"]}

    inspection_targets = [
        {
            "label": "Agent loop",
            "path": "app/tool_agent.py",
            "reason": "shows LLM-driven tool choice, loop state, and tool-result feedback",
        },
        {
            "label": "LLM boundary",
            "path": "app/llm.py",
            "reason": "shows structured model calls, fallback handling, and output validation boundaries",
        },
        {
            "label": "Tool contracts",
            "path": "app/models.py",
            "reason": "shows structured request and response schemas used by the API and agent",
        },
        {
            "label": "Business data adapter",
            "path": "app/postgres_adapter.py",
            "reason": "shows read-only PostgreSQL access for realistic tabular business data",
        },
        {
            "label": "Evidence verifier",
            "path": "app/verifier.py",
            "reason": "shows deterministic checks that keep LLM conclusions tied to evidence",
        },
        {
            "label": "Evaluation scenarios",
            "path": "evals/scenarios.jsonl",
            "reason": "shows the project is evaluated against repeatable agent behavior cases",
        },
    ]

    commands = [
        {
            "label": "Run tests",
            "command": ".venv/bin/python -m pytest",
            "expected": "191 passing tests before this card is regenerated",
        },
        {
            "label": "Run evidence verifier",
            "command": ".venv/bin/python scripts/verify_outcome_evidence.py",
            "expected": "all resume outcome gates pass without upgrading zero-count claims",
        },
        {
            "label": "Run local demo",
            "command": "docker compose up --build",
            "expected": "FastAPI, dashboard, and seeded PostgreSQL replay are available locally",
        },
    ]

    review_prompts = [
        "Does the model choose tools from evidence, or does the code force a fixed workflow?",
        "Are tool outputs fed back into the agent before the final report is produced?",
        "Are findings, hypotheses, recommendations, evidence, confidence, and limitations separated?",
        "Where would prompt injection, sensitive data, or unsupported claims be blocked?",
        "What one change would make this more credible for an AI Engineer Intern resume?",
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_ai_engineer_reviewer_card.py",
        "purpose": "Give one external AI/ML reviewer a single low-friction card for inspecting the agent and submitting public evidence.",
        "target_metric": "ai_engineer_review_items",
        "current_count": intake["current_counts"]["accepted_ai_engineer_reviews"],
        "review_minutes": 12,
        "inspection_target_count": len(inspection_targets),
        "inspection_targets": inspection_targets,
        "command_count": len(commands),
        "commands": commands,
        "review_prompt_count": len(review_prompts),
        "review_prompts": review_prompts,
        "submit_review_url": ai_route["submission_url"],
        "public_slot_url": router["prioritized_next_send"]["public_issue"],
        "outcome_badge_snapshot": {
            "ci_tests": badge_by_id["ci-tests"]["message"],
            "ai_review": badge_by_id["ai-review"]["message"],
            "confirmed_users": badge_by_id["confirmed-users"]["message"],
            "external_feedback": badge_by_id["external-feedback"]["message"],
        },
        "acceptance_gate": (
            "Counts only after a non-owner public GitHub issue lists inspected paths, includes permission to count, "
            "contains no private data, and passes the external reviewer evidence gate."
        ),
        "resume_status": "review_card_ready_not_claimable",
        "resume_safe_summary": (
            "Published a one-page AI Engineer reviewer card with 6 inspection targets, 3 run commands, "
            "5 review prompts, public submission links, and a zero-review baseline."
        ),
        "not_claimed": [
            "No external AI Engineer review has been accepted yet.",
            "No confirmed external users are claimed.",
            "No production deployment or business adoption is claimed.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    targets = "\n".join(
        f"| {target['label']} | `{target['path']}` | {target['reason']} |"
        for target in payload["inspection_targets"]
    )
    commands = "\n".join(
        f"| {command['label']} | `{command['command']}` | {command['expected']} |"
        for command in payload["commands"]
    )
    prompts = "\n".join(f"{index}. {prompt}" for index, prompt in enumerate(payload["review_prompts"], 1))
    badges = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["outcome_badge_snapshot"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# AI Engineer Reviewer Card

This generated card gives one external AI/ML reviewer the shortest path to inspect the project and leave countable public feedback.

## Purpose

{payload["purpose"]}

## Current Status

| Metric | Value |
| --- | --- |
| Target metric | `{payload["target_metric"]}` |
| Current accepted reviews | {payload["current_count"]} |
| Expected review time | {payload["review_minutes"]} minutes |
| Resume status | `{payload["resume_status"]}` |

## Inspect These First

| Area | Path | Why It Matters |
| --- | --- | --- |
{targets}

## Optional Run Commands

| Step | Command | Expected Result |
| --- | --- | --- |
{commands}

## Review Prompts

{prompts}

## Submit Public Review

- Public slot: [{payload["public_slot_url"]}]({payload["public_slot_url"]})
- Submit review: [{payload["submit_review_url"]}]({payload["submit_review_url"]})

## Outcome Badge Snapshot

| Signal | Current Value |
| --- | --- |
{badges}

## Acceptance Gate

{payload["acceptance_gate"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_ai_engineer_reviewer_card(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["target_metric"] != "ai_engineer_review_items":
        raise AssertionError("reviewer card must target AI Engineer review evidence")
    if payload["current_count"] != 0:
        raise AssertionError("reviewer card must preserve the zero accepted-review baseline")
    if payload["inspection_target_count"] != 6:
        raise AssertionError("reviewer card must expose 6 concrete inspection targets")
    if payload["command_count"] != 3:
        raise AssertionError("reviewer card must expose 3 optional run commands")
    if payload["review_prompt_count"] != 5:
        raise AssertionError("reviewer card must expose 5 focused review prompts")
    if not payload["submit_review_url"].startswith("https://github.com/"):
        raise AssertionError("reviewer card must submit to a public GitHub evidence surface")
    if payload["outcome_badge_snapshot"]["ai_review"] != "0 accepted":
        raise AssertionError("reviewer card must not claim accepted AI reviews")
    required_paths = {"app/tool_agent.py", "app/llm.py", "app/postgres_adapter.py", "app/verifier.py"}
    actual_paths = {target["path"] for target in payload["inspection_targets"]}
    if not required_paths.issubset(actual_paths):
        raise AssertionError("reviewer card is missing core AI-agent inspection paths")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("non-owner public github issue", "permission to count", "no private data"):
        if required not in joined:
            raise AssertionError(f"reviewer card acceptance gate missing: {required}")
    for forbidden in ("no external ai engineer review has been accepted yet", "no confirmed external users are claimed"):
        if forbidden not in joined:
            raise AssertionError(f"reviewer card must block claim: {forbidden}")
    return {
        "ai_engineer_reviewer_card_verified": True,
        "inspection_target_count": payload["inspection_target_count"],
        "command_count": payload["command_count"],
        "review_prompt_count": payload["review_prompt_count"],
    }


def main() -> None:
    payload = build_ai_engineer_reviewer_card()
    verify_ai_engineer_reviewer_card(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
