from scripts.build_reviewer_action_queue import (
    build_reviewer_action_queue,
    render_markdown,
    verify_reviewer_action_queue,
)


def test_reviewer_action_queue_turns_traction_goal_into_countable_public_tasks():
    payload = build_reviewer_action_queue()
    verification = verify_reviewer_action_queue(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_action_queue_verified"] is True
    assert payload["queue_count"] == 9
    assert payload["not_contacted_count"] == 9
    assert payload["evidence_goal_count"] == 6
    assert payload["status_counts"]["contacted"] == 0
    assert payload["status_counts"]["completed"] == 0
    assert payload["resume_status"] == "outreach_queue_ready_not_claimable"
    assert set(payload["evidence_goals"]) == {
        "external_feedback_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "accepted_real_model_runs",
    }
    assert all(task["status"] == "not_contacted" for task in payload["tasks"])
    assert all("github.com/sunnnn2005/data-quality-agent" in task["submission_url"] for task in payload["tasks"])
    assert all("raw customer data" in task["privacy_boundary"].lower() for task in payload["tasks"])
    assert "zero contacted or completed reviewers" in payload["resume_safe_summary"]
    assert "active users" in payload["blocked_resume_claims"]
    assert "accepted real-model LLM runs" in payload["blocked_resume_claims"]
    assert "Reviewer Action Queue" in markdown
    assert "UC Davis data science peer" in markdown
    assert "real_model_run_evidence" in markdown
