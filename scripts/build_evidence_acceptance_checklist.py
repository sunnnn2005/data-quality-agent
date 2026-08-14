import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCOREBOARD_PATH = ROOT / "docs" / "resume-outcome-scoreboard.json"
QUICKSTART_ROUTER_PATH = ROOT / "docs" / "reviewer-quickstart-router.json"
EVIDENCE_GATE_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "evidence-acceptance-checklist.json"
OUTPUT_MD_PATH = ROOT / "docs" / "evidence-acceptance-checklist.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_evidence_acceptance_checklist() -> dict[str, Any]:
    scoreboard = load_json(SCOREBOARD_PATH)
    router = load_json(QUICKSTART_ROUTER_PATH)
    gate = load_json(EVIDENCE_GATE_PATH)
    route_by_metric = {route["target_metric"]: route for route in router["routes"]}
    blocked_by_metric = {item["metric"]: item for item in scoreboard["blocked_outcomes"]}

    acceptance_items = []
    for metric in (
        "ai_engineer_review_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "external_feedback_items",
        "github_stars",
    ):
        blocked = blocked_by_metric[metric]
        route = route_by_metric.get(metric)
        if metric == "github_stars":
            required_fields = [
                "public GitHub star count reaches threshold",
                "docs/adoption-metrics.json records the same public count",
                "no paid, traded, or fake engagement",
            ]
            submission_url = "https://github.com/sunnnn2005/data-quality-agent/stargazers"
            review_path = "https://github.com/sunnnn2005/data-quality-agent"
            reviewer_situation = "Someone genuinely finds the repo useful enough to star it"
        else:
            required_fields = route["evidence_to_collect"]
            submission_url = route["submission_url"]
            review_path = route["review_path"]
            reviewer_situation = route["label"]
        acceptance_items.append(
            {
                "metric": metric,
                "current_count": blocked["current_count"],
                "required_count": blocked["required_count"],
                "remaining_to_threshold": blocked["remaining_to_threshold"],
                "reviewer_situation": reviewer_situation,
                "review_path": review_path,
                "submission_url": submission_url,
                "required_fields": required_fields,
                "evidence_gate": blocked["evidence_gate"],
                "future_resume_line": blocked["future_resume_line"],
                "status": "blocked_until_public_evidence",
            }
        )

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_evidence_acceptance_checklist.py",
        "purpose": (
            "Turn every blocked resume outcome into a concrete acceptance checklist, so stronger claims are "
            "added only after public, non-owner, permissioned, redacted evidence exists."
        ),
        "acceptance_item_count": len(acceptance_items),
        "accepted_issue_count": gate["accepted_issue_count"],
        "rejected_issue_count": gate["rejected_issue_count"],
        "current_public_counts": scoreboard["current_public_counts"],
        "acceptance_items": acceptance_items,
        "manual_counting_rule": router["manual_counting_rule"],
        "resume_safe_summary": (
            "Published an evidence acceptance checklist mapping 6 blocked resume outcome metrics to required "
            "public fields, submission URLs, evidence gates, and future resume lines while preserving zero "
            "accepted external evidence."
        ),
        "not_claimed": scoreboard["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary_rows = "\n".join(
        "| `{metric}` | {current_count} | {required_count} | {remaining_to_threshold} | `{status}` |".format(**item)
        for item in payload["acceptance_items"]
    )
    detail_sections = "\n\n".join(
        "### `{metric}`\n\n".format(**item)
        + f"- Reviewer situation: {item['reviewer_situation']}\n"
        + f"- Review path: [{item['review_path']}]({item['review_path']})\n"
        + f"- Submit evidence: [{item['submission_url']}]({item['submission_url']})\n"
        + f"- Evidence gate: {item['evidence_gate']}\n"
        + f"- Future resume line: {item['future_resume_line']}\n\n"
        + "Required fields:\n"
        + "\n".join(f"- {field}" for field in item["required_fields"])
        for item in payload["acceptance_items"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    count_rows = "\n".join(
        f"| `{metric}` | {count} |" for metric, count in sorted(payload["current_public_counts"].items())
    )
    return f"""# Evidence Acceptance Checklist

This generated checklist defines what evidence is required before stronger resume outcome claims can be made.

## Purpose

{payload["purpose"]}

## Current Gate Status

| Metric | Value |
| --- | ---: |
| Accepted public reviewer issues | {payload["accepted_issue_count"]} |
| Rejected/planning issues | {payload["rejected_issue_count"]} |
| Acceptance checklist items | {payload["acceptance_item_count"]} |

No accepted external reviewer issue exists yet.

## Blocked Outcome Checklist

| Metric | Current | Required | Remaining | Status |
| --- | ---: | ---: | ---: | --- |
{summary_rows}

## Acceptance Details

{detail_sections}

## Current Public Counts

| Metric | Count |
| --- | ---: |
{count_rows}

## Manual Counting Rule

{payload["manual_counting_rule"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_evidence_acceptance_checklist(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["acceptance_item_count"] != 6:
        raise AssertionError("evidence acceptance checklist must track six blocked outcome metrics")
    if payload["accepted_issue_count"] != 0:
        raise AssertionError("evidence acceptance checklist must preserve zero accepted external evidence")
    required_metrics = {
        "ai_engineer_review_items",
        "business_case_feedback_items",
        "confirmed_external_users",
        "external_feedback_items",
        "github_stars",
        "reproducible_feedback_items",
    }
    actual_metrics = {item["metric"] for item in payload["acceptance_items"]}
    if actual_metrics != required_metrics:
        raise AssertionError("evidence acceptance checklist must cover every blocked outcome metric")
    for item in payload["acceptance_items"]:
        if item["current_count"] != 0:
            raise AssertionError(f"{item['metric']} must stay at zero until public evidence is accepted")
        if item["status"] != "blocked_until_public_evidence":
            raise AssertionError(f"{item['metric']} must be blocked until evidence exists")
        if not item["submission_url"].startswith("https://"):
            raise AssertionError(f"{item['metric']} must include a public submission URL")
        if len(item["required_fields"]) < 3:
            raise AssertionError(f"{item['metric']} must include at least three required evidence fields")
        if "future_resume_line" not in item or not item["future_resume_line"]:
            raise AssertionError(f"{item['metric']} must include future resume wording")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in (
        "public",
        "non-owner",
        "permission",
        "redacted",
        "zero accepted external evidence",
        "no paid, traded, or fake engagement",
    ):
        if phrase not in joined:
            raise AssertionError(f"evidence acceptance checklist missing safety phrase: {phrase}")
    return {
        "evidence_acceptance_checklist_verified": True,
        "acceptance_item_count": payload["acceptance_item_count"],
        "accepted_issue_count": payload["accepted_issue_count"],
        "blocked_metric_count": len(actual_metrics),
    }


def main() -> None:
    payload = build_evidence_acceptance_checklist()
    verify_evidence_acceptance_checklist(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
