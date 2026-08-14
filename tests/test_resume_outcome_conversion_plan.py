from scripts.build_resume_outcome_conversion_plan import (
    build_resume_outcome_conversion_plan,
    render_markdown,
    verify_resume_outcome_conversion_plan,
)


def test_resume_outcome_conversion_plan_turns_blocked_claims_into_next_actions():
    payload = build_resume_outcome_conversion_plan()
    verification = verify_resume_outcome_conversion_plan(payload)
    markdown = render_markdown(payload)

    assert verification["resume_outcome_conversion_plan_verified"] is True
    assert payload["conversion_row_count"] == 6
    assert payload["claimable_now_count"] == 6
    assert payload["blocked_outcome_count"] == 6
    assert payload["one_click_evidence_url"].endswith("/one-click-evidence-links.html")
    assert {item["metric"] for item in payload["conversion_rows"]} == {
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "github_stars",
    }
    assert all(item["current_count"] == 0 for item in payload["conversion_rows"])
    assert all(item["status"] == "blocked_until_public_evidence" for item in payload["conversion_rows"])
    ai_review = next(item for item in payload["conversion_rows"] if item["metric"] == "ai_engineer_review_items")
    assert "AI engineer" in ai_review["reviewer_profile"]
    assert payload["one_click_evidence_url"] in ai_review["copy_ready_message"]
    github_stars = next(item for item in payload["conversion_rows"] if item["metric"] == "github_stars")
    assert "only if the project is useful" in github_stars["copy_ready_message"]
    assert "outreach attempts alone do not count" in payload["execution_rule"].lower()
    assert "zero upgraded outcome claims" in payload["resume_safe_summary"]
    assert "Conversion Queue" in markdown
    assert "Copy-Ready Asks" in markdown
