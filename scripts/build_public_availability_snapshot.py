import json
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON_PATH = ROOT / "docs" / "public-availability-snapshot.json"
OUTPUT_MD_PATH = ROOT / "docs" / "public-availability-snapshot.md"
REPO = "sunnnn2005/data-quality-agent"
TIMEOUT_SECONDS = 15


PUBLIC_ENDPOINTS = [
    {
        "id": "public_demo",
        "url": "https://sunnnn2005.github.io/data-quality-agent/",
        "expected_text": "Data Quality Agent",
        "surface": "GitHub Pages",
    },
    {
        "id": "reviewer_landing_page",
        "url": "https://sunnnn2005.github.io/data-quality-agent/review.html",
        "expected_text": "8-minute public review",
        "surface": "GitHub Pages",
    },
    {
        "id": "openapi_contract",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/openapi.json",
        "expected_text": "/business-data/agent-report",
        "surface": "GitHub raw artifact",
    },
    {
        "id": "public_metrics",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/public-metrics-summary.json",
        "expected_text": "resume_safe_signals",
        "surface": "GitHub raw artifact",
    },
]

WORKFLOWS = [
    {"id": "ci", "workflow": "test.yml"},
    {"id": "public_evidence_health", "workflow": "public-evidence-health.yml"},
    {"id": "container_publish", "workflow": "publish-image.yml"},
]


