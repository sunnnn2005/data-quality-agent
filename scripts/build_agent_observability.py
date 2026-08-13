import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agent import DataQualityAgent
from app.data import DATASETS, load_dataset
from app.tool_agent import LLMDataQualityAgent
from app.traces import RunTraceStore


OUTPUT_JSON_PATH = ROOT / "docs" / "agent-observability.json"
OUTPUT_MD_PATH = ROOT / "docs" / "agent-observability.md"


def build_agent_observability_payload() -> dict[str, Any]:
    store = RunTraceStore()
    dataset = DATASETS["orders_daily"]
    frame = load_dataset(dataset.id)
    quality_report = store.save_quality_report(DataQualityAgent().analyze(dataset, frame))
    agent_report = store.save_agent_report(LLMDataQualityAgent().run(dataset, frame))
    telemetry_report = _run_mock_telemetry_agent(dataset, frame)
    memory = store.list_by_dataset(dataset.id, limit=5)
    traces = [trace for trace in (store.get(quality_report.trace_id), store.get(agent_report.trace_id)) if trace]
    fallback_events = [trace for trace in traces if trace.fallback_status]
    verification_passed = [
        trace
        for trace in traces
        if trace.evaluation.get("verification_passed") is True or trace.summary.get("verification_passed") is True
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_agent_observability.py",
        "dataset_id": dataset.id,
        "observed_trace_count": len(traces),
        "trace_ids": [trace.trace_id for trace in traces],
        "report_types": sorted({trace.report_type for trace in traces}),
        "fallback_event_count": len(fallback_events),
        "fallback_statuses": sorted({trace.fallback_status for trace in fallback_events if trace.fallback_status}),
        "verification_passed_trace_count": len(verification_passed),
        "memory_trace_count": memory.trace_count,
        "memory_incident_pattern_count": len(memory.incident_patterns),
        "tool_call_preview_count": sum(len(trace.tool_calls) for trace in traces),
        "model_telemetry": {
            "provider": telemetry_report.evaluation.get("provider"),
            "model": telemetry_report.evaluation.get("model"),
            "prompt_version": telemetry_report.evaluation.get("prompt_version"),
            "model_call_count": telemetry_report.evaluation.get("model_call_count"),
            "total_tokens": telemetry_report.evaluation.get("total_tokens"),
            "estimated_cost_usd": telemetry_report.evaluation.get("estimated_cost_usd"),
            "latency_ms": telemetry_report.evaluation.get("latency_ms"),
            "timeout_seconds": telemetry_report.evaluation.get("timeout_seconds"),
            "max_retries": telemetry_report.evaluation.get("max_retries"),
            "raw_prompt_logged": any("messages" in call for call in telemetry_report.evaluation.get("model_calls", [])),
        },
        "observability_fields": [
            "trace_id",
            "dataset_id",
            "report_type",
            "fallback_status",
            "verification_passed",
            "memory_trace_count",
            "incident_pattern_count",
            "model",
            "prompt_version",
            "model_call_count",
            "total_tokens",
            "estimated_cost_usd",
        ],
        "resume_safe_summary": (
            "Generated an observability artifact covering trace ids, report types, fallback status, "
            "verification status, dataset memory, incident-pattern memory, tool-call previews, and "
            "mocked model token/cost telemetry."
        ),
        "not_claimed": [
            "production monitoring dashboard",
            "real user traffic",
            "paid model benchmark results",
        ],
    }


def _run_mock_telemetry_agent(dataset, frame):
    class FakeSettings:
        api_key = "test-key"
        base_url = "http://example.test/v1"
        model = "fake-model"
        timeout_seconds = 3
        max_retries = 1

    agent = LLMDataQualityAgent(settings=FakeSettings())
    calls = [
        {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": "call_strategy",
                                "type": "function",
                                "function": {"name": "select_quality_strategy", "arguments": "{}"},
                            },
                            {
                                "id": "call_report",
                                "type": "function",
                                "function": {"name": "build_quality_report", "arguments": "{}"},
                            },
                        ],
                    }
                }
            ],
            "usage": {"prompt_tokens": 120, "completion_tokens": 40, "total_tokens": 160},
        },
        {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Mocked telemetry run produced an evidence-backed quality report.",
                    }
                }
            ],
            "usage": {"prompt_tokens": 180, "completion_tokens": 20, "total_tokens": 200},
        },
    ]

    def fake_post(_body):
        return calls.pop(0), 7

    agent.advisor._post_with_retries = fake_post
    return agent.run(dataset, frame)


def render_markdown(payload: dict[str, Any]) -> str:
    fields = "\n".join(f"- `{item}`" for item in payload["observability_fields"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Agent Observability

This generated artifact summarizes local agent run observability. It is a reproducible engineering signal, not evidence of production traffic.

## Coverage

| Metric | Value |
| --- | ---: |
| Observed traces | {payload["observed_trace_count"]} |
| Fallback events | {payload["fallback_event_count"]} |
| Verification-passed traces | {payload["verification_passed_trace_count"]} |
| Dataset memory traces | {payload["memory_trace_count"]} |
| Memory incident patterns | {payload["memory_incident_pattern_count"]} |
| Tool-call previews | {payload["tool_call_preview_count"]} |
| Mock model calls | {payload["model_telemetry"]["model_call_count"]} |
| Mock total tokens | {payload["model_telemetry"]["total_tokens"]} |
| Mock estimated cost USD | {payload["model_telemetry"]["estimated_cost_usd"]} |
| Raw prompt logged | {payload["model_telemetry"]["raw_prompt_logged"]} |

## Observability Fields

{fields}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_agent_observability(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "observed_trace_count": 2,
        "fallback_event_count": 2,
        "verification_passed_trace_count": 1,
        "memory_trace_count": 2,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    if sorted(payload["report_types"]) != ["agent_report", "quality_report"]:
        raise AssertionError("observability must cover deterministic and agent reports")
    if "agent_disabled" not in payload["fallback_statuses"]:
        raise AssertionError("observability must include disabled-agent fallback status")
    for required in ("trace_id", "fallback_status", "verification_passed"):
        if required not in payload["observability_fields"]:
            raise AssertionError(f"observability fields missing {required}")
    if "production monitoring dashboard" not in payload["not_claimed"]:
        raise AssertionError("observability artifact must not claim production monitoring")
    telemetry = payload["model_telemetry"]
    if telemetry.get("model_call_count") != 2:
        raise AssertionError("observability must include model-call telemetry")
    if telemetry.get("total_tokens") != 360:
        raise AssertionError("observability must include token telemetry")
    if telemetry.get("estimated_cost_usd") != 0.000081:
        raise AssertionError("observability must include estimated mock cost")
    if telemetry.get("prompt_version") != "tool-agent-v3":
        raise AssertionError("observability must include prompt version")
    if telemetry.get("raw_prompt_logged") is not False:
        raise AssertionError("observability must not log raw prompts")
    if "paid model benchmark results" not in payload["not_claimed"]:
        raise AssertionError("observability artifact must not claim paid benchmark results")
    return {"agent_observability_verified": True, **expected}


def main() -> None:
    payload = build_agent_observability_payload()
    verify_agent_observability(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
