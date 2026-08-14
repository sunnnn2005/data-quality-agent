from scripts.build_ai_engineer_review_intake import (
    build_ai_engineer_review_intake,
    render_markdown,
    verify_ai_engineer_review_intake,
)


def test_ai_engineer_review_intake_collects_targeted_external_feedback_without_claiming_it():
    payload = build_ai_engineer_review_intake()
    verification = verify_ai_engineer_review_intake(payload)
    markdown = render_markdown(payload)

    assert verification["ai_engineer_review_intake_verified"] is True
    assert payload["review_path_count"] == 6
    assert payload["review_question_count"] == 6
    assert payload["countable_condition_count"] == 6
    assert payload["implemented_ai_signals"] == 8
    assert payload["current_counts"]["accepted_ai_engineer_reviews"] == 0
    assert payload["current_counts"]["external_ai_feedback_items"] == 0
    assert payload["template_checks"]["has_permission_checkbox"] is True
    assert payload["template_checks"]["has_no_private_data_checkbox"] is True
    assert payload["template_checks"]["mentions_planning_trace"] is True
    assert "AI Engineer Review Intake" in markdown
    assert "tool calling" in markdown.lower()
