from scripts.build_outcome_summary import build_outcome_summary_payload, render_markdown, verify_outcome_summary


def test_outcome_summary_is_derived_from_business_impact_artifact():
    payload = build_outcome_summary_payload()
    verification = verify_outcome_summary(payload)
    markdown = render_markdown(payload)

    assert verification["outcome_summary_verified"] is True
    assert payload["verified_outcomes"]["issue_category_count"] == 4
    assert payload["verified_outcomes"]["recommended_action_count"] == 5
    assert len(payload["issue_categories"]) == 4
    assert "Support operations dashboard data" in payload["business_problem"]
    assert "External users" not in markdown
    assert "No verified external users yet." in markdown
