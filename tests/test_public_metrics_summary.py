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
    assert payload["public_metrics"]["test_count"] == 155
    assert payload["public_metrics"]["github_view_count"] >= 0
    assert payload["public_metrics"]["github_unique_visitors"] <= payload["public_metrics"]["github_view_count"]
    assert payload["public_metrics"]["github_clone_count"] >= 0
    assert payload["public_metrics"]["github_unique_cloners"] <= payload["public_metrics"]["github_clone_count"]
    assert payload["public_metrics"]["available_public_endpoints"] <= payload["public_metrics"]["public_endpoint_count"]
    assert (
        payload["public_metrics"]["successful_main_branch_workflows"]
        <= payload["public_metrics"]["main_branch_workflow_count"]
    )
    assert payload["verified_project_outcomes"]["root_cause_hypotheses"] == 3
    assert payload["verified_project_outcomes"]["business_risk_areas"] == 4
    assert payload["verified_project_outcomes"]["high_priority_actions"] == 3
    assert payload["verified_project_outcomes"]["owner_handoffs"] == 4
    assert payload["verified_project_outcomes"]["eval_scenarios"] == 14
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
    assert payload["verified_project_outcomes"]["agent_capability_matrix"] == 1
    assert payload["verified_project_outcomes"]["agent_matrix_implemented_capabilities"] == 13
    assert payload["verified_project_outcomes"]["agent_matrix_partial_capabilities"] == 4
    assert payload["verified_project_outcomes"]["agent_matrix_not_claimed_count"] == 1
    assert payload["verified_project_outcomes"]["local_reviewer_demo"] == 1
    assert payload["verified_project_outcomes"]["local_reviewer_seeded_rows"] == 8
    assert payload["verified_project_outcomes"]["local_reviewer_routes"] == 3
    assert payload["verified_project_outcomes"]["runnable_release_packet"] == 1
    assert payload["verified_project_outcomes"]["runnable_release_surfaces"] == 3
    assert payload["verified_project_outcomes"]["runnable_release_acceptance_checks"] == 4
    assert payload["verified_project_outcomes"]["runnable_release_required_api_paths"] == 6
    assert payload["verified_project_outcomes"]["external_run_evidence_packet"] == 1
    assert payload["verified_project_outcomes"]["external_run_review_paths"] == 3
    assert payload["verified_project_outcomes"]["external_run_submission_fields"] == 8
    assert payload["verified_project_outcomes"]["external_run_upgrade_rules"] == 3
    assert payload["verified_project_outcomes"]["external_reviewer_request_pack"] == 1
    assert payload["verified_project_outcomes"]["external_reviewer_request_messages"] == 3
    assert payload["verified_project_outcomes"]["external_reviewer_request_run_paths"] == 3
    assert payload["verified_project_outcomes"]["external_reviewer_request_fields"] == 8
    assert payload["verified_project_outcomes"]["external_run_quickstart_page"] == 1
    assert payload["verified_project_outcomes"]["external_run_quickstart_paths"] == 3
    assert payload["verified_project_outcomes"]["external_run_quickstart_fields"] == 8
    assert payload["verified_project_outcomes"]["external_reviewer_outreach_tracker"] == 1
    assert payload["verified_project_outcomes"]["external_reviewer_outreach_queue"] == 3
    assert payload["verified_project_outcomes"]["external_reviewer_outreach_not_contacted"] == 3
    assert payload["verified_project_outcomes"]["external_reviewer_outreach_source_messages"] == 3
    assert payload["verified_project_outcomes"]["external_reviewer_evidence_gate"] == 1
    assert payload["verified_project_outcomes"]["external_reviewer_gate_rules"] == 8
    assert payload["verified_project_outcomes"]["external_reviewer_gate_collected_issues"] >= 0
    assert payload["verified_project_outcomes"]["external_reviewer_gate_accepted_issues"] == 0
    assert payload["verified_project_outcomes"]["external_reviewer_gate_linked_queue"] == 3
    assert payload["verified_project_outcomes"]["accepted_evidence_rollup"] == 1
    assert payload["verified_project_outcomes"]["accepted_evidence_rollup_claimable_metrics"] == 5
    assert payload["verified_project_outcomes"]["accepted_evidence_rollup_accepted_issues"] == 0
    assert payload["verified_project_outcomes"]["accepted_evidence_rollup_blocked_claims"] == 5
    assert payload["verified_project_outcomes"]["business_impact_ledger"] == 1
    assert payload["verified_project_outcomes"]["business_impact_ledger_accepted_signals"] == 0
    assert payload["verified_project_outcomes"]["reviewer_evidence_kit"] == 1
    assert payload["verified_project_outcomes"]["reviewer_evidence_forms"] == 5
    assert payload["verified_project_outcomes"]["reviewer_evidence_script_steps"] == 5
    assert payload["verified_project_outcomes"]["resume_traction_proof"] == 1
    assert payload["verified_project_outcomes"]["resume_traction_claimable_now"] == 6
    assert payload["verified_project_outcomes"]["resume_traction_future_claims"] == 4
    assert payload["verified_project_outcomes"]["resume_traction_blocked_claims"] == 5
    assert payload["verified_project_outcomes"]["reviewer_action_queue"] == 1
    assert payload["verified_project_outcomes"]["reviewer_action_tasks"] == 8
    assert payload["verified_project_outcomes"]["reviewer_action_evidence_goals"] == 5
    assert payload["verified_project_outcomes"]["reviewer_action_not_contacted"] == 8
    assert payload["verified_project_outcomes"]["reviewer_outreach_execution_pack"] == 1
    assert payload["verified_project_outcomes"]["reviewer_outreach_ready_messages"] == 8
    assert payload["verified_project_outcomes"]["reviewer_outreach_follow_up_rules"] == 8
    assert payload["verified_project_outcomes"]["reviewer_outreach_not_sent"] == 8
    assert payload["verified_project_outcomes"]["reviewer_outreach_status_board"] == 1
    assert payload["verified_project_outcomes"]["reviewer_outreach_status_slots"] == 8
    assert payload["verified_project_outcomes"]["reviewer_outreach_status_stages"] == 5
    assert payload["verified_project_outcomes"]["reviewer_outreach_status_not_sent"] == 8
    assert payload["verified_project_outcomes"]["reviewer_outreach_status_accepted_evidence"] == 0
    assert payload["verified_project_outcomes"]["resume_outcome_metrics"] == 1
    assert payload["verified_project_outcomes"]["resume_outcome_metrics_tracked"] == 6
    assert payload["verified_project_outcomes"]["resume_outcome_metrics_claimable"] == 0
    assert payload["verified_project_outcomes"]["resume_outcome_metrics_blocked"] == 6
    assert payload["verified_project_outcomes"]["resume_outcome_action_checklist"] == 1
    assert payload["verified_project_outcomes"]["resume_outcome_action_count"] == 5
    assert payload["verified_project_outcomes"]["resume_outcome_next_actions_needed"] == 5
    assert payload["verified_project_outcomes"]["resume_outcome_action_accepted_public_evidence"] == 0
    assert payload["verified_project_outcomes"]["reviewer_submission_hub"] == 1
    assert payload["verified_project_outcomes"]["reviewer_submission_paths"] == 6
    assert payload["verified_project_outcomes"]["reviewer_submission_target_metrics"] == 6
    assert payload["verified_project_outcomes"]["reviewer_submission_required_fields"] == 24
    assert payload["verified_project_outcomes"]["first_10_reviewer_sprint"] == 1
    assert payload["verified_project_outcomes"]["first_10_reviewer_slots"] == 10
    assert payload["verified_project_outcomes"]["first_10_reviewer_issue_launch_drafts"] == 10
    assert payload["verified_project_outcomes"]["first_10_reviewer_public_issue_entrypoints"] == 10
    assert payload["verified_project_outcomes"]["first_10_reviewer_target_metrics"] == 6
    assert payload["verified_project_outcomes"]["first_10_reviewer_not_sent"] == 10
    assert payload["verified_project_outcomes"]["first_10_reviewer_completed"] == 0
    assert payload["verified_project_outcomes"]["first_10_outreach_execution_log"] == 1
    assert payload["verified_project_outcomes"]["first_10_outreach_messages"] == 10
    assert payload["verified_project_outcomes"]["first_10_outreach_public_issue_entrypoints"] == 10
    assert payload["verified_project_outcomes"]["first_10_outreach_not_sent"] == 10
    assert payload["verified_project_outcomes"]["first_10_outreach_accepted_evidence"] == 0
    assert payload["verified_project_outcomes"]["outcome_collection_page"] == 1
    assert payload["verified_project_outcomes"]["outcome_collection_actions"] == 5
    assert payload["verified_project_outcomes"]["outcome_collection_submission_paths"] == 6
    assert payload["verified_project_outcomes"]["outcome_collection_evidence_fields"] == 24
    assert payload["verified_project_outcomes"]["public_reviewer_call"] == 1
    assert payload["verified_project_outcomes"]["public_reviewer_call_segments"] == 3
    assert payload["verified_project_outcomes"]["public_reviewer_call_submission_paths"] == 6
    assert payload["verified_project_outcomes"]["public_reviewer_call_outreach_tasks"] == 8
    assert payload["verified_project_outcomes"]["public_reviewer_call_evidence_fields"] == 24
    assert payload["verified_project_outcomes"]["api_smoke_report"] == 1
    assert payload["verified_project_outcomes"]["api_smoke_checks"] == 6
    assert payload["verified_project_outcomes"]["api_smoke_passed_checks"] == 6
    assert payload["verified_project_outcomes"]["performance_baseline"] == 1
    assert payload["verified_project_outcomes"]["performance_benchmark_count"] == 2
    assert payload["verified_project_outcomes"]["performance_measured_endpoint_calls"] == 24
    assert payload["verified_project_outcomes"]["demo_usage_baseline"] == 1
    assert payload["verified_project_outcomes"]["demo_usage_tracked_funnel_steps"] == 5
    assert payload["verified_project_outcomes"]["demo_usage_entrypoints_verified"] == 6
    assert payload["verified_project_outcomes"]["business_data_intake_baseline"] == 1
    assert payload["verified_project_outcomes"]["business_data_intake_endpoints"] == 4
    assert payload["verified_project_outcomes"]["business_data_intake_tests"] == 6
    assert payload["verified_project_outcomes"]["business_data_intake_max_rows"] == 10_000
    assert payload["verified_project_outcomes"]["business_data_intake_max_columns"] == 80
    assert payload["verified_project_outcomes"]["community_growth_baseline"] == 1
    assert payload["verified_project_outcomes"]["community_issue_templates"] == 8
    assert payload["verified_project_outcomes"]["community_labels"] == 10
    assert payload["verified_project_outcomes"]["community_public_growth_channels"] == 9
    assert payload["verified_project_outcomes"]["impact_review_packet"] == 1
    assert payload["verified_project_outcomes"]["impact_review_business_metrics"] == 12
    assert payload["verified_project_outcomes"]["impact_review_evidence_links"] == 8
    assert payload["verified_project_outcomes"]["business_problem_casebook"] == 1
    assert payload["verified_project_outcomes"]["business_problem_cases"] == 1
    assert payload["verified_project_outcomes"]["business_problem_detected_risks"] == 4
    assert payload["verified_project_outcomes"]["business_problem_owner_handoffs"] == 4
    assert payload["verified_project_outcomes"]["business_resolution_brief"] == 1
    assert payload["verified_project_outcomes"]["business_resolution_findings"] == 5
    assert payload["verified_project_outcomes"]["business_resolution_risk_areas"] == 4
    assert payload["verified_project_outcomes"]["business_resolution_high_priority_actions"] == 3
    assert payload["verified_project_outcomes"]["business_resolution_owner_handoffs"] == 4
    assert payload["verified_project_outcomes"]["public_traction_dashboard"] == 1
    assert payload["verified_project_outcomes"]["public_traction_surfaces"] == 4
    assert payload["verified_project_outcomes"]["public_traction_growth_channels"] == 19
    assert payload["verified_project_outcomes"]["public_traction_resume_upgrade_rules"] == 3
    assert payload["verified_project_outcomes"]["github_traffic_snapshot"] == 1
    assert payload["verified_project_outcomes"]["public_availability_snapshot"] == 1
    assert payload["verified_project_outcomes"]["public_availability_endpoint_count"] == 4
    assert payload["verified_project_outcomes"]["live_project_scorecard"] == 1
    assert payload["verified_project_outcomes"]["scorecard_reviewer_paths"] == 23
    assert payload["verified_project_outcomes"]["openapi_required_endpoints"] == 6
    assert payload["verified_project_outcomes"]["recruiter_pitch_resume_bullets"] == 3
    assert payload["verified_project_outcomes"]["recruiter_pitch_target_roles"] == 4
    assert payload["verified_project_outcomes"]["application_evidence_pack"] == 1
    assert payload["verified_project_outcomes"]["application_evidence_links"] == 48
    assert payload["verified_project_outcomes"]["github_discovery_profile"] == 1
    assert payload["verified_project_outcomes"]["github_discovery_topics"] == 16
    assert payload["verified_project_outcomes"]["github_discovery_reviewer_entrypoints"] == 6
    assert payload["verified_project_outcomes"]["pilot_evidence_quicklink"] == 1
    assert payload["verified_project_outcomes"]["pilot_evidence_quicklink_actions"] == 3
    assert payload["verified_project_outcomes"]["pilot_evidence_quicklink_fields"] == 12
    assert payload["verified_project_outcomes"]["pilot_evidence_quicklink_target_metrics"] == 3
    assert payload["verified_project_outcomes"]["pilot_launch_control_room"] == 1
    assert payload["verified_project_outcomes"]["pilot_launch_public_issue_threads"] == 4
    assert payload["verified_project_outcomes"]["pilot_launch_gates"] == 5
    assert payload["verified_project_outcomes"]["pilot_launch_target_outcomes"] == 4
    assert payload["verified_project_outcomes"]["pilot_launch_reviewer_send_paths"] == 3
    assert payload["verified_project_outcomes"]["resume_outcome_adjudication"] == 1
    assert payload["verified_project_outcomes"]["resume_outcome_adjudication_categories"] == 5
    assert payload["verified_project_outcomes"]["resume_outcome_adjudication_blocked_categories"] == 5
    assert payload["verified_project_outcomes"]["resume_outcome_adjudication_claimable_categories"] == 0
    assert payload["verified_project_outcomes"]["reviewer_share_channels"] == 5
    assert payload["verified_project_outcomes"]["reviewer_share_ready_messages"] == 5
    assert payload["verified_project_outcomes"]["reviewer_share_not_sent"] == 5
    assert payload["verified_project_outcomes"]["ai_engineer_review_intake"] == 1
    assert payload["verified_project_outcomes"]["ai_engineer_review_paths"] == 6
    assert payload["verified_project_outcomes"]["ai_engineer_review_questions"] == 6
    assert payload["verified_project_outcomes"]["ai_engineer_review_countable_conditions"] == 5
    assert payload["verified_project_outcomes"]["pilot_outreach_messages"] == 3
    assert payload["verified_project_outcomes"]["pilot_review_paths"] == 10
    assert payload["verified_project_outcomes"]["pilot_program_segments"] == 3
    assert payload["verified_project_outcomes"]["pilot_program_weeks"] == 3
    assert payload["verified_project_outcomes"]["pilot_review_tracker"] == 1
    assert payload["verified_project_outcomes"]["pilot_review_tracker_planned_reviews"] == 3
    assert payload["verified_project_outcomes"]["pilot_review_tracker_not_contacted"] == 3
    assert payload["verified_project_outcomes"]["pilot_review_tracker_resume_rules"] == 3
    assert payload["verified_project_outcomes"]["pilot_conversion_board"] == 1
    assert payload["verified_project_outcomes"]["pilot_conversion_stages"] == 6
    assert payload["verified_project_outcomes"]["pilot_conversion_claimable_stages"] == 2
    assert payload["verified_project_outcomes"]["pilot_conversion_blocked_stages"] == 4
    assert payload["verified_project_outcomes"]["resume_outcome_readiness"] == 1
    assert payload["verified_project_outcomes"]["resume_outcome_readiness_stages"] == 6
    assert payload["verified_project_outcomes"]["resume_outcome_claimable_stages"] == 2
    assert payload["verified_project_outcomes"]["resume_outcome_blocked_stages"] == 4
    assert payload["verified_project_outcomes"]["resume_outcome_missing_evidence_items"] == 4
    assert payload["verified_project_outcomes"]["external_review_evidence_ledger"] == 1
    assert payload["verified_project_outcomes"]["external_review_ledger_entries"] == 0
    assert payload["verified_project_outcomes"]["external_review_ledger_requirement_types"] == 5
    assert payload["verified_project_outcomes"]["external_review_ledger_linked_reviews"] == 3
    assert payload["verified_project_outcomes"]["outcome_upgrade_playbook"] == 1
    assert payload["verified_project_outcomes"]["outcome_upgrade_rules"] == 5
    assert payload["verified_project_outcomes"]["outcome_upgrade_blocked_rules"] == 5
    assert payload["verified_project_outcomes"]["outcome_upgrade_claimable_now"] == 6
    assert payload["verified_project_outcomes"]["resume_claim_upgrade_ledger"] == 1
    assert payload["verified_project_outcomes"]["resume_claim_upgrade_rows"] == 6
    assert payload["verified_project_outcomes"]["resume_claim_upgrade_blocked_rows"] == 6
    assert payload["verified_project_outcomes"]["resume_claim_upgrade_claimable_rows"] == 0
    assert payload["verified_project_outcomes"]["reviewer_feedback_packet"] == 1
    assert payload["verified_project_outcomes"]["reviewer_feedback_tasks"] == 4
    assert payload["verified_project_outcomes"]["reviewer_feedback_questions"] == 6
    assert payload["verified_project_outcomes"]["reviewer_feedback_conversion_paths"] == 5
    assert payload["verified_project_outcomes"]["reviewer_funnel_board"] == 1
    assert payload["verified_project_outcomes"]["reviewer_funnel_stages"] == 4
    assert payload["verified_project_outcomes"]["reviewer_funnel_open_gaps"] == 4
    assert payload["verified_project_outcomes"]["reviewer_funnel_remaining_evidence_items"] == 7
    assert payload["verified_project_outcomes"]["feedback_intake_quality"] == 1
    assert payload["verified_project_outcomes"]["feedback_intake_required_sections"] == 5
    assert payload["verified_project_outcomes"]["feedback_intake_try_paths"] == 5
    assert payload["verified_project_outcomes"]["feedback_intake_outcomes"] == 4
    assert payload["verified_project_outcomes"]["feedback_intake_captured_fields"] == 5
    assert payload["verified_project_outcomes"]["star_growth_kit"] == 1
    assert payload["verified_project_outcomes"]["star_growth_required_topics"] == 16
    assert payload["verified_project_outcomes"]["star_growth_ethical_actions"] == 4
    assert payload["verified_project_outcomes"]["star_growth_resume_upgrade_rules"] == 4
    assert payload["verified_project_outcomes"]["business_case_intake"] == 1
    assert payload["verified_project_outcomes"]["business_case_intake_required_sections"] == 8
    assert payload["verified_project_outcomes"]["business_case_intake_try_paths"] == 5
    assert payload["verified_project_outcomes"]["business_case_intake_outcomes"] == 8
    assert payload["verified_project_outcomes"]["business_case_intake_captured_fields"] == 8
    assert payload["verified_project_outcomes"]["business_case_intake_outcome_fields"] == 9
    assert payload["verified_project_outcomes"]["business_data_replay_packet"] == 1
    assert payload["verified_project_outcomes"]["business_data_replay_paths"] == 3
    assert payload["verified_project_outcomes"]["business_data_replay_evidence_fields"] == 8
    assert payload["verified_project_outcomes"]["business_data_replay_safety_requirements"] == 5
    assert payload["verified_project_outcomes"]["business_replay_demo"] == 1
    assert payload["verified_project_outcomes"]["business_replay_demo_rows"] == 8
    assert payload["verified_project_outcomes"]["business_replay_demo_findings"] == 5
    assert payload["verified_project_outcomes"]["business_replay_demo_check_types"] == 4
    assert payload["verified_project_outcomes"]["business_replay_demo_rule_references"] == 4
    assert payload["verified_project_outcomes"]["business_replay_demo_root_causes"] == 3
    assert payload["verified_project_outcomes"]["real_model_runbook"] == 1
    assert payload["verified_project_outcomes"]["real_model_current_runs"] == 0
    assert payload["verified_project_outcomes"]["real_model_run_commands"] == 5
    assert payload["verified_project_outcomes"]["real_model_evidence_fields"] == 15
    assert payload["verified_project_outcomes"]["real_model_acceptance_criteria"] == 8
    assert payload["verified_project_outcomes"]["real_model_safety_gates"] == 5
    assert payload["verified_project_outcomes"]["real_model_evidence_capture"] == 1
    assert payload["verified_project_outcomes"]["real_model_capture_required_fields"] == 17
    assert payload["verified_project_outcomes"]["real_model_capture_accepted_runs"] == 0
    assert payload["verified_project_outcomes"]["real_model_capture_blocked_claims"] == 4
    assert payload["verified_project_outcomes"]["recommended_actions"] == 5
    assert payload["verified_project_outcomes"]["implemented_agent_capabilities"] == 16
    assert "14-scenario agent evaluation harness" in payload["resume_safe_signals"]
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
    assert (
        "Runnable release packet with 3 runnable surfaces, 4 acceptance checks, and 6 required API paths"
        in payload["resume_safe_signals"]
    )
    assert (
        "External-run evidence packet with public issue #18, 3 reviewer run paths, 8 required submission fields, and 3 resume-upgrade rules"
        in payload["resume_safe_signals"]
    )
    assert (
        "External reviewer request pack linked to issue #18 with 3 copy-ready messages, 3 run paths, 8 evidence fields, and zero-count baseline"
        in payload["resume_safe_signals"]
    )
    assert "CI-verified API smoke report covering 6 passing FastAPI route checks" in payload["resume_safe_signals"]
    assert (
        "CI-verified local performance baseline covering 2 route benchmarks and 24 measured endpoint calls"
        in payload["resume_safe_signals"]
    )
    assert (
        "Public demo usage baseline with 5 tracked funnel steps and 6 verified entrypoints"
        in payload["resume_safe_signals"]
    )
    assert (
        "Business-data intake baseline covering 4 integration endpoints, 6 API tests, and bounded CSV uploads up to 10000 rows / 80 columns"
        in payload["resume_safe_signals"]
    )
    assert (
        "Community growth baseline with 8 issue templates, 10 configured labels, and 9 public contribution or feedback channels"
        in payload["resume_safe_signals"]
    )
    assert (
        "Impact review packet with 12 verified business metrics, 8 evidence links, 5 remediation actions, and 4 owner handoffs"
        in payload["resume_safe_signals"]
    )
    assert (
        "Business problem casebook with 1 verified case, 4 detected business risks, and 4 owner handoffs"
        in payload["resume_safe_signals"]
    )
    assert any(
        "Business resolution brief with 5 findings, 4 business risk areas" in signal
        for signal in payload["resume_safe_signals"]
    )
    assert (
            "Public traction dashboard with 4 live project surfaces, 19 growth or review channels, 5 tracked funnel steps, and 3 resume upgrade rules"
        in payload["resume_safe_signals"]
    )
    assert any("GitHub traffic snapshot with" in signal for signal in payload["resume_safe_signals"])
    assert any("Public availability snapshot with" in signal for signal in payload["resume_safe_signals"])
    assert "23 reviewer paths in a CI-verified live project scorecard" in payload["resume_safe_signals"]
    assert "CI-verified OpenAPI contract covering 6 integration endpoints" in payload["resume_safe_signals"]
    assert "3 recruiter-safe resume bullets for 4 target roles" in payload["resume_safe_signals"]
    assert (
        "Reviewer outreach execution pack with 8 ready-to-send messages, 8 follow-up rules, 8 not-sent baseline entries, and zero sent outreach claimed"
        in payload["resume_safe_signals"]
    )
    assert (
        "Resume outcome metrics board tracking 6 outcome metrics, 0 claimable outcome lines, 6 blocked outcome lines, and honest user/feedback/star baselines"
        in payload["resume_safe_signals"]
    )
    assert (
        "Reviewer submission hub with 6 public submission paths, 6 tracked outcome metrics, 24 required evidence fields, and zero current outcome claims upgraded"
        in payload["resume_safe_signals"]
    )
    assert (
        "Public reviewer call linked to 3 reviewer segments, 6 submission paths, 8 outreach tasks, and 24 evidence fields without claiming outcomes"
        in payload["resume_safe_signals"]
    )
    assert (
        "Resume outcome action checklist with 5 concrete next actions, 4 evaluated public GitHub issues, "
        "0 accepted public evidence items, and 8 not-sent reviewer outreach slots"
        in payload["resume_safe_signals"]
    )
    assert (
        "Outcome collection page with 5 next actions, 6 submission paths, 24 required evidence fields, 0 confirmed users, 0 feedback items, and 0 GitHub stars"
        in payload["resume_safe_signals"]
    )
    assert (
        "First-10 outreach execution log with 10 copy-ready reviewer messages, 10 public issue entrypoints, 10 not-sent entries, and zero claimable external outcomes"
        in payload["resume_safe_signals"]
    )
    assert "48 application evidence links in a recruiter-ready evidence pack" in payload["resume_safe_signals"]
    assert any("GitHub discovery profile with 16 precise topics" in signal for signal in payload["resume_safe_signals"])
    assert any("Pilot launch control room with 4 public issue threads" in signal for signal in payload["resume_safe_signals"])
    assert any("Resume outcome adjudication report with 5 outcome categories" in signal for signal in payload["resume_safe_signals"])
    assert any("First-10 reviewer sprint with 10 public evidence slots" in signal for signal in payload["resume_safe_signals"])
    assert any("Resume claim upgrade ledger with 6 outcome metrics" in signal for signal in payload["resume_safe_signals"])
    assert any("Reviewer share kit with 5 copy-ready messages" in signal for signal in payload["resume_safe_signals"])
    assert any("Business impact ledger with 0 accepted business-impact signals" in signal for signal in payload["resume_safe_signals"])
    assert any("Resume traction proof with 6 claimable launch/quality/traffic/availability signals" in signal for signal in payload["resume_safe_signals"])
    assert (
        "AI Engineer review intake with 6 review paths, 6 reviewer questions, 5 countable-evidence conditions, and zero accepted reviews"
        in payload["resume_safe_signals"]
    )
    assert any("External reviewer outreach tracker with 3 queued reviewer segments" in signal for signal in payload["resume_safe_signals"])
    assert any(
        "External reviewer evidence gate with 8 validation rules" in signal
        and "collected public GitHub issues" in signal
        for signal in payload["resume_safe_signals"]
    )
    assert any("Accepted evidence rollup with 5 tracked outcome metrics" in signal for signal in payload["resume_safe_signals"])
    assert "Reviewer funnel board with 4 public evidence paths and 7 remaining evidence items" in payload["resume_safe_signals"]
    assert "3 pilot outreach messages and 10 review paths for collecting real feedback" in payload["resume_safe_signals"]
    assert (
        "Pilot review tracker with 3 planned reviewer segments, 3 not-contacted baseline entries, and 3 resume-upgrade rules"
        in payload["resume_safe_signals"]
    )
    assert (
        "Pilot conversion board with 6 outcome stages, 2 resume-safe readiness claims, and 4 blocked outcome claims until public evidence exists"
        in payload["resume_safe_signals"]
    )
    assert (
        "Resume outcome readiness evaluator with 6 stages, 2 claimable readiness lines, 4 blocked outcome claims, and 4 missing-evidence items"
        in payload["resume_safe_signals"]
    )
    assert (
        "External review evidence ledger with 5 public evidence types, 3 linked planned reviews, and 0 current evidence entries"
        in payload["resume_safe_signals"]
    )
    assert "3 pilot participant segments across a 3-week feedback plan" in payload["resume_safe_signals"]
    assert (
        "Feedback intake system with 5 required sections, 5 demo paths, 4 outcome signals, and 5 captured evidence groups"
        in payload["resume_safe_signals"]
    )
    assert (
            "Star growth kit with 16 verified repo topics, 4 ethical growth actions, and 4 resume upgrade rules with traffic context without inflating current stars"
        in payload["resume_safe_signals"]
    )
    assert (
        "Business-case intake path with 8 required sections, 5 tried paths, 8 outcome signals, and 8 captured evidence groups including 9 resume outcome fields"
        in payload["resume_safe_signals"]
    )
    assert (
        "Business-data replay packet with 3 safe replay paths, 8 evidence fields, 5 safety requirements, and zero current external replay claims"
        in payload["resume_safe_signals"]
    )
    assert (
        "Business replay demo with 8 anonymized rows, 5 findings, 4 failed check types, 4 business-rule references, and deterministic verification"
        in payload["resume_safe_signals"]
    )
    assert (
        "Real-model runbook with 5 run commands, 15 evidence fields, 8 acceptance criteria, 5 safety gates, and zero current real model run claims"
        in payload["resume_safe_signals"]
    )
    assert "Dataset-level memory retrieval over recent sanitized traces" in payload["resume_safe_signals"]
    assert "Do not claim external users" in payload["resume_policy"]
    assert "Confirmed external users | 0" in markdown
    assert "GitHub stars beyond the current public count" in markdown
