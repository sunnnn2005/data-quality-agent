from scripts.build_first_10_reviewer_sprint import (
    build_first_10_reviewer_sprint,
    render_markdown,
    verify_first_10_reviewer_sprint,
)


def test_first_10_reviewer_sprint_maps_real_outcome_goals_without_claiming_them():
    payload = build_first_10_reviewer_sprint()
    verification = verify_first_10_reviewer_sprint(payload)
    markdown = render_markdown(payload)

    assert verification["first_10_reviewer_sprint_verified"] is True
    assert payload["slot_count"] == 10
    assert payload["not_sent_count"] == 10
    assert payload["completed_count"] == 0
    assert payload["target_metric_count"] == 6
    assert payload["resume_status"] == "first_10_sprint_ready_not_claimable"
    assert set(payload["target_counts"]) == {
        "external_feedback_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "github_stars",
    }
    assert all(value == 0 for value in payload["current_counts"].values())
    assert all(slot["status"] == "not_sent" for slot in payload["slots"])
    assert all("permission" in slot["counts_only_after"].lower() for slot in payload["slots"])
    assert all(
        slot["submission_url"].startswith("https://github.com/sunnnn2005/data-quality-agent")
        for slot in payload["slots"]
    )
    assert "zero sent outreach" in payload["resume_safe_summary"]
    assert "GitHub star growth" in payload["blocked_resume_claims"]
    assert "First 10 Reviewer Sprint" in markdown
    assert "slot_07_ai_engineer_review" in markdown
    assert "slot_09_public_star_if_useful" in markdown
