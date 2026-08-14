from scripts.build_real_model_run_request_pack import (
    build_real_model_run_request_pack,
    render_markdown,
    verify_real_model_run_request_pack,
)


def test_real_model_run_request_pack_creates_privacy_safe_evidence_path_without_claiming_run():
    payload = build_real_model_run_request_pack()
    verification = verify_real_model_run_request_pack(payload)
    markdown = render_markdown(payload)

    assert verification["real_model_run_request_pack_verified"] is True
    assert payload["current_real_model_runs"] == 0
    assert payload["preflight_status"] == "not_ready"
    assert payload["evidence_link_count"] == 5
    assert payload["acceptance_condition_count"] == 8
    assert payload["resume_unlock_count"] == 4
    assert payload["capture_required_field_count"] == 17
    assert payload["claimable_now"] == []
    assert payload["template_checks"]["has_redacted_telemetry"] is True
    assert payload["template_checks"]["blocks_credentials"] is True
    assert payload["template_checks"]["blocks_raw_prompts"] is True
    assert "real_model_tool_calling_runs" in markdown
    assert "Current real model runs | 0" in markdown
