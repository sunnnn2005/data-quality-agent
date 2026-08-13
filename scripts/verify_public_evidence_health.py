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
        "expected_json": {"stars": 0, "forks": 1, "test_count": 62},
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
        "url": "https://github.com/sunnnn2005/data-quality-agent/releases/tag/v0.2.0",
        "expected_text": "v0.2.0",
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
