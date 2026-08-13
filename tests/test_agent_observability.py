from scripts.build_agent_observability import (
    build_agent_observability_payload,
    render_markdown,
    verify_agent_observability,
)


def test_agent_observability_artifact_tracks_trace_fallback_and_memory():
    payload = build_agent_observability_payload()
    verification = verify_agent_observability(payload)
    markdown = render_markdown(payload)

    assert verification["agent_observability_verified"] is True
    assert payload["observed_trace_count"] == 2
    assert payload["fallback_event_count"] == 2
    assert payload["verification_passed_trace_count"] == 1
    assert payload["model_telemetry"]["model_call_count"] == 2
    assert payload["model_telemetry"]["total_tokens"] == 360
    assert payload["model_telemetry"]["estimated_cost_usd"] == 0.000081
    assert payload["model_telemetry"]["prompt_version"] == "tool-agent-v3"
    assert payload["model_telemetry"]["raw_prompt_logged"] is False
    assert "agent_disabled" in payload["fallback_statuses"]
    assert "quality_report" in payload["report_types"]
    assert "agent_report" in payload["report_types"]
    assert "production monitoring dashboard" in payload["not_claimed"]
    assert "paid model benchmark results" in payload["not_claimed"]
    assert "Agent Observability" in markdown
    assert "Mock total tokens | 360" in markdown
