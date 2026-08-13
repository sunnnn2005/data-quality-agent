from scripts.build_business_problem_casebook import (
    build_business_problem_casebook_payload,
    render_markdown,
    verify_business_problem_casebook,
)


def test_business_problem_casebook_explains_enterprise_problem_without_usage_claims():
    payload = build_business_problem_casebook_payload()
    verification = verify_business_problem_casebook(payload)
    markdown = render_markdown(payload)

    assert verification["business_problem_casebook_verified"] is True
    assert payload["business_case_count"] == 1
    assert payload["detected_risk_count"] == 4
    assert payload["owner_handoff_count"] == 4
    assert payload["evidence_link_count"] == 5
    assert payload["casebook"][0]["agent_outputs"]["finding_count"] == 5
    assert payload["casebook"][0]["agent_outputs"]["root_cause_hypothesis_count"] == 3
    assert "real customer dataset" in payload["not_claimed"]
    assert "Business Problem Casebook" in markdown
    assert "Detected Business Risks" in markdown
