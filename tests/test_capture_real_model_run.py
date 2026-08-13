from scripts.capture_real_model_run import (
    build_capture_record,
    capture_real_model_run,
)


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeTransport:
    def __init__(self):
        self.urls = []

    def post(self, url, timeout):
        self.urls.append(("POST", url, timeout))
        return FakeResponse(
            {
                "trace_id": "run_real_001",
                "dataset": {"id": "orders_daily"},
                "status": "FAIL",
                "tool_calls": [
                    {"tool_name": "select_quality_strategy"},
                    {"tool_name": "profile_dataset"},
                    {"tool_name": "run_quality_checks"},
                    {"tool_name": "build_quality_report"},
                ],
                "quality_report": {"verification": {"passed": True}},
                "evaluation": {
                    "provider": "openai-compatible",
                    "model": "gpt-4o-mini",
                    "prompt_version": "tool-agent-v3",
                    "model_call_count": 2,
                    "tool_call_count": 4,
                    "distinct_tool_count": 4,
                    "used_strategy_tool": True,
                    "used_required_report_tool": True,
                    "final_report_attached": True,
                    "total_tokens": 1234,
                    "estimated_cost_usd": 0.0012,
                    "latency_ms": 1200,
                },
            }
        )

    def get(self, url, timeout):
        self.urls.append(("GET", url, timeout))
        return FakeResponse(
            {
                "trace_id": "run_real_001",
                "report_type": "agent_report",
                "summary": {"verification_passed": True},
                "evaluation": {"verification_passed": True},
                "fallback_status": None,
                "error": None,
            }
        )


def test_build_capture_record_extracts_gate_fields_from_agent_report_and_trace():
    record = build_capture_record(
        {
            "trace_id": "run_real_001",
            "dataset": {"id": "orders_daily"},
            "quality_report": {"verification": {"passed": True}},
            "evaluation": {
                "provider": "openai-compatible",
                "model": "gpt-4o-mini",
                "prompt_version": "tool-agent-v3",
                "model_call_count": 2,
                "tool_call_count": 4,
                "distinct_tool_count": 4,
                "used_strategy_tool": True,
                "used_required_report_tool": True,
                "final_report_attached": True,
                "total_tokens": 1234,
                "estimated_cost_usd": 0.0012,
                "latency_ms": 1200,
            },
        },
        {"summary": {"verification_passed": True}, "evaluation": {"verification_passed": True}},
    )

    assert record["trace_id"] == "run_real_001"
    assert record["provider"] == "openai-compatible"
    assert record["model"] == "gpt-4o-mini"
    assert record["dataset_id"] == "orders_daily"
    assert record["tool_call_count"] == 4
    assert record["verification_passed"] is True
    assert record["redaction_status"] == "redacted"
    assert record["raw_prompt_logged"] is False


def test_capture_real_model_run_calls_agent_and_trace_endpoints_then_verifies_gate():
    transport = FakeTransport()

    payload = capture_real_model_run(
        base_url="http://127.0.0.1:8000",
        dataset_id="orders_daily",
        transport=transport,
    )

    assert payload["accepted_real_model_run_count"] == 1
    assert payload["blocked_outcome_claim_count"] == 0
    assert payload["accepted_runs"][0]["trace_id"] == "run_real_001"
    assert ("POST", "http://127.0.0.1:8000/datasets/orders_daily/agent-report", 60) in transport.urls
    assert ("GET", "http://127.0.0.1:8000/runs/run_real_001", 60) in transport.urls
