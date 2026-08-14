import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OBSERVABILITY_PATH = ROOT / "docs" / "agent-observability.json"
CAPABILITY_MATRIX_PATH = ROOT / "docs" / "agent-capability-matrix.json"
OPENAPI_PATH = ROOT / "docs" / "openapi.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "real-model-runbook.json"
OUTPUT_MD_PATH = ROOT / "docs" / "real-model-runbook.md"


REAL_MODEL_EVIDENCE_FIELDS = [
    "provider",
    "model",
    "prompt_version",
    "dataset_id",
    "model_call_count",
    "tool_call_count",
    "distinct_tool_count",
    "used_strategy_tool",
    "used_required_report_tool",
    "final_report_attached",
    "total_tokens",
    "estimated_cost_usd",
    "latency_ms",
    "verification_passed",
    "redaction_status",
]

RUN_COMMANDS = [
    {
        "id": "start_api",
        "command": "OPENAI_API_KEY=$OPENAI_API_KEY uvicorn app.main:app --reload",
        "purpose": "Start the FastAPI app with an explicit OpenAI-compatible model key.",
    },
    {
        "id": "run_builtin_agent",
        "command": "curl -X POST http://127.0.0.1:8000/datasets/orders_daily/agent-report",
        "purpose": "Execute the tool-calling agent on a deterministic dataset.",
    },
    {
        "id": "run_business_csv_agent",
        "command": (
            "curl -X POST http://127.0.0.1:8000/business-data/agent-report "
            "-F file=@sample.csv -F dataset_name='Replay Dataset' -F owner='reviewer' "
            "-F primary_key='id'"
        ),
        "purpose": "Execute the tool-calling agent on anonymized business-shaped CSV data.",
    },
    {
        "id": "inspect_trace",
        "command": "curl http://127.0.0.1:8000/runs/<trace_id>",
        "purpose": "Inspect sanitized trace, tool calls, final report attachment, and telemetry summary.",
    },
    {
        "id": "capture_real_model_evidence",
        "command": "python scripts/capture_real_model_run.py --dataset-id orders_daily --write",
        "purpose": "Capture a redacted real-model run artifact from the local API and verify it against the evidence gate.",
    },
    {
        "id": "capture_business_csv_real_model_evidence",
        "command": (
            "python scripts/capture_real_model_run.py --csv-path sample.csv "
            "--dataset-name 'Replay Dataset' --owner reviewer --primary-key id "
            "--expected-columns 'id,status,amount' --description 'Anonymized business replay dataset' --write"
        ),
        "purpose": (
            "Capture a redacted real-model run artifact from the business CSV agent route so resume evidence can "
            "show the agent works on anonymized business-shaped data, not only built-in examples."
        ),
    },
]

ACCEPTANCE_CRITERIA = [
    "Agent status is not DISABLED.",
    "At least two model calls are recorded.",
    "At least three tool calls are recorded.",
    "The strategy tool and final report tool are both used.",
    "A deterministic QualityReport is attached.",
    "Report verification passes or lists explicit issues.",
    "Token count, estimated cost, latency, prompt version, provider, and model are recorded.",
    "No raw prompt, uploaded rows, credentials, customer identifiers, or secrets are published.",
]

