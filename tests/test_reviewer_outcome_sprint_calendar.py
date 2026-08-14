from scripts.build_reviewer_outcome_sprint_calendar import (
    build_reviewer_outcome_sprint_calendar,
    render_markdown,
    verify_reviewer_outcome_sprint_calendar,
)


def test_reviewer_outcome_sprint_calendar_prioritizes_real_resume_evidence_without_claiming_it():
    payload = build_reviewer_outcome_sprint_calendar()
    verification = verify_reviewer_outcome_sprint_calendar(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_outcome_sprint_calendar_verified"] is True
    assert payload["sprint_day_count"] == 7
    assert payload["send_day_count"] == 5
    assert payload["follow_up_day_count"] == 2
    assert payload["target_metric_count"] == 5
    assert payload["completion_criteria_count"] == 25
    assert payload["current_sent_count"] == 0
    assert payload["current_accepted_evidence_count"] == 0
    assert payload["resume_claim_allowed_now"] is False
    assert payload["day_cards"][0]["target_metric"] == "ai_engineer_review_items"
    assert "Reviewer Outcome Sprint Calendar" in markdown
    assert "external reviewer evidence gate" in markdown.lower()
    assert "The calendar itself does not count as users" in payload["not_claimed"][0]


def test_reviewer_outcome_sprint_calendar_maps_each_send_to_public_submission_and_unlock():
    payload = build_reviewer_outcome_sprint_calendar()

    metrics = [card["target_metric"] for card in payload["day_cards"]]
    assert metrics == [
        "ai_engineer_review_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "external_feedback_items",
    ]
    assert len({card["submission_url"] for card in payload["day_cards"]}) == payload["public_submission_path_count"]
    for card in payload["day_cards"]:
        assert card["submission_url"].startswith("https://github.com/")
        assert card["tracking_issue_url"].startswith("https://github.com/")
        assert card["remaining_needed"] == 1
        assert card["claimable_now"] is False
        assert "{name}" in card["copy_ready_message"]
        assert len(card["completion_criteria"]) == 5
        assert "accepted" in card["completion_criteria"][-1].lower()
        assert card["resume_unlock_after_accepted_evidence"]
