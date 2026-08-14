from scripts.build_application_evidence_pack import (
    build_application_evidence_pack_payload,
    render_markdown,
    verify_application_evidence_pack,
)


def test_application_evidence_pack_gives_recruiters_verified_review_path():
    payload = build_application_evidence_pack_payload()
    verification = verify_application_evidence_pack(payload)
    markdown = render_markdown(payload)

    assert verification["application_evidence_pack_verified"] is True
    assert len(payload["application_links"]) == 50
    assert "reviewer_share_kit" in payload["application_links"]
    assert "business_data_replay_packet" in payload["application_links"]
    assert "business_replay_demo" in payload["application_links"]
    assert "business_resolution_brief" in payload["application_links"]
    assert "business_resolution_review_request" in payload["application_links"]
    assert "real_model_runbook" in payload["application_links"]
    assert "real_model_evidence_capture" in payload["application_links"]
    assert "resume_outcome_readiness" in payload["application_links"]
    assert "reviewer_feedback_packet" in payload["application_links"]
    assert "reviewer_funnel_board" in payload["application_links"]
    assert "external_run_evidence_packet" in payload["application_links"]
    assert "external_run_quickstart" in payload["application_links"]
    assert "external_reviewer_outreach_tracker" in payload["application_links"]
    assert "external_reviewer_evidence_gate" in payload["application_links"]
    assert "accepted_evidence_rollup" in payload["application_links"]
    assert "business_impact_ledger" in payload["application_links"]
    assert "reviewer_evidence_kit" in payload["application_links"]
    assert "resume_traction_proof" in payload["application_links"]
    assert "reviewer_outreach_execution_pack" in payload["application_links"]
    assert "reviewer_outreach_status_board" in payload["application_links"]
    assert "resume_outcome_metrics" in payload["application_links"]
    assert "resume_outcome_action_checklist" in payload["application_links"]
    assert "reviewer_submission_hub" in payload["application_links"]
    assert "outcome_collection" in payload["application_links"]
    assert "public_reviewer_call" in payload["application_links"]
    assert "resume_claim_upgrade_ledger" in payload["application_links"]
    assert "resume_outcome_scoreboard" in payload["application_links"]
    assert "github_discovery_profile" in payload["application_links"]
    assert "first_10_reviewer_sprint" in payload["application_links"]
    assert "first_10_outreach_execution_log" in payload["application_links"]
    assert len(payload["resume_bullets"]) == 3
    assert payload["verified_outcome_numbers"]["passing_tests"] == 168
    assert payload["verified_outcome_numbers"]["verified_resume_claims"] == 84
    assert payload["verified_outcome_numbers"]["outcome_collection_actions"] == 5
    assert payload["verified_outcome_numbers"]["outcome_collection_submission_paths"] == 6
    assert payload["verified_outcome_numbers"]["outcome_collection_evidence_fields"] == 24
    assert payload["verified_outcome_numbers"]["reviewer_share_channels"] == 5
    assert payload["verified_outcome_numbers"]["reviewer_share_ready_messages"] == 5
    assert payload["verified_outcome_numbers"]["reviewer_share_not_sent"] == 5
    assert payload["verified_outcome_numbers"]["business_data_replay_paths"] == 3
    assert payload["verified_outcome_numbers"]["business_data_replay_evidence_fields"] == 8
    assert payload["verified_outcome_numbers"]["business_replay_demo_rows"] == 8
    assert payload["verified_outcome_numbers"]["business_replay_demo_findings"] == 5
    assert payload["verified_outcome_numbers"]["business_replay_demo_check_types"] == 4
    assert payload["verified_outcome_numbers"]["real_model_run_commands"] == 5
    assert payload["verified_outcome_numbers"]["real_model_evidence_fields"] == 15
    assert payload["verified_outcome_numbers"]["real_model_capture_required_fields"] == 17
    assert payload["verified_outcome_numbers"]["real_model_capture_accepted_runs"] == 0
    assert payload["verified_outcome_numbers"]["real_model_capture_blocked_claims"] == 4
    assert payload["verified_outcome_numbers"]["impact_review_business_metrics"] == 12
    assert payload["verified_outcome_numbers"]["impact_review_evidence_links"] == 8
    assert payload["verified_outcome_numbers"]["business_problem_cases"] == 1
    assert payload["verified_outcome_numbers"]["business_problem_detected_risks"] == 4
    assert payload["verified_outcome_numbers"]["business_resolution_findings"] == 5
    assert payload["verified_outcome_numbers"]["business_resolution_risk_areas"] == 4
    assert payload["verified_outcome_numbers"]["business_resolution_high_priority_actions"] == 3
    assert payload["verified_outcome_numbers"]["business_resolution_owner_handoffs"] == 4
    assert payload["verified_outcome_numbers"]["business_resolution_review_request"] == 1
    assert payload["verified_outcome_numbers"]["business_resolution_review_questions"] == 5
    assert payload["verified_outcome_numbers"]["business_resolution_review_external_feedback"] == 0
    assert payload["verified_outcome_numbers"]["public_traction_surfaces"] == 4
    assert payload["verified_outcome_numbers"]["public_traction_growth_channels"] == 19
    assert payload["verified_outcome_numbers"]["feedback_intake_required_sections"] == 5
    assert payload["verified_outcome_numbers"]["feedback_intake_captured_fields"] == 5
    assert payload["verified_outcome_numbers"]["reviewer_funnel_stages"] == 4
    assert payload["verified_outcome_numbers"]["reviewer_funnel_remaining_evidence_items"] == 7
    assert payload["verified_outcome_numbers"]["accepted_evidence_rollup_claimable_metrics"] == 5
    assert payload["verified_outcome_numbers"]["accepted_evidence_rollup_blocked_claims"] == 5
    assert payload["verified_outcome_numbers"]["business_impact_ledger_accepted_signals"] == 0
    assert payload["verified_outcome_numbers"]["reviewer_evidence_forms"] == 5
    assert payload["verified_outcome_numbers"]["reviewer_evidence_script_steps"] == 5
    assert payload["verified_outcome_numbers"]["resume_traction_claimable_now"] == 6
    assert payload["verified_outcome_numbers"]["resume_traction_future_claims"] == 4
    assert payload["verified_outcome_numbers"]["resume_traction_blocked_claims"] == 5
    assert payload["verified_outcome_numbers"]["reviewer_outreach_ready_messages"] == 8
    assert payload["verified_outcome_numbers"]["reviewer_outreach_status_slots"] == 8
    assert payload["verified_outcome_numbers"]["reviewer_outreach_status_stages"] == 5
    assert payload["verified_outcome_numbers"]["reviewer_outreach_status_accepted_evidence"] == 0
    assert payload["verified_outcome_numbers"]["resume_outcome_metrics_tracked"] == 6
    assert payload["verified_outcome_numbers"]["resume_outcome_metrics_claimable"] == 0
    assert payload["verified_outcome_numbers"]["resume_outcome_metrics_blocked"] == 6
    assert payload["verified_outcome_numbers"]["resume_outcome_action_count"] == 5
    assert payload["verified_outcome_numbers"]["resume_outcome_next_actions_needed"] == 5
    assert payload["verified_outcome_numbers"]["reviewer_submission_paths"] == 6
    assert payload["verified_outcome_numbers"]["reviewer_submission_required_fields"] == 24
    assert payload["verified_outcome_numbers"]["first_10_reviewer_slots"] == 10
    assert payload["verified_outcome_numbers"]["first_10_reviewer_public_issue_entrypoints"] == 10
    assert payload["verified_outcome_numbers"]["first_10_reviewer_target_metrics"] == 6
    assert payload["verified_outcome_numbers"]["first_10_reviewer_not_sent"] == 10
    assert payload["verified_outcome_numbers"]["first_10_reviewer_completed"] == 0
    assert payload["verified_outcome_numbers"]["first_10_outreach_messages"] == 10
    assert payload["verified_outcome_numbers"]["first_10_outreach_public_issue_entrypoints"] == 10
    assert payload["verified_outcome_numbers"]["first_10_outreach_not_sent"] == 10
    assert payload["verified_outcome_numbers"]["first_10_outreach_accepted_evidence"] == 0
    assert payload["verified_outcome_numbers"]["public_reviewer_call_segments"] == 3
    assert payload["verified_outcome_numbers"]["public_reviewer_call_outreach_tasks"] == 8
    assert payload["verified_outcome_numbers"]["public_reviewer_call_evidence_fields"] == 24
    assert payload["verified_outcome_numbers"]["resume_claim_upgrade_rows"] == 6
    assert payload["verified_outcome_numbers"]["resume_claim_upgrade_blocked_rows"] == 6
    assert payload["verified_outcome_numbers"]["resume_claim_upgrade_claimable_rows"] == 0
    assert payload["verified_outcome_numbers"]["resume_outcome_scoreboard_claimable_now"] == 3
    assert payload["verified_outcome_numbers"]["resume_outcome_scoreboard_blocked"] == 6
    assert payload["verified_outcome_numbers"]["resume_outcome_scoreboard_remaining_evidence"] == 7
    assert payload["verified_outcome_numbers"]["github_discovery_topics"] == 16
    assert payload["verified_outcome_numbers"]["github_discovery_reviewer_entrypoints"] == 6
    assert payload["honest_baseline"]["stars"] == 0
    assert payload["honest_baseline"]["confirmed_external_users"] == 0
    assert "Application Evidence Pack" in markdown
