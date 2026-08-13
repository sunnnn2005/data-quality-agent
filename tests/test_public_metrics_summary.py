from scripts.build_public_metrics_summary import (
    build_public_metrics_summary,
    render_markdown,
    verify_public_metrics_summary,
)


def test_public_metrics_summary_keeps_resume_metrics_honest():
    payload = build_public_metrics_summary()
    verification = verify_public_metrics_summary(payload)
    markdown = render_markdown(payload)

    assert verification["public_metrics_summary_verified"] is True
    assert payload["public_metrics"]["stars"] == 0
    assert payload["public_metrics"]["forks"] == 1
    assert payload["public_metrics"]["test_count"] == 66
    assert payload["verified_project_outcomes"]["root_cause_hypotheses"] == 3
    assert payload["verified_project_outcomes"]["eval_scenarios"] == 3
    assert payload["verified_project_outcomes"]["hypothesis_feedback_labels"] == 3
    assert payload["verified_project_outcomes"]["incident_pattern_count"] == 3
    assert payload["verified_project_outcomes"]["observed_trace_count"] == 2
    assert payload["verified_project_outcomes"]["fallback_event_count"] == 2
    assert payload["verified_project_outcomes"]["tool_allowlist_count"] == 5
    assert payload["verified_project_outcomes"]["postgres_rejected_write_query_count"] == 3
    assert payload["verified_project_outcomes"]["verifier_rule_count"] == 6
    assert payload["verified_project_outcomes"]["openapi_required_endpoints"] == 6
    assert payload["verified_project_outcomes"]["recommended_actions"] == 5
    assert payload["verified_project_outcomes"]["implemented_agent_capabilities"] == 14
    assert "3-scenario agent evaluation harness" in payload["resume_safe_signals"]
    assert "3 human-reviewed root-cause feedback labels" in payload["resume_safe_signals"]
    assert "3 recurring incident patterns retrieved from sanitized traces" in payload["resume_safe_signals"]
    assert "2 observed run traces with fallback and verification status" in payload["resume_safe_signals"]
    assert "5 allowed agent tools and 3 rejected unsafe PostgreSQL queries" in payload["resume_safe_signals"]
    assert "CI-verified OpenAPI contract covering 6 integration endpoints" in payload["resume_safe_signals"]
    assert "Dataset-level memory retrieval over recent sanitized traces" in payload["resume_safe_signals"]
    assert "Do not claim external users" in payload["resume_policy"]
    assert "Confirmed external users | 0" in markdown
    assert "GitHub stars beyond the current public count" in markdown
