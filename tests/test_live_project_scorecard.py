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
    assert payload["headline_metrics"]["passing_tests"] == 87
    assert payload["headline_metrics"]["verified_resume_claims"] == 46
    assert payload["headline_metrics"]["implemented_agent_capabilities"] == 16
    assert payload["live_footprint"]["stars"] == 0
    assert payload["live_footprint"]["confirmed_external_users"] == 0
    assert all(payload["claim_coverage"].values())
    assert any(path["label"] == "Inspect impact review packet" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect business problem casebook" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect public traction dashboard" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect feedback intake quality" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Run the local reviewer demo" for path in payload["reviewer_paths"])
    assert "Live Project Scorecard" in markdown
