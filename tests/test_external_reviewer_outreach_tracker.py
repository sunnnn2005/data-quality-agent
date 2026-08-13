from scripts.build_external_reviewer_outreach_tracker import (
    build_external_reviewer_outreach_tracker,
    render_markdown,
    verify_external_reviewer_outreach_tracker,
)


def test_external_reviewer_outreach_tracker_prepares_countable_review_requests_without_inflation():
    payload = build_external_reviewer_outreach_tracker()
    verification = verify_external_reviewer_outreach_tracker(payload)
    markdown = render_markdown(payload)

    assert verification["external_reviewer_outreach_tracker_verified"] is True
    assert payload["queue_count"] == 3
    assert payload["source_message_count"] == 3
    assert payload["quickstart_review_path_count"] == 3
    assert payload["quickstart_submission_field_count"] == 8
    assert payload["linked_pilot_review_slots"] == 3
    assert payload["status_counts"]["not_contacted"] == 3
    assert payload["status_counts"]["contacted"] == 0
    assert payload["status_counts"]["public_evidence_received"] == 0
    assert payload["public_counts"]["external_feedback_items"] == 0
    assert payload["public_counts"]["confirmed_external_users"] == 0
    assert all(not item["counts_toward_resume"] for item in payload["queue"])
    assert any(item["primary_link"].endswith("/external-run-quickstart.html") for item in payload["queue"])
    assert "External Reviewer Outreach Tracker" in markdown
    assert "A sent message does not count as feedback." in markdown
