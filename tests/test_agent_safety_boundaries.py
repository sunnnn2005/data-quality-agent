from scripts.build_agent_safety_boundaries import (
    build_agent_safety_boundaries_payload,
    render_markdown,
    verify_agent_safety_boundaries,
)


def test_agent_safety_boundaries_capture_tool_permissions_and_guardrails():
    payload = build_agent_safety_boundaries_payload()
    verification = verify_agent_safety_boundaries(payload)
    markdown = render_markdown(payload)

    assert verification["agent_safety_boundaries_verified"] is True
    assert payload["tool_allowlist_count"] == 9
    assert payload["postgres_rejected_write_query_count"] == 3
    assert payload["llm_sensitive_redaction_verified"] is True
    assert payload["agent_disabled_fallback_verified"] is True
    assert "formal security audit" in payload["not_claimed"]
    assert "Agent Safety Boundaries" in markdown
