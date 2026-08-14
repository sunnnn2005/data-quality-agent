from scripts.build_outcome_launch_day_tracker import (
    build_outcome_launch_day_tracker,
    render_markdown,
    verify_outcome_launch_day_tracker,
)


def test_outcome_launch_day_tracker_keeps_outreach_separate_from_outcomes():
    payload = build_outcome_launch_day_tracker()
    verification = verify_outcome_launch_day_tracker(payload)
    markdown = render_markdown(payload)

    assert verification["outcome_launch_day_tracker_verified"] is True
    assert payload["baseline"]["planned_send_count"] == 5
    assert payload["baseline"]["recorded_outreach_event_count"] == 0
    assert payload["baseline"]["accepted_external_evidence_count"] == 0
    assert payload["baseline"]["resume_outcome_claimable_now"] is False
    assert payload["first_resume_unlock"]["target_metric"] == "ai_engineer_review_items"
    assert payload["first_resume_unlock"]["remaining_to_unlock"] == 1
    assert len(payload["launch_items"]) == 5
    assert all(item["after_send_counts_as"] == "outreach_execution_only" for item in payload["launch_items"])
    assert all(item["resume_countable_now"] is False for item in payload["launch_items"])
    assert "--slot-id review_slot_07" in payload["launch_items"][0]["record_sent_command"]
    assert "## Send These Today" in markdown
    assert "No external users, feedback, business impact" in markdown
