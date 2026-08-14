from scripts.build_ai_engineer_readiness import (
    build_ai_engineer_readiness_payload,
    render_markdown,
    verify_ai_engineer_readiness,
)


def test_ai_engineer_readiness_maps_agent_work_to_resume_safe_signals():
    payload = build_ai_engineer_readiness_payload()
    verification = verify_ai_engineer_readiness(payload)
    markdown = render_markdown(payload)

    assert verification["ai_engineer_readiness_verified"] is True
    assert payload["implemented_signal_count"] == 8
    assert payload["partial_signal_count"] == 1
    assert payload["not_claimed_signal_count"] == 1
    assert payload["evidence_counts"]["allowed_tools"] == 7
    assert payload["evidence_counts"]["business_replay_rows"] == 8
    assert payload["evidence_counts"]["business_replay_findings"] == 5
    assert payload["evidence_counts"]["real_model_capture_accepted_runs"] == 0
    assert payload["evidence_counts"]["application_evidence_links"] == 41
    assert "AI Engineer Intern" in markdown
    assert "OpenAI-compatible" in payload["resume_bullet"]
    assert "tool calling" in payload["readiness_summary"].lower()
    assert "production users" in " ".join(payload["not_resume_safe_yet"]).lower()
