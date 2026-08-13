from scripts.build_live_project_scorecard import (
    build_live_project_scorecard_payload,
    render_markdown,
    verify_live_project_scorecard,
)


def test_live_project_scorecard_summarizes_public_resume_evidence_without_inflation():
    payload = build_live_project_scorecard_payload()
    verification = verify_live_project_scorecard(payload)
    markdown = render_markdown(payload)

    assert verification["live_project_scorecard_verified"] is True
    assert payload["headline_metrics"]["passing_tests"] == 73
    assert payload["headline_metrics"]["verified_resume_claims"] == 32
    assert payload["headline_metrics"]["implemented_agent_capabilities"] == 15
    assert payload["live_footprint"]["stars"] == 0
    assert payload["live_footprint"]["confirmed_external_users"] == 0
    assert all(payload["claim_coverage"].values())
    assert "Live Project Scorecard" in markdown
