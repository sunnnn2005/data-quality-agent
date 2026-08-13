import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
PILOT_REVIEW_TRACKER_PATH = ROOT / "docs" / "pilot-review-tracker.json"
EXTERNAL_REVIEW_EVIDENCE_LEDGER_PATH = ROOT / "docs" / "external-review-evidence-ledger.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "outcome-upgrade-playbook.json"
OUTPUT_MD_PATH = ROOT / "docs" / "outcome-upgrade-playbook.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_outcome_upgrade_playbook() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    tracker = load_json(PILOT_REVIEW_TRACKER_PATH)
    ledger = load_json(EXTERNAL_REVIEW_EVIDENCE_LEDGER_PATH)
    current_counts = {
        "stars": adoption["stars"],
        "forks": adoption["forks"],
        "external_feedback_items": feedback["external_feedback_items"],
        "confirmed_external_users": feedback["confirmed_external_users"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        "business_case_feedback_items": feedback["business_case_feedback_items"],
    }
    upgrade_rules = [
        {
            "id": "first_confirmed_external_run",
            "metric": "confirmed_external_users",
            "current_value": current_counts["confirmed_external_users"],
            "threshold": 1,
            "required_public_evidence": [
                "GitHub issue or review note labeled confirmed-user",
                "A reviewer states they ran the demo or local Docker path",
            ],
            "allowed_resume_claim_after_threshold": "1 external reviewer confirmed running the demo or local repo.",
        },
        {
            "id": "pilot_feedback_signal",
            "metric": "external_feedback_items",
            "current_value": current_counts["external_feedback_items"],
            "threshold": 3,
            "required_public_evidence": [
                "Three GitHub issues created from docs/feedback-log.md or demo feedback prompts",
                "Each issue includes role, path tried, outcome, and improvement request",
            ],
            "allowed_resume_claim_after_threshold": "Collected 3 public pilot feedback items and converted them into prioritized fixes.",
        },
        {
            "id": "reproducible_bug_signal",
            "metric": "reproducible_feedback_items",
            "current_value": current_counts["reproducible_feedback_items"],
            "threshold": 1,
            "required_public_evidence": [
                "GitHub issue labeled bug and reproducible",
                "Issue includes expected result, actual result, environment, and reproduction steps",
            ],
            "allowed_resume_claim_after_threshold": "Converted 1 reproducible reviewer report into an evidence-backed fix backlog.",
        },
        {
            "id": "business_case_signal",
            "metric": "business_case_feedback_items",
            "current_value": current_counts["business_case_feedback_items"],
            "threshold": 1,
            "required_public_evidence": [
                "GitHub issue created from docs/business-case-intake.md",
                "Anonymized schema, quality failure, expected business impact, and reviewer role are provided",
            ],
            "allowed_resume_claim_after_threshold": "Reviewed the agent against 1 anonymized real-world data-quality scenario.",
        },
        {
            "id": "github_interest_signal",
            "metric": "stars",
            "current_value": current_counts["stars"],
            "threshold": 5,
            "required_public_evidence": [
                "GitHub repository public star count reaches at least 5",
                "docs/adoption-metrics.json and public evidence health both show the same count",
            ],
            "allowed_resume_claim_after_threshold": "Reached 5 organic GitHub stars after publishing a reproducible demo.",
        },
    ]
    for rule in upgrade_rules:
        rule["status"] = "claimable" if rule["current_value"] >= rule["threshold"] else "not_claimable_yet"
        rule["remaining_to_threshold"] = max(0, rule["threshold"] - rule["current_value"])

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_outcome_upgrade_playbook.py",
        "purpose": (
            "Define exactly when public adoption, feedback, business-case review, and repository-interest metrics "
            "can upgrade resume wording from baseline engineering evidence to real outcome claims."
        ),
        "current_public_counts": current_counts,
        "upgrade_rule_count": len(upgrade_rules),
        "blocked_upgrade_rule_count": sum(1 for rule in upgrade_rules if rule["status"] == "not_claimable_yet"),
        "upgrade_rules": upgrade_rules,
        "claimable_now": [
            "Public GitHub Pages demo",
            "v0.3.0 release",
            "GHCR container image",
            f"{adoption['test_count']} passing CI tests",
            "16 implemented LLM agent-readiness capabilities",
            "Read-only PostgreSQL and bounded CSV business-data intake",
        ],
        "resume_baseline_wording": (
            "Built a public, containerized LLM data-quality agent with tool-calling, memory-informed planning, "
            "read-only PostgreSQL analysis, structured report guardrails, and CI-verified outcome evidence."
        ),
        "forbidden_until_proven": [
            "external users",
            "customer feedback",
            "enterprise production usage",
            "business impact avoided",
            "revenue saved",
            "GitHub stars beyond the current public count",
        ],
        "evidence_sources": {
            "adoption_metrics": "docs/adoption-metrics.json",
            "feedback_metrics": "docs/feedback-metrics.json",
            "pilot_review_tracker": "docs/pilot-review-tracker.json",
            "external_review_evidence_ledger": "docs/external-review-evidence-ledger.json",
        },
        "linked_planned_reviews": tracker["planned_review_count"],
        "external_review_evidence_entries": ledger["entry_count"],
        "resume_status": "baseline_only",
        "resume_safe_summary": (
            "Published a CI-verified outcome upgrade playbook with 5 threshold-based rules that keep adoption, "
            "feedback, business-case, and repository-interest claims blocked until public evidence exists."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_public_counts"].items()
    )
    rules = "\n".join(
        "| {id} | `{metric}` | {current_value} | {threshold} | `{status}` | {remaining_to_threshold} |".format(**rule)
        for rule in payload["upgrade_rules"]
    )
    claimable = "\n".join(f"- {item}" for item in payload["claimable_now"])
    forbidden = "\n".join(f"- {item}" for item in payload["forbidden_until_proven"])
    sources = "\n".join(f"- `{label}`: `{path}`" for label, path in payload["evidence_sources"].items())
    return f"""# Outcome Upgrade Playbook

This generated playbook defines when the project is allowed to upgrade resume wording from engineering evidence to real outcome claims.

## Purpose

{payload["purpose"]}

## Current Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Upgrade Rules

| Rule | Metric | Current | Threshold | Status | Remaining |
| --- | --- | ---: | ---: | --- | ---: |
{rules}

## Claimable Now

{claimable}

## Baseline Resume Wording

{payload["resume_baseline_wording"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Forbidden Until Proven

{forbidden}

## Evidence Sources

{sources}
"""


def verify_outcome_upgrade_playbook(payload: dict[str, Any]) -> dict[str, Any]:
    expected_counts = {
        "stars": 0,
        "forks": 1,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
        "business_case_feedback_items": 0,
    }
    if payload["current_public_counts"] != expected_counts:
        raise AssertionError("outcome upgrade playbook must preserve current public counts")
    if payload["upgrade_rule_count"] != 5:
        raise AssertionError("outcome upgrade playbook must define five upgrade rules")
    if payload["blocked_upgrade_rule_count"] != 5:
        raise AssertionError("all outcome upgrade rules must remain blocked before public evidence exists")
    if payload["resume_status"] != "baseline_only":
        raise AssertionError("outcome upgrade playbook must preserve baseline-only resume status")
    for rule in payload["upgrade_rules"]:
        if rule["status"] != "not_claimable_yet":
            raise AssertionError(f"rule {rule['id']} must not be claimable yet")
        if rule["current_value"] >= rule["threshold"]:
            raise AssertionError(f"rule {rule['id']} unexpectedly met its threshold")
        if not rule["required_public_evidence"]:
            raise AssertionError(f"rule {rule['id']} must define required public evidence")
    required_rules = {
        "first_confirmed_external_run",
        "pilot_feedback_signal",
        "reproducible_bug_signal",
        "business_case_signal",
        "github_interest_signal",
    }
    if {rule["id"] for rule in payload["upgrade_rules"]} != required_rules:
        raise AssertionError("outcome upgrade playbook has the wrong rule set")
    required_forbidden = {
        "external users",
        "customer feedback",
        "enterprise production usage",
        "GitHub stars beyond the current public count",
    }
    if not required_forbidden.issubset(set(payload["forbidden_until_proven"])):
        raise AssertionError("outcome upgrade playbook missing forbidden outcome language")
    if payload["linked_planned_reviews"] != 3:
        raise AssertionError("outcome upgrade playbook must link to three planned reviews")
    if payload["external_review_evidence_entries"] != 0:
        raise AssertionError("outcome upgrade playbook must preserve zero external review entries")
    return {
        "outcome_upgrade_playbook_verified": True,
        "upgrade_rule_count": payload["upgrade_rule_count"],
        "blocked_upgrade_rule_count": payload["blocked_upgrade_rule_count"],
    }


def main() -> None:
    payload = build_outcome_upgrade_playbook()
    verify_outcome_upgrade_playbook(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
