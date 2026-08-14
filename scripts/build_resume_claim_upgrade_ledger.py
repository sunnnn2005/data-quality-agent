import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCEPTED_EVIDENCE_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
OUTCOME_COLLECTION_PATH = ROOT / "docs" / "outcome-collection.json"
OUTCOME_UPGRADE_PLAYBOOK_PATH = ROOT / "docs" / "outcome-upgrade-playbook.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-claim-upgrade-ledger.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-claim-upgrade-ledger.md"


UPGRADE_ROWS = [
    {
        "metric": "confirmed_external_users",
        "label": "Confirmed external user",
        "required_count": 1,
        "allowed_resume_wording_after_threshold": (
            "Validated the data-quality LLM agent with 1 external reviewer who ran the public demo or local repo."
        ),
        "evidence_gate": "A non-owner public GitHub issue confirms the path tried and includes permission to count.",
    },
    {
        "metric": "external_feedback_items",
        "label": "External feedback",
        "required_count": 3,
        "allowed_resume_wording_after_threshold": (
            "Collected 3 public reviewer feedback items and converted them into prioritized product fixes."
        ),
        "evidence_gate": "Public feedback issues include role, path tried, outcome, improvement request, and permission.",
    },
    {
        "metric": "reproducible_feedback_items",
        "label": "Reproducible external run or bug",
        "required_count": 1,
        "allowed_resume_wording_after_threshold": (
            "Converted 1 reproducible external run report into an evidence-backed fix backlog."
        ),
        "evidence_gate": "A public issue includes command or URL evidence, expected result, actual result, and environment.",
    },
    {
        "metric": "business_case_feedback_items",
        "label": "Business-case feedback",
        "required_count": 1,
        "allowed_resume_wording_after_threshold": (
            "Reviewed the agent against 1 anonymized real-world data-quality workflow and mapped the resulting risks."
        ),
        "evidence_gate": "A public business-case issue includes anonymized schema, quality failure, impact, and reviewer role.",
    },
    {
        "metric": "ai_engineer_review_items",
        "label": "AI Engineer review",
        "required_count": 1,
        "allowed_resume_wording_after_threshold": (
            "Received external AI Engineer review of the tool-calling loop, guardrails, structured output, and evidence trail."
        ),
        "evidence_gate": "A non-owner public review issue lists inspected paths and grants permission to count.",
    },
    {
        "metric": "github_stars",
        "label": "GitHub stars",
        "required_count": 5,
        "allowed_resume_wording_after_threshold": (
            "Reached 5 organic GitHub stars after publishing a reproducible LLM agent demo and evidence pack."
        ),
        "evidence_gate": "GitHub public star count and docs/adoption-metrics.json both show at least 5 stars.",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_resume_claim_upgrade_ledger() -> dict[str, Any]:
    accepted = load_json(ACCEPTED_EVIDENCE_ROLLUP_PATH)
    adoption = load_json(ADOPTION_METRICS_PATH)
    collection = load_json(OUTCOME_COLLECTION_PATH)
    playbook = load_json(OUTCOME_UPGRADE_PLAYBOOK_PATH)
    accepted_counts = accepted["accepted_counts"]
    current_counts = {
        "confirmed_external_users": accepted_counts["confirmed_external_users"],
        "external_feedback_items": accepted_counts["external_feedback_items"],
        "reproducible_feedback_items": accepted_counts["reproducible_feedback_items"],
        "business_case_feedback_items": accepted_counts["business_case_feedback_items"],
        "ai_engineer_review_items": accepted_counts["ai_engineer_review_items"],
        "github_stars": adoption["stars"],
    }
    rows = []
    for row in UPGRADE_ROWS:
        current_count = current_counts[row["metric"]]
        claimable = current_count >= row["required_count"]
        rows.append(
            {
                **row,
                "current_count": current_count,
                "remaining_to_threshold": max(row["required_count"] - current_count, 0),
                "status": "claimable" if claimable else "blocked_until_public_evidence",
                "current_resume_wording": row["allowed_resume_wording_after_threshold"] if claimable else None,
                "not_allowed_until_met": None
                if claimable
                else f"Do not claim {row['label'].lower()} until the evidence gate passes.",
            }
        )

    blocked_rows = [row for row in rows if row["status"] != "claimable"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_resume_claim_upgrade_ledger.py",
        "purpose": (
            "Map real outcome evidence into exact resume-safe wording while blocking users, feedback, "
            "business impact, AI review, and GitHub-star claims until public evidence exists."
        ),
        "input_artifacts": [
            "docs/accepted-evidence-rollup.json",
            "docs/adoption-metrics.json",
            "docs/outcome-collection.json",
            "docs/outcome-upgrade-playbook.json",
        ],
        "current_counts": current_counts,
        "upgrade_row_count": len(rows),
        "claimable_row_count": len(rows) - len(blocked_rows),
        "blocked_row_count": len(blocked_rows),
        "upgrade_rows": rows,
        "evidence_collection_paths": collection["submission_paths"],
        "baseline_claimable_now": playbook["claimable_now"],
        "blocked_resume_phrases": [
            "used by external users",
            "collected customer feedback",
            "solved a real enterprise production issue",
            "received AI Engineer review",
            "earned GitHub stars",
        ],
        "resume_safe_summary": (
            "Published a CI-verified resume claim upgrade ledger mapping 6 outcome metrics to public evidence "
            "gates and exact future resume wording while preserving 0 users, 0 feedback items, 0 AI reviews, "
            "0 business-case reviews, and 0 GitHub stars."
        ),
        "resume_status": "baseline_only_until_public_evidence",
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {label} | {current_count} | {required_count} | {status} | {wording} |".format(
            label=row["label"],
            current_count=row["current_count"],
            required_count=row["required_count"],
            status=row["status"],
            wording=row["current_resume_wording"] or row["allowed_resume_wording_after_threshold"],
        )
        for row in payload["upgrade_rows"]
    )
    blocked = "\n".join(f"- {item}" for item in payload["blocked_resume_phrases"])
    baseline = "\n".join(f"- {item}" for item in payload["baseline_claimable_now"])
    return f"""# Resume Claim Upgrade Ledger

{payload["purpose"]}

## Current Status

- Upgrade rows: {payload["upgrade_row_count"]}
- Claimable outcome rows: {payload["claimable_row_count"]}
- Blocked outcome rows: {payload["blocked_row_count"]}
- Resume status: `{payload["resume_status"]}`

## Upgrade Rows

| Outcome | Current | Required | Status | Allowed wording after threshold |
| --- | ---: | ---: | --- | --- |
{rows}

## Baseline Claimable Now

{baseline}

## Blocked Resume Phrases

{blocked}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_resume_claim_upgrade_ledger(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["upgrade_row_count"] != 6:
        raise AssertionError("resume claim upgrade ledger must track 6 outcome metrics")
    if payload["claimable_row_count"] != 0:
        raise AssertionError("no external outcome claim should be claimable while all public counts are zero")
    if payload["blocked_row_count"] != 6:
        raise AssertionError("all outcome rows must remain blocked before public evidence exists")
    if payload["current_counts"]["github_stars"] != 0:
        raise AssertionError("ledger must preserve the current GitHub star baseline")
    for key, value in payload["current_counts"].items():
        if value != 0:
            raise AssertionError(f"{key} must be zero before public evidence exists")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("public evidence", "permission", "evidence gate", "resume-safe"):
        if required not in joined:
            raise AssertionError(f"ledger must mention {required}")
    return {
        "resume_claim_upgrade_ledger_verified": True,
        "upgrade_row_count": payload["upgrade_row_count"],
        "blocked_row_count": payload["blocked_row_count"],
        "claimable_row_count": payload["claimable_row_count"],
    }


def main() -> None:
    payload = build_resume_claim_upgrade_ledger()
    verify_resume_claim_upgrade_ledger(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
