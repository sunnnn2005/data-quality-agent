import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "evidence-gap-diagnostics.json"
OUTPUT_MD_PATH = ROOT / "docs" / "evidence-gap-diagnostics.md"


REVIEWER_FIX_CHECKLISTS = {
    "external_run_review": [
        "Use a non-owner GitHub account.",
        "Check the no-private-data permission box.",
        "Check the public external run permission box.",
        "Select a runnable path such as public demo, GHCR container, or Docker Compose replay.",
        "Include non-placeholder commands or URLs used.",
        "Include observed result and main feedback.",
    ],
    "business_data_replay": [
        "Use a non-owner GitHub account.",
        "Confirm no customer names, emails, addresses, tokens, secrets, or raw production rows.",
        "Grant permission to count the anonymized replay and external feedback.",
        "Select CSV upload, read-only PostgreSQL, or Docker Compose replay path.",
        "Include data source type, dataset shape, agent run summary, and catch-or-miss notes.",
    ],
    "business_case_review": [
        "Use a non-owner GitHub account.",
        "Grant anonymized business-case and business-impact counting permission.",
        "Describe business context, data-quality problem, business impact, fields involved, and project evidence mapping.",
        "Keep organization names, customer names, raw rows, and sensitive identifiers out of the issue.",
    ],
    "ai_engineer_review": [
        "Use a non-owner GitHub account.",
        "Confirm no private business data, secrets, customer names, emails, addresses, or raw production rows.",
        "Grant permission to count the issue as external AI Engineer project feedback.",
        "Include inspected paths or commands.",
        "Include strongest AI Engineer signals and missing or weak signals.",
    ],
    "unknown": [
        "Apply one tracked evidence label.",
        "Use the matching issue template instead of a free-form issue.",
        "Include explicit permission to count and no-private-data confirmation.",
    ],
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _reason_counts(evaluations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for item in evaluations:
        if item.get("accepted"):
            continue
        counter.update(item.get("failure_reasons", []))
    return [{"reason": reason, "count": count} for reason, count in counter.most_common()]


def _evidence_type_gaps(evaluations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in evaluations:
        grouped[item.get("evidence_type", "unknown")].append(item)

    rows = []
    for evidence_type in sorted(grouped):
        items = grouped[evidence_type]
        rejected = [item for item in items if not item.get("accepted")]
        reasons = Counter(reason for item in rejected for reason in item.get("failure_reasons", []))
        rows.append(
            {
                "evidence_type": evidence_type,
                "evaluated_issue_count": len(items),
                "accepted_issue_count": sum(1 for item in items if item.get("accepted")),
                "rejected_issue_count": len(rejected),
                "top_failure_reasons": [
                    {"reason": reason, "count": count} for reason, count in reasons.most_common(5)
                ],
                "next_reviewer_checklist": REVIEWER_FIX_CHECKLISTS.get(
                    evidence_type, REVIEWER_FIX_CHECKLISTS["unknown"]
                ),
            }
        )
    return rows


def _nearest_unlock_paths(gate: dict[str, Any]) -> list[dict[str, Any]]:
    accepted_counts = gate["accepted_counts"]
    return [
        {
            "target_metric": "ai_engineer_review_items",
            "current_count": accepted_counts.get("ai_engineer_review_items", 0),
            "first_unlock_requirement": "One non-owner `ai-engineer-review` issue with inspected paths, no-private-data checkbox, and permission to count.",
            "submission_url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md",
        },
        {
            "target_metric": "confirmed_external_users",
            "current_count": accepted_counts.get("confirmed_external_users", 0),
            "first_unlock_requirement": "One non-owner external run issue with a runnable path, observed result, command or URL evidence, and permission to count.",
            "submission_url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md",
        },
        {
            "target_metric": "business_case_feedback_items",
            "current_count": accepted_counts.get("business_case_feedback_items", 0),
            "first_unlock_requirement": "One anonymized business-case review issue with workflow context, impact, fields, project evidence mapping, and permission to count.",
            "submission_url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md",
        },
    ]


def build_evidence_gap_diagnostics(gate_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    gate = load_json(GATE_PATH) if gate_payload is None else gate_payload
    evaluations = gate.get("evaluations", [])
    rejected = [item for item in evaluations if not item.get("accepted")]
    self_authored_rejections = sum(
        1 for item in rejected if "self-authored issue" in item.get("failure_reasons", [])
    )
    sensitive_risk_rejections = sum(
        1 for item in rejected if "contains sensitive-data risk terms" in item.get("failure_reasons", [])
    )
    payload = {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_evidence_gap_diagnostics.py",
        "purpose": (
            "Diagnose why current public reviewer issues do not yet unlock resume outcome claims and "
            "give the next reviewer the shortest path to countable evidence."
        ),
        "evaluated_issue_count": gate["evaluated_issue_count"],
        "accepted_issue_count": gate["accepted_issue_count"],
        "rejected_issue_count": gate["rejected_issue_count"],
        "accepted_counts": gate["accepted_counts"],
        "self_authored_rejection_count": self_authored_rejections,
        "sensitive_risk_rejection_count": sensitive_risk_rejections,
        "failure_reason_count": len(_reason_counts(evaluations)),
        "top_failure_reasons": _reason_counts(evaluations)[:10],
        "evidence_type_gaps": _evidence_type_gaps(evaluations),
        "nearest_unlock_paths": _nearest_unlock_paths(gate),
        "not_claimed": [
            "No rejected issue is counted as a user, feedback item, reproducible run, business case, or AI Engineer review.",
            "Self-authored planning issues remain excluded from outcome metrics.",
            "Sensitive or private data must be redacted before any public issue can count.",
        ],
        "resume_safe_summary": (
            "Published evidence-gap diagnostics for "
            f"{gate['evaluated_issue_count']} evaluated public issues, "
            f"{gate['accepted_issue_count']} accepted issues, "
            f"{gate['rejected_issue_count']} rejected issues, "
            f"{self_authored_rejections} self-authored rejections, and "
            f"{len(_nearest_unlock_paths(gate))} nearest unlock paths for future resume-safe outcome evidence."
        ),
    }
    verify_evidence_gap_diagnostics(payload)
    return payload


def verify_evidence_gap_diagnostics(payload: dict[str, Any]) -> None:
    if payload["project"] != "Data Quality Agent":
        raise AssertionError("evidence gap diagnostics must identify the project")
    if payload["accepted_issue_count"] != 0:
        raise AssertionError("default diagnostics must not claim accepted public evidence yet")
    if any(value != 0 for value in payload["accepted_counts"].values()):
        raise AssertionError("default diagnostics must preserve zero accepted outcome counts")
    if payload["rejected_issue_count"] <= 0:
        raise AssertionError("default diagnostics should explain current rejected evidence issues")
    if payload["self_authored_rejection_count"] <= 0:
        raise AssertionError("diagnostics must identify self-authored planning issues as non-countable")
    if len(payload["nearest_unlock_paths"]) != 3:
        raise AssertionError("diagnostics must provide three nearest unlock paths")
    joined = json.dumps(payload, sort_keys=True)
    for required in (
        "ai_engineer_review_items",
        "confirmed_external_users",
        "business_case_feedback_items",
        "Self-authored planning issues remain excluded from outcome metrics.",
    ):
        if required not in joined:
            raise AssertionError(f"missing diagnostics requirement: {required}")


def render_markdown(payload: dict[str, Any]) -> str:
    reason_rows = "\n".join(
        f"| {item['reason']} | {item['count']} |" for item in payload["top_failure_reasons"]
    )
    if not reason_rows:
        reason_rows = "| - | 0 |"

    gap_rows = "\n".join(
        "| {evidence_type} | {evaluated_issue_count} | {accepted_issue_count} | {rejected_issue_count} | {checklist} |".format(
            evidence_type=item["evidence_type"],
            evaluated_issue_count=item["evaluated_issue_count"],
            accepted_issue_count=item["accepted_issue_count"],
            rejected_issue_count=item["rejected_issue_count"],
            checklist="<br>".join(item["next_reviewer_checklist"]),
        )
        for item in payload["evidence_type_gaps"]
    )
    if not gap_rows:
        gap_rows = "| - | 0 | 0 | 0 | - |"

    unlock_rows = "\n".join(
        f"| {item['target_metric']} | {item['current_count']} | {item['first_unlock_requirement']} | [submit]({item['submission_url']}) |"
        for item in payload["nearest_unlock_paths"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Evidence Gap Diagnostics

This generated artifact explains why current public reviewer issues are not yet resume-countable.

## Summary

| Metric | Value |
| --- | ---: |
| Evaluated issues | {payload["evaluated_issue_count"]} |
| Accepted issues | {payload["accepted_issue_count"]} |
| Rejected issues | {payload["rejected_issue_count"]} |
| Self-authored rejections | {payload["self_authored_rejection_count"]} |
| Sensitive-risk rejections | {payload["sensitive_risk_rejection_count"]} |
| Failure reason types | {payload["failure_reason_count"]} |

## Top Failure Reasons

| Reason | Count |
| --- | ---: |
{reason_rows}

## Evidence Type Gaps

| Evidence Type | Evaluated | Accepted | Rejected | Next Reviewer Checklist |
| --- | ---: | ---: | ---: | --- |
{gap_rows}

## Nearest Unlock Paths

| Target Metric | Current | First Unlock Requirement | Submission |
| --- | ---: | --- | --- |
{unlock_rows}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def main() -> None:
    payload = build_evidence_gap_diagnostics()
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
