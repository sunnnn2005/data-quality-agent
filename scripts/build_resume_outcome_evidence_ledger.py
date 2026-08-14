import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTREACH_STATUS_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
ACCEPTED_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
APPLICATION_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-outcome-evidence-ledger.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-outcome-evidence-ledger.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_resume_outcome_evidence_ledger() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    outreach_status = load_json(OUTREACH_STATUS_PATH)
    accepted_rollup = load_json(ACCEPTED_ROLLUP_PATH)
    application_pack = load_json(APPLICATION_PACK_PATH)

    claimable_now = [
        {
            "signal": "public_launch",
            "resume_safe_line": "Published a public demo, container image, OpenAPI contract, and CI-verified project evidence pages.",
            "evidence_url": "https://sunnnn2005.github.io/data-quality-agent/",
            "proof_type": "public_url_and_ci",
        },
        {
            "signal": "ci_quality",
            "resume_safe_line": f"Maintained {adoption['test_count']} passing tests across agent behavior, APIs, evidence gates, and safety checks.",
            "evidence_url": "https://github.com/sunnnn2005/data-quality-agent/actions/workflows/test.yml",
            "proof_type": "ci",
        },
        {
            "signal": "agent_implementation",
            "resume_safe_line": (
                "Built an LLM tool-calling data-quality agent with controlled tools, structured reports, "
                "read-only PostgreSQL access, trace persistence, and evidence guardrails."
            ),
            "evidence_url": "https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/agent-readiness.md",
            "proof_type": "source_and_docs",
        },
        {
            "signal": "recruiter_evidence_pack",
            "resume_safe_line": (
                f"Published {len(application_pack['application_links'])} "
                "recruiter-readable evidence links while separating blocked outcome claims from verified work."
            ),
            "evidence_url": "https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/application-evidence-pack.md",
            "proof_type": "generated_artifact",
        },
    ]

    outreach_slots = outreach_status["outreach_slots"]
    in_pipeline = [
        {
            "pipeline_stage": "reviewer_outreach",
            "current_count": outreach_status["recorded_event_count"],
            "sent_count": outreach_status["sent_count"],
            "reply_count": outreach_status["reply_count"],
            "public_issue_submitted_count": outreach_status["public_issue_submitted_count"],
            "resume_countable": False,
            "why_not_claimable": "Outreach is not a resume outcome until public non-owner evidence passes the gate.",
            "next_action": "Send the first real reviewer message, then record it with scripts/record_reviewer_outreach_event.py.",
        },
        {
            "pipeline_stage": "accepted_public_evidence",
            "current_count": accepted_rollup["accepted_issue_count"],
            "resume_countable": False,
            "why_not_claimable": "No public reviewer issue has passed the evidence gate yet.",
            "next_action": "Ask reviewers to submit redacted GitHub issues with permission to count.",
        },
    ]

    blocked_until_evidence = []
    for metric in accepted_rollup["claimable_metrics"]:
        blocked_until_evidence.append(
            {
                "metric": metric["metric"],
                "current_count": metric["current_count"],
                "target_resume_claim": metric["label"],
                "blocked_reason": metric["missing_reason"],
                "required_public_evidence": (
                    "Non-owner public GitHub issue with inspected path or run evidence, no private data, "
                    "explicit permission to count, and accepted evidence-gate status."
                ),
            }
        )

    public_counts = {
        "stars": adoption["stars"],
        "forks": adoption["forks"],
        "watchers": adoption["watchers"],
        "confirmed_external_users": feedback["confirmed_external_users"],
        "external_feedback_items": feedback["external_feedback_items"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        "ai_engineer_review_items": feedback.get("ai_engineer_review_items", 0),
        "business_case_feedback_items": feedback.get("business_case_feedback_items", 0),
    }

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_resume_outcome_evidence_ledger.py",
        "purpose": (
            "Keep resume outcome claims honest by separating verified accomplishments, active outcome pipeline "
            "work, and blocked claims that still need public non-owner evidence."
        ),
        "claimable_now_count": len(claimable_now),
        "in_pipeline_count": len(in_pipeline),
        "blocked_until_evidence_count": len(blocked_until_evidence),
        "outreach_slot_count": len(outreach_slots),
        "recorded_outreach_event_count": outreach_status["recorded_event_count"],
        "accepted_public_evidence_count": accepted_rollup["accepted_issue_count"],
        "resume_upgrade_count": 0,
        "public_counts": public_counts,
        "claimable_now": claimable_now,
        "in_pipeline_not_claimable": in_pipeline,
        "blocked_until_evidence": blocked_until_evidence,
        "manual_update_commands": [
            (
                "python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent "
                "--reviewer-contact \"<real reviewer>\" --channel-used LinkedIn"
            ),
            "python scripts/build_external_reviewer_evidence_gate.py",
            "python scripts/build_accepted_evidence_rollup.py",
            "python scripts/build_resume_outcome_evidence_ledger.py",
        ],
        "not_claimed": [
            "No external users are claimed while confirmed_external_users is 0.",
            "No feedback impact is claimed while accepted public feedback is 0.",
            "No AI Engineer review is claimed while accepted AI-review evidence is 0.",
            "No GitHub-star growth is claimed beyond the live public count.",
            "No enterprise production deployment is claimed.",
        ],
        "resume_safe_summary": (
            f"Published a resume outcome evidence ledger with {len(claimable_now)} claimable engineering signals, "
            f"{len(in_pipeline)} active but non-claimable outcome pipeline stages, "
            f"{len(blocked_until_evidence)} blocked outcome claims, {outreach_status['recorded_event_count']} recorded outreach events, "
            f"and {accepted_rollup['accepted_issue_count']} accepted public evidence items."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    claimable_rows = "\n".join(
        f"| {item['signal']} | {item['resume_safe_line']} | [{item['proof_type']}]({item['evidence_url']}) |"
        for item in payload["claimable_now"]
    )
    pipeline_rows = "\n".join(
        f"| {item['pipeline_stage']} | {item['current_count']} | {item['resume_countable']} | {item['why_not_claimable']} | {item['next_action']} |"
        for item in payload["in_pipeline_not_claimable"]
    )
    blocked_rows = "\n".join(
        f"| {item['metric']} | {item['current_count']} | {item['blocked_reason']} |"
        for item in payload["blocked_until_evidence"]
    )
    counts = "\n".join(
        f"| {key.replace('_', ' ')} | {value} |" for key, value in payload["public_counts"].items()
    )
    commands = "\n".join(f"- `{command}`" for command in payload["manual_update_commands"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Resume Outcome Evidence Ledger

This ledger separates what can be used on a resume today from outcome claims that still need public evidence.

## Purpose

{payload["purpose"]}

## Claimable Now

| Signal | Resume-Safe Line | Evidence |
| --- | --- | --- |
{claimable_rows}

## In Pipeline, Not Claimable Yet

| Stage | Current Count | Resume Countable | Why Not Claimable | Next Action |
| --- | ---: | --- | --- | --- |
{pipeline_rows}

## Blocked Until Public Evidence

| Metric | Current Count | Blocked Reason |
| --- | ---: | --- |
{blocked_rows}

## Public Counts

| Metric | Count |
| --- | ---: |
{counts}

## Manual Update Commands

{commands}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_resume_outcome_evidence_ledger(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["claimable_now_count"] != 4:
        raise AssertionError("ledger must expose four claimable engineering signals")
    if payload["in_pipeline_count"] != 2:
        raise AssertionError("ledger must expose two active non-claimable pipeline stages")
    if payload["blocked_until_evidence_count"] != 5:
        raise AssertionError("ledger must preserve five blocked outcome claims")
    if payload["outreach_slot_count"] != 8:
        raise AssertionError("ledger must read the eight reviewer outreach slots")
    if payload["accepted_public_evidence_count"] != 0:
        raise AssertionError("ledger must not claim accepted external evidence yet")
    if payload["resume_upgrade_count"] != 0:
        raise AssertionError("ledger must not upgrade resume outcomes without accepted evidence")
    for key in (
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "ai_engineer_review_items",
        "business_case_feedback_items",
    ):
        if payload["public_counts"][key] != 0:
            raise AssertionError(f"ledger must preserve zero {key}")
    if payload["public_counts"]["stars"] != 0:
        raise AssertionError("ledger must preserve the current zero-star baseline")
    required_commands = " ".join(payload["manual_update_commands"])
    for required in (
        "record_reviewer_outreach_event.py",
        "build_external_reviewer_evidence_gate.py",
        "build_accepted_evidence_rollup.py",
    ):
        if required not in required_commands:
            raise AssertionError(f"ledger missing update command {required}")
    if "enterprise production deployment" not in " ".join(payload["not_claimed"]):
        raise AssertionError("ledger must explicitly avoid production adoption claims")
    return {
        "resume_outcome_evidence_ledger_verified": True,
        "claimable_now_count": payload["claimable_now_count"],
        "blocked_until_evidence_count": payload["blocked_until_evidence_count"],
        "accepted_public_evidence_count": payload["accepted_public_evidence_count"],
    }


def main() -> None:
    payload = build_resume_outcome_evidence_ledger()
    verify_resume_outcome_evidence_ledger(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
