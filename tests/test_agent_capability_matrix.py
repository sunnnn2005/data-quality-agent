from scripts.build_agent_capability_matrix import (
    build_agent_capability_matrix_payload,
    render_markdown,
    verify_agent_capability_matrix,
)


def test_agent_capability_matrix_maps_real_agent_requirements_without_inflation():
    payload = build_agent_capability_matrix_payload()
    verification = verify_agent_capability_matrix(payload)
    markdown = render_markdown(payload)

    assert verification["agent_capability_matrix_verified"] is True
    assert payload["tool_count"] == 9
    assert payload["implemented_count"] == 13
    assert payload["partial_count"] == 4
    assert payload["planned_count"] == 1
    assert payload["not_claimed_count"] == 1
    assert "select_quality_strategy" in payload["tool_names"]
    assert "retrieve_dataset_memory" in payload["tool_names"]
    assert "inspect_primary_key_integrity" in payload["tool_names"]
    assert "analyze_numeric_distribution" in payload["tool_names"]
    assert "retrieve_business_rules" in payload["tool_names"]
    assert any(item["id"] == "llm-decision-making" for item in payload["capabilities"])
    assert any(item["id"] == "tool-feedback-loop" for item in payload["capabilities"])
    assert any(item["id"] == "dynamic-path" for item in payload["capabilities"])
    assert any(item["id"] == "production-adoption" for item in payload["capabilities"])
    assert "external users" in payload["not_claimed"]
    assert "enterprise production deployment" in payload["not_claimed"]
    assert "Agent Capability Matrix" in markdown
