from scripts.build_application_evidence_pack import (
    build_application_evidence_pack_payload,
    render_markdown,
    verify_application_evidence_pack,
)


def test_application_evidence_pack_gives_recruiters_verified_review_path():
    payload = build_application_evidence_pack_payload()
    verification = verify_application_evidence_pack(payload)
    markdown = render_markdown(payload)

    assert verification["application_evidence_pack_verified"] is True
    assert len(payload["application_links"]) == 27
    assert "business_data_replay_packet" in payload["application_links"]
    assert "business_replay_demo" in payload["application_links"]
    assert "real_model_runbook" in payload["application_links"]
    assert "real_model_evidence_capture" in payload["application_links"]
    assert "resume_outcome_readiness" in payload["application_links"]
    assert "reviewer_feedback_packet" in payload["application_links"]
    assert "reviewer_funnel_board" in payload["application_links"]
    assert "external_run_evidence_packet" in payload["application_links"]
    assert "external_run_quickstart" in payload["application_links"]
    assert "external_reviewer_outreach_tracker" in payload["application_links"]
    assert "external_reviewer_evidence_gate" in payload["application_links"]
    assert "accepted_evidence_rollup" in payload["application_links"]
    assert len(payload["resume_bullets"]) == 3
    assert payload["verified_outcome_numbers"]["passing_tests"] == 131
    assert payload["verified_outcome_numbers"]["verified_resume_claims"] == 67
    assert payload["verified_outcome_numbers"]["business_data_replay_paths"] == 3
    assert payload["verified_outcome_numbers"]["business_data_replay_evidence_fields"] == 8
    assert payload["verified_outcome_numbers"]["business_replay_demo_rows"] == 8
    assert payload["verified_outcome_numbers"]["business_replay_demo_findings"] == 5
    assert payload["verified_outcome_numbers"]["business_replay_demo_check_types"] == 4
    assert payload["verified_outcome_numbers"]["real_model_run_commands"] == 5
    assert payload["verified_outcome_numbers"]["real_model_evidence_fields"] == 15
    assert payload["verified_outcome_numbers"]["real_model_capture_required_fields"] == 17
    assert payload["verified_outcome_numbers"]["real_model_capture_accepted_runs"] == 0
    assert payload["verified_outcome_numbers"]["real_model_capture_blocked_claims"] == 4
    assert payload["verified_outcome_numbers"]["impact_review_business_metrics"] == 12
    assert payload["verified_outcome_numbers"]["impact_review_evidence_links"] == 8
    assert payload["verified_outcome_numbers"]["business_problem_cases"] == 1
    assert payload["verified_outcome_numbers"]["business_problem_detected_risks"] == 4
    assert payload["verified_outcome_numbers"]["public_traction_surfaces"] == 4
    assert payload["verified_outcome_numbers"]["public_traction_growth_channels"] == 19
    assert payload["verified_outcome_numbers"]["feedback_intake_required_sections"] == 5
    assert payload["verified_outcome_numbers"]["feedback_intake_captured_fields"] == 5
    assert payload["verified_outcome_numbers"]["reviewer_funnel_stages"] == 4
    assert payload["verified_outcome_numbers"]["reviewer_funnel_remaining_evidence_items"] == 7
    assert payload["verified_outcome_numbers"]["accepted_evidence_rollup_claimable_metrics"] == 5
    assert payload["verified_outcome_numbers"]["accepted_evidence_rollup_blocked_claims"] == 5
    assert payload["honest_baseline"]["stars"] == 0
    assert payload["honest_baseline"]["confirmed_external_users"] == 0
    assert "Application Evidence Pack" in markdown
