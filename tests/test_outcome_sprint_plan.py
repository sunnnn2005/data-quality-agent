from scripts.build_outcome_sprint_plan import (
    build_outcome_sprint_plan,
    render_markdown,
    verify_outcome_sprint_plan,
)


def test_outcome_sprint_plan_turns_zero_outcomes_into_real_next_actions():
    payload = build_outcome_sprint_plan()
    verification = verify_outcome_sprint_plan(payload)
    markdown = render_markdown(payload)

    assert verification["outcome_sprint_plan_verified"] is True
    assert payload["sprint_day_count"] == 5
    assert payload["target_metric_count"] == 5
    assert payload["accepted_issue_count"] == 0
    assert payload["claimable_resume_metric_count"] == 0
    assert all(value == 0 for value in payload["current_public_counts"].values())
    assert payload["sprint_days"][0]["target_metric"] == "ai_engineer_review_items"
    assert payload["sprint_days"][-1]["execution_artifact"] == "docs/resume-claim-materializer.md"
    assert "real non-owner action" in payload["daily_success_rule"]
    assert "Do not add user" in payload["resume_upgrade_rule"]
    assert "# Outcome Sprint Plan" in markdown


def test_outcome_sprint_plan_does_not_fabricate_resume_outcomes():
    payload = build_outcome_sprint_plan()

    assert "zero resume upgrades" in payload["resume_safe_summary"]
    assert "No external users are claimed" in payload["not_claimed"][0]
    assert "No GitHub star growth is claimed" in payload["not_claimed"][-1]
    assert {day["current_count"] for day in payload["sprint_days"][:-1]} == {0}
