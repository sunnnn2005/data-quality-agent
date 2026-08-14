import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_GATE_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
ACCEPTED_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
CLAIM_MATERIALIZER_PATH = ROOT / "docs" / "resume-claim-materializer.json"
LAUNCH_TRACKER_PATH = ROOT / "docs" / "outcome-launch-day-tracker.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "external-evidence-triage-board.json"
OUTPUT_MD_PATH = ROOT / "docs" / "external-evidence-triage-board.md"


ACTION_RULES = {
    "self-authored issue": "Ask a non-owner reviewer to submit their own public GitHub issue.",
    "contains sensitive-data risk terms": "Remove private values and ask the reviewer to confirm the issue is redacted.",
    "missing no-private-data checkbox": "Ask the reviewer to check the no-private-data confirmation.",
    "missing public external run permission": "Ask the reviewer to add explicit permission to count the public evidence.",
    "missing runnable path tried": "Ask the reviewer to name the exact demo path, command, endpoint, or page they tried.",
    "missing command or URL evidence": "Ask the reviewer to include the command, URL, API route, or public page used.",
    "missing observed result evidence": "Ask the reviewer to include the observed result, finding, or report status.",
    "missing main feedback": "Ask the reviewer to add one concrete sentence of feedback.",
    "missing LLM value comparison inspection": "Ask the reviewer to inspect the LLM value comparison artifact.",
    "real-model run must show at least two selected whitelisted tools": (
        "Capture a redacted real-model run with at least two selected whitelisted tools."
    ),
    "real-model run must include token, cost, latency, retry, and verification telemetry": (
        "Attach model, prompt version, token, cost, latency, retry, and verification evidence."
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _next_actions(failure_reasons: list[str]) -> list[str]:
    actions: list[str] = []
    for reason in failure_reasons:
        action = ACTION_RULES.get(reason)
        if action and action not in actions:
            actions.append(action)
    if not actions:
        actions.append("Review the evidence template and add the missing public proof fields.")
    return actions


def _triage_state(evaluation: dict[str, Any]) -> str:
    if evaluation.get("accepted"):
        return "accepted_claimable"
    reasons = set(evaluation.get("failure_reasons", []))
    if "self-authored issue" in reasons:
        return "rejected_needs_external_reviewer"
    if "contains sensitive-data risk terms" in reasons:
        return "rejected_sensitive_or_unredacted"
    if "missing public external run permission" in reasons:
        return "rejected_missing_permission"
    if "missing no-private-data checkbox" in reasons:
        return "rejected_missing_no_private_data"
    if {"missing runnable path tried", "missing command or URL evidence", "missing observed result evidence"} & reasons:
        return "rejected_missing_runnable_evidence"
    return "rejected_needs_template_completion"


def _triage_issue(evaluation: dict[str, Any]) -> dict[str, Any]:
    return {
        "issue_number": evaluation.get("issue_number"),
        "title": evaluation.get("title"),
        "url": evaluation.get("url"),
        "author": evaluation.get("author"),
        "evidence_type": evaluation.get("evidence_type"),
        "accepted": bool(evaluation.get("accepted")),
        "triage_state": _triage_state(evaluation),
        "counts_toward": evaluation.get("counts_toward", []),
        "rejected_counts_toward": evaluation.get("rejected_counts_toward", []),
        "failure_reasons": evaluation.get("failure_reasons", []),
        "next_actions": _next_actions(evaluation.get("failure_reasons", [])),
        "resume_countable_now": bool(evaluation.get("accepted") and evaluation.get("counts_toward")),
    }


def _waiting_items(launch_tracker: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "queue_slot_id": item["queue_slot_id"],
            "status_board_slot_id": item["status_board_slot_id"],
            "target_metric": item["target_metric"],
            "reviewer_profile": item["reviewer_profile"],
            "submission_url": item["submission_url"],
            "triage_state": "waiting_for_public_issue",
            "resume_countable_now": False,
            "next_action": "Send the reviewer request, then wait for a non-owner public issue to pass the gate.",
        }
        for item in launch_tracker["launch_items"]
    ]


def build_external_evidence_triage_board(
    gate_payload: dict[str, Any] | None = None,
    accepted_payload: dict[str, Any] | None = None,
    materializer_payload: dict[str, Any] | None = None,
    launch_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    gate = load_json(EVIDENCE_GATE_PATH) if gate_payload is None else gate_payload
    accepted = load_json(ACCEPTED_ROLLUP_PATH) if accepted_payload is None else accepted_payload
    materializer = load_json(CLAIM_MATERIALIZER_PATH) if materializer_payload is None else materializer_payload
    launch = load_json(LAUNCH_TRACKER_PATH) if launch_payload is None else launch_payload

    triage_items = [_triage_issue(item) for item in gate["evaluations"]]
    state_counts = Counter(item["triage_state"] for item in triage_items)
    failure_counts = Counter(reason for item in triage_items for reason in item["failure_reasons"])
    waiting_items = _waiting_items(launch)
    claimable_resume_lines = [
        item for item in accepted["claimable_metrics"] if item.get("claimable") and item.get("resume_wording")
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_external_evidence_triage_board.py",
        "purpose": (
            "Turn public reviewer issues and launch-day reviewer slots into a resume-claim decision board that "
            "separates accepted outcome evidence from blocked, self-authored, incomplete, or waiting evidence."
        ),
        "evaluated_issue_count": gate["evaluated_issue_count"],
        "accepted_issue_count": gate["accepted_issue_count"],
        "rejected_issue_count": gate["rejected_issue_count"],
        "waiting_reviewer_issue_count": len(waiting_items),
        "claimable_resume_outcome_count": len(claimable_resume_lines),
        "blocked_outcome_claim_count": accepted["blocked_outcome_claim_count"],
        "safe_current_bullet_count": materializer["safe_current_bullet_count"],
        "accepted_counts": accepted["accepted_counts"],
        "triage_state_counts": dict(sorted(state_counts.items())),
        "top_failure_reasons": [
            {"reason": reason, "count": count} for reason, count in failure_counts.most_common(8)
        ],
        "triage_items": triage_items,
        "waiting_reviewer_items": waiting_items,
        "claimable_resume_lines": claimable_resume_lines,
        "resume_safe_summary": (
            "Published an external evidence triage board across "
            f"{gate['evaluated_issue_count']} evaluated public issues, "
            f"{gate['accepted_issue_count']} accepted evidence items, "
            f"{gate['rejected_issue_count']} rejected issue checks, "
            f"{len(waiting_items)} waiting reviewer sends, and "
            f"{len(claimable_resume_lines)} claimable external-outcome resume lines."
        ),
        "not_claimed": [
            "No external users, feedback, business impact, production deployment, or GitHub stars are claimed.",
            "Self-authored issues do not count as external evidence.",
            "Private replies do not count until a public redacted GitHub issue passes the evidence gate.",
            "Outreach and waiting reviewer slots are not counted as usage or feedback.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary_rows = [
        ("Evaluated issues", payload["evaluated_issue_count"]),
        ("Accepted issues", payload["accepted_issue_count"]),
        ("Rejected issues", payload["rejected_issue_count"]),
        ("Waiting reviewer issues", payload["waiting_reviewer_issue_count"]),
        ("Claimable external outcome resume lines", payload["claimable_resume_outcome_count"]),
        ("Blocked outcome claims", payload["blocked_outcome_claim_count"]),
        ("Safe current bullets", payload["safe_current_bullet_count"]),
    ]
    state_rows = "\n".join(
        f"| `{state}` | {count} |" for state, count in payload["triage_state_counts"].items()
    ) or "| - | 0 |"
    failure_rows = "\n".join(
        f"| {item['reason']} | {item['count']} |" for item in payload["top_failure_reasons"]
    ) or "| - | 0 |"
    triage_rows = "\n".join(
        "| #{issue} | [{title}]({url}) | `{state}` | {countable} | {actions} |".format(
            issue=item["issue_number"],
            title=item["title"],
            url=item["url"],
            state=item["triage_state"],
            countable=item["resume_countable_now"],
            actions="; ".join(item["next_actions"]),
        )
        for item in payload["triage_items"]
    ) or "| - | - | - | - | - |"
    waiting_rows = "\n".join(
        "| {slot} | `{metric}` | {profile} | [{url}]({url}) | {action} |".format(
            slot=item["queue_slot_id"],
            metric=item["target_metric"],
            profile=item["reviewer_profile"],
            url=item["submission_url"],
            action=item["next_action"],
        )
        for item in payload["waiting_reviewer_items"]
    ) or "| - | - | - | - | - |"
    claim_lines = "\n".join(
        f"- {item['resume_wording']}" for item in payload["claimable_resume_lines"]
    ) or "- None yet"
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    summary_table = "\n".join(f"| {label} | {value} |" for label, value in summary_rows)

    return f"""# External Evidence Triage Board

This generated board decides whether public reviewer evidence is resume-countable now, blocked, or still waiting.

## Summary

| Metric | Value |
| --- | ---: |
{summary_table}

## Triage State Counts

| State | Count |
| --- | ---: |
{state_rows}

## Top Failure Reasons

| Failure Reason | Count |
| --- | ---: |
{failure_rows}

## Public Issue Triage

| Issue | Title | State | Resume Countable Now | Next Actions |
| --- | --- | --- | --- | --- |
{triage_rows}

## Waiting Reviewer Items

| Slot | Target Metric | Reviewer Profile | Submission URL | Next Action |
| --- | --- | --- | --- | --- |
{waiting_rows}

## Claimable Resume Lines

{claim_lines}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_external_evidence_triage_board(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["evaluated_issue_count"] != 15:
        raise AssertionError("triage board must cover the 15 currently evaluated public issues")
    if payload["accepted_issue_count"] != 0:
        raise AssertionError("triage board must preserve zero accepted evidence at baseline")
    if payload["claimable_resume_outcome_count"] != 0:
        raise AssertionError("triage board must not create external outcome resume lines at zero baseline")
    if payload["waiting_reviewer_issue_count"] != 5:
        raise AssertionError("triage board must keep the first five waiting reviewer sends visible")
    if payload["blocked_outcome_claim_count"] != 6:
        raise AssertionError("triage board must keep all six outcome claims blocked at baseline")
    if payload["triage_state_counts"].get("rejected_needs_external_reviewer", 0) < 1:
        raise AssertionError("triage board must identify self-authored issues as needing external reviewers")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in (
        "resume-claim decision board",
        "self-authored issues do not count",
        "private replies do not count",
        "waiting_for_public_issue",
        "no external users, feedback, business impact, production deployment, or github stars are claimed",
    ):
        if phrase not in joined:
            raise AssertionError(f"triage board missing required evidence phrase: {phrase}")
    return {
        "external_evidence_triage_board_verified": True,
        "evaluated_issue_count": payload["evaluated_issue_count"],
        "waiting_reviewer_issue_count": payload["waiting_reviewer_issue_count"],
        "claimable_resume_outcome_count": payload["claimable_resume_outcome_count"],
    }


def main() -> None:
    payload = build_external_evidence_triage_board()
    verification = verify_external_evidence_triage_board(payload)
    payload["verification"] = verification
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
