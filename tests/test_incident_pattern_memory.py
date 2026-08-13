from scripts.build_incident_pattern_memory import (
    build_incident_pattern_memory_payload,
    render_markdown,
    verify_incident_pattern_memory,
)


def test_incident_pattern_memory_retrieves_recurring_sanitized_patterns():
    payload = build_incident_pattern_memory_payload()
    verification = verify_incident_pattern_memory(payload)
    markdown = render_markdown(payload)

    assert verification["incident_pattern_memory_verified"] is True
    assert payload["trace_count"] == 2
    assert payload["incident_pattern_count"] == 3
    assert all(pattern["recurrence_count"] == 2 for pattern in payload["patterns"])
    assert all(pattern["evidence_trace_ids"] for pattern in payload["patterns"])
    assert "external production incidents" in payload["not_claimed"]
    assert "Incident Pattern Memory" in markdown
