import json
import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import app.main as main_module  # noqa: E402
from app.tool_agent import LLMDataQualityAgent  # noqa: E402

OUTPUT_JSON_PATH = ROOT / "docs" / "api-smoke-report.json"
OUTPUT_MD_PATH = ROOT / "docs" / "api-smoke-report.md"


SMOKE_CHECKS = [
    {
        "id": "health",
        "method": "GET",
        "path": "/health",
        "expected_status": 200,
        "expected_fields": {"status": "ok", "service": "data-quality-agent"},
    },
    {
        "id": "dataset_catalog",
        "method": "GET",
        "path": "/datasets",
        "expected_status": 200,
        "expected_list_min_length": 3,
    },
    {
        "id": "profile",
        "method": "GET",
        "path": "/datasets/orders_daily/profile",
        "expected_status": 200,
        "expected_fields": {"row_count": 7},
    },
    {
        "id": "quality_report",
        "method": "POST",
        "path": "/datasets/orders_daily/quality-report",
        "expected_status": 200,
        "expected_fields": {"status": "FAIL", "row_count": 7},
        "expected_nested_fields": {"verification.passed": True},
    },
    {
        "id": "agent_report_disabled_fallback",
        "method": "POST",
        "path": "/datasets/orders_daily/agent-report",
        "expected_status": 200,
        "expected_fields": {"status": "DISABLED", "error": "OPENAI_API_KEY is not configured"},
    },
    {
        "id": "incident_markdown",
        "method": "POST",
        "path": "/datasets/orders_daily/incident-report.md",
        "expected_status": 200,
        "expected_text": "# Data Quality Incident: Daily Orders",
    },
]


class SmokeSettings:
    api_key = None
    base_url = "https://api.openai.com/v1"
    model = "gpt-4o-mini"
    timeout_seconds = 30
    max_retries = 2


def _get_nested(payload: dict[str, Any], path: str) -> Any:
    current: Any = payload
    for part in path.split("."):
        current = current[part]
    return current


def _run_check(client: TestClient, check: dict[str, Any]) -> dict[str, Any]:
    response = client.request(check["method"], check["path"])
    passed = response.status_code == check["expected_status"]
    failure_reasons: list[str] = []
    payload_preview: dict[str, Any] = {}

    if response.headers.get("content-type", "").startswith("application/json"):
        payload = response.json()
        if isinstance(payload, dict):
            payload_preview = {key: payload.get(key) for key in ("status", "service", "row_count", "error", "trace_id")}
            for field, expected in check.get("expected_fields", {}).items():
                if payload.get(field) != expected:
                    passed = False
                    failure_reasons.append(f"{field} expected {expected!r}, got {payload.get(field)!r}")
            for field, expected in check.get("expected_nested_fields", {}).items():
                if _get_nested(payload, field) != expected:
                    passed = False
                    failure_reasons.append(f"{field} expected {expected!r}")
        elif isinstance(payload, list):
            payload_preview = {"list_length": len(payload)}
            min_length = check.get("expected_list_min_length")
            if min_length is not None and len(payload) < min_length:
                passed = False
                failure_reasons.append(f"list length expected >= {min_length}, got {len(payload)}")
    else:
        expected_text = check.get("expected_text")
        payload_preview = {"text_length": len(response.text)}
        if expected_text and expected_text not in response.text:
            passed = False
            failure_reasons.append(f"missing text: {expected_text}")

    return {
        "id": check["id"],
        "method": check["method"],
        "path": check["path"],
        "status_code": response.status_code,
        "passed": passed,
        "payload_preview": payload_preview,
        "failure_reasons": failure_reasons,
    }


def build_api_smoke_report_payload() -> dict[str, Any]:
    main_module.llm_agent = LLMDataQualityAgent(settings=SmokeSettings())
    client = TestClient(main_module.app)
    checks = [_run_check(client, check) for check in SMOKE_CHECKS]
    passed_count = sum(1 for check in checks if check["passed"])
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_api_smoke_report.py",
        "deterministic_mode": {
            "llm_agent_forced_disabled": True,
            "reason": "API smoke report must not require model credentials.",
        },
        "check_count": len(checks),
        "passed_count": passed_count,
        "failed_count": len(checks) - passed_count,
        "status": "PASS" if passed_count == len(checks) else "FAIL",
        "checks": checks,
        "resume_safe_summary": (
            "Published a CI-verified API smoke report covering 6 FastAPI routes for health, catalog, "
            "profiling, deterministic report, disabled agent fallback, and incident Markdown export."
        ),
        "not_claimed": [
            "No production uptime SLA is claimed.",
            "No external traffic volume is claimed.",
            "No hosted API usage is claimed.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| {check['id']} | `{check['method']}` | `{check['path']}` | {check['status_code']} | {check['passed']} |"
        for check in payload["checks"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# API Smoke Report

This generated artifact verifies core FastAPI routes with `TestClient`. It proves local endpoint behavior without claiming production traffic.

## Summary

| Metric | Value |
| --- | ---: |
| Checks | {payload["check_count"]} |
| Passed | {payload["passed_count"]} |
| Failed | {payload["failed_count"]} |
| Status | `{payload["status"]}` |

## Route Checks

| Check | Method | Path | Status | Passed |
| --- | --- | --- | ---: | --- |
{rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_api_smoke_report(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["check_count"] != 6:
        raise AssertionError("API smoke report must cover 6 routes")
    if payload["passed_count"] != 6 or payload["status"] != "PASS":
        raise AssertionError("API smoke report must pass every route check")
    paths = {check["path"] for check in payload["checks"]}
    required_paths = {
        "/health",
        "/datasets",
        "/datasets/orders_daily/profile",
        "/datasets/orders_daily/quality-report",
        "/datasets/orders_daily/agent-report",
        "/datasets/orders_daily/incident-report.md",
    }
    if paths != required_paths:
        raise AssertionError("API smoke report must cover the required route set")
    if "production uptime sla" not in " ".join(payload["not_claimed"]).lower():
        raise AssertionError("API smoke report must avoid production uptime claims")
    return {"api_smoke_report_verified": True, "check_count": 6, "passed_count": 6}


def main() -> None:
    payload = build_api_smoke_report_payload()
    verify_api_smoke_report(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
