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
    assert payload["public_metrics"]["test_count"] == 85
    assert payload["verified_project_outcomes"]["root_cause_hypotheses"] == 3
    assert payload["verified_project_outcomes"]["business_risk_areas"] == 4
    assert payload["verified_project_outcomes"]["high_priority_actions"] == 3
    assert payload["verified_project_outcomes"]["owner_handoffs"] == 4
    assert payload["verified_project_outcomes"]["eval_scenarios"] == 3
    assert payload["verified_project_outcomes"]["hypothesis_feedback_labels"] == 3
    assert payload["verified_project_outcomes"]["incident_pattern_count"] == 3
    assert payload["verified_project_outcomes"]["observed_trace_count"] == 2
    assert payload["verified_project_outcomes"]["fallback_event_count"] == 2
    assert payload["verified_project_outcomes"]["model_telemetry_artifact"] == 1
    assert payload["verified_project_outcomes"]["mock_model_calls"] == 2
    assert payload["verified_project_outcomes"]["mock_model_tokens"] == 360
    assert payload["verified_project_outcomes"]["tool_allowlist_count"] == 7
    assert payload["verified_project_outcomes"]["postgres_rejected_write_query_count"] == 3
    assert payload["verified_project_outcomes"]["verifier_rule_count"] == 6
    assert payload["verified_project_outcomes"]["local_reviewer_demo"] == 1
    assert payload["verified_project_outcomes"]["local_reviewer_seeded_rows"] == 8
    assert payload["verified_project_outcomes"]["local_reviewer_routes"] == 3
    assert payload["verified_project_outcomes"]["api_smoke_report"] == 1
    assert payload["verified_project_outcomes"]["api_smoke_checks"] == 6
    assert payload["verified_project_outcomes"]["api_smoke_passed_checks"] == 6
    assert payload["verified_project_outcomes"]["performance_baseline"] == 1
    assert payload["verified_project_outcomes"]["performance_benchmark_count"] == 2
    assert payload["verified_project_outcomes"]["performance_measured_endpoint_calls"] == 24
    assert payload["verified_project_outcomes"]["demo_usage_baseline"] == 1
    assert payload["verified_project_outcomes"]["demo_usage_tracked_funnel_steps"] == 5
    assert payload["verified_project_outcomes"]["demo_usage_entrypoints_verified"] == 4
    assert payload["verified_project_outcomes"]["business_data_intake_baseline"] == 1
    assert payload["verified_project_outcomes"]["business_data_intake_endpoints"] == 4
    assert payload["verified_project_outcomes"]["business_data_intake_tests"] == 6
    assert payload["verified_project_outcomes"]["business_data_intake_max_rows"] == 10_000
    assert payload["verified_project_outcomes"]["business_data_intake_max_columns"] == 80
    assert payload["verified_project_outcomes"]["community_growth_baseline"] == 1
    assert payload["verified_project_outcomes"]["community_issue_templates"] == 4
    assert payload["verified_project_outcomes"]["community_labels"] == 5
    assert payload["verified_project_outcomes"]["community_public_growth_channels"] == 5
    assert payload["verified_project_outcomes"]["impact_review_packet"] == 1
    assert payload["verified_project_outcomes"]["impact_review_business_metrics"] == 12
    assert payload["verified_project_outcomes"]["impact_review_evidence_links"] == 8
    assert payload["verified_project_outcomes"]["public_traction_dashboard"] == 1
    assert payload["verified_project_outcomes"]["public_traction_surfaces"] == 4
    assert payload["verified_project_outcomes"]["public_traction_growth_channels"] == 12
    assert payload["verified_project_outcomes"]["public_traction_resume_upgrade_rules"] == 3
    assert payload["verified_project_outcomes"]["live_project_scorecard"] == 1
    assert payload["verified_project_outcomes"]["scorecard_reviewer_paths"] == 8
    assert payload["verified_project_outcomes"]["openapi_required_endpoints"] == 6
    assert payload["verified_project_outcomes"]["recruiter_pitch_resume_bullets"] == 3
    assert payload["verified_project_outcomes"]["recruiter_pitch_target_roles"] == 4
    assert payload["verified_project_outcomes"]["application_evidence_pack"] == 1
    assert payload["verified_project_outcomes"]["application_evidence_links"] == 10
    assert payload["verified_project_outcomes"]["pilot_outreach_messages"] == 3
    assert payload["verified_project_outcomes"]["pilot_review_paths"] == 7
    assert payload["verified_project_outcomes"]["pilot_program_segments"] == 3
    assert payload["verified_project_outcomes"]["pilot_program_weeks"] == 3
    assert payload["verified_project_outcomes"]["recommended_actions"] == 5
    assert payload["verified_project_outcomes"]["implemented_agent_capabilities"] == 16
    assert "3-scenario agent evaluation harness" in payload["resume_safe_signals"]
    assert "3 human-reviewed root-cause feedback labels" in payload["resume_safe_signals"]
    assert "3 recurring incident patterns retrieved from sanitized traces" in payload["resume_safe_signals"]
    assert "2 observed run traces with fallback and verification status" in payload["resume_safe_signals"]
    assert "2 mocked LLM calls with 360 tokens, prompt version, latency, retry budget, and estimated cost telemetry" in payload["resume_safe_signals"]
    assert (
        "4 business risk areas mapped to 3 high-priority actions and 4 owner handoffs"
        in payload["resume_safe_signals"]
    )
    assert "7 allowed agent tools and 3 rejected unsafe PostgreSQL queries" in payload["resume_safe_signals"]
    assert (
        "Local Docker Compose reviewer demo with 8 seeded PostgreSQL rows and 3 review paths"
        in payload["resume_safe_signals"]
    )
    assert "CI-verified API smoke report covering 6 passing FastAPI route checks" in payload["resume_safe_signals"]
    assert (
        "CI-verified local performance baseline covering 2 route benchmarks and 24 measured endpoint calls"
        in payload["resume_safe_signals"]
    )
    assert (
        "Public demo usage baseline with 5 tracked funnel steps and 4 verified entrypoints"
        in payload["resume_safe_signals"]
    )
    assert (
        "Business-data intake baseline covering 4 integration endpoints, 6 API tests, and bounded CSV uploads up to 10000 rows / 80 columns"
        in payload["resume_safe_signals"]
    )
    assert (
        "Community growth baseline with 4 issue templates, 5 configured labels, and 5 public contribution or feedback channels"
        in payload["resume_safe_signals"]
    )
    assert (
        "Impact review packet with 12 verified business metrics, 8 evidence links, 5 remediation actions, and 4 owner handoffs"
        in payload["resume_safe_signals"]
    )
    assert (
        "Public traction dashboard with 4 live project surfaces, 12 growth or review channels, 5 tracked funnel steps, and 3 resume upgrade rules"
        in payload["resume_safe_signals"]
    )
    assert "8 reviewer paths in a CI-verified live project scorecard" in payload["resume_safe_signals"]
    assert "CI-verified OpenAPI contract covering 6 integration endpoints" in payload["resume_safe_signals"]
    assert "3 recruiter-safe resume bullets for 4 target roles" in payload["resume_safe_signals"]
    assert "10 application evidence links in a recruiter-ready evidence pack" in payload["resume_safe_signals"]
    assert "3 pilot outreach messages and 7 review paths for collecting real feedback" in payload["resume_safe_signals"]
    assert "3 pilot participant segments across a 3-week feedback plan" in payload["resume_safe_signals"]
    assert "Dataset-level memory retrieval over recent sanitized traces" in payload["resume_safe_signals"]
    assert "Do not claim external users" in payload["resume_policy"]
    assert "Confirmed external users | 0" in markdown
    assert "GitHub stars beyond the current public count" in markdown
