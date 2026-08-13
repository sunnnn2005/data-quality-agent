from scripts.build_pilot_review_tracker import (
    build_pilot_review_tracker_payload,
    render_markdown,
    verify_pilot_review_tracker,
)


def test_pilot_review_tracker_tracks_planned_reviews_without_counting_unverified_feedback():
    payload = build_pilot_review_tracker_payload()
    verification = verify_pilot_review_tracker(payload)
    markdown = render_markdown(payload)

    assert verification["pilot_review_tracker_verified"] is True
    assert payload["planned_review_count"] == 3
    assert payload["status_counts"]["not_contacted"] == 3
    assert payload["status_counts"]["contacted"] == 0
    assert payload["status_counts"]["feedback_received"] == 0
    assert payload["public_counts"]["external_feedback_items"] == 0
    assert payload["public_counts"]["confirmed_external_users"] == 0
    assert payload["public_counts"]["business_case_feedback_items"] == 0
    assert len(payload["resume_upgrade_rules"]) == 3
    assert all(not item["counts_toward_resume"] for item in payload["planned_reviews"])
    assert all(rule["resume_status"] == "not_claimable_yet" for rule in payload["resume_upgrade_rules"])
    assert "Pilot Review Tracker" in markdown
    assert "business-case" in markdown
