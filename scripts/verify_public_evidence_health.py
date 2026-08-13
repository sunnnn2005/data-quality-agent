import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "public-evidence-health.json"
TIMEOUT_SECONDS = 15


PUBLIC_CHECKS = [
    {
        "id": "public-demo",
        "url": "https://sunnnn2005.github.io/data-quality-agent/",
        "expected_text": "Data Quality Agent",
        "evidence_type": "html",
    },
    {
        "id": "demo-feedback-entrypoints",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/index.html",
        "expected_text": "Try It & Leave Feedback",
        "expected_texts": ["feedback-metrics.json", "bug_report.md", "feature_request.md"],
        "evidence_type": "source",
    },
    {
        "id": "business-impact-artifact",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-impact.json",
        "expected_json": {"issue_category_count": 4, "affected_column_count": 4, "recommended_action_count": 5},
        "evidence_type": "json",
    },
    {
        "id": "outcome-evidence-manifest",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-evidence.json",
        "expected_text": "business-impact-artifact",
        "evidence_type": "json",
    },
    {
        "id": "adoption-metrics",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/adoption-metrics.json",
        "expected_json": {"stars": 0, "forks": 1, "test_count": 93},
        "evidence_type": "json",
    },
    {
        "id": "openapi-contract",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/openapi.json",
        "expected_text": "/business-data/agent-report",
        "expected_texts": ["/datasets/{dataset_id}/memory", "/postgres/support-tickets/agent-report"],
        "evidence_type": "json",
    },
    {
        "id": "eval-summary",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/eval-summary.json",
        "expected_json": {"scenario_count": 3},
        "evidence_type": "json",
    },
    {
        "id": "hypothesis-feedback",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/hypothesis-feedback.json",
        "expected_json": {"label_count": 3, "accepted_count": 2, "needs_review_count": 1},
        "evidence_type": "json",
    },
    {
        "id": "incident-pattern-memory",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/incident-pattern-memory.json",
        "expected_json": {"trace_count": 2, "incident_pattern_count": 3},
        "expected_text": "external production incidents",
        "evidence_type": "json",
    },
    {
        "id": "agent-observability",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-observability.json",
        "expected_json": {"observed_trace_count": 2, "fallback_event_count": 2},
        "expected_text": "production monitoring dashboard",
        "evidence_type": "json",
    },
    {
        "id": "agent-safety-boundaries",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-safety-boundaries.json",
        "expected_json": {"tool_allowlist_count": 7, "postgres_rejected_write_query_count": 3},
        "expected_text": "formal security audit",
        "evidence_type": "json",
    },
    {
        "id": "agent-capability-matrix",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-capability-matrix.json",
        "expected_json": {"tool_count": 7, "implemented_count": 13, "partial_count": 4},
        "expected_text": "enterprise production deployment",
        "expected_texts": ["llm-decision-making", "tool-feedback-loop", "production-adoption"],
        "evidence_type": "json",
    },
    {
        "id": "local-reviewer-demo",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/local-reviewer-demo.json",
        "expected_json": {"project": "Data Quality Agent", "reviewer_command": "docker compose up --build"},
        "expected_text": "readonly_agent",
        "expected_texts": ["support_tickets", "external reviewer completion"],
        "evidence_type": "json",
    },
    {
        "id": "api-smoke-report",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/api-smoke-report.json",
        "expected_json": {"project": "Data Quality Agent", "check_count": 6, "passed_count": 6},
        "expected_text": "production uptime SLA",
        "expected_texts": ["/datasets/orders_daily/quality-report", "/datasets/orders_daily/agent-report"],
        "evidence_type": "json",
    },
    {
        "id": "performance-baseline",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/performance-baseline.json",
        "expected_json": {"project": "Data Quality Agent", "benchmark_count": 2, "passed_count": 2},
        "expected_text": "production latency SLA",
        "expected_texts": ["/datasets/orders_daily/quality-report", "/datasets/orders_daily/profile"],
        "evidence_type": "json",
    },
    {
        "id": "demo-usage-baseline",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/demo-usage-baseline.json",
        "expected_json": {"project": "Data Quality Agent", "release": "v0.3.0"},
        "expected_text": "visitor analytics",
        "expected_texts": ["tracked_usage_funnel", "confirmed_external_users", "star_repository"],
        "evidence_type": "json",
    },
    {
        "id": "community-growth-baseline",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/community-growth-baseline.json",
        "expected_json": {"project": "Data Quality Agent", "issue_template_count": 5, "label_count": 6},
        "expected_text": "external contributors",
        "expected_texts": ["public_growth_channels", "good%20first%20issue", "demo_feedback.md"],
        "evidence_type": "json",
    },
    {
        "id": "impact-review-packet",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/impact-review-packet.json",
        "expected_json": {"project": "Data Quality Agent", "business_metric_count": 12, "evidence_link_count": 8},
        "expected_text": "support-operations data-quality case study",
        "expected_texts": ["production financial impact avoided", "company adoption"],
        "evidence_type": "json",
    },
    {
        "id": "business-problem-casebook",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-problem-casebook.json",
        "expected_json": {"project": "Data Quality Agent", "business_case_count": 1, "detected_risk_count": 4},
        "expected_text": "verified data-quality casebook",
        "expected_texts": ["real customer dataset", "production financial impact avoided"],
        "evidence_type": "json",
    },
    {
        "id": "public-traction-dashboard",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/public-traction-dashboard.json",
        "expected_json": {"project": "Data Quality Agent", "traction_surface_count": 4, "growth_channel_count": 15},
        "expected_text": "not_claimable_yet",
        "expected_texts": ["public_demo", "feedback_issue_template", "GitHub star growth beyond the current public count"],
        "evidence_type": "json",
    },
    {
        "id": "star-growth-kit",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/star-growth-kit.json",
        "expected_json": {"project": "Data Quality Agent", "generated_by": "scripts/build_star_growth_kit.py"},
        "expected_text": "fake or incentivized stars",
        "expected_texts": ["topic_readiness", "ethical_growth_actions", "resume_upgrade_rules"],
        "evidence_type": "json",
    },
    {
        "id": "feedback-intake-quality",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/feedback-intake-quality.json",
        "expected_json": {"project": "Data Quality Agent", "required_section_count": 5, "captured_field_count": 5},
        "expected_text": "CI-verified feedback intake system",
        "expected_texts": ["external users", "survey responses"],
        "evidence_type": "json",
    },
    {
        "id": "business-case-intake",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-case-intake.json",
        "expected_json": {"project": "Data Quality Agent", "required_section_count": 6, "captured_field_count": 6},
        "expected_text": "business-case",
        "expected_texts": ["submitted external business cases", "permission_boundary"],
        "evidence_type": "json",
    },
    {
        "id": "live-project-scorecard",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/live-project-scorecard.json",
        "expected_json": {"release": "v0.3.0"},
        "expected_text": "verified_resume_claims",
        "expected_texts": ["confirmed_external_users", "GitHub stars beyond the current public count"],
        "evidence_type": "json",
    },
    {
        "id": "recruiter-pitch",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/recruiter-pitch.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "AI Engineer Intern",
        "expected_texts": ["honest_baseline", "external users"],
        "evidence_type": "json",
    },
    {
        "id": "application-evidence-pack",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/application-evidence-pack.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "one_line_project_proof",
        "expected_texts": ["application_links", "honest_baseline", "external users"],
        "evidence_type": "json",
    },
    {
        "id": "pilot-outreach-kit",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-outreach-kit.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "outreach_messages",
        "expected_texts": ["success_metrics", "tracking_rules", "external users"],
        "evidence_type": "json",
    },
    {
        "id": "pilot-program-plan",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-program-plan.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "participant_segments",
        "expected_texts": ["success_thresholds", "resume_upgrade_rules", "minimum_feedback_items_before_resume_claim"],
        "evidence_type": "json",
    },
    {
        "id": "pilot-review-tracker",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-review-tracker.json",
        "expected_json": {"project": "Data Quality Agent", "planned_review_count": 3},
        "expected_text": "not_contacted",
        "expected_texts": ["counts_toward_resume", "business_case_feedback_items", "not_claimable_yet"],
        "evidence_type": "json",
    },
    {
        "id": "external-review-evidence-ledger",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/external-review-evidence-ledger.json",
        "expected_json": {"project": "Data Quality Agent", "entry_count": 0, "evidence_requirement_count": 4},
        "expected_text": "not_claimable_yet",
        "expected_texts": ["demo_feedback", "confirmed_run", "business_case_review", "reproducible_bug"],
        "evidence_type": "json",
    },
    {
        "id": "outcome-upgrade-playbook",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-upgrade-playbook.json",
        "expected_json": {"project": "Data Quality Agent", "upgrade_rule_count": 5, "blocked_upgrade_rule_count": 5},
        "expected_text": "baseline_only",
        "expected_texts": ["github_interest_signal", "business_case_signal", "not_claimable_yet"],
        "evidence_type": "json",
    },
    {
        "id": "feedback-metrics",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/feedback-metrics.json",
        "expected_json": {"external_feedback_items": 0, "confirmed_external_users": 0, "reproducible_feedback_items": 0},
        "evidence_type": "json",
    },
    {
        "id": "postgres-agent-route",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/app/main.py",
        "expected_text": "/postgres/support-tickets/agent-report",
        "evidence_type": "source",
    },
    {
        "id": "github-release",
        "url": "https://github.com/sunnnn2005/data-quality-agent/releases/tag/v0.3.0",
        "expected_text": "v0.3.0",
        "evidence_type": "release_page",
    },
]


