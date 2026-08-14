from scripts.build_reviewer_outreach_execution_pack import (
    build_reviewer_outreach_execution_pack,
    render_markdown,
    verify_reviewer_outreach_execution_pack,
)


def test_reviewer_outreach_execution_pack_makes_queue_sendable_without_claiming_results():
    payload = build_reviewer_outreach_execution_pack()
    verification = verify_reviewer_outreach_execution_pack(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_outreach_execution_pack_verified"] is True
    assert payload["outreach_item_count"] == 9
    assert payload["ready_message_count"] == 9
    assert payload["follow_up_rule_count"] == 9
    assert payload["evidence_goal_count"] == 6
    assert payload["send_status_counts"] == {
        "not_sent": 9,
        "sent": 0,
        "completed": 0,
    }
    assert payload["resume_status"] == "ready_to_send_not_claimable"
    assert all(item["send_status"] == "not_sent" for item in payload["outreach_items"])
    assert all("{name}" in item["ready_to_send_message"] for item in payload["outreach_items"])
    assert all("permission" in item["ready_to_send_message"].lower() for item in payload["outreach_items"])
    assert all("raw customer data" in item["ready_to_send_message"].lower() for item in payload["outreach_items"])
    assert all("github.com/sunnnn2005/data-quality-agent" in item["submission_url"] for item in payload["outreach_items"])
    assert "zero sent or completed outreach claimed" in payload["resume_safe_summary"]
    assert "Reviewer Outreach Execution Pack" in markdown
    assert "Manual Execution Rules" in markdown