SAFETY_GATES = [
    "Do not commit OPENAI_API_KEY or provider credentials.",
    "Do not publish raw request prompts or raw uploaded business rows.",
    "Use anonymized or synthetic-but-business-shaped CSV data for public artifacts.",
    "Store only telemetry summaries and redacted report evidence.",
    "Keep deterministic report verification as the source of truth.",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_real_model_runbook_payload() -> dict[str, Any]:
    observability = load_json(OBSERVABILITY_PATH)
    capability = load_json(CAPABILITY_MATRIX_PATH)
    openapi = load_json(OPENAPI_PATH)
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_real_model_runbook.py",
        "purpose": (
            "Define the exact evidence gate for converting the existing mocked tool-calling telemetry into a "
            "public, resume-safe real OpenAI-compatible model run once provider credentials are explicitly supplied."
        ),
        "current_real_model_runs": 0,
        "current_mock_model_calls": observability["model_telemetry"]["model_call_count"],
        "current_mock_tokens": observability["model_telemetry"]["total_tokens"],
        "prompt_version": observability["model_telemetry"]["prompt_version"],
        "implemented_agent_capabilities": capability["implemented_count"],
        "tool_count": capability["tool_count"],
        "openapi_agent_routes": [
            path
            for path in sorted(openapi["paths"])
            if path.endswith("/agent-report")
        ],
        "run_command_count": len(RUN_COMMANDS),
        "run_commands": RUN_COMMANDS,
        "evidence_field_count": len(REAL_MODEL_EVIDENCE_FIELDS),
        "evidence_fields": REAL_MODEL_EVIDENCE_FIELDS,
        "acceptance_criteria_count": len(ACCEPTANCE_CRITERIA),
        "acceptance_criteria": ACCEPTANCE_CRITERIA,
        "safety_gate_count": len(SAFETY_GATES),
        "safety_gates": SAFETY_GATES,
        "resume_upgrade_rules": [
            {
                "metric": "real_model_runs",
                "current_value": 0,
                "minimum_before_claim": 1,
                "claim_when_met": "executed a real OpenAI-compatible tool-calling run with public redacted telemetry",
            },
            {
                "metric": "real_model_tool_calls",
                "current_value": 0,
                "minimum_before_claim": 3,
                "claim_when_met": "real model selected multiple tools before finalizing a verified report",
            },
        ],
        "resume_status": "real_model_run_ready_not_claimable",
        "resume_safe_summary": (
            "Published a CI-verified real-model runbook with 6 run commands, 15 evidence fields, "
            "8 acceptance criteria, and 5 safety gates without claiming a paid model run yet."
        ),
        "not_claimed": [
            "real OpenAI model run completed",
            "paid model benchmark results",
            "real model accuracy improvement",
            "production model traffic",
            "raw prompts published",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    commands = "\n\n".join(
        f"### {item['id']}\n\n{item['purpose']}\n\n```bash\n{item['command']}\n```"
        for item in payload["run_commands"]
    )
    fields = "\n".join(f"- `{field}`" for field in payload["evidence_fields"])
    criteria = "\n".join(f"- {item}" for item in payload["acceptance_criteria"])
    safety = "\n".join(f"- {item}" for item in payload["safety_gates"])
    routes = "\n".join(f"- `{route}`" for route in payload["openapi_agent_routes"])
    rules = "\n".join(
        "| {metric} | {current_value} | {minimum_before_claim} | {claim_when_met} |".format(**rule)
        for rule in payload["resume_upgrade_rules"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Real Model Runbook

This generated artifact defines the evidence gate for a future real OpenAI-compatible tool-calling run. It does not claim that a paid model run has already been completed.

## Purpose

{payload["purpose"]}

## Current Status

| Metric | Value |
| --- | ---: |
| Current real model runs | {payload["current_real_model_runs"]} |
| Current mocked model calls | {payload["current_mock_model_calls"]} |
| Current mocked tokens | {payload["current_mock_tokens"]} |
| Prompt version | `{payload["prompt_version"]}` |
| Implemented agent capabilities | {payload["implemented_agent_capabilities"]} |
| Allowed agent tools | {payload["tool_count"]} |

## Agent Routes

{routes}

## Run Commands

{commands}

## Evidence Fields

{fields}

## Acceptance Criteria

{criteria}

## Safety Gates

{safety}

## Resume Upgrade Rules

| Metric | Current value | Minimum before claim | Claim when met |
| --- | ---: | ---: | --- |
{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_real_model_runbook(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "current_real_model_runs": 0,
        "current_mock_model_calls": 2,
        "current_mock_tokens": 360,
        "tool_count": 9,
        "run_command_count": 6,
        "evidence_field_count": 15,
        "acceptance_criteria_count": 8,
        "safety_gate_count": 5,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    if payload["prompt_version"] != "tool-agent-v3":
        raise AssertionError("real model runbook must pin the current prompt version")
    required_routes = {"/datasets/{dataset_id}/agent-report", "/business-data/agent-report"}
    if not required_routes <= set(payload["openapi_agent_routes"]):
        raise AssertionError("real model runbook must include built-in and business-data agent routes")
    if payload["resume_status"] != "real_model_run_ready_not_claimable":
        raise AssertionError("real model runbook must not claim a real model run before evidence")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in (
        "openai_api_key",
        "total_tokens",
        "estimated_cost_usd",
        "final_report_attached",
        "capture_business_csv_real_model_evidence",
        "business csv agent route",
    ):
        if required not in joined:
            raise AssertionError(f"real model runbook missing {required}")
    not_claimed = {item.lower() for item in payload["not_claimed"]}
    for forbidden in ("real openai model run completed", "paid model benchmark results", "production model traffic"):
        if forbidden not in not_claimed:
            raise AssertionError(f"real model runbook must explicitly not claim {forbidden}")
    return {"real_model_runbook_verified": True, **expected}


def main() -> None:
    payload = build_real_model_runbook_payload()
    verify_real_model_runbook(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
