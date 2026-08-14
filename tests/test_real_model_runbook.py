from scripts.build_real_model_runbook import (
    build_real_model_runbook_payload,
    render_markdown,
    verify_real_model_runbook,
)


def test_real_model_runbook_defines_resume_safe_evidence_gate_without_claiming_paid_run():
    payload = build_real_model_runbook_payload()
    verification = verify_real_model_runbook(payload)
    markdown = render_markdown(payload)

    assert verification["real_model_runbook_verified"] is True
    assert payload["current_real_model_runs"] == 0
    assert payload["current_mock_model_calls"] == 2
    assert payload["current_mock_tokens"] == 360
    assert payload["tool_count"] == 9
    assert payload["run_command_count"] == 5
    assert payload["evidence_field_count"] == 15
    assert payload["acceptance_criteria_count"] == 8
    assert payload["safety_gate_count"] == 5
    assert payload["resume_status"] == "real_model_run_ready_not_claimable"
    assert "/business-data/agent-report" in payload["openapi_agent_routes"]
    assert "real OpenAI model run completed" in payload["not_claimed"]
    assert "paid model benchmark results" in payload["not_claimed"]
    assert "Real Model Runbook" in markdown
    assert "OPENAI_API_KEY" in markdown
