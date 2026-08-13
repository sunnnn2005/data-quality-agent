from scripts.build_business_case_intake import (
    build_business_case_intake_payload,
    render_markdown,
    verify_business_case_intake,
)


def test_business_case_intake_collects_real_problem_context_without_claiming_cases():
    payload = build_business_case_intake_payload()
    verification = verify_business_case_intake(payload)
    markdown = render_markdown(payload)

    assert verification["business_case_intake_verified"] is True
    assert payload["required_section_count"] == 8
    assert payload["required_context_field_count"] == 3
    assert payload["required_impact_field_count"] == 4
    assert payload["required_project_evidence_field_count"] == 4
    assert payload["required_try_path_count"] == 5
    assert payload["required_outcome_count"] == 8
    assert payload["captured_field_count"] == 8
    assert payload["captured_fields"]["business_context"] is True
    assert payload["captured_fields"]["business_impact"] is True
    assert payload["captured_fields"]["project_evidence_mapping"] is True
    assert payload["captured_fields"]["permission_boundary"] is True
    assert payload["tracking_label"] == "business-case"
    assert payload["current_public_counts"]["business_case_feedback_items"] == 0
    assert payload["current_public_counts"]["confirmed_external_users"] == 0
    assert payload["resume_upgrade_rule"]["resume_status"] == "not_claimable_yet"
    assert payload["resume_upgrade_rule"]["signal"] == "anonymized business-impact feedback"
    assert "manual investigation time" in payload["resume_outcome_fields"]
    assert "pilot readiness with anonymized data" in payload["resume_outcome_fields"]
    assert "Business Case Intake" in markdown
    assert "Resume Outcome Fields" in markdown
    assert "submitted external business cases" in payload["not_claimed"]
