import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNBOOK_PATH = ROOT / "docs" / "real-model-runbook.json"
CAPTURE_GATE_PATH = ROOT / "docs" / "real-model-evidence-capture.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "real-model-preflight.json"
OUTPUT_MD_PATH = ROOT / "docs" / "real-model-preflight.md"
DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def check_api_health(api_base_url: str, timeout_seconds: float = 2.0) -> dict[str, Any]:
    url = api_base_url.rstrip("/") + "/health"
    try:
        with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8"))
        return {
            "name": "local_api_health",
            "ready": body.get("status") == "ok",
            "status": body.get("status"),
            "url": url,
        }
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return {
            "name": "local_api_health",
            "ready": False,
            "status": "unavailable",
            "url": url,
            "error_type": exc.__class__.__name__,
        }


def public_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def runbook_command(runbook: dict[str, Any], command_id: str) -> str:
    for command in runbook["run_commands"]:
        if command["id"] == command_id:
            return command["command"]
    raise KeyError(f"missing runbook command: {command_id}")


def build_real_model_preflight_payload(
    *,
    env: dict[str, str] | None = None,
    api_health: dict[str, Any] | None = None,
    sample_csv_path: Path | None = None,
) -> dict[str, Any]:
    environment = env if env is not None else os.environ
    runbook = load_json(RUNBOOK_PATH)
    capture_gate = load_json(CAPTURE_GATE_PATH)
    sample_path = sample_csv_path or (ROOT / "examples" / "support_tickets.csv")
    health = api_health if api_health is not None else check_api_health(DEFAULT_API_BASE_URL)
    has_api_key = bool(environment.get("OPENAI_API_KEY"))

    checks = [
        {
            "name": "openai_api_key_configured",
            "ready": has_api_key,
            "evidence": (
                "OPENAI_API_KEY is present in the environment; the value is never printed."
                if has_api_key
                else "OPENAI_API_KEY is not configured in the environment."
            ),
        },
        {
            "name": "local_api_health",
            "ready": bool(health.get("ready")),
            "evidence": health,
        },
        {
            "name": "business_csv_sample_available",
            "ready": sample_path.exists(),
            "evidence": public_path(sample_path),
        },
        {
            "name": "business_agent_route_documented",
            "ready": "/business-data/agent-report" in runbook["openapi_agent_routes"],
            "evidence": runbook["openapi_agent_routes"],
        },
        {
            "name": "redacted_capture_gate_ready",
            "ready": capture_gate["capture_required_field_count"] == 17
            and "raw_prompt_logged" in capture_gate["capture_required_fields"],
            "evidence": {
                "capture_required_field_count": capture_gate["capture_required_field_count"],
                "requires_raw_prompt_logged_false": "raw_prompt_logged" in capture_gate["capture_required_fields"],
            },
        },
    ]
    ready_checks = sum(1 for check in checks if check["ready"])
    blocked_checks = [check["name"] for check in checks if not check["ready"]]
    real_model_ready = not blocked_checks
    next_command = (
        runbook_command(runbook, "capture_business_csv_real_model_evidence")
        if real_model_ready
        else "Start the API with OPENAI_API_KEY, then rerun this preflight."
    )

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_real_model_preflight.py",
        "purpose": (
            "Check whether the environment is ready to execute and capture a public-safe real OpenAI-compatible "
            "LLM agent run without exposing secrets or raw business rows."
        ),
        "real_model_execution_status": "ready_to_execute" if real_model_ready else "not_ready",
        "real_model_run_executed_by_preflight": False,
        "ready_check_count": ready_checks,
        "total_check_count": len(checks),
        "blocked_check_count": len(blocked_checks),
        "blocked_checks": blocked_checks,
        "checks": checks,
        "next_real_model_capture_command": next_command,
        "resume_status": "preflight_ready_not_claimable" if real_model_ready else "preflight_blocked_not_claimable",
        "resume_safe_summary": (
            "Published a real-model preflight gate that checks API readiness, provider-key presence, business CSV "
            "sample availability, documented agent routes, and redacted telemetry requirements before any real LLM "
            "run is claimed."
        ),
        "not_claimed": [
            "real model run completed by this preflight",
            "provider credential value",
            "raw prompt contents",
            "raw business rows",
            "production model traffic",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    checks = "\n".join(
        f"| `{check['name']}` | {check['ready']} | `{json.dumps(check['evidence'], sort_keys=True)}` |"
        for check in payload["checks"]
    )
    blocked = "\n".join(f"- `{item}`" for item in payload["blocked_checks"]) or "- None."
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Real Model Preflight

This generated artifact checks whether the project can safely run a real OpenAI-compatible LLM tool-calling pass. It never executes a paid model call and never prints provider credentials.

## Current Status

| Metric | Value |
| --- | ---: |
| Execution status | `{payload["real_model_execution_status"]}` |
| Real model run executed by preflight | {payload["real_model_run_executed_by_preflight"]} |
| Ready checks | {payload["ready_check_count"]} |
| Total checks | {payload["total_check_count"]} |
| Blocked checks | {payload["blocked_check_count"]} |

## Checks

| Check | Ready | Evidence |
| --- | --- | --- |
{checks}

## Blocked Checks

{blocked}

## Next Capture Command

```bash
{payload["next_real_model_capture_command"]}
```

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_real_model_preflight(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["real_model_run_executed_by_preflight"] is not False:
        raise AssertionError("preflight must not execute paid model calls")
    if payload["total_check_count"] != 5:
        raise AssertionError("preflight must verify five readiness checks")
    names = {check["name"] for check in payload["checks"]}
    required = {
        "openai_api_key_configured",
        "local_api_health",
        "business_csv_sample_available",
        "business_agent_route_documented",
        "redacted_capture_gate_ready",
    }
    if names != required:
        raise AssertionError("preflight checks changed unexpectedly")
    if payload["blocked_check_count"] != len(payload["blocked_checks"]):
        raise AssertionError("blocked check count must match blocked checks")
    if payload["ready_check_count"] + payload["blocked_check_count"] != payload["total_check_count"]:
        raise AssertionError("ready and blocked counts must add up")
    not_claimed = {item.lower() for item in payload["not_claimed"]}
    for forbidden in ("provider credential value", "raw prompt contents", "raw business rows"):
        if forbidden not in not_claimed:
            raise AssertionError(f"preflight must explicitly avoid claiming or exposing {forbidden}")
    return {
        "real_model_preflight_verified": True,
        "total_check_count": payload["total_check_count"],
        "blocked_check_count": payload["blocked_check_count"],
    }


def main() -> None:
    payload = build_real_model_preflight_payload()
    verify_real_model_preflight(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
