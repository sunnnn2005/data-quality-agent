from scripts.build_reviewer_feedback_packet import (
    build_reviewer_feedback_packet,
    render_markdown,
    verify_reviewer_feedback_packet,
)


def test_reviewer_feedback_packet_turns_review_requests_into_metric_aware_public_evidence():
    payload = build_reviewer_feedback_packet()
    verification = verify_reviewer_feedback_packet(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_feedback_packet_verified"] is True
    assert payload["reviewer_task_count"] == 3
    assert payload["evidence_question_count"] == 5
    assert payload["conversion_path_count"] == 4
    assert payload["planned_review_slots"] == 3
    assert payload["resume_status"] == "collection_ready_not_claimable"
    assert payload["current_public_counts"] == {
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
        "business_case_feedback_items": 0,
    }
    assert {task["counts_toward"] for task in payload["reviewer_tasks"]} == {
        "external_feedback_items",
        "confirmed_external_users",
        "business_case_feedback_items",
    }
    assert "Reviewer Feedback Packet" in markdown
    assert "collection_ready_not_claimable" not in markdown
