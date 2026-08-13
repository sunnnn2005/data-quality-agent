from scripts.build_business_data_replay_packet import (
    build_business_data_replay_packet,
    render_markdown,
    verify_business_data_replay_packet,
)


def test_business_data_replay_packet_turns_realistic_data_runs_into_public_evidence():
    payload = build_business_data_replay_packet()
    verification = verify_business_data_replay_packet(payload)
    markdown = render_markdown(payload)

    assert verification["business_data_replay_packet_verified"] is True
    assert payload["replay_path_count"] == 3
    assert payload["evidence_field_count"] == 8
    assert payload["safety_requirement_count"] == 5
    assert payload["verified_input_boundaries"]["business_data_endpoint_verified"] is True
    assert payload["verified_input_boundaries"]["postgres_agent_endpoint_verified"] is True
    assert payload["verified_input_boundaries"]["max_rows"] == 10_000
    assert payload["verified_input_boundaries"]["max_columns"] == 80
    assert payload["current_public_counts"] == {
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "business_case_feedback_items": 0,
        "reproducible_feedback_items": 0,
    }
    assert payload["resume_status"] == "replay_ready_not_claimable"
    assert {path["id"] for path in payload["replay_paths"]} == {
        "sanitized_csv_upload",
        "readonly_postgres_table",
        "business_case_replay",
    }
    assert "Business Data Replay Packet" in markdown
    assert "real company data analyzed" in payload["not_claimed"]
