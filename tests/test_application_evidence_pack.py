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
    assert len(payload["application_links"]) == 14
    assert "business_data_replay_packet" in payload["application_links"]
    assert len(payload["resume_bullets"]) == 3
    assert payload["verified_outcome_numbers"]["passing_tests"] == 95
    assert payload["verified_outcome_numbers"]["verified_resume_claims"] == 54
    assert payload["verified_outcome_numbers"]["business_data_replay_paths"] == 3
    assert payload["verified_outcome_numbers"]["business_data_replay_evidence_fields"] == 8
    assert payload["verified_outcome_numbers"]["impact_review_business_metrics"] == 12
    assert payload["verified_outcome_numbers"]["impact_review_evidence_links"] == 8
    assert payload["verified_outcome_numbers"]["business_problem_cases"] == 1
    assert payload["verified_outcome_numbers"]["business_problem_detected_risks"] == 4
    assert payload["verified_outcome_numbers"]["public_traction_surfaces"] == 4
    assert payload["verified_outcome_numbers"]["public_traction_growth_channels"] == 15
    assert payload["verified_outcome_numbers"]["feedback_intake_required_sections"] == 5
    assert payload["verified_outcome_numbers"]["feedback_intake_captured_fields"] == 5
    assert payload["honest_baseline"]["stars"] == 0
    assert payload["honest_baseline"]["confirmed_external_users"] == 0
    assert "Application Evidence Pack" in markdown
