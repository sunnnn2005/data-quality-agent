import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
COMMUNITY_GROWTH_BASELINE_PATH = ROOT / "docs" / "community-growth-baseline.json"
STAR_GROWTH_KIT_PATH = ROOT / "docs" / "star-growth-kit.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "contributor-conversion-kit.json"
OUTPUT_MD_PATH = ROOT / "docs" / "contributor-conversion-kit.md"


REPO_URL = "https://github.com/sunnnn2005/data-quality-agent"
ISSUE_URL = REPO_URL + "/issues/new?template="


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_contributor_conversion_kit() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    community = load_json(COMMUNITY_GROWTH_BASELINE_PATH)
    star_growth = load_json(STAR_GROWTH_KIT_PATH)

    current_public_counts = {
        "stars": adoption["stars"],
        "forks": adoption["forks"],
        "confirmed_external_users": feedback["confirmed_external_users"],
        "external_feedback_items": feedback["external_feedback_items"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        "ai_engineer_review_items": feedback["ai_engineer_review_items"],
        "business_case_feedback_items": feedback["business_case_feedback_items"],
        "feature_feedback_items_excluded_from_external_claims": feedback["feature_feedback_items"],
    }

    conversion_paths = [
        {
            "id": "demo_feedback_review",
            "target_signal": "external_feedback_items",
            "entrypoint_url": ISSUE_URL + "demo_feedback.md",
            "best_reviewer": "classmate, club member, or engineer who can try the public demo",
            "action": "Run the public demo and submit structured feedback with permission to count publicly.",
            "evidence_gate": "public non-owner issue using demo_feedback.md and explicit permission to count",
            "counts_only_after": "The accepted evidence gate increments external_feedback_items.",
            "copy_ready_message": (
                "I published a local-first LLM data-quality agent with a public demo and evidence-backed reports. "
                "Could you spend 8-10 minutes running the demo and leave feedback through this issue form? "
                "Please only grant permission to count the review publicly if you are comfortable with that."
            ),
        },
        {
            "id": "business_data_replay",
            "target_signal": "reproducible_feedback_items",
            "entrypoint_url": ISSUE_URL + "business_data_replay.md",
            "best_reviewer": "data analyst, data engineer, or operations teammate with an anonymized CSV workflow",
            "action": "Replay an anonymized business-shaped CSV or read-only PostgreSQL table through the agent.",
            "evidence_gate": "public non-owner issue using business_data_replay.md with no raw private data",
            "counts_only_after": "The accepted evidence gate confirms a reproducible replay without sensitive data.",
            "copy_ready_message": (
                "I am validating whether this agent is useful on realistic business data. If you have a small "
                "anonymized CSV shape, could you run the replay path and submit what failed, what was useful, "
                "and whether the evidence-backed report matched the workflow?"
            ),
        },
        {
            "id": "ai_engineer_review",
            "target_signal": "ai_engineer_review_items",
            "entrypoint_url": ISSUE_URL + "ai_engineer_review.md",
            "best_reviewer": "AI engineer, ML engineer, or senior CS student familiar with LLM agents",
            "action": "Review tool calling, state loop, guardrails, structured output, traces, and eval evidence.",
            "evidence_gate": "public non-owner issue using ai_engineer_review.md with permission to count",
            "counts_only_after": "The accepted evidence gate confirms an external AI-engineering review.",
            "copy_ready_message": (
                "I am trying to make this project strong enough for AI Engineer internship interviews. Could you "
                "review the LLM tool-calling loop, guardrails, structured output, and eval artifacts, then leave "
                "specific technical feedback through the AI Engineer review issue?"
            ),
        },
        {
            "id": "business_case_review",
            "target_signal": "business_case_feedback_items",
            "entrypoint_url": ISSUE_URL + "business_case_review.md",
            "best_reviewer": "someone who has worked with support, billing, ecommerce, or operations data",
            "action": "Judge whether the detected quality failures and owner handoffs match a realistic business problem.",
            "evidence_gate": "public non-owner issue using business_case_review.md and explicit business-case feedback",
            "counts_only_after": "The accepted evidence gate increments business_case_feedback_items.",
            "copy_ready_message": (
                "Could you review the support-operations case study and tell me whether the data-quality failures, "
                "root-cause hypotheses, and owner handoffs feel realistic for an actual business workflow?"
            ),
        },
        {
            "id": "ethical_star_or_fork",
            "target_signal": "github_stars",
            "entrypoint_url": REPO_URL,
            "best_reviewer": "developer who inspected the repo, demo, tests, or Docker run and genuinely wants to follow it",
            "action": "Star or fork only if the project is useful, credible, or worth revisiting.",
            "evidence_gate": "public GitHub stargazer or fork count; no paid, traded, or fake engagement",
            "counts_only_after": "The public GitHub count changes organically.",
            "copy_ready_message": (
                "If you inspect the repo or demo and genuinely find the project useful, a GitHub star would help "
                "signal public interest. No pressure, and please do not star it unless it is actually useful to you."
            ),
        },
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_contributor_conversion_kit.py",
        "purpose": (
            "Convert public repo visibility into real, resume-safe outcome evidence by routing reviewers through "
            "specific contribution, replay, review, and ethical star paths."
        ),
        "current_public_counts": current_public_counts,
        "conversion_path_count": len(conversion_paths),
        "conversion_paths": conversion_paths,
        "evidence_gate_count": len(conversion_paths),
        "contributor_claimable_count": 0,
        "linked_public_assets": {
            "community_growth_baseline": "docs/community-growth-baseline.md",
            "star_growth_kit": "docs/star-growth-kit.md",
            "public_demo": adoption["public_demo"],
            "repo": adoption["repo"],
            "open_feedback_loop": adoption["open_feedback_loop"],
        },
        "source_cross_checks": {
            "issue_template_count": community["issue_template_count"],
            "public_growth_channel_count": len(community["public_growth_channels"]),
            "topic_readiness": star_growth["topic_readiness"],
            "self_authored_planning_excluded": feedback["self_authored_planning_excluded"],
        },
        "counts_only_after": [
            "public non-owner issue",
            "explicit permission to count publicly",
            "accepted evidence gate",
            "public GitHub star or fork count",
            "no private business data or secrets",
        ],
        "resume_safe_summary": (
            "Published a contributor conversion kit with 5 public contributor paths, 5 evidence gates, "
            "0 contributor-claimable outcomes, and explicit rules for turning reviews, replays, AI-engineering "
            "feedback, and organic GitHub stars into future resume-safe metrics."
        ),
        "not_claimed": [
            "external contributors",
            "external users",
            "customer feedback",
            "production adoption",
            "GitHub stars beyond the current public count",
            "business impact validated by a company",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_public_counts"].items()
    )
    rows = "\n".join(
        "| {id} | {target_signal} | {best_reviewer} | [open]({entrypoint_url}) | {evidence_gate} |".format(**item)
        for item in payload["conversion_paths"]
    )
    messages = "\n\n".join(
        "### {id}\n\nCounts only after: {counts_only_after}\n\n```text\n{copy_ready_message}\n```".format(**item)
        for item in payload["conversion_paths"]
    )
    rules = "\n".join(f"- {item}" for item in payload["counts_only_after"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Contributor Conversion Kit

{payload["purpose"]}

## Current Public Counts

| Metric | Value |
| --- | ---: |
{counts}

## Conversion Paths

| Path | Target Signal | Best Reviewer | Entrypoint | Evidence Gate |
| --- | --- | --- | --- | --- |
{rows}

## Copy-Ready Asks

{messages}

## Counting Rules

{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_contributor_conversion_kit(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["conversion_path_count"] != 5:
        raise AssertionError("contributor conversion kit must expose exactly five conversion paths")
    if payload["evidence_gate_count"] != 5:
        raise AssertionError("each conversion path must have an evidence gate")
    if payload["contributor_claimable_count"] != 0:
        raise AssertionError("contributor outcomes must remain unclaimed until public evidence exists")
    counts = payload["current_public_counts"]
    if counts["stars"] != 0:
        raise AssertionError("current public star count must stay honest")
    if counts["confirmed_external_users"] != 0 or counts["external_feedback_items"] != 0:
        raise AssertionError("external users and feedback must not be claimed yet")

    required_path_ids = {
        "demo_feedback_review",
        "business_data_replay",
        "ai_engineer_review",
        "business_case_review",
        "ethical_star_or_fork",
    }
    actual_path_ids = {item["id"] for item in payload["conversion_paths"]}
    if actual_path_ids != required_path_ids:
        raise AssertionError("contributor conversion kit must preserve all required conversion paths")

    for item in payload["conversion_paths"]:
        if item["id"] != "ethical_star_or_fork" and "issues/new?template=" not in item["entrypoint_url"]:
            raise AssertionError("non-star conversion paths must route through issue templates")
        if "public" not in item["evidence_gate"].lower():
            raise AssertionError("each evidence gate must require public evidence")
        if not item["copy_ready_message"]:
            raise AssertionError("each conversion path needs a copy-ready ask")

    for phrase in ("public non-owner issue", "explicit permission", "accepted evidence gate", "public GitHub"):
        if phrase not in " ".join(payload["counts_only_after"]):
            raise AssertionError(f"counting rules missing: {phrase}")
    summary = payload["resume_safe_summary"]
    for phrase in ("5 public contributor paths", "0 contributor-claimable outcomes", "organic GitHub stars"):
        if phrase not in summary:
            raise AssertionError(f"resume-safe summary missing: {phrase}")
    for required in ("external users", "customer feedback", "production adoption", "GitHub stars beyond"):
        if not any(required in item for item in payload["not_claimed"]):
            raise AssertionError(f"not_claimed missing: {required}")

    markdown = render_markdown(payload)
    for section in ("Conversion Paths", "Copy-Ready Asks", "Counting Rules", "Not Claimed"):
        if section not in markdown:
            raise AssertionError(f"markdown missing section: {section}")

    return {
        "contributor_conversion_kit_verified": True,
        "conversion_path_count": payload["conversion_path_count"],
        "contributor_claimable_count": payload["contributor_claimable_count"],
    }


def main() -> None:
    payload = build_contributor_conversion_kit()
    verify_contributor_conversion_kit(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
