import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_GATE_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
OUTPUT_MD_PATH = ROOT / "docs" / "accepted-evidence-rollup.md"

METRIC_LABELS = {
    "confirmed_external_users": "confirmed external users",
    "external_feedback_items": "external feedback items",
    "reproducible_feedback_items": "reproducible external runs",
    "business_case_feedback_items": "business-case feedback items",
    "ai_engineer_review_items": "AI Engineer review items",
    "accepted_real_model_runs": "accepted real-model LLM runs",
}

BLOCKED_CLAIMS = {
    "confirmed_external_users": "Cannot claim external users until at least one non-owner reviewer issue passes the evidence gate.",
    "external_feedback_items": "Cannot claim user feedback until at least one accepted reviewer issue includes feedback permission and non-placeholder feedback.",
    "reproducible_feedback_items": "Cannot claim reproducible external runs until a reviewer submits runnable command or URL evidence.",
    "business_case_feedback_items": "Cannot claim real business-case feedback until an anonymized business-case issue passes the gate.",
    "ai_engineer_review_items": "Cannot claim external AI Engineer review feedback until a non-owner reviewer submits inspected-path evidence and permission to count.",
    "accepted_real_model_runs": (
        "Cannot claim accepted real-model LLM runs until a redacted run issue includes model, prompt version, "
        "tool calls, latency, token, cost, retry, verification, and permission evidence."
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _accepted_issue_urls(evaluations: list[dict[str, Any]]) -> list[str]:
    return [item["url"] for item in evaluations if item.get("accepted") and item.get("url")]


def _rejected_issue_summaries(evaluations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "issue_number": item.get("issue_number"),
            "title": item.get("title"),
            "url": item.get("url"),
            "failure_reasons": item.get("failure_reasons", []),
        }
        for item in evaluations
        if not item.get("accepted")
    ]


def _claimable_metrics(accepted_counts: dict[str, int]) -> list[dict[str, Any]]:
    metrics: list[dict[str, Any]] = []
    for metric, label in METRIC_LABELS.items():
        count = accepted_counts.get(metric, 0)
        claimable = count > 0
        metrics.append(
            {
                "metric": metric,
                "label": label,
                "current_count": count,
                "claimable": claimable,
                "resume_wording": (
                    f"Collected {count} public {label} through a gated external review workflow."
                    if claimable
                    else None
                ),
                "missing_reason": None if claimable else BLOCKED_CLAIMS[metric],
            }
        )
    return metrics


def _blocked_outcome_claims(claimable_metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "metric": item["metric"],
            "blocked_claim": item["label"],
            "reason": item["missing_reason"],
        }
        for item in claimable_metrics
        if not item["claimable"]
    ]


