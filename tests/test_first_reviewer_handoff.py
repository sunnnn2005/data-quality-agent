from scripts.build_first_reviewer_handoff import (
    build_first_reviewer_handoff,
    render_markdown,
    verify_first_reviewer_handoff,
)


def test_first_reviewer_handoff_selects_ai_engineer_review_without_claiming_outcome():
    payload = build_first_reviewer_handoff()
    verification = verify_first_reviewer_handoff(payload)
    markdown = render_markdown(payload)

    assert verification["first_reviewer_handoff_verified"] is True
    assert payload["target_metric"] == "ai_engineer_review_items"
    assert payload["current_count"] == 0
    assert payload["required_count"] == 1
    assert payload["status"] == "not_sent"
    assert payload["resume_status"] == "not_claimable_until_public_issue_is_accepted"
    assert "AI/ML engineer" in payload["who_to_choose"]
    assert "--slot-id review_slot_07" in payload["record_sent_command"]
    assert payload["after_send_expected_pipeline_change"]["sent_reviewer_messages"]["after_recording_one_real_send"] == 1
    assert payload["after_send_expected_pipeline_change"]["claimable_resume_metric_count"]["after_recording_one_real_send"] == 0
    assert "tool-calling loop" in payload["future_resume_line"]
    assert "accepted AI Engineer review" in payload["not_claimed"]
    assert "First Reviewer Handoff" in markdown
    assert "After You Send" in markdown
    assert "This line is locked until the public evidence gate passes" in markdown
