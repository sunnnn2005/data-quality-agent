from scripts.build_reviewer_share_kit import (
    build_reviewer_share_kit,
    render_markdown,
    verify_reviewer_share_kit,
)


def test_reviewer_share_kit_packages_public_call_without_claiming_outcomes():
    payload = build_reviewer_share_kit()
    verification = verify_reviewer_share_kit(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_share_kit_verified"] is True
    assert payload["share_channel_count"] == 5
    assert payload["ready_message_count"] == 5
    assert payload["linked_submission_paths"] == 6
    assert payload["linked_public_call_segments"] == 3
    assert payload["required_evidence_fields"] == 24
    assert payload["outreach_tasks_linked"] == 9
    assert payload["public_call_issue"] == "https://github.com/sunnnn2005/data-quality-agent/issues/19"
    assert payload["send_status_counts"] == {"not_sent": 5, "sent": 0, "completed": 0}
    assert all(value == 0 for value in payload["current_counts"].values())
    assert payload["resume_status"] == "share_ready_not_claimable"
    assert {message["channel"] for message in payload["share_messages"]} == {
        "linkedin_dm",
        "email_or_mentor",
        "class_discord_or_slack",
        "github_discussion_or_issue_comment",
        "resume_portfolio_link",
    }
    assert all("permission" in message["message"].lower() for message in payload["share_messages"])
    assert all("private data" in message["message"].lower() for message in payload["share_messages"])
    assert "fake GitHub engagement" in str(payload)
    assert "Reviewer Share Kit" in markdown
    assert "not_sent" in markdown