def build_accepted_evidence_rollup(gate_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    gate = load_json(EVIDENCE_GATE_PATH) if gate_payload is None else gate_payload
    gate["accepted_counts"] = {metric: gate["accepted_counts"].get(metric, 0) for metric in METRIC_LABELS}
    gate["current_public_counts"] = {metric: gate["current_public_counts"].get(metric, 0) for metric in METRIC_LABELS}
    claimable_metrics = _claimable_metrics(gate["accepted_counts"])
    blocked_claims = _blocked_outcome_claims(claimable_metrics)
    accepted_issue_count = gate["accepted_issue_count"]
    accepted_counts = gate["accepted_counts"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_accepted_evidence_rollup.py",
        "purpose": (
            "Summarize accepted public reviewer evidence into resume-safe outcome metrics while preserving "
            "blocked claims until the external reviewer evidence gate accepts proof."
        ),
        "evaluated_issue_count": gate["evaluated_issue_count"],
        "accepted_issue_count": accepted_issue_count,
        "rejected_issue_count": gate["rejected_issue_count"],
        "accepted_counts": accepted_counts,
        "current_public_counts": gate["current_public_counts"],
        "linked_outreach_queue_count": gate["linked_outreach_queue_count"],
        "claimable_metrics": claimable_metrics,
        "claimable_metric_count": len(claimable_metrics),
        "blocked_outcome_claims": blocked_claims,
        "blocked_outcome_claim_count": len(blocked_claims),
        "accepted_issue_urls": _accepted_issue_urls(gate["evaluations"]),
        "rejected_issue_summaries": _rejected_issue_summaries(gate["evaluations"]),
        "resume_safe_summary": (
            "Published a CI-verified accepted evidence rollup that summarizes "
            f"{accepted_issue_count} accepted reviewer issues, "
            f"{accepted_counts['confirmed_external_users']} confirmed users, "
            f"{accepted_counts['external_feedback_items']} feedback items, "
            f"{accepted_counts['reproducible_feedback_items']} reproducible runs, and "
            f"{accepted_counts['business_case_feedback_items']} business-case feedback items, and "
            f"{accepted_counts['ai_engineer_review_items']} AI Engineer review items, and "
            f"{accepted_counts['accepted_real_model_runs']} accepted real-model LLM runs before stronger "
            "resume outcome claims are allowed."
        ),
        "not_claimed": [
            "No accepted external reviewer issue exists yet."
            if accepted_issue_count == 0
            else "Only accepted external reviewer issues are counted.",
            "No user, feedback, reproducible-run, business-case, AI Engineer review, or real-model outcome is claimable while its accepted count is zero.",
            "No private business data is used as outcome evidence.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    metric_rows = "\n".join(
        "| {label} | {current_count} | {claimable} | {wording} | {missing} |".format(
            label=item["label"],
            current_count=item["current_count"],
            claimable=item["claimable"],
            wording=item["resume_wording"] or "-",
            missing=item["missing_reason"] or "-",
        )
        for item in payload["claimable_metrics"]
    )
    blocked_rows = "\n".join(
        f"| {item['blocked_claim']} | {item['metric']} | {item['reason']} |"
        for item in payload["blocked_outcome_claims"]
    )
    if not blocked_rows:
        blocked_rows = "| - | - | - |"
    accepted_urls = "\n".join(f"- {url}" for url in payload["accepted_issue_urls"]) or "- None yet"
    rejected_rows = "\n".join(
        "| #{issue_number} | [{title}]({url}) | {reasons} |".format(
            issue_number=item["issue_number"],
            title=item["title"],
            url=item["url"],
            reasons=", ".join(item["failure_reasons"]),
        )
        for item in payload["rejected_issue_summaries"]
    )
    if not rejected_rows:
        rejected_rows = "| - | - | - |"
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Accepted Evidence Rollup

This generated rollup turns accepted public reviewer issues into resume-safe outcome metrics.

## Summary

| Metric | Value |
| --- | ---: |
| Evaluated issues | {payload["evaluated_issue_count"]} |
| Accepted issues | {payload["accepted_issue_count"]} |
| Rejected issues | {payload["rejected_issue_count"]} |
| Linked outreach queue | {payload["linked_outreach_queue_count"]} |
| Claimable metrics tracked | {payload["claimable_metric_count"]} |
| Blocked outcome claims | {payload["blocked_outcome_claim_count"]} |

## Claimable Metrics

| Metric | Current Count | Claimable | Resume Wording | Missing Reason |
| --- | ---: | --- | --- | --- |
{metric_rows}

## Blocked Outcome Claims

| Blocked Claim | Metric | Reason |
| --- | --- | --- |
{blocked_rows}

## Accepted Issue URLs

{accepted_urls}

## Rejected Issue Summaries

| Issue | Title | Failure Reasons |
| --- | --- | --- |
{rejected_rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_accepted_evidence_rollup(payload: dict[str, Any]) -> dict[str, Any]:
    expected_zero = {
        "business_case_feedback_items": 0,
        "confirmed_external_users": 0,
        "external_feedback_items": 0,
        "reproducible_feedback_items": 0,
        "ai_engineer_review_items": 0,
        "accepted_real_model_runs": 0,
    }
    if payload["linked_outreach_queue_count"] != 3:
        raise AssertionError("accepted evidence rollup must link the 3 queued reviewer segments")
    if payload["accepted_counts"] != expected_zero:
        raise AssertionError("accepted evidence rollup must preserve zero accepted-count baseline")
    if payload["accepted_issue_count"] != 0:
        raise AssertionError("accepted evidence rollup must not count accepted issues before public proof exists")
    if payload["claimable_metric_count"] != 6:
        raise AssertionError("accepted evidence rollup must track six claimable outcome metrics")
    if payload["blocked_outcome_claim_count"] != 6:
        raise AssertionError("accepted evidence rollup must block all six outcome claims at zero baseline")
    if any(item["claimable"] for item in payload["claimable_metrics"]):
        raise AssertionError("accepted evidence rollup must not mark zero-count metrics as claimable")
    for required in (
        "No accepted external reviewer issue exists yet.",
        "No private business data is used as outcome evidence.",
    ):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"accepted evidence rollup must preserve not-claimed signal: {required}")
    return {
        "accepted_evidence_rollup_verified": True,
        "claimable_metric_count": payload["claimable_metric_count"],
        "blocked_outcome_claim_count": payload["blocked_outcome_claim_count"],
    }


def main() -> None:
    payload = build_accepted_evidence_rollup()
    verify_accepted_evidence_rollup(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