def _fetch(url: str) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "data-quality-agent-public-health/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8", errors="replace")
            return int(response.status), body
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return int(exc.code), body


def _verify_check(check: dict[str, Any]) -> dict[str, Any]:
    status_code, body = _fetch(check["url"])
    result = {
        "id": check["id"],
        "url": check["url"],
        "evidence_type": check["evidence_type"],
        "status_code": status_code,
        "passed": status_code == 200,
    }

    if status_code != 200:
        result["error"] = f"expected 200, got {status_code}"
        return result

    expected_text = check.get("expected_text")
    if expected_text and expected_text not in body:
        result["passed"] = False
        result["error"] = f"missing expected text: {expected_text}"
        return result

    expected_texts = check.get("expected_texts", [])
    for item in expected_texts:
        if item not in body:
            result["passed"] = False
            result["error"] = f"missing expected text: {item}"
            return result

    expected_json = check.get("expected_json")
    if expected_json:
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            result["passed"] = False
            result["error"] = f"invalid json: {exc}"
            return result
        for key, expected_value in expected_json.items():
            actual_value = payload.get(key)
            if actual_value != expected_value:
                result["passed"] = False
                result["error"] = f"{key} expected {expected_value!r}, got {actual_value!r}"
                return result
        result["verified_fields"] = sorted(expected_json)

    return result


def build_public_evidence_health_payload() -> dict[str, Any]:
    checks = [_verify_check(check) for check in PUBLIC_CHECKS]
    passed_count = sum(1 for check in checks if check["passed"])
    return {
        "generated_by": "scripts/verify_public_evidence_health.py",
        "check_count": len(checks),
        "passed_count": passed_count,
        "failed_count": len(checks) - passed_count,
        "status": "PASS" if passed_count == len(checks) else "FAIL",
        "checks": checks,
    }


def verify_public_evidence_health(payload: dict[str, Any]) -> None:
    if payload["status"] != "PASS":
        failures = [check for check in payload["checks"] if not check["passed"]]
        raise AssertionError(f"public evidence health failed: {failures}")
    if payload["check_count"] < 6:
        raise AssertionError("public evidence health should check demo, artifacts, metrics, and release")


def main() -> None:
    payload = build_public_evidence_health_payload()
    verify_public_evidence_health(payload)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"public evidence health check failed: {exc}", file=sys.stderr)
        raise
