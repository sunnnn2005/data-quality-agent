import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.main import app  # noqa: E402


OUTPUT_JSON_PATH = ROOT / "docs" / "performance-baseline.json"
OUTPUT_MD_PATH = ROOT / "docs" / "performance-baseline.md"


BENCHMARK_CHECKS = [
    {
        "id": "quality_report_local_baseline",
        "method": "POST",
        "path": "/datasets/orders_daily/quality-report",
        "iterations": 12,
        "warmup_iterations": 2,
        "max_p95_ms": 80.0,
        "expected_status": 200,
        "expected_body_fields": {"status": "FAIL", "row_count": 7},
    },
    {
        "id": "profile_local_baseline",
        "method": "GET",
        "path": "/datasets/orders_daily/profile",
        "iterations": 12,
        "warmup_iterations": 2,
        "max_p95_ms": 40.0,
        "expected_status": 200,
        "expected_body_fields": {"row_count": 7},
    },
]


def _request(client: TestClient, check: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    response = client.request(check["method"], check["path"])
    payload = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
    return response.status_code, payload


def _run_benchmark_check(client: TestClient, check: dict[str, Any]) -> dict[str, Any]:
    for _ in range(check["warmup_iterations"]):
        _request(client, check)

    durations_ms: list[float] = []
    failure_reasons: list[str] = []
    last_payload: dict[str, Any] = {}
    for _ in range(check["iterations"]):
        started = time.perf_counter()
        status_code, payload = _request(client, check)
        durations_ms.append((time.perf_counter() - started) * 1000)
        last_payload = payload
        if status_code != check["expected_status"]:
            failure_reasons.append(f"expected status {check['expected_status']}, got {status_code}")
        for field, expected in check.get("expected_body_fields", {}).items():
            if payload.get(field) != expected:
                failure_reasons.append(f"{field} expected {expected!r}, got {payload.get(field)!r}")

    p95_ms = statistics.quantiles(durations_ms, n=20, method="inclusive")[18]
    avg_ms = statistics.fmean(durations_ms)
    passed = not failure_reasons and p95_ms <= check["max_p95_ms"]
    if p95_ms > check["max_p95_ms"]:
        failure_reasons.append(f"p95_ms expected <= {check['max_p95_ms']}, got {p95_ms:.3f}")

    return {
        "id": check["id"],
        "method": check["method"],
        "path": check["path"],
        "iterations": check["iterations"],
        "warmup_iterations": check["warmup_iterations"],
        "avg_ms": round(avg_ms, 3),
        "p95_ms": round(p95_ms, 3),
        "max_ms": round(max(durations_ms), 3),
        "min_ms": round(min(durations_ms), 3),
        "max_p95_ms": check["max_p95_ms"],
        "passed": passed,
        "payload_preview": {
            key: last_payload.get(key) for key in ("status", "row_count", "quality_score", "trace_id")
        },
        "failure_reasons": failure_reasons,
    }


def build_performance_baseline_payload() -> dict[str, Any]:
    client = TestClient(app)
    checks = [_run_benchmark_check(client, check) for check in BENCHMARK_CHECKS]
    passed_count = sum(1 for check in checks if check["passed"])
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_performance_baseline.py",
        "environment": "local FastAPI TestClient, built-in sample datasets, no network server",
        "benchmark_count": len(checks),
        "passed_count": passed_count,
        "failed_count": len(checks) - passed_count,
        "status": "PASS" if passed_count == len(checks) else "FAIL",
        "checks": checks,
        "resume_safe_summary": (
            "Published a CI-verified local performance baseline for 2 core FastAPI report/profile routes "
            "using 24 measured endpoint calls over built-in sample data."
        ),
        "not_claimed": [
            "No production latency SLA is claimed.",
            "No hosted traffic benchmark is claimed.",
            "No external load test is claimed.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {id} | `{method}` | `{path}` | {iterations} | {avg_ms} | {p95_ms} | {max_p95_ms} | {passed} |".format(
            **check
        )
        for check in payload["checks"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Performance Baseline

This generated artifact measures local FastAPI `TestClient` endpoint latency for built-in sample data. It is useful as a CI regression baseline and does not claim hosted production performance.

## Summary

| Metric | Value |
| --- | ---: |
| Benchmarks | {payload["benchmark_count"]} |
| Passed | {payload["passed_count"]} |
| Failed | {payload["failed_count"]} |
| Status | `{payload["status"]}` |

## Benchmarks

| Check | Method | Path | Iterations | Avg ms | P95 ms | Max P95 ms | Passed |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
{rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_performance_baseline(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["benchmark_count"] != 2:
        raise AssertionError("performance baseline must cover 2 route benchmarks")
    if payload["passed_count"] != 2 or payload["status"] != "PASS":
        raise AssertionError("performance baseline must pass every benchmark")
    total_iterations = sum(check["iterations"] for check in payload["checks"])
    if total_iterations != 24:
        raise AssertionError("performance baseline must include 24 measured endpoint calls")
    paths = {check["path"] for check in payload["checks"]}
    if paths != {"/datasets/orders_daily/quality-report", "/datasets/orders_daily/profile"}:
        raise AssertionError("performance baseline must cover quality-report and profile routes")
    if "production latency sla" not in " ".join(payload["not_claimed"]).lower():
        raise AssertionError("performance baseline must not claim production latency SLA")
    return {"performance_baseline_verified": True, "benchmark_count": 2, "measured_endpoint_calls": 24}


def main() -> None:
    payload = build_performance_baseline_payload()
    verify_performance_baseline(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
