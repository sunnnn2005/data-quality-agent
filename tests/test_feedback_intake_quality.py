from scripts.build_feedback_intake_quality import (
    build_feedback_intake_quality_payload,
    render_markdown,
    verify_feedback_intake_quality,
)


def test_feedback_intake_quality_verifies_public_feedback_template_without_usage_claims():
    payload = build_feedback_intake_quality_payload()
    verification = verify_feedback_intake_quality(payload)
    markdown = render_markdown(payload)

    assert verification["feedback_intake_quality_verified"] is True
    assert payload["required_section_count"] == 5
    assert payload["required_try_path_count"] == 5
    assert payload["required_outcome_count"] == 4
    assert payload["captured_field_count"] == 5
    assert payload["captured_fields"]["review_path"] is True
    assert payload["captured_fields"]["environment"] is True
    assert payload["current_public_counts"]["external_feedback_items"] == 0
    assert payload["current_public_counts"]["confirmed_external_users"] == 0
    assert "confirmed-user" in payload["tracking_labels"].values()
    assert "Feedback Intake Quality" in markdown
    assert "external users" in payload["not_claimed"]
