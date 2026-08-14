from scripts.build_real_reviewer_outreach_playbook import (
    build_real_reviewer_outreach_playbook,
    render_markdown,
    verify_real_reviewer_outreach_playbook,
)


def test_real_reviewer_outreach_playbook_turns_zero_baseline_into_next_sends():
    payload = build_real_reviewer_outreach_playbook()
    verification = verify_real_reviewer_outreach_playbook(payload)
    markdown = render_markdown(payload)

    assert verification["real_reviewer_outreach_playbook_verified"] is True
    assert payload["first_action"]["metric"] == "ai_engineer_review_items"
    assert payload["first_action"]["slot_id"] == "review_slot_07"
    assert payload["contact_pool_count"] == 5
    assert payload["outreach_step_count"] == 5
    assert {step["target_metric"] for step in payload["outreach_steps"]} == {
        "ai_engineer_review_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "external_feedback_items",
    }
    assert all(step["resume_outcome_after_send"] is False for step in payload["outreach_steps"])
    assert "sent message is only distribution evidence" in payload["counting_policy"].lower()
    assert "# Real Reviewer Outreach Playbook" in markdown
    assert "Record after a real send" in markdown