def probe_endpoint(endpoint: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(
        endpoint["url"],
        headers={"User-Agent": "data-quality-agent-availability-snapshot/1.0"},
    )
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read(250_000).decode("utf-8", errors="replace")
            status_code = response.status
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        body = exc.read(10_000).decode("utf-8", errors="replace")
    except Exception as exc:
        return {
            **endpoint,
            "status_code": None,
            "latency_ms": int((time.monotonic() - started) * 1000),
            "available": False,
            "error": exc.__class__.__name__,
        }

    return {
        **endpoint,
        "status_code": status_code,
        "latency_ms": int((time.monotonic() - started) * 1000),
        "available": status_code == 200 and endpoint["expected_text"] in body,
        "error": None,
    }


def fetch_latest_workflow_runs() -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for item in WORKFLOWS:
        try:
            completed = subprocess.run(
                [
                    "gh",
                    "run",
                    "list",
                    "--repo",
                    REPO,
                    "--workflow",
                    item["workflow"],
                    "--branch",
                    "main",
                    "--limit",
                    "1",
                    "--json",
                    "databaseId,status,conclusion,createdAt,displayTitle,url,workflowName",
                ],
                check=True,
                capture_output=True,
                text=True,
                cwd=ROOT,
            )
            payload = json.loads(completed.stdout)
            latest = payload[0] if payload else {}
        except (FileNotFoundError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
            latest = {"error": exc.__class__.__name__}
        runs.append(
            {
                "id": item["id"],
                "workflow": item["workflow"],
                "status": latest.get("status"),
                "conclusion": latest.get("conclusion"),
                "created_at": latest.get("createdAt"),
                "url": latest.get("url"),
                "verified": latest.get("status") == "completed" and latest.get("conclusion") == "success",
                "error": latest.get("error"),
            }
        )
    return runs


def build_deployment_evidence(endpoints: list[dict[str, Any]], workflows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    endpoints_by_id = {item["id"]: item for item in endpoints}
    workflows_by_id = {item["id"]: item for item in workflows}
    public_demo = endpoints_by_id.get("public_demo", {})
    return [
        {
            "id": "public_demo_live",
            "label": "Public GitHub Pages demo",
            "url": public_demo.get("url"),
            "status": "available" if public_demo.get("available") else "unavailable",
            "evidence": f"HTTP {public_demo.get('status_code')}, latency {public_demo.get('latency_ms')} ms",
        },
        {
            "id": "ci_verified",
            "label": "Main-branch CI",
            "url": workflows_by_id.get("ci", {}).get("url"),
            "status": workflows_by_id.get("ci", {}).get("conclusion"),
            "evidence": workflows_by_id.get("ci", {}).get("workflow"),
        },
        {
            "id": "public_health_verified",
            "label": "Public evidence health",
            "url": workflows_by_id.get("public_evidence_health", {}).get("url"),
            "status": workflows_by_id.get("public_evidence_health", {}).get("conclusion"),
            "evidence": workflows_by_id.get("public_evidence_health", {}).get("workflow"),
        },
        {
            "id": "container_publish_verified",
            "label": "Container publish workflow",
            "url": workflows_by_id.get("container_publish", {}).get("url"),
            "status": workflows_by_id.get("container_publish", {}).get("conclusion"),
            "evidence": workflows_by_id.get("container_publish", {}).get("workflow"),
        },
    ]


def build_public_availability_snapshot(
    endpoint_results: list[dict[str, Any]] | None = None,
    workflow_runs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    endpoints = endpoint_results if endpoint_results is not None else [probe_endpoint(item) for item in PUBLIC_ENDPOINTS]
    workflows = workflow_runs if workflow_runs is not None else fetch_latest_workflow_runs()
    available_count = sum(1 for item in endpoints if item.get("available") is True)
    successful_workflow_count = sum(1 for item in workflows if item.get("verified") is True)
    latency_values = [item["latency_ms"] for item in endpoints if isinstance(item.get("latency_ms"), int)]
    public_evidence_ready = available_count == len(endpoints) and successful_workflow_count == len(workflows)
    deployment_evidence = build_deployment_evidence(endpoints, workflows)
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_public_availability_snapshot.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": f"https://github.com/{REPO}",
        "snapshot_type": "public demo availability and workflow health snapshot",
        "endpoint_count": len(endpoints),
        "available_endpoint_count": available_count,
        "workflow_count": len(workflows),
        "successful_workflow_count": successful_workflow_count,
        "max_latency_ms": max(latency_values) if latency_values else None,
        "endpoints": endpoints,
        "workflows": workflows,
        "public_evidence_ready": public_evidence_ready,
        "deployment_evidence": deployment_evidence,
        "resume_policy": (
            "This snapshot proves public entrypoint reachability and recent workflow health only. "
            "Do not claim production uptime SLA, active users, customer adoption, or paid availability monitoring from this artifact."
        ),
        "resume_safe_deployment_line": (
            "Published a public GitHub Pages demo with reachable project surfaces and passing CI, public evidence health, "
            "and container publish workflows at snapshot time."
            if public_evidence_ready
            else "Published project surfaces exist, but at least one endpoint or workflow did not pass at snapshot time."
        ),
        "resume_safe_summary": (
            f"Captured {available_count}/{len(endpoints)} reachable public project surfaces and "
            f"{successful_workflow_count}/{len(workflows)} successful main-branch workflows in a generated availability snapshot."
        ),
        "not_claimed": [
            "production uptime SLA",
            "active users",
            "customer adoption",
            "paid availability monitoring",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    endpoints = "\n".join(
        (
            f"| {item['id']} | {item['surface']} | {item['status_code']} | "
            f"{item['available']} | {item['latency_ms']} |"
        )
        for item in payload["endpoints"]
    )
    workflows = "\n".join(
        f"| {item['id']} | {item['workflow']} | {item.get('status')} | {item.get('conclusion')} | {item['verified']} |"
        for item in payload["workflows"]
    )
    deployment_rows = "\n".join(
        f"| {item['id']} | {item['label']} | {item.get('status')} | {item.get('evidence')} | {item.get('url') or '-'} |"
        for item in payload["deployment_evidence"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Public Availability Snapshot

This generated artifact captures whether the public demo and evidence surfaces are reachable at snapshot time.

## Summary

| Metric | Value |
| --- | ---: |
| Available public endpoints | {payload["available_endpoint_count"]} / {payload["endpoint_count"]} |
| Successful main-branch workflows | {payload["successful_workflow_count"]} / {payload["workflow_count"]} |
| Max observed endpoint latency | {payload["max_latency_ms"]} ms |

## Public Endpoints

| Endpoint | Surface | Status | Available | Latency ms |
| --- | --- | ---: | --- | ---: |
{endpoints}

## Workflow Health

| Check | Workflow | Status | Conclusion | Verified |
| --- | --- | --- | --- | --- |
{workflows}

## Deployment Evidence

| Evidence | Surface | Status | Detail | URL |
| --- | --- | --- | --- | --- |
{deployment_rows}

## Resume Policy

{payload["resume_policy"]}

## Resume-Safe Deployment Line

{payload["resume_safe_deployment_line"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_public_availability_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["endpoint_count"] < 4:
        raise AssertionError("availability snapshot must check at least four public endpoints")
    if payload["workflow_count"] < 3:
        raise AssertionError("availability snapshot must check CI, public evidence health, and container workflows")
    if payload["available_endpoint_count"] > payload["endpoint_count"]:
        raise AssertionError("available endpoint count cannot exceed endpoint count")
    if payload["successful_workflow_count"] > payload["workflow_count"]:
        raise AssertionError("successful workflow count cannot exceed workflow count")
    for item in payload["endpoints"]:
        if item.get("available") and item.get("status_code") != 200:
            raise AssertionError("available endpoints must return status 200")
        if isinstance(item.get("latency_ms"), int) and item["latency_ms"] < 0:
            raise AssertionError("latency cannot be negative")
    for forbidden in ("production uptime SLA", "active users", "customer adoption"):
        if forbidden not in payload["resume_policy"]:
            raise AssertionError(f"availability policy must not claim {forbidden}")
    if len(payload["deployment_evidence"]) != 4:
        raise AssertionError("availability snapshot must include four deployment evidence entries")
    if payload["public_evidence_ready"] is True and "Published a public GitHub Pages demo" not in payload["resume_safe_deployment_line"]:
        raise AssertionError("availability snapshot must expose a resume-safe deployment line when ready")
    return {
        "public_availability_snapshot_verified": True,
        "available_endpoint_count": payload["available_endpoint_count"],
        "endpoint_count": payload["endpoint_count"],
        "successful_workflow_count": payload["successful_workflow_count"],
        "workflow_count": payload["workflow_count"],
    }


def main() -> None:
    payload = build_public_availability_snapshot()
    verify_public_availability_snapshot(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
