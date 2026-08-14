from scripts.build_resume_outcome_metrics import (
    build_resume_outcome_metrics,
    render_markdown,
    verify_resume_outcome_metrics,
)


def test_resume_outcome_metrics_blocks_unproven_outcome_claims():
    payload = build_resume_outcome_metrics()
    verification = verify_resume_outcome_metrics(payload)
    markdown = render_markdown(payload)

    assert verification["resume_outcome_metrics_verified"] is True
    assert payload["tracked_outcome_count"] == 7
    assert payload["claimable_outcome_count"] == 0
    assert payload["blocked_outcome_count"] == 7
    assert payload["claimable_resume_lines"] == []
    assert {item["metric"] for item in payload["tracked_outcomes"]} == {
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "github_stars",
        "accepted_real_model_runs",
    }
    assert all(item["current_count"] == 0 for item in payload["tracked_outcomes"])
    assert all(item["resume_status"] == "not_claimable_yet" for item in payload["tracked_outcomes"])
    assert payload["outreach_readiness"]["ready_message_count"] == 9
    assert payload["outreach_readiness"]["not_sent_count"] == 9
    assert payload["public_interest_signals"]["github_forks"] == 1
    assert "GitHub traffic is treated as repository interest, not as users." in payload["not_claimed"]
    assert "No accepted real-model LLM run is claimed while accepted_real_model_runs is zero." in payload["not_claimed"]
    assert "Resume Outcome Metrics" in markdown
    assert "Blocked Resume Lines" in markdown
