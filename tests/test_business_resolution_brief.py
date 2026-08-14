from scripts.build_business_resolution_brief import (
    build_business_resolution_brief,
    render_markdown,
    verify_business_resolution_brief,
)


def test_business_resolution_brief_turns_demo_into_resume_safe_business_result():
    payload = build_business_resolution_brief()
    verification = verify_business_resolution_brief(payload)
    markdown = render_markdown(payload)

    assert verification["business_resolution_brief_verified"] is True
    assert payload["dataset_context"]["contains_real_company_data"] is False
    assert payload["dataset_context"]["contains_pii"] is False
    assert payload["detected_signal_counts"]["findings"] == 5
    assert payload["detected_signal_counts"]["business_risk_areas"] == 4
    assert payload["detected_signal_counts"]["high_priority_actions"] == 3
    assert payload["detected_signal_counts"]["owner_handoffs"] == 4
    assert len(payload["resolution_steps"]) == 4
    assert "Data Engineering" in payload["owners"]
    assert "Support Operations" in payload["owners"]
    assert "Analytics Engineering" in payload["owners"]
    assert "Data Analytics" in payload["owners"]
    assert "no customer production deployment is claimed" in payload["claim_boundaries"]
    assert "Produced a verified business-resolution brief" in payload["resume_safe_result"]
    assert "Business Resolution Brief" in markdown
    assert "Next Evidence To Unlock Stronger Claim" in markdown
