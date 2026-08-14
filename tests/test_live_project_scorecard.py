from scripts.build_live_project_scorecard import (
    load_json,
    OUTCOME_EVIDENCE_PATH,
    build_live_project_scorecard_payload,
    render_markdown,
    verify_live_project_scorecard,
)


def test_live_project_scorecard_summarizes_public_resume_evidence_without_inflation():
    payload = build_live_project_scorecard_payload()
    verification = verify_live_project_scorecard(payload)
    markdown = render_markdown(payload)

    assert verification["live_project_scorecard_verified"] is True
    assert payload["headline_metrics"]["passing_tests"] == 243
    assert payload["headline_metrics"]["verified_resume_claims"] == len(load_json(OUTCOME_EVIDENCE_PATH)["claims"])
    assert len(payload["reviewer_paths"]) == 23
    assert any(path["label"] == "Inspect accepted evidence rollup" for path in payload["reviewer_paths"])
    assert payload["headline_metrics"]["implemented_agent_capabilities"] == 16
    assert payload["headline_metrics"]["agent_matrix_implemented_capabilities"] == 13
    assert payload["live_footprint"]["stars"] == 0
    assert payload["live_footprint"]["confirmed_external_users"] == 0
    assert all(payload["claim_coverage"].values())
    assert payload["claim_coverage"]["has_agent_capability_matrix"] is True
    assert payload["claim_coverage"]["has_business_data_replay_packet"] is True
    assert payload["claim_coverage"]["has_business_replay_demo"] is True
    assert payload["claim_coverage"]["has_real_model_runbook"] is True
    assert payload["claim_coverage"]["has_real_model_evidence_capture"] is True
    assert payload["claim_coverage"]["has_pilot_conversion_board"] is True
    assert payload["claim_coverage"]["has_resume_outcome_readiness"] is True
    assert payload["claim_coverage"]["has_reviewer_funnel_board"] is True
    assert payload["claim_coverage"]["has_external_run_quickstart"] is True
    assert payload["claim_coverage"]["has_external_reviewer_outreach_tracker"] is True
    assert payload["claim_coverage"]["has_external_reviewer_evidence_gate"] is True
    assert payload["claim_coverage"]["has_business_impact_ledger"] is True
    assert payload["claim_coverage"]["has_reviewer_evidence_kit"] is True
    assert any(path["label"] == "Inspect impact review packet" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect business problem casebook" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect public traction dashboard" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect feedback intake quality" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect business-data replay packet" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect business replay demo" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect real-model runbook" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect real-model evidence capture" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect agent capability matrix" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Run the local reviewer demo" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Use external run quickstart" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Use external reviewer outreach tracker" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect external reviewer evidence gate" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Inspect business impact ledger" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Use reviewer evidence kit" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Use external run evidence packet" for path in payload["reviewer_paths"])
    assert any(path["label"] == "Use reviewer funnel board" for path in payload["reviewer_paths"])
    assert "Live Project Scorecard" in markdown
