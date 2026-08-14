import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPRINT_CALENDAR_PATH = ROOT / "docs" / "reviewer-outcome-sprint-calendar.json"
OUTREACH_STATUS_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
ACCEPTED_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
CLAIM_UPGRADE_PATH = ROOT / "docs" / "resume-claim-upgrade-ledger.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-outcome-ledger.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-outcome-ledger.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _stage_status(current: int, required: int) -> str:
    if current >= required:
        return "complete"
    if current > 0:
        return "in_progress"
    return "not_started"


def _first_day_by_metric(sprint_calendar: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {card["target_metric"]: card for card in sprint_calendar["day_cards"]}


def _slot_count_by_metric(outreach_status: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for slot in outreach_status["outreach_slots"]:
        counts[slot["counts_toward"]] = counts.get(slot["counts_toward"], 0) + 1
    return counts


def _public_issue_count_by_metric(outreach_status: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for slot in outreach_status["outreach_slots"]:
        if slot["status"] == "public_issue_submitted":
            counts[slot["counts_toward"]] = counts.get(slot["counts_toward"], 0) + 1
    return counts


def _build_outcome_rows(
    sprint_calendar: dict[str, Any],
    outreach_status: dict[str, Any],
    accepted_rollup: dict[str, Any],
    claim_upgrade: dict[str, Any],
) -> list[dict[str, Any]]:
    sprint_by_metric = _first_day_by_metric(sprint_calendar)
    slot_counts = _slot_count_by_metric(outreach_status)
    issue_counts = _public_issue_count_by_metric(outreach_status)
    accepted_counts = accepted_rollup["accepted_counts"]
    claim_rows = [
        row
        for row in claim_upgrade["upgrade_rows"]
        if row["metric"] in sprint_by_metric
    ]
    rows = []
    for row in claim_rows:
        metric = row["metric"]
        sprint = sprint_by_metric[metric]
        accepted_count = accepted_counts.get(metric, 0)
        public_issue_count = issue_counts.get(metric, 0)
        rows.append(
            {
                "metric": metric,
                "label": row["label"],
                "sprint_day": sprint["day"],
                "reviewer_profile": sprint["reviewer_profile"],
                "recommended_channel": sprint["recommended_channel"],
                "submission_url": sprint["submission_url"],
                "candidate_slot_count": slot_counts.get(metric, 0),
                "sent_count": outreach_status["sent_count"],
                "public_issue_submitted_count": public_issue_count,
                "accepted_evidence_count": accepted_count,
                "required_count": row["required_count"],
                "remaining_to_resume_claim": max(row["required_count"] - accepted_count, 0),
                "status": _stage_status(accepted_count, row["required_count"]),
                "resume_claimable_now": row["status"] == "claimable",
                "allowed_resume_wording_after_threshold": row["allowed_resume_wording_after_threshold"],
                "current_resume_wording": row["current_resume_wording"],
                "next_action": (
                    "Run the evidence gate and regenerate resume claim artifacts."
                    if public_issue_count > accepted_count
                    else sprint["sprint_action"]
                ),
                "evidence_gate": row["evidence_gate"],
            }
        )
    return sorted(rows, key=lambda item: item["sprint_day"])


def build_reviewer_outcome_ledger() -> dict[str, Any]:
    sprint_calendar = load_json(SPRINT_CALENDAR_PATH)
    outreach_status = load_json(OUTREACH_STATUS_PATH)
    accepted_rollup = load_json(ACCEPTED_ROLLUP_PATH)
    claim_upgrade = load_json(CLAIM_UPGRADE_PATH)
    rows = _build_outcome_rows(
        sprint_calendar,
        outreach_status,
        accepted_rollup,
        claim_upgrade,
    )
    claimable_rows = [row for row in rows if row["resume_claimable_now"]]
    blocked_rows = [row for row in rows if not row["resume_claimable_now"]]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_outcome_ledger.py",
        "purpose": (
            "Join reviewer outreach, public issue submission, evidence-gate acceptance, and exact resume wording "
            "into one ledger so real outcomes can be counted only after public evidence exists."
        ),
        "input_artifacts": [
            "docs/reviewer-outcome-sprint-calendar.json",
            "docs/reviewer-outreach-status-board.json",
            "docs/accepted-evidence-rollup.json",
            "docs/resume-claim-upgrade-ledger.json",
        ],
        "outcome_row_count": len(rows),
        "claimable_row_count": len(claimable_rows),
        "blocked_row_count": len(blocked_rows),
        "current_sent_count": outreach_status["sent_count"],
        "current_public_issue_submitted_count": outreach_status["public_issue_submitted_count"],
        "current_accepted_evidence_count": accepted_rollup["accepted_issue_count"],
        "next_action_count": sum(1 for row in rows if row["remaining_to_resume_claim"] > 0),
        "outcome_rows": rows,
        "resume_status": "outcome_ledger_ready_not_claimable",
        "not_claimed": [
            "This ledger does not count outreach attempts as users, feedback, business impact, or GitHub stars.",
            "A resume outcome row becomes claimable only after accepted public, non-owner evidence reaches its threshold.",
            "Private replies and self-authored planning issues are excluded from resume outcome counts.",
        ],
        "resume_safe_summary": (
            "Published a reviewer outcome ledger mapping 5 evidence goals to public issue gates, accepted-evidence "
            "thresholds, next actions, and exact future resume wording while preserving 0 claimable external outcomes."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {sprint_day} | `{metric}` | {accepted_evidence_count}/{required_count} | {status} | {resume_claimable_now} | {next_action} |".format(
            **row
        )
        for row in payload["outcome_rows"]
    )
    wording_rows = "\n".join(
        "| {label} | {allowed_resume_wording_after_threshold} | {evidence_gate} |".format(
            **row
        )
        for row in payload["outcome_rows"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Reviewer Outcome Ledger

This generated ledger shows which real reviewer outcomes can become resume-safe claims after public evidence is accepted.

## Summary

| Metric | Value |
| --- | ---: |
| Outcome rows | {payload["outcome_row_count"]} |
| Claimable rows | {payload["claimable_row_count"]} |
| Blocked rows | {payload["blocked_row_count"]} |
| Current sent outreach | {payload["current_sent_count"]} |
| Current public issues submitted | {payload["current_public_issue_submitted_count"]} |
| Current accepted evidence | {payload["current_accepted_evidence_count"]} |
| Next actions | {payload["next_action_count"]} |
| Resume status | `{payload["resume_status"]}` |

## Outcome Rows

| Sprint Day | Metric | Accepted / Required | Status | Resume Claimable Now | Next Action |
| ---: | --- | ---: | --- | --- | --- |
{rows}

## Future Resume Wording

| Outcome | Allowed wording after threshold | Evidence gate |
| --- | --- | --- |
{wording_rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_reviewer_outcome_ledger(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["outcome_row_count"] != 5:
        raise AssertionError("reviewer outcome ledger must track five reviewer evidence goals")
    if payload["claimable_row_count"] != 0:
        raise AssertionError("reviewer outcome ledger must not claim external outcomes before accepted evidence")
    if payload["blocked_row_count"] != 5:
        raise AssertionError("all reviewer outcome rows must be blocked at zero evidence")
    if payload["current_accepted_evidence_count"] != 0:
        raise AssertionError("reviewer outcome ledger must preserve the zero accepted-evidence baseline")
    if payload["current_sent_count"] != 0 or payload["current_public_issue_submitted_count"] != 0:
        raise AssertionError("reviewer outcome ledger must preserve the zero outreach baseline")
    expected_order = [
        "ai_engineer_review_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "external_feedback_items",
    ]
    if [row["metric"] for row in payload["outcome_rows"]] != expected_order:
        raise AssertionError("reviewer outcome ledger must follow the sprint calendar priority order")
    for row in payload["outcome_rows"]:
        if row["resume_claimable_now"]:
            raise AssertionError("zero-evidence rows must not be resume-claimable")
        if not row["submission_url"].startswith("https://github.com/"):
            raise AssertionError("reviewer outcome rows must link public GitHub submission paths")
        if "public" not in row["evidence_gate"].lower():
            raise AssertionError("each outcome row must document a public evidence gate")
    for required in ("outreach attempts", "accepted public", "Private replies"):
        if not any(required in item for item in payload["not_claimed"]):
            raise AssertionError(f"reviewer outcome ledger must preserve not-claimed boundary: {required}")
    return {
        "reviewer_outcome_ledger_verified": True,
        "outcome_row_count": payload["outcome_row_count"],
        "claimable_row_count": payload["claimable_row_count"],
        "blocked_row_count": payload["blocked_row_count"],
    }


def main() -> None:
    payload = build_reviewer_outcome_ledger()
    verify_reviewer_outcome_ledger(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
