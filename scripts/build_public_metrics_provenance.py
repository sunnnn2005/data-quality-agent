import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
EXTERNAL_REVIEWER_GATE_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "public-metrics-provenance.json"
OUTPUT_MD_PATH = ROOT / "docs" / "public-metrics-provenance.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_public_metrics_provenance() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    gate = load_json(EXTERNAL_REVIEWER_GATE_PATH)
    accepted_counts = gate["accepted_counts"]

    metrics = [
        public_metric(
            "github_stars",
            adoption["stars"],
            "GitHub public repository count via update_adoption_metrics.py",
            "claimable" if adoption["stars"] > 0 else "baseline_only",
            "May claim the exact public star count only; never imply growth beyond GitHub's public number.",
        ),
        public_metric(
            "github_forks",
            adoption["forks"],
            "GitHub public repository count via update_adoption_metrics.py",
            "claimable",
            "May claim the exact public fork baseline because it is visible on GitHub.",
        ),
        public_metric(
            "passing_tests",
            adoption["test_count"],
            "pytest collection and CI evidence via update_adoption_metrics.py",
            "claimable",
            "May claim passing test count after local and CI verification.",
        ),
        gated_metric(
            "confirmed_external_users",
            feedback["confirmed_external_users"],
            accepted_counts["confirmed_external_users"],
            "Counts only accepted public reviewer issues with explicit permission and non-owner authorship.",
        ),
        gated_metric(
            "external_feedback_items",
            feedback["external_feedback_items"],
            accepted_counts["external_feedback_items"],
            "Counts only accepted public reviewer issues that pass the evidence gate.",
        ),
        gated_metric(
            "business_case_feedback_items",
            feedback["business_case_feedback_items"],
            accepted_counts["business_case_feedback_items"],
            "Counts only accepted anonymized business-case reviews.",
        ),
        gated_metric(
            "ai_engineer_review_items",
            feedback["ai_engineer_review_items"],
            accepted_counts["ai_engineer_review_items"],
            "Counts only accepted AI Engineer review issues with inspected paths and concrete feedback.",
        ),
        {
            "metric": "feature_feedback_items",
            "value": feedback["feature_feedback_items"],
            "evidence_source": "GitHub issue labels via update_feedback_metrics.py",
            "resume_status": "tracking_only",
            "resume_rule": "Feature-request labels are product backlog signal, not user adoption or customer feedback.",
            "counts_match_gate": None,
        },
    ]

    claimable = [item for item in metrics if item["resume_status"] == "claimable"]
    blocked = [item for item in metrics if item["resume_status"] in {"blocked_until_accepted_evidence", "baseline_only"}]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_public_metrics_provenance.py",
        "purpose": "Explain where each public outcome metric comes from and whether it can be used in resume wording.",
        "repo": adoption["repo"],
        "external_reviewer_gate": "docs/external-reviewer-evidence-gate.json",
        "metric_count": len(metrics),
        "claimable_metric_count": len(claimable),
        "blocked_or_baseline_metric_count": len(blocked),
        "metrics": metrics,
        "source_controls": [
            "GitHub public metrics use update_adoption_metrics.py with gh CLI first and GitHub public API fallback.",
            "External users, external feedback, business-case feedback, and AI Engineer reviews are counted only from accepted evidence-gate counts.",
            "Self-authored planning issues and unaccepted labeled issues do not unlock resume outcome claims.",
            "Feature-request labels are tracked separately from user/customer outcome metrics.",
        ],
        "resume_safe_summary": (
            f"Published a public metrics provenance record for {len(metrics)} outcome metrics, showing "
            f"{len(claimable)} currently claimable metrics and evidence-gated zero counts for users, "
            "feedback, business-case validation, and AI Engineer review."
        ),
        "not_claimed": [
            "No external users are claimed while confirmed_external_users is zero.",
            "No external feedback is claimed while external_feedback_items is zero.",
            "No business-case validation is claimed while business_case_feedback_items is zero.",
            "No AI Engineer review is claimed while ai_engineer_review_items is zero.",
            "No GitHub star growth is claimed while github_stars is zero.",
        ],
    }


def public_metric(metric: str, value: int, source: str, status: str, rule: str) -> dict[str, Any]:
    return {
        "metric": metric,
        "value": value,
        "evidence_source": source,
        "resume_status": status,
        "resume_rule": rule,
        "counts_match_gate": None,
    }


def gated_metric(metric: str, value: int, accepted_count: int, rule: str) -> dict[str, Any]:
    return {
        "metric": metric,
        "value": value,
        "accepted_gate_count": accepted_count,
        "evidence_source": "docs/external-reviewer-evidence-gate.json accepted_counts",
        "resume_status": "claimable" if accepted_count > 0 else "blocked_until_accepted_evidence",
        "resume_rule": rule,
        "counts_match_gate": value == accepted_count,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {metric} | {value} | {source} | `{status}` | {rule} |".format(
            metric=item["metric"],
            value=item["value"],
            source=item["evidence_source"],
            status=item["resume_status"],
            rule=item["resume_rule"],
        )
        for item in payload["metrics"]
    )
    controls = "\n".join(f"- {item}" for item in payload["source_controls"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Public Metrics Provenance

This generated artifact explains where public outcome metrics come from and whether each metric is safe for resume wording.

## Summary

| Metric | Value |
| --- | ---: |
| Tracked metrics | {payload["metric_count"]} |
| Claimable metrics | {payload["claimable_metric_count"]} |
| Blocked or baseline metrics | {payload["blocked_or_baseline_metric_count"]} |

## Metric Sources

| Metric | Value | Evidence Source | Resume Status | Rule |
| --- | ---: | --- | --- | --- |
{rows}

## Source Controls

{controls}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_public_metrics_provenance(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["metric_count"] != 8:
        raise AssertionError("public metrics provenance must track eight public outcome metrics")
    metrics = {item["metric"]: item for item in payload["metrics"]}
    for required in (
        "github_stars",
        "github_forks",
        "passing_tests",
        "confirmed_external_users",
        "external_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "feature_feedback_items",
    ):
        if required not in metrics:
            raise AssertionError(f"public metrics provenance missing {required}")
    if metrics["github_stars"]["resume_status"] != "baseline_only":
        raise AssertionError("zero GitHub stars must remain a baseline-only metric")
    if metrics["github_forks"]["resume_status"] != "claimable":
        raise AssertionError("public fork count should be claimable as an exact baseline")
    if metrics["passing_tests"]["resume_status"] != "claimable":
        raise AssertionError("passing tests should be claimable after verification")
    for metric in (
        "confirmed_external_users",
        "external_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
    ):
        if metrics[metric]["counts_match_gate"] is not True:
            raise AssertionError(f"{metric} must match accepted evidence-gate counts")
        if metrics[metric]["value"] != 0 or metrics[metric]["resume_status"] != "blocked_until_accepted_evidence":
            raise AssertionError(f"{metric} must stay blocked while accepted count is zero")
    if metrics["feature_feedback_items"]["resume_status"] != "tracking_only":
        raise AssertionError("feature feedback labels must be tracking-only")
    for phrase in ("Self-authored planning issues", "accepted evidence-gate counts", "GitHub public API fallback"):
        if not any(phrase in item for item in payload["source_controls"]):
            raise AssertionError(f"public metrics provenance missing source control: {phrase}")
    if payload["claimable_metric_count"] != 2:
        raise AssertionError("only fork baseline and passing tests should be claimable now")
    return {"public_metrics_provenance_verified": True}


def main() -> None:
    payload = build_public_metrics_provenance()
    verify_public_metrics_provenance(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
