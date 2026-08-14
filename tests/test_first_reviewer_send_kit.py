from scripts.build_first_reviewer_send_kit import (
    build_first_reviewer_send_kit,
    render_markdown,
    verify_first_reviewer_send_kit,
)


def test_first_reviewer_send_kit_maps_ai_reviewer_to_recordable_slot():
    payload = build_first_reviewer_send_kit()
    verification = verify_first_reviewer_send_kit(payload)
    markdown = render_markdown(payload)

    assert verification["first_reviewer_send_kit_verified"] is True
    assert payload["selected_metric"] == "ai_engineer_review_items"
    assert payload["status_board_slot_id"] == "review_slot_07"
    assert "--slot-id review_slot_07" in payload["record_sent_command"]
    assert payload["after_send_expected_pipeline_change"]["sent_reviewer_messages"]["before"] == 0
    assert payload["after_send_expected_pipeline_change"]["sent_reviewer_messages"]["after_recording_one_real_send"] == 1
    assert payload["after_send_expected_pipeline_change"]["claimable_resume_metric_count"]["after_recording_one_real_send"] == 0
    assert "Run this only after the message is actually sent" in markdown
    assert "# First Reviewer Send Kit" in markdown
