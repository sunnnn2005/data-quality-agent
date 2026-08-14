from scripts.build_resume_outcome_action_checklist import (
    build_resume_outcome_action_checklist,
    render_markdown,
    verify_resume_outcome_action_checklist,
)


def test_resume_outcome_action_checklist_turns_blocked_outcomes_into_next_actions():
    payload = build_resume_outcome_action_checklist()
    verification = verify_resume_outcome_action_checklist(payload)
    markdown = render_markdown(payload)

    assert verification["resume_outcome_action_checklist_verified"] is True
    assert payload["tracked_action_count"] == 6
    assert payload["next_action_needed_count"] == 6
    assert payload["claimable_action_count"] == 0
    assert payload["accepted_public_issue_count"] == 0
    assert payload["outreach_slot_count"] == 9
    assert payload["not_sent_outreach_count"] == 9
    assert {action["id"] for action in payload["actions"]} == {
        "capture_first_real_model_run",
        "send_first_reviewer_request",
        "collect_first_public_run_issue",
        "collect_ai_engineer_review",
        "collect_business_case",
        "earn_first_star",
    }
    assert payload["actions"][0]["id"] == "capture_first_real_model_run"
    assert payload["actions"][0]["target_metric"] == "accepted_real_model_runs"
    assert "tokens" in payload["actions"][0]["completion_check"]
    assert "Resume Outcome Action Checklist" in markdown
    assert "Not claimable yet" in markdown
