import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
ACCEPTED_EVIDENCE_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
RESUME_CLAIM_UPGRADE_LEDGER_PATH = ROOT / "docs" / "resume-claim-upgrade-ledger.json"
RESUME_TRACTION_PROOF_PATH = ROOT / "docs" / "resume-traction-proof.json"
REVIEWER_FUNNEL_BOARD_PATH = ROOT / "docs" / "reviewer-funnel-board.json"
AI_ENGINEER_READINESS_PATH = ROOT / "docs" / "ai-engineer-readiness.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-outcome-scoreboard.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-outcome-scoreboard.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_resume_outcome_scoreboard() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    accepted = load_json(ACCEPTED_EVIDENCE_ROLLUP_PATH)
    upgrade = load_json(RESUME_CLAIM_UPGRADE_LEDGER_PATH)
    traction = load_json(RESUME_TRACTION_PROOF_PATH)
    funnel = load_json(REVIEWER_FUNNEL_BOARD_PATH)
    ai_readiness = load_json(AI_ENGINEER_READINESS_PATH)

    unlocked = [
        {
            "label": "Public launch",
            "resume_line": f"Published a public LLM data-quality agent demo with release {adoption['release']['tagName']} and GHCR container packaging.",
            "evidence_url": adoption["public_demo"],
        },
        {
            "label": "CI verification",
            "resume_line": f"Maintained {adoption['test_count']} passing tests covering agent behavior, APIs, evidence gates, and resume-safe metrics.",
            "evidence_url": "https://github.com/sunnnn2005/data-quality-agent/actions",
        },
        {
            "label": "AI Engineer readiness",
            "resume_line": (
                f"Documented {ai_readiness['implemented_signal_count']} implemented AI Engineer signals across tool calling, "
                f"guardrails, structured output, evidence traces, and evaluation."
            ),
            "evidence_url": "https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-readiness.md",
        },
    ]

    next_unlocks = [
        {
            "metric": row["metric"],
            "current_count": row["current_count"],
            "required_count": row["required_count"],
            "remaining_to_threshold": row["remaining_to_threshold"],
            "future_resume_line": row["allowed_resume_wording_after_threshold"],
            "evidence_gate": row["evidence_gate"],
        }
        for row in upgrade["upgrade_rows"]
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_resume_outcome_scoreboard.py",
        "purpose": (
            "Give recruiters and reviewers a single resume outcome scoreboard: what is claimable now, "
            "what is blocked, and which public evidence unlocks stronger user, feedback, business, AI-review, "
            "and GitHub-star claims."
        ),
        "claimable_now_count": len(unlocked),
        "claimable_now": unlocked,
        "blocked_outcome_count": upgrade["blocked_row_count"],
        "blocked_outcomes": next_unlocks,
        "current_public_counts": {
            **accepted["accepted_counts"],
            "github_stars": adoption["stars"],
            "github_forks": adoption["forks"],
        },
        "reviewer_funnel": {
            "funnel_stage_count": funnel["funnel_stage_count"],
            "open_gap_count": funnel["open_gap_count"],
            "remaining_evidence_items": funnel["total_remaining_evidence_items"],
        },
        "traction_baseline": {
            "claimable_now_count": traction["claimable_now_count"],
            "future_claim_count": traction["future_claim_count"],
            "blocked_claim_count": traction["blocked_claim_count"],
        },
        "resume_safe_summary": (
            f"Published a resume outcome scoreboard with {len(unlocked)} currently claimable evidence-backed lines, "
            f"{upgrade['blocked_row_count']} blocked outcome claims, {funnel['total_remaining_evidence_items']} remaining "
            "reviewer evidence items, and zero external-user, feedback, business-validation, AI-review, or star claims."
        ),
        "not_claimed": [
            "external users",
            "external feedback",
            "real business validation",
            "external AI Engineer review",
            "GitHub stars",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    claimable_rows = "\n".join(
        "| {label} | {resume_line} | [evidence]({evidence_url}) |".format(**item)
        for item in payload["claimable_now"]
    )
    blocked_rows = "\n".join(
        "| {metric} | {current_count} | {required_count} | {remaining_to_threshold} | {future_resume_line} | {evidence_gate} |".format(
            **item
        )
        for item in payload["blocked_outcomes"]
    )
    count_rows = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["current_public_counts"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Resume Outcome Scoreboard

{payload["purpose"]}

## Current Counts

| Metric | Value |
| --- | ---: |
| Claimable lines now | {payload["claimable_now_count"]} |
| Blocked outcome claims | {payload["blocked_outcome_count"]} |
| Reviewer funnel stages | {payload["reviewer_funnel"]["funnel_stage_count"]} |
| Open reviewer gaps | {payload["reviewer_funnel"]["open_gap_count"]} |
| Remaining reviewer evidence items | {payload["reviewer_funnel"]["remaining_evidence_items"]} |

## Public Outcome Baseline

| Metric | Current Value |
| --- | ---: |
{count_rows}

## Claimable Now

| Signal | Resume-Safe Line | Evidence |
| --- | --- | --- |
{claimable_rows}

## Locked Until Public Evidence

| Metric | Current | Required | Remaining | Future Resume Line | Evidence Gate |
| --- | ---: | ---: | ---: | --- | --- |
{blocked_rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_resume_outcome_scoreboard(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["claimable_now_count"] != 3:
        raise AssertionError("scoreboard must keep exactly three currently claimable evidence-backed lines")
    if payload["blocked_outcome_count"] != 6:
        raise AssertionError("scoreboard must keep six outcome claims blocked before public evidence")
    if payload["reviewer_funnel"]["remaining_evidence_items"] != 7:
        raise AssertionError("scoreboard must preserve the seven-item reviewer evidence gap")
    for metric in (
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "github_stars",
    ):
        if payload["current_public_counts"][metric] != 0:
            raise AssertionError(f"{metric} must stay zero until public evidence exists")
    if payload["current_public_counts"]["github_forks"] < 0:
        raise AssertionError("github_forks must be non-negative")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("tool calling", "guardrails", "structured output", "evidence traces", "evaluation"):
        if required not in joined:
            raise AssertionError(f"scoreboard must preserve AI Engineer signal: {required}")
    markdown = render_markdown(payload)
    for fragment in ("Claimable Now", "Locked Until Public Evidence", "Not Claimed"):
        if fragment not in markdown:
            raise AssertionError(f"scoreboard markdown missing section: {fragment}")
    return {
        "resume_outcome_scoreboard_verified": True,
        "claimable_now_count": payload["claimable_now_count"],
        "blocked_outcome_count": payload["blocked_outcome_count"],
        "remaining_evidence_items": payload["reviewer_funnel"]["remaining_evidence_items"],
    }


def main() -> None:
    payload = build_resume_outcome_scoreboard()
    verify_resume_outcome_scoreboard(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
