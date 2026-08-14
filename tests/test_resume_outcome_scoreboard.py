from scripts.build_resume_outcome_scoreboard import (
    build_resume_outcome_scoreboard,
    render_markdown,
    verify_resume_outcome_scoreboard,
)


def test_resume_outcome_scoreboard_separates_claimable_and_locked_outcomes():
    payload = build_resume_outcome_scoreboard()
    verification = verify_resume_outcome_scoreboard(payload)
    markdown = render_markdown(payload)

    assert verification["resume_outcome_scoreboard_verified"] is True
    assert payload["claimable_now_count"] == 3
    assert payload["blocked_outcome_count"] == 6
    assert payload["reviewer_funnel"]["remaining_evidence_items"] == 7
    assert payload["current_public_counts"]["github_forks"] == 1
    assert payload["current_public_counts"]["github_stars"] == 0
    assert payload["current_public_counts"]["confirmed_external_users"] == 0
    assert payload["current_public_counts"]["external_feedback_items"] == 0
    assert payload["current_public_counts"]["business_case_feedback_items"] == 0
    assert {item["metric"] for item in payload["blocked_outcomes"]} == {
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "github_stars",
    }
    assert "tool calling" in payload["claimable_now"][2]["resume_line"]
    assert "guardrails" in payload["claimable_now"][2]["resume_line"]
    assert "structured output" in payload["claimable_now"][2]["resume_line"]
    assert "Locked Until Public Evidence" in markdown
    assert "external users" in payload["not_claimed"]
