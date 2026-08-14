import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
PUBLIC_METRICS_PROVENANCE_PATH = ROOT / "docs" / "public-metrics-provenance.json"
OUTCOME_SUMMARY_PATH = ROOT / "docs" / "outcome-summary.json"
AGENT_READINESS_PATH = ROOT / "docs" / "agent-readiness.json"
EVAL_SUMMARY_PATH = ROOT / "docs" / "eval-summary.json"
HYPOTHESIS_FEEDBACK_PATH = ROOT / "docs" / "hypothesis-feedback.json"
INCIDENT_PATTERN_MEMORY_PATH = ROOT / "docs" / "incident-pattern-memory.json"
AGENT_OBSERVABILITY_PATH = ROOT / "docs" / "agent-observability.json"
AGENT_SAFETY_PATH = ROOT / "docs" / "agent-safety-boundaries.json"
AGENT_CAPABILITY_MATRIX_PATH = ROOT / "docs" / "agent-capability-matrix.json"
AGENT_MATURITY_AUDIT_PATH = ROOT / "docs" / "agent-maturity-audit.json"
LOCAL_REVIEWER_DEMO_PATH = ROOT / "docs" / "local-reviewer-demo.json"
RUNNABLE_RELEASE_PACKET_PATH = ROOT / "docs" / "runnable-release-packet.json"
EXTERNAL_RUN_EVIDENCE_PACKET_PATH = ROOT / "docs" / "external-run-evidence-packet.json"
EXTERNAL_REVIEWER_REQUEST_PACK_PATH = ROOT / "docs" / "external-reviewer-request-pack.json"
EXTERNAL_RUN_QUICKSTART_PATH = ROOT / "docs" / "external-run-quickstart.json"
EXTERNAL_REVIEWER_OUTREACH_TRACKER_PATH = ROOT / "docs" / "external-reviewer-outreach-tracker.json"
EXTERNAL_REVIEWER_EVIDENCE_GATE_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
ACCEPTED_EVIDENCE_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
BUSINESS_IMPACT_LEDGER_PATH = ROOT / "docs" / "business-impact-ledger.json"
REVIEWER_EVIDENCE_KIT_PATH = ROOT / "docs" / "reviewer-evidence-kit.json"
RESUME_TRACTION_PROOF_PATH = ROOT / "docs" / "resume-traction-proof.json"
REVIEWER_ACTION_QUEUE_PATH = ROOT / "docs" / "reviewer-action-queue.json"
REVIEWER_OUTREACH_EXECUTION_PACK_PATH = ROOT / "docs" / "reviewer-outreach-execution-pack.json"
REVIEWER_OUTREACH_STATUS_BOARD_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
RESUME_OUTCOME_METRICS_PATH = ROOT / "docs" / "resume-outcome-metrics.json"
RESUME_OUTCOME_ACTION_CHECKLIST_PATH = ROOT / "docs" / "resume-outcome-action-checklist.json"
REVIEWER_SUBMISSION_HUB_PATH = ROOT / "docs" / "reviewer-submission-hub.json"
FIRST_10_REVIEWER_SPRINT_PATH = ROOT / "docs" / "first-10-reviewer-sprint.json"
FIRST_10_OUTREACH_EXECUTION_LOG_PATH = ROOT / "docs" / "first-10-outreach-execution-log.json"
OUTCOME_COLLECTION_PATH = ROOT / "docs" / "outcome-collection.json"
PUBLIC_REVIEWER_CALL_PATH = ROOT / "docs" / "public-reviewer-call.json"
REVIEWER_SHARE_KIT_PATH = ROOT / "docs" / "reviewer-share-kit.json"
API_SMOKE_REPORT_PATH = ROOT / "docs" / "api-smoke-report.json"
PERFORMANCE_BASELINE_PATH = ROOT / "docs" / "performance-baseline.json"
DEMO_USAGE_BASELINE_PATH = ROOT / "docs" / "demo-usage-baseline.json"
BUSINESS_DATA_INTAKE_BASELINE_PATH = ROOT / "docs" / "business-data-intake-baseline.json"
COMMUNITY_GROWTH_BASELINE_PATH = ROOT / "docs" / "community-growth-baseline.json"
IMPACT_REVIEW_PACKET_PATH = ROOT / "docs" / "impact-review-packet.json"
BUSINESS_PROBLEM_CASEBOOK_PATH = ROOT / "docs" / "business-problem-casebook.json"
BUSINESS_RESOLUTION_BRIEF_PATH = ROOT / "docs" / "business-resolution-brief.json"
BUSINESS_RESOLUTION_REVIEW_REQUEST_PATH = ROOT / "docs" / "business-resolution-review-request.json"
PUBLIC_TRACTION_DASHBOARD_PATH = ROOT / "docs" / "public-traction-dashboard.json"
GITHUB_TRAFFIC_SNAPSHOT_PATH = ROOT / "docs" / "github-traffic-snapshot.json"
PUBLIC_AVAILABILITY_SNAPSHOT_PATH = ROOT / "docs" / "public-availability-snapshot.json"
LIVE_PROJECT_SCORECARD_PATH = ROOT / "docs" / "live-project-scorecard.json"
OPENAPI_PATH = ROOT / "docs" / "openapi.json"
RECRUITER_PITCH_PATH = ROOT / "docs" / "recruiter-pitch.json"
APPLICATION_EVIDENCE_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
AI_ENGINEER_REVIEW_INTAKE_PATH = ROOT / "docs" / "ai-engineer-review-intake.json"
PILOT_OUTREACH_KIT_PATH = ROOT / "docs" / "pilot-outreach-kit.json"
PILOT_PROGRAM_PLAN_PATH = ROOT / "docs" / "pilot-program-plan.json"
PILOT_REVIEW_TRACKER_PATH = ROOT / "docs" / "pilot-review-tracker.json"
PILOT_CONVERSION_BOARD_PATH = ROOT / "docs" / "pilot-conversion-board.json"
RESUME_OUTCOME_READINESS_PATH = ROOT / "docs" / "resume-outcome-readiness.json"
EXTERNAL_REVIEW_EVIDENCE_LEDGER_PATH = ROOT / "docs" / "external-review-evidence-ledger.json"
OUTCOME_UPGRADE_PLAYBOOK_PATH = ROOT / "docs" / "outcome-upgrade-playbook.json"
REVIEWER_FEEDBACK_PACKET_PATH = ROOT / "docs" / "reviewer-feedback-packet.json"
FEEDBACK_INTAKE_QUALITY_PATH = ROOT / "docs" / "feedback-intake-quality.json"
STAR_GROWTH_KIT_PATH = ROOT / "docs" / "star-growth-kit.json"
GITHUB_DISCOVERY_PROFILE_PATH = ROOT / "docs" / "github-discovery-profile.json"
PILOT_EVIDENCE_QUICKLINK_PATH = ROOT / "docs" / "pilot-evidence-quicklink.json"
PILOT_LAUNCH_CONTROL_ROOM_PATH = ROOT / "docs" / "pilot-launch-control-room.json"
BUSINESS_CASE_INTAKE_PATH = ROOT / "docs" / "business-case-intake.json"
BUSINESS_DATA_REPLAY_PACKET_PATH = ROOT / "docs" / "business-data-replay-packet.json"
REAL_MODEL_RUNBOOK_PATH = ROOT / "docs" / "real-model-runbook.json"
REAL_MODEL_EVIDENCE_CAPTURE_PATH = ROOT / "docs" / "real-model-evidence-capture.json"
REAL_MODEL_PREFLIGHT_PATH = ROOT / "docs" / "real-model-preflight.json"
AI_ENGINEER_READINESS_PATH = ROOT / "docs" / "ai-engineer-readiness.json"
BUSINESS_REPLAY_DEMO_PATH = ROOT / "docs" / "business-replay-demo.json"
REVIEWER_FUNNEL_BOARD_PATH = ROOT / "docs" / "reviewer-funnel-board.json"
RESUME_CLAIM_UPGRADE_LEDGER_PATH = ROOT / "docs" / "resume-claim-upgrade-ledger.json"
RESUME_OUTCOME_ADJUDICATION_PATH = ROOT / "docs" / "resume-outcome-adjudication.json"
RESUME_OUTCOME_SCOREBOARD_PATH = ROOT / "docs" / "resume-outcome-scoreboard.json"
EVIDENCE_ACCEPTANCE_CHECKLIST_PATH = ROOT / "docs" / "evidence-acceptance-checklist.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "public-metrics-summary.json"
OUTPUT_MD_PATH = ROOT / "docs" / "public-metrics-summary.md"
SCORECARD_REVIEWER_PATH_COUNT = 23
APPLICATION_EVIDENCE_LINK_COUNT = 50


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_public_metrics_summary() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    metrics_provenance = load_json(PUBLIC_METRICS_PROVENANCE_PATH)
    outcome = load_json(OUTCOME_SUMMARY_PATH)
    readiness = load_json(AGENT_READINESS_PATH)
    eval_summary = load_json(EVAL_SUMMARY_PATH)
    hypothesis_feedback = load_json(HYPOTHESIS_FEEDBACK_PATH)
    incident_memory = load_json(INCIDENT_PATTERN_MEMORY_PATH)
    observability = load_json(AGENT_OBSERVABILITY_PATH)
    safety = load_json(AGENT_SAFETY_PATH)
    capability_matrix = load_json(AGENT_CAPABILITY_MATRIX_PATH)
    maturity_audit = load_json(AGENT_MATURITY_AUDIT_PATH)
    local_demo = load_json(LOCAL_REVIEWER_DEMO_PATH)
    runnable_release = load_json(RUNNABLE_RELEASE_PACKET_PATH)
    external_run_evidence = load_json(EXTERNAL_RUN_EVIDENCE_PACKET_PATH)
    external_reviewer_request = load_json(EXTERNAL_REVIEWER_REQUEST_PACK_PATH)
    external_run_quickstart = load_json(EXTERNAL_RUN_QUICKSTART_PATH)
    external_reviewer_outreach = load_json(EXTERNAL_REVIEWER_OUTREACH_TRACKER_PATH)
    external_reviewer_gate = load_json(EXTERNAL_REVIEWER_EVIDENCE_GATE_PATH)
    accepted_evidence_rollup = load_json(ACCEPTED_EVIDENCE_ROLLUP_PATH)
    business_impact_ledger = load_json(BUSINESS_IMPACT_LEDGER_PATH)
    reviewer_evidence_kit = load_json(REVIEWER_EVIDENCE_KIT_PATH)
    resume_traction_proof = load_json(RESUME_TRACTION_PROOF_PATH)
    reviewer_action_queue = load_json(REVIEWER_ACTION_QUEUE_PATH)
    reviewer_outreach_execution = load_json(REVIEWER_OUTREACH_EXECUTION_PACK_PATH)
    reviewer_outreach_status = load_json(REVIEWER_OUTREACH_STATUS_BOARD_PATH)
    resume_outcome_metrics = load_json(RESUME_OUTCOME_METRICS_PATH)
    resume_outcome_action_checklist = load_json(RESUME_OUTCOME_ACTION_CHECKLIST_PATH)
    reviewer_submission_hub = load_json(REVIEWER_SUBMISSION_HUB_PATH)
    first_10_sprint = load_json(FIRST_10_REVIEWER_SPRINT_PATH)
    first_10_outreach_log = load_json(FIRST_10_OUTREACH_EXECUTION_LOG_PATH)
    outcome_collection = load_json(OUTCOME_COLLECTION_PATH)
    public_reviewer_call = load_json(PUBLIC_REVIEWER_CALL_PATH)
    reviewer_share_kit = load_json(REVIEWER_SHARE_KIT_PATH)
    api_smoke = load_json(API_SMOKE_REPORT_PATH)
    performance = load_json(PERFORMANCE_BASELINE_PATH)
    demo_usage = load_json(DEMO_USAGE_BASELINE_PATH)
    business_data_intake = load_json(BUSINESS_DATA_INTAKE_BASELINE_PATH)
    community_growth = load_json(COMMUNITY_GROWTH_BASELINE_PATH)
    impact_review = load_json(IMPACT_REVIEW_PACKET_PATH)
    business_casebook = load_json(BUSINESS_PROBLEM_CASEBOOK_PATH)
    business_resolution = load_json(BUSINESS_RESOLUTION_BRIEF_PATH)
    business_resolution_review = load_json(BUSINESS_RESOLUTION_REVIEW_REQUEST_PATH)
    traction = load_json(PUBLIC_TRACTION_DASHBOARD_PATH)
    traffic = load_json(GITHUB_TRAFFIC_SNAPSHOT_PATH)
    availability = load_json(PUBLIC_AVAILABILITY_SNAPSHOT_PATH)
    scorecard = load_json(LIVE_PROJECT_SCORECARD_PATH)
    openapi = load_json(OPENAPI_PATH)
    recruiter_pitch = load_json(RECRUITER_PITCH_PATH)
    application_pack = load_json(APPLICATION_EVIDENCE_PACK_PATH)
    ai_engineer_review_intake = load_json(AI_ENGINEER_REVIEW_INTAKE_PATH)
    pilot_outreach = load_json(PILOT_OUTREACH_KIT_PATH)
    pilot_plan = load_json(PILOT_PROGRAM_PLAN_PATH)
    pilot_tracker = load_json(PILOT_REVIEW_TRACKER_PATH)
    pilot_conversion = load_json(PILOT_CONVERSION_BOARD_PATH)
    resume_outcome_readiness = load_json(RESUME_OUTCOME_READINESS_PATH)
    external_ledger = load_json(EXTERNAL_REVIEW_EVIDENCE_LEDGER_PATH)
    outcome_upgrade = load_json(OUTCOME_UPGRADE_PLAYBOOK_PATH)
    reviewer_packet = load_json(REVIEWER_FEEDBACK_PACKET_PATH)
    feedback_intake = load_json(FEEDBACK_INTAKE_QUALITY_PATH)
    star_growth = load_json(STAR_GROWTH_KIT_PATH)
    github_discovery = load_json(GITHUB_DISCOVERY_PROFILE_PATH)
    pilot_evidence_quicklink = load_json(PILOT_EVIDENCE_QUICKLINK_PATH)
    pilot_launch_control_room = load_json(PILOT_LAUNCH_CONTROL_ROOM_PATH)
    business_case_intake = load_json(BUSINESS_CASE_INTAKE_PATH)
    replay_packet = load_json(BUSINESS_DATA_REPLAY_PACKET_PATH)
    real_model_runbook = load_json(REAL_MODEL_RUNBOOK_PATH)
    real_model_evidence_capture = load_json(REAL_MODEL_EVIDENCE_CAPTURE_PATH)
    real_model_preflight = load_json(REAL_MODEL_PREFLIGHT_PATH)
    ai_engineer_readiness = load_json(AI_ENGINEER_READINESS_PATH)
    replay_demo = load_json(BUSINESS_REPLAY_DEMO_PATH)
    reviewer_funnel = load_json(REVIEWER_FUNNEL_BOARD_PATH)
    claim_upgrade = load_json(RESUME_CLAIM_UPGRADE_LEDGER_PATH)
    adjudication = load_json(RESUME_OUTCOME_ADJUDICATION_PATH)
    outcome_scoreboard = load_json(RESUME_OUTCOME_SCOREBOARD_PATH)
    evidence_acceptance = load_json(EVIDENCE_ACCEPTANCE_CHECKLIST_PATH)
    verified_outcomes = outcome["verified_outcomes"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_public_metrics_summary.py",
        "repo": adoption["repo"],
        "public_demo": adoption["public_demo"],
        "release": adoption["release"]["tagName"],
        "container_image": adoption["container_image"]["image"],
        "public_metrics": {
            "stars": adoption["stars"],
            "forks": adoption["forks"],
            "watchers": adoption["watchers"],
            "issues_total": adoption["issues_total"],
            "test_count": adoption["test_count"],
            "claimable_public_metrics": metrics_provenance["claimable_metric_count"],
            "tracked_public_metrics": metrics_provenance["metric_count"],
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
            "github_view_count": traffic["views"]["count"],
            "github_unique_visitors": traffic["views"]["uniques"],
            "github_clone_count": traffic["clones"]["count"],
            "github_unique_cloners": traffic["clones"]["uniques"],
            "available_public_endpoints": availability["available_endpoint_count"],
            "public_endpoint_count": availability["endpoint_count"],
            "successful_main_branch_workflows": availability["successful_workflow_count"],
            "main_branch_workflow_count": availability["workflow_count"],
        },
        "verified_project_outcomes": {
            "support_ticket_issue_categories": verified_outcomes["issue_category_count"],
            "support_ticket_findings": verified_outcomes["finding_count"],
            "recommended_actions": verified_outcomes["recommended_action_count"],
            "root_cause_hypotheses": verified_outcomes["root_cause_hypothesis_count"],
            "business_risk_areas": verified_outcomes["business_risk_area_count"],
            "high_priority_actions": verified_outcomes["high_priority_action_count"],
            "owner_handoffs": verified_outcomes["owner_handoff_count"],
            "eval_scenarios": eval_summary["scenario_count"],
            "hypothesis_feedback_labels": hypothesis_feedback["label_count"],
            "incident_pattern_count": incident_memory["incident_pattern_count"],
            "observed_trace_count": observability["observed_trace_count"],
            "fallback_event_count": observability["fallback_event_count"],
            "model_telemetry_artifact": 1,
            "mock_model_calls": observability["model_telemetry"]["model_call_count"],
            "mock_model_tokens": observability["model_telemetry"]["total_tokens"],
            "mock_estimated_cost_usd": observability["model_telemetry"]["estimated_cost_usd"],
            "tool_allowlist_count": safety["tool_allowlist_count"],
            "postgres_rejected_write_query_count": safety["postgres_rejected_write_query_count"],
            "verifier_rule_count": safety["verifier_rule_count"],
            "agent_capability_matrix": 1,
            "agent_matrix_implemented_capabilities": capability_matrix["implemented_count"],
            "agent_matrix_partial_capabilities": capability_matrix["partial_count"],
            "agent_matrix_not_claimed_count": capability_matrix["not_claimed_count"],
            "agent_maturity_audit": 1,
            "agent_maturity_audit_rows": maturity_audit["audit_row_count"],
            "agent_maturity_implemented_areas": maturity_audit["status_counts"]["implemented"],
            "agent_maturity_partial_areas": maturity_audit["status_counts"]["partial"],
            "agent_maturity_not_claimed_areas": maturity_audit["status_counts"]["not_claimed"],
            "local_reviewer_demo": 1,
            "local_reviewer_seeded_rows": local_demo["seeded_business_table"]["row_count"],
            "local_reviewer_routes": len(local_demo["reviewer_routes"]),
            "runnable_release_packet": 1,
            "runnable_release_surfaces": len(runnable_release["runnable_surfaces"]),
            "runnable_release_acceptance_checks": len(runnable_release["acceptance_checks"]),
            "runnable_release_required_api_paths": len(runnable_release["openapi_coverage"]["required_paths"]),
            "external_run_evidence_packet": 1,
            "external_run_review_paths": external_run_evidence["review_path_count"],
            "external_run_submission_fields": external_run_evidence["submission_field_count"],
            "external_run_upgrade_rules": external_run_evidence["upgrade_rule_count"],
            "external_reviewer_request_pack": 1,
            "external_reviewer_request_messages": len(external_reviewer_request["outreach_messages"]),
            "external_reviewer_request_run_paths": len(
                {item["run_path"] for item in external_reviewer_request["outreach_messages"]}
            ),
            "external_reviewer_request_fields": len(external_reviewer_request["required_comment_fields"]),
            "external_run_quickstart_page": 1,
            "external_run_quickstart_paths": external_run_quickstart["review_path_count"],
            "external_run_quickstart_fields": external_run_quickstart["submission_field_count"],
            "external_reviewer_outreach_tracker": 1,
            "external_reviewer_outreach_queue": external_reviewer_outreach["queue_count"],
            "external_reviewer_outreach_not_contacted": external_reviewer_outreach["status_counts"]["not_contacted"],
            "external_reviewer_outreach_source_messages": external_reviewer_outreach["source_message_count"],
            "external_reviewer_evidence_gate": 1,
            "external_reviewer_gate_rules": len(external_reviewer_gate["gate_rules"]),
            "external_reviewer_gate_collected_issues": external_reviewer_gate["issue_collection"][
                "collected_issue_count"
            ],
            "external_reviewer_gate_accepted_issues": external_reviewer_gate["accepted_issue_count"],
            "external_reviewer_gate_linked_queue": external_reviewer_gate["linked_outreach_queue_count"],
            "accepted_evidence_rollup": 1,
            "accepted_evidence_rollup_claimable_metrics": accepted_evidence_rollup["claimable_metric_count"],
            "accepted_evidence_rollup_accepted_issues": accepted_evidence_rollup["accepted_issue_count"],
            "accepted_evidence_rollup_blocked_claims": accepted_evidence_rollup["blocked_outcome_claim_count"],
            "business_impact_ledger": 1,
            "business_impact_ledger_accepted_signals": business_impact_ledger["accepted_business_impact_signal_count"],
            "reviewer_evidence_kit": 1,
            "reviewer_evidence_forms": reviewer_evidence_kit["evidence_form_count"],
            "reviewer_evidence_script_steps": reviewer_evidence_kit["reviewer_script_step_count"],
            "resume_traction_proof": 1,
            "resume_traction_claimable_now": resume_traction_proof["claimable_now_count"],
            "resume_traction_future_claims": resume_traction_proof["future_claim_count"],
            "resume_traction_blocked_claims": resume_traction_proof["blocked_claim_count"],
            "reviewer_action_queue": 1,
            "reviewer_action_tasks": reviewer_action_queue["queue_count"],
            "reviewer_action_not_contacted": reviewer_action_queue["not_contacted_count"],
            "reviewer_action_evidence_goals": reviewer_action_queue["evidence_goal_count"],
            "reviewer_outreach_execution_pack": 1,
            "reviewer_outreach_ready_messages": reviewer_outreach_execution["ready_message_count"],
            "reviewer_outreach_follow_up_rules": reviewer_outreach_execution["follow_up_rule_count"],
            "reviewer_outreach_not_sent": reviewer_outreach_execution["send_status_counts"]["not_sent"],
            "reviewer_outreach_evidence_goals": reviewer_outreach_execution["evidence_goal_count"],
            "reviewer_outreach_status_board": 1,
            "reviewer_outreach_status_slots": reviewer_outreach_status["outreach_slot_count"],
            "reviewer_outreach_status_stages": reviewer_outreach_status["status_stage_count"],
            "reviewer_outreach_status_not_sent": reviewer_outreach_status["not_sent_count"],
            "reviewer_outreach_status_accepted_evidence": reviewer_outreach_status["accepted_evidence_count"],
            "resume_outcome_metrics": 1,
            "resume_outcome_metrics_tracked": resume_outcome_metrics["tracked_outcome_count"],
            "resume_outcome_metrics_claimable": resume_outcome_metrics["claimable_outcome_count"],
            "resume_outcome_metrics_blocked": resume_outcome_metrics["blocked_outcome_count"],
            "public_metrics_provenance": 1,
            "public_metrics_provenance_tracked": metrics_provenance["metric_count"],
            "public_metrics_provenance_claimable": metrics_provenance["claimable_metric_count"],
            "public_metrics_provenance_blocked_or_baseline": metrics_provenance[
                "blocked_or_baseline_metric_count"
            ],
            "resume_outcome_action_checklist": 1,
            "resume_outcome_action_count": resume_outcome_action_checklist["tracked_action_count"],
            "resume_outcome_next_actions_needed": resume_outcome_action_checklist["next_action_needed_count"],
            "resume_outcome_action_accepted_public_evidence": resume_outcome_action_checklist[
                "accepted_public_issue_count"
            ],
            "reviewer_submission_hub": 1,
            "reviewer_submission_paths": reviewer_submission_hub["submission_path_count"],
            "reviewer_submission_target_metrics": reviewer_submission_hub["target_metric_count"],
            "reviewer_submission_required_fields": reviewer_submission_hub["total_required_evidence_fields"],
            "first_10_reviewer_sprint": 1,
            "first_10_reviewer_slots": first_10_sprint["slot_count"],
            "first_10_reviewer_issue_launch_drafts": first_10_sprint["issue_launch_count"],
            "first_10_reviewer_public_issue_entrypoints": first_10_sprint["public_issue_entrypoint_count"],
            "first_10_reviewer_target_metrics": first_10_sprint["target_metric_count"],
            "first_10_reviewer_not_sent": first_10_sprint["not_sent_count"],
            "first_10_reviewer_completed": first_10_sprint["completed_count"],
            "first_10_outreach_execution_log": 1,
            "first_10_outreach_messages": first_10_outreach_log["entry_count"],
            "first_10_outreach_public_issue_entrypoints": first_10_outreach_log["public_issue_entrypoint_count"],
            "first_10_outreach_not_sent": first_10_outreach_log["not_sent_count"],
            "first_10_outreach_accepted_evidence": first_10_outreach_log["accepted_evidence_count"],
            "outcome_collection_page": 1,
            "outcome_collection_actions": outcome_collection["tracked_action_count"],
            "outcome_collection_submission_paths": outcome_collection["submission_path_count"],
            "outcome_collection_evidence_fields": outcome_collection["required_evidence_field_count"],
            "public_reviewer_call": 1,
            "public_reviewer_call_segments": public_reviewer_call["reviewer_segment_count"],
            "public_reviewer_call_submission_paths": public_reviewer_call["linked_submission_paths"],
            "public_reviewer_call_outreach_tasks": public_reviewer_call["linked_outreach_tasks"],
            "public_reviewer_call_evidence_fields": public_reviewer_call["required_public_evidence_fields"],
            "reviewer_share_kit": 1,
            "reviewer_share_channels": reviewer_share_kit["share_channel_count"],
            "reviewer_share_ready_messages": reviewer_share_kit["ready_message_count"],
            "reviewer_share_linked_submission_paths": reviewer_share_kit["linked_submission_paths"],
            "reviewer_share_required_fields": reviewer_share_kit["required_evidence_fields"],
            "reviewer_share_not_sent": reviewer_share_kit["send_status_counts"]["not_sent"],
            "api_smoke_report": 1,
            "api_smoke_checks": api_smoke["check_count"],
            "api_smoke_passed_checks": api_smoke["passed_count"],
            "performance_baseline": 1,
            "performance_benchmark_count": performance["benchmark_count"],
            "performance_measured_endpoint_calls": sum(check["iterations"] for check in performance["checks"]),
            "demo_usage_baseline": 1,
            "demo_usage_tracked_funnel_steps": len(demo_usage["tracked_usage_funnel"]),
            "demo_usage_entrypoints_verified": sum(1 for value in demo_usage["demo_entrypoints_verified"].values() if value),
            "business_data_intake_baseline": 1,
            "business_data_intake_endpoints": business_data_intake["endpoint_count"],
            "business_data_intake_tests": business_data_intake["test_count"],
            "business_data_intake_max_rows": business_data_intake["safety_limits"]["max_rows"],
            "business_data_intake_max_columns": business_data_intake["safety_limits"]["max_columns"],
            "community_growth_baseline": 1,
            "community_issue_templates": community_growth["issue_template_count"],
            "community_labels": community_growth["label_count"],
            "community_public_growth_channels": len(community_growth["public_growth_channels"]),
            "impact_review_packet": 1,
            "impact_review_business_metrics": impact_review["business_metric_count"],
            "impact_review_evidence_links": impact_review["evidence_link_count"],
            "business_problem_casebook": 1,
            "business_problem_cases": business_casebook["business_case_count"],
            "business_problem_detected_risks": business_casebook["detected_risk_count"],
            "business_problem_owner_handoffs": business_casebook["owner_handoff_count"],
            "business_resolution_brief": 1,
            "business_resolution_findings": business_resolution["detected_signal_counts"]["findings"],
            "business_resolution_risk_areas": business_resolution["detected_signal_counts"]["business_risk_areas"],
            "business_resolution_high_priority_actions": business_resolution["detected_signal_counts"]["high_priority_actions"],
            "business_resolution_owner_handoffs": business_resolution["detected_signal_counts"]["owner_handoffs"],
            "business_resolution_review_request": 1,
            "business_resolution_review_questions": len(business_resolution_review["review_questions"]),
            "business_resolution_review_external_feedback": business_resolution_review["evidence_gate"][
                "current_external_feedback_items"
            ],
            "public_traction_dashboard": 1,
            "public_traction_surfaces": traction["traction_surface_count"],
            "public_traction_growth_channels": traction["growth_channel_count"],
            "public_traction_resume_upgrade_rules": len(traction["resume_upgrade_rules"]),
            "github_traffic_snapshot": 1,
            "github_traffic_available": 1 if traffic["traffic_available"] else 0,
            "public_availability_snapshot": 1,
            "public_availability_endpoint_count": availability["endpoint_count"],
            "public_availability_available_endpoints": availability["available_endpoint_count"],
            "public_availability_successful_workflows": availability["successful_workflow_count"],
            "live_project_scorecard": 1,
            "scorecard_reviewer_paths": SCORECARD_REVIEWER_PATH_COUNT,
            "openapi_required_endpoints": 6,
            "openapi_paths": len(openapi["paths"]),
            "recruiter_pitch_resume_bullets": len(recruiter_pitch["resume_bullets"]),
            "recruiter_pitch_target_roles": len(recruiter_pitch["target_roles"]),
            "application_evidence_pack": 1,
            "application_evidence_links": APPLICATION_EVIDENCE_LINK_COUNT,
            "github_discovery_profile": 1,
            "github_discovery_topics": github_discovery["topic_count"],
            "github_discovery_reviewer_entrypoints": len(github_discovery["reviewer_entrypoints"]),
            "pilot_evidence_quicklink": 1,
            "pilot_evidence_quicklink_actions": pilot_evidence_quicklink["action_count"],
            "pilot_evidence_quicklink_fields": pilot_evidence_quicklink["total_evidence_fields"],
            "pilot_evidence_quicklink_target_metrics": pilot_evidence_quicklink["target_metric_count"],
            "pilot_launch_control_room": 1,
            "pilot_launch_public_issue_threads": pilot_launch_control_room["public_issue_thread_count"],
            "pilot_launch_gates": pilot_launch_control_room["launch_gate_count"],
            "pilot_launch_target_outcomes": pilot_launch_control_room["target_outcome_count"],
            "pilot_launch_reviewer_send_paths": pilot_launch_control_room["reviewer_send_plan_count"],
            "resume_outcome_adjudication": 1,
            "resume_outcome_adjudication_categories": adjudication["claim_category_count"],
            "resume_outcome_adjudication_blocked_categories": adjudication["blocked_category_count"],
            "resume_outcome_adjudication_claimable_categories": adjudication["claimable_category_count"],
            "resume_outcome_scoreboard": 1,
            "resume_outcome_scoreboard_claimable_now": outcome_scoreboard["claimable_now_count"],
            "resume_outcome_scoreboard_blocked": outcome_scoreboard["blocked_outcome_count"],
            "resume_outcome_scoreboard_remaining_evidence": outcome_scoreboard["reviewer_funnel"][
                "remaining_evidence_items"
            ],
            "evidence_acceptance_checklist": 1,
            "evidence_acceptance_items": evidence_acceptance["acceptance_item_count"],
            "evidence_acceptance_accepted_issues": evidence_acceptance["accepted_issue_count"],
            "evidence_acceptance_rejected_issues": evidence_acceptance["rejected_issue_count"],
            "ai_engineer_review_intake": 1,
            "ai_engineer_review_paths": ai_engineer_review_intake["review_path_count"],
            "ai_engineer_review_questions": ai_engineer_review_intake["review_question_count"],
            "ai_engineer_review_countable_conditions": ai_engineer_review_intake["countable_condition_count"],
            "pilot_outreach_messages": len(pilot_outreach["outreach_messages"]),
            "pilot_review_paths": len(pilot_outreach["review_paths"]),
            "pilot_program_segments": len(pilot_plan["participant_segments"]),
            "pilot_program_weeks": len(pilot_plan["weekly_plan"]),
            "pilot_review_tracker": 1,
            "pilot_review_tracker_planned_reviews": pilot_tracker["planned_review_count"],
            "pilot_review_tracker_not_contacted": pilot_tracker["status_counts"]["not_contacted"],
            "pilot_review_tracker_resume_rules": len(pilot_tracker["resume_upgrade_rules"]),
            "pilot_conversion_board": 1,
            "pilot_conversion_stages": pilot_conversion["stage_count"],
            "pilot_conversion_claimable_stages": pilot_conversion["claimable_stage_count"],
            "pilot_conversion_blocked_stages": pilot_conversion["blocked_stage_count"],
            "resume_outcome_readiness": 1,
            "resume_outcome_readiness_stages": resume_outcome_readiness["stage_count"],
            "resume_outcome_claimable_stages": resume_outcome_readiness["claimable_stage_count"],
            "resume_outcome_blocked_stages": resume_outcome_readiness["blocked_stage_count"],
            "resume_outcome_missing_evidence_items": len(resume_outcome_readiness["missing_evidence"]),
            "external_review_evidence_ledger": 1,
            "external_review_ledger_entries": external_ledger["entry_count"],
            "external_review_ledger_requirement_types": external_ledger["evidence_requirement_count"],
            "external_review_ledger_linked_reviews": external_ledger["linked_planned_reviews"],
            "outcome_upgrade_playbook": 1,
            "outcome_upgrade_rules": outcome_upgrade["upgrade_rule_count"],
            "outcome_upgrade_blocked_rules": outcome_upgrade["blocked_upgrade_rule_count"],
            "outcome_upgrade_claimable_now": len(outcome_upgrade["claimable_now"]),
            "resume_claim_upgrade_ledger": 1,
            "resume_claim_upgrade_rows": claim_upgrade["upgrade_row_count"],
            "resume_claim_upgrade_blocked_rows": claim_upgrade["blocked_row_count"],
            "resume_claim_upgrade_claimable_rows": claim_upgrade["claimable_row_count"],
            "reviewer_feedback_packet": 1,
            "reviewer_feedback_tasks": reviewer_packet["reviewer_task_count"],
            "reviewer_feedback_questions": reviewer_packet["evidence_question_count"],
            "reviewer_feedback_conversion_paths": reviewer_packet["conversion_path_count"],
            "reviewer_funnel_board": 1,
            "reviewer_funnel_stages": reviewer_funnel["funnel_stage_count"],
            "reviewer_funnel_open_gaps": reviewer_funnel["open_gap_count"],
            "reviewer_funnel_remaining_evidence_items": reviewer_funnel["total_remaining_evidence_items"],
            "feedback_intake_quality": 1,
            "feedback_intake_required_sections": feedback_intake["required_section_count"],
            "feedback_intake_try_paths": feedback_intake["required_try_path_count"],
            "feedback_intake_outcomes": feedback_intake["required_outcome_count"],
            "feedback_intake_captured_fields": feedback_intake["captured_field_count"],
            "star_growth_kit": 1,
            "star_growth_required_topics": len(star_growth["topic_readiness"]["required_topics"]),
            "star_growth_ethical_actions": len(star_growth["ethical_growth_actions"]),
            "star_growth_resume_upgrade_rules": len(star_growth["resume_upgrade_rules"]),
            "business_case_intake": 1,
            "business_case_intake_required_sections": business_case_intake["required_section_count"],
            "business_case_intake_try_paths": business_case_intake["required_try_path_count"],
            "business_case_intake_outcomes": business_case_intake["required_outcome_count"],
            "business_case_intake_captured_fields": business_case_intake["captured_field_count"],
            "business_case_intake_outcome_fields": len(business_case_intake["resume_outcome_fields"]),
            "business_data_replay_packet": 1,
            "business_data_replay_paths": replay_packet["replay_path_count"],
            "business_data_replay_evidence_fields": replay_packet["evidence_field_count"],
            "business_data_replay_safety_requirements": replay_packet["safety_requirement_count"],
            "business_replay_demo": 1,
            "business_replay_demo_rows": replay_demo["dataset"]["row_count"],
            "business_replay_demo_findings": replay_demo["quality_report_summary"]["finding_count"],
            "business_replay_demo_check_types": replay_demo["quality_report_summary"]["check_count"],
            "business_replay_demo_rule_references": replay_demo["quality_report_summary"]["business_rule_reference_count"],
            "business_replay_demo_root_causes": replay_demo["quality_report_summary"]["root_cause_hypothesis_count"],
            "real_model_runbook": 1,
            "real_model_current_runs": real_model_runbook["current_real_model_runs"],
            "real_model_run_commands": real_model_runbook["run_command_count"],
            "real_model_evidence_fields": real_model_runbook["evidence_field_count"],
            "real_model_acceptance_criteria": real_model_runbook["acceptance_criteria_count"],
            "real_model_safety_gates": real_model_runbook["safety_gate_count"],
            "real_model_evidence_capture": 1,
            "real_model_capture_required_fields": real_model_evidence_capture["capture_required_field_count"],
            "real_model_capture_accepted_runs": real_model_evidence_capture["accepted_real_model_run_count"],
            "real_model_capture_blocked_claims": real_model_evidence_capture["blocked_outcome_claim_count"],
            "real_model_preflight": 1,
            "real_model_preflight_total_checks": real_model_preflight["total_check_count"],
            "real_model_preflight_ready_checks": real_model_preflight["ready_check_count"],
            "real_model_preflight_blocked_checks": real_model_preflight["blocked_check_count"],
            "ai_engineer_readiness": 1,
            "ai_engineer_readiness_implemented_signals": ai_engineer_readiness["implemented_signal_count"],
            "ai_engineer_readiness_partial_signals": ai_engineer_readiness["partial_signal_count"],
            "ai_engineer_readiness_not_claimed_signals": ai_engineer_readiness["not_claimed_signal_count"],
            "implemented_agent_capabilities": len(readiness["implemented"]),
            "partial_agent_capabilities": len(readiness["partial"]),
        },
        "feedback_channels": feedback["feedback_channels"],
        "resume_policy": (
            "Use public demo, release, CI, container, support-ticket outcomes, and readiness metrics now. "
            "Do not claim external users, customer feedback, or production adoption until corresponding public metrics are greater than zero."
        ),
        "resume_safe_signals": [
            f"Public demo and {adoption['release']['tagName']} release",
            f"{adoption['test_count']} passing CI tests",
            f"{verified_outcomes['issue_category_count']} support-ticket issue categories",
            f"{verified_outcomes['root_cause_hypothesis_count']} evidence-ranked root-cause hypotheses",
            (
                f"{verified_outcomes['business_risk_area_count']} business risk areas mapped to "
                f"{verified_outcomes['high_priority_action_count']} high-priority actions and "
                f"{verified_outcomes['owner_handoff_count']} owner handoffs"
            ),
            "Dataset-level memory retrieval over recent sanitized traces",
            f"{eval_summary['scenario_count']}-scenario agent evaluation harness",
            f"{hypothesis_feedback['label_count']} human-reviewed root-cause feedback labels",
            (
                f"Pilot review tracker with {pilot_tracker['planned_review_count']} planned reviewer segments, "
                f"{pilot_tracker['status_counts']['not_contacted']} not-contacted baseline entries, and "
                f"{len(pilot_tracker['resume_upgrade_rules'])} resume-upgrade rules"
            ),
            (
                f"Pilot conversion board with {pilot_conversion['stage_count']} outcome stages, "
                f"{pilot_conversion['claimable_stage_count']} resume-safe readiness claims, and "
                f"{pilot_conversion['blocked_stage_count']} blocked outcome claims until public evidence exists"
            ),
            (
                f"Resume outcome readiness evaluator with {resume_outcome_readiness['stage_count']} stages, "
                f"{resume_outcome_readiness['claimable_stage_count']} claimable readiness lines, "
                f"{resume_outcome_readiness['blocked_stage_count']} blocked outcome claims, and "
                f"{len(resume_outcome_readiness['missing_evidence'])} missing-evidence items"
            ),
            (
                f"External review evidence ledger with {external_ledger['evidence_requirement_count']} public evidence types, "
                f"{external_ledger['linked_planned_reviews']} linked planned reviews, and "
                f"{external_ledger['entry_count']} current evidence entries"
            ),
            (
                f"Outcome upgrade playbook with {outcome_upgrade['upgrade_rule_count']} metric thresholds, "
                f"{outcome_upgrade['blocked_upgrade_rule_count']} blocked upgrade rules, and "
                f"{len(outcome_upgrade['claimable_now'])} baseline signals claimable now"
            ),
            (
                f"Resume claim upgrade ledger with {claim_upgrade['upgrade_row_count']} outcome metrics, "
                f"{claim_upgrade['blocked_row_count']} blocked upgrade rows, "
                f"{claim_upgrade['claimable_row_count']} claimable outcome rows, and exact future resume wording"
            ),
            (
                f"Resume outcome scoreboard with {outcome_scoreboard['claimable_now_count']} claimable evidence-backed "
                f"lines now, {outcome_scoreboard['blocked_outcome_count']} locked outcome claims, and "
                f"{outcome_scoreboard['reviewer_funnel']['remaining_evidence_items']} remaining public evidence items"
            ),
            (
                f"Reviewer feedback packet with {reviewer_packet['reviewer_task_count']} task paths, "
                f"{reviewer_packet['evidence_question_count']} evidence questions, and "
                f"{reviewer_packet['conversion_path_count']} metric conversion paths"
            ),
            (
                f"Reviewer funnel board with {reviewer_funnel['funnel_stage_count']} public evidence paths "
                f"and {reviewer_funnel['total_remaining_evidence_items']} remaining evidence items"
            ),
            f"{incident_memory['incident_pattern_count']} recurring incident patterns retrieved from sanitized traces",
            f"{observability['observed_trace_count']} observed run traces with fallback and verification status",
            (
                f"{observability['model_telemetry']['model_call_count']} mocked LLM calls with "
                f"{observability['model_telemetry']['total_tokens']} tokens, prompt version, latency, "
                "retry budget, and estimated cost telemetry"
            ),
            f"{safety['tool_allowlist_count']} allowed agent tools and {safety['postgres_rejected_write_query_count']} rejected unsafe PostgreSQL queries",
            (
                f"CI-verified agent capability matrix with {capability_matrix['implemented_count']} implemented "
                f"LLM-agent checklist items, {capability_matrix['partial_count']} partial maturity areas, "
                f"and {capability_matrix['not_claimed_count']} explicit not-claimed area"
            ),
            (
                f"Local Docker Compose reviewer demo with {local_demo['seeded_business_table']['row_count']} seeded "
                f"PostgreSQL rows and {len(local_demo['reviewer_routes'])} review paths"
            ),
            (
                f"Runnable release packet with {len(runnable_release['runnable_surfaces'])} runnable surfaces, "
                f"{len(runnable_release['acceptance_checks'])} acceptance checks, and "
                f"{len(runnable_release['openapi_coverage']['required_paths'])} required API paths"
            ),
            (
                f"External-run evidence packet with public issue #{external_run_evidence['public_collection_issue']['number']}, "
                f"{external_run_evidence['review_path_count']} reviewer run paths, "
                f"{external_run_evidence['submission_field_count']} required submission fields, and "
                f"{external_run_evidence['upgrade_rule_count']} resume-upgrade rules"
            ),
            (
                f"External reviewer request pack linked to issue #{external_reviewer_request['public_collection_issue']['number']} "
                f"with {len(external_reviewer_request['outreach_messages'])} copy-ready messages, "
                f"{len({item['run_path'] for item in external_reviewer_request['outreach_messages']})} run paths, "
                f"{len(external_reviewer_request['required_comment_fields'])} evidence fields, and zero-count baseline"
            ),
            (
                f"External-run quickstart page with {external_run_quickstart['review_path_count']} reviewer run paths, "
                f"{external_run_quickstart['submission_field_count']} evidence fields, public issue #18, and privacy boundaries"
            ),
            (
                f"External reviewer outreach tracker with {external_reviewer_outreach['queue_count']} queued reviewer segments, "
                f"{external_reviewer_outreach['source_message_count']} source messages, "
                f"{external_reviewer_outreach['status_counts']['not_contacted']} not-contacted baseline entries, and public-evidence rules"
            ),
            (
                f"External reviewer evidence gate with {len(external_reviewer_gate['gate_rules'])} validation rules, "
                f"{external_reviewer_gate['issue_collection']['collected_issue_count']} collected public GitHub issues, "
                f"{external_reviewer_gate['linked_outreach_queue_count']} linked outreach queue entries, "
                f"{external_reviewer_gate['accepted_issue_count']} accepted public reviewer issues, and sensitive-data safeguards"
            ),
            (
                f"Accepted evidence rollup with {accepted_evidence_rollup['claimable_metric_count']} tracked outcome metrics, "
                f"{accepted_evidence_rollup['accepted_issue_count']} accepted reviewer issues, and "
                f"{accepted_evidence_rollup['blocked_outcome_claim_count']} blocked claims until public evidence exists"
            ),
            (
                f"Business impact ledger with {business_impact_ledger['accepted_business_impact_signal_count']} accepted "
                "business-impact signals, anonymized workflow fields, and blocked resume claims until public evidence exists"
            ),
            (
                f"Reviewer evidence kit with {reviewer_evidence_kit['evidence_form_count']} public issue templates, "
                f"{reviewer_evidence_kit['reviewer_script_step_count']} copy-ready privacy and permission steps, "
                "and zero current external outcome counts"
            ),
            (
                f"Resume traction proof with {resume_traction_proof['claimable_now_count']} claimable launch/quality/traffic/availability signals, "
                f"{resume_traction_proof['future_claim_count']} threshold-based future outcome claims, and "
                f"{resume_traction_proof['blocked_claim_count']} blocked overclaiming rules"
            ),
            (
                f"Reviewer action queue with {reviewer_action_queue['queue_count']} concrete outreach tasks, "
                f"{reviewer_action_queue['evidence_goal_count']} public evidence goals, "
                f"{reviewer_action_queue['not_contacted_count']} not-contacted baseline entries, and zero completed reviews claimed"
            ),
            (
                f"Reviewer outreach execution pack with {reviewer_outreach_execution['ready_message_count']} ready-to-send messages, "
                f"{reviewer_outreach_execution['follow_up_rule_count']} follow-up rules, "
                f"{reviewer_outreach_execution['send_status_counts']['not_sent']} not-sent baseline entries, and zero sent outreach claimed"
            ),
            (
                f"Reviewer outreach status board tracking {reviewer_outreach_status['outreach_slot_count']} reviewer slots, "
                f"{reviewer_outreach_status['status_stage_count']} status stages, and zero sent/replied/accepted outreach claims"
            ),
            (
                f"First-10 outreach execution log with {first_10_outreach_log['entry_count']} copy-ready reviewer messages, "
                f"{first_10_outreach_log['public_issue_entrypoint_count']} public issue entrypoints, "
                f"{first_10_outreach_log['not_sent_count']} not-sent entries, and zero claimable external outcomes"
            ),
            (
                f"Resume outcome metrics board tracking {resume_outcome_metrics['tracked_outcome_count']} outcome metrics, "
                f"{resume_outcome_metrics['claimable_outcome_count']} claimable outcome lines, "
                f"{resume_outcome_metrics['blocked_outcome_count']} blocked outcome lines, and honest user/feedback/star baselines"
            ),
            (
                f"Public metrics provenance with {metrics_provenance['metric_count']} tracked metrics, "
                f"{metrics_provenance['claimable_metric_count']} currently claimable metrics, and evidence-gated "
                "zero counts for users, external feedback, business-case validation, AI Engineer review, and star growth"
            ),
            (
                f"Resume outcome action checklist with {resume_outcome_action_checklist['tracked_action_count']} concrete next actions, "
                f"{resume_outcome_action_checklist['evaluated_public_issue_count']} evaluated public GitHub issues, "
                f"{resume_outcome_action_checklist['accepted_public_issue_count']} accepted public evidence items, and "
                f"{resume_outcome_action_checklist['not_sent_outreach_count']} not-sent reviewer outreach slots"
            ),
            (
                f"Reviewer submission hub with {reviewer_submission_hub['submission_path_count']} public submission paths, "
                f"{reviewer_submission_hub['target_metric_count']} tracked outcome metrics, "
                f"{reviewer_submission_hub['total_required_evidence_fields']} required evidence fields, and zero current outcome claims upgraded"
            ),
            (
                f"First-10 reviewer sprint with {first_10_sprint['slot_count']} public evidence slots, "
                f"{first_10_sprint['issue_launch_count']} issue launch drafts, "
                f"{first_10_sprint['target_metric_count']} target metrics, "
                f"{first_10_sprint['not_sent_count']} not-sent outreach slots, and zero upgraded outcome claims"
            ),
            (
                f"Outcome collection page with {outcome_collection['tracked_action_count']} next actions, "
                f"{outcome_collection['submission_path_count']} submission paths, "
                f"{outcome_collection['required_evidence_field_count']} required evidence fields, "
                f"{outcome_collection['current_counts']['confirmed_external_users']} confirmed users, "
                f"{outcome_collection['current_counts']['external_feedback_items']} feedback items, and "
                f"{outcome_collection['current_counts']['github_stars']} GitHub stars"
            ),
            (
                f"Public reviewer call linked to {public_reviewer_call['reviewer_segment_count']} reviewer segments, "
                f"{public_reviewer_call['linked_submission_paths']} submission paths, "
                f"{public_reviewer_call['linked_outreach_tasks']} outreach tasks, and "
                f"{public_reviewer_call['required_public_evidence_fields']} evidence fields without claiming outcomes"
            ),
            (
                f"Reviewer share kit with {reviewer_share_kit['ready_message_count']} copy-ready messages, "
                f"{reviewer_share_kit['share_channel_count']} share channels, issue #19, "
                f"{reviewer_share_kit['linked_submission_paths']} submission paths, and zero sent or completed outreach claimed"
            ),
            f"CI-verified API smoke report covering {api_smoke['passed_count']} passing FastAPI route checks",
            (
                f"CI-verified local performance baseline covering {performance['benchmark_count']} route benchmarks "
                f"and {sum(check['iterations'] for check in performance['checks'])} measured endpoint calls"
            ),
            (
                f"Public demo usage baseline with {len(demo_usage['tracked_usage_funnel'])} tracked funnel steps and "
                f"{sum(1 for value in demo_usage['demo_entrypoints_verified'].values() if value)} verified entrypoints"
            ),
            (
                f"Business-data intake baseline covering {business_data_intake['endpoint_count']} integration endpoints, "
                f"{business_data_intake['test_count']} API tests, and bounded CSV uploads up to "
                f"{business_data_intake['safety_limits']['max_rows']} rows / "
                f"{business_data_intake['safety_limits']['max_columns']} columns"
            ),
            (
                f"Community growth baseline with {community_growth['issue_template_count']} issue templates, "
                f"{community_growth['label_count']} configured labels, and "
                f"{len(community_growth['public_growth_channels'])} public contribution or feedback channels"
            ),
            (
                f"Impact review packet with {impact_review['business_metric_count']} verified business metrics, "
                f"{impact_review['evidence_link_count']} evidence links, "
                f"{impact_review['business_metrics']['recommended_actions']} remediation actions, and "
                f"{impact_review['business_metrics']['owner_handoffs']} owner handoffs"
            ),
            (
                f"Business problem casebook with {business_casebook['business_case_count']} verified case, "
                f"{business_casebook['detected_risk_count']} detected business risks, and "
                f"{business_casebook['owner_handoff_count']} owner handoffs"
            ),
            (
                f"Business resolution brief with {business_resolution['detected_signal_counts']['findings']} findings, "
                f"{business_resolution['detected_signal_counts']['business_risk_areas']} business risk areas, "
                f"{business_resolution['detected_signal_counts']['high_priority_actions']} high-priority actions, and "
                f"{business_resolution['detected_signal_counts']['owner_handoffs']} owner handoffs without claiming customer adoption"
            ),
            (
                "Public business-resolution review request with 5 focused questions and explicit evidence gates "
                "before any external feedback or business validation can count"
            ),
            (
                f"Public traction dashboard with {traction['traction_surface_count']} live project surfaces, "
                f"{traction['growth_channel_count']} growth or review channels, "
                f"{traction['tracked_funnel_steps']} tracked funnel steps, and "
                f"{len(traction['resume_upgrade_rules'])} resume upgrade rules"
            ),
            (
                f"GitHub traffic snapshot with {traffic['views']['count']} views, "
                f"{traffic['views']['uniques']} unique visitors, {traffic['clones']['count']} clones, and "
                f"{traffic['clones']['uniques']} unique cloners in GitHub's rolling 14-day window"
            ),
            (
                f"Public availability snapshot with {availability['available_endpoint_count']}/"
                f"{availability['endpoint_count']} reachable public endpoints and "
                f"{availability['successful_workflow_count']}/{availability['workflow_count']} "
                "successful main-branch workflows"
            ),
            f"{SCORECARD_REVIEWER_PATH_COUNT} reviewer paths in a CI-verified live project scorecard",
            "CI-verified OpenAPI contract covering 6 integration endpoints",
            f"{len(recruiter_pitch['resume_bullets'])} recruiter-safe resume bullets for {len(recruiter_pitch['target_roles'])} target roles",
            f"{APPLICATION_EVIDENCE_LINK_COUNT} application evidence links in a recruiter-ready evidence pack",
            (
                f"GitHub discovery profile with {github_discovery['topic_count']} precise topics, "
                f"{len(github_discovery['reviewer_entrypoints'])} reviewer entrypoints, public homepage metadata, "
                "and zero-star baseline"
            ),
            (
                f"Pilot evidence quicklink with {pilot_evidence_quicklink['action_count']} short reviewer actions, "
                f"{pilot_evidence_quicklink['total_evidence_fields']} required evidence fields, "
                f"{pilot_evidence_quicklink['target_metric_count']} target outcome metrics, and zero-count baselines"
            ),
            (
                f"Pilot launch control room with {pilot_launch_control_room['public_issue_thread_count']} public issue "
                f"threads, {pilot_launch_control_room['launch_gate_count']} launch gates, "
                f"{pilot_launch_control_room['target_outcome_count']} target outcome metrics, and "
                f"{pilot_launch_control_room['reviewer_send_plan_count']} reviewer-send paths"
            ),
            (
                f"Resume outcome adjudication report with {adjudication['claim_category_count']} outcome categories, "
                f"{adjudication['claimable_category_count']} claimable external categories, "
                f"{adjudication['blocked_category_count']} blocked categories, and explicit unlock conditions"
            ),
            (
                f"AI Engineer review intake with {ai_engineer_review_intake['review_path_count']} review paths, "
                f"{ai_engineer_review_intake['review_question_count']} reviewer questions, "
                f"{ai_engineer_review_intake['countable_condition_count']} countable-evidence conditions, and zero accepted reviews"
            ),
            f"{len(pilot_outreach['outreach_messages'])} pilot outreach messages and {len(pilot_outreach['review_paths'])} review paths for collecting real feedback",
            f"{len(pilot_plan['participant_segments'])} pilot participant segments across a {len(pilot_plan['weekly_plan'])}-week feedback plan",
            (
                f"Feedback intake system with {feedback_intake['required_section_count']} required sections, "
                f"{feedback_intake['required_try_path_count']} demo paths, "
                f"{feedback_intake['required_outcome_count']} outcome signals, and "
                f"{feedback_intake['captured_field_count']} captured evidence groups"
            ),
            (
                f"Star growth kit with {len(star_growth['topic_readiness']['required_topics'])} verified repo topics, "
                f"{len(star_growth['ethical_growth_actions'])} ethical growth actions, and "
                f"{len(star_growth['resume_upgrade_rules'])} resume upgrade rules with traffic context without inflating current stars"
            ),
            (
                f"Business-case intake path with {business_case_intake['required_section_count']} required sections, "
                f"{business_case_intake['required_try_path_count']} tried paths, "
                f"{business_case_intake['required_outcome_count']} outcome signals, and "
                f"{business_case_intake['captured_field_count']} captured evidence groups including "
                f"{len(business_case_intake['resume_outcome_fields'])} resume outcome fields"
            ),
            (
                f"Business-data replay packet with {replay_packet['replay_path_count']} safe replay paths, "
                f"{replay_packet['evidence_field_count']} evidence fields, "
                f"{replay_packet['safety_requirement_count']} safety requirements, and zero current external replay claims"
            ),
            (
                f"Business replay demo with {replay_demo['dataset']['row_count']} anonymized rows, "
                f"{replay_demo['quality_report_summary']['finding_count']} findings, "
                f"{replay_demo['quality_report_summary']['check_count']} failed check types, "
                f"{replay_demo['quality_report_summary']['business_rule_reference_count']} business-rule references, "
                f"and deterministic verification"
            ),
            (
                f"Real-model runbook with {real_model_runbook['run_command_count']} run commands, "
                f"{real_model_runbook['evidence_field_count']} evidence fields, "
                f"{real_model_runbook['acceptance_criteria_count']} acceptance criteria, "
                f"{real_model_runbook['safety_gate_count']} safety gates, and zero current real model run claims"
            ),
            (
                f"Real-model evidence capture gate with {real_model_evidence_capture['capture_required_field_count']} "
                f"required fields, {real_model_evidence_capture['accepted_real_model_run_count']} accepted real-model runs, "
                f"and {real_model_evidence_capture['blocked_outcome_claim_count']} blocked outcome claims until redacted telemetry passes"
            ),
            (
                f"Real-model preflight gate with {real_model_preflight['total_check_count']} readiness checks, "
                f"{real_model_preflight['ready_check_count']} ready checks, "
                f"{real_model_preflight['blocked_check_count']} blocked checks, and no paid model call execution"
            ),
            (
                f"AI Engineer readiness artifact with {ai_engineer_readiness['implemented_signal_count']} implemented "
                f"AI skill signals, {ai_engineer_readiness['partial_signal_count']} partial signal, and "
                f"{ai_engineer_readiness['not_claimed_signal_count']} explicitly blocked signal"
            ),
            f"{verified_outcomes['recommended_action_count']} evidence-backed remediation actions",
            f"{len(readiness['implemented'])} implemented LLM agent-readiness capabilities",
            f"{adoption['forks']} public fork and {adoption['stars']} public stars as current honest adoption baseline",
        ],
        "not_claimed": [
            "external users",
            "customer feedback",
            "enterprise production usage",
            "GitHub stars beyond the current public count",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    metrics = payload["public_metrics"]
    outcomes = payload["verified_project_outcomes"]
    channels = "\n".join(f"- [{item['name']}]({item['url']}) -> `{item['counts_toward']}`" for item in payload["feedback_channels"])
    signals = "\n".join(f"- {item}" for item in payload["resume_safe_signals"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Public Metrics Summary

This page collects public adoption, feedback, release, CI, and outcome metrics into one resume-safe artifact.

## Public Footprint

| Metric | Current value |
| --- | ---: |
| Stars | {metrics["stars"]} |
| Forks | {metrics["forks"]} |
| Watchers | {metrics["watchers"]} |
| GitHub issues | {metrics["issues_total"]} |
| Passing CI tests | {metrics["test_count"]} |
| Tracked public outcome metrics | {metrics["tracked_public_metrics"]} |
| Claimable public outcome metrics | {metrics["claimable_public_metrics"]} |
| External feedback items | {metrics["external_feedback_items"]} |
| Confirmed external users | {metrics["confirmed_external_users"]} |
| Reproducible feedback items | {metrics["reproducible_feedback_items"]} |
| GitHub views | {metrics["github_view_count"]} |
| GitHub unique visitors | {metrics["github_unique_visitors"]} |
| GitHub clones | {metrics["github_clone_count"]} |
| GitHub unique cloners | {metrics["github_unique_cloners"]} |
| Available public endpoints | {metrics["available_public_endpoints"]} / {metrics["public_endpoint_count"]} |
| Successful main-branch workflows | {metrics["successful_main_branch_workflows"]} / {metrics["main_branch_workflow_count"]} |

## Verified Project Outcomes

| Outcome | Current value |
| --- | ---: |
| Support-ticket issue categories | {outcomes["support_ticket_issue_categories"]} |
| Support-ticket findings | {outcomes["support_ticket_findings"]} |
| Evidence-ranked root-cause hypotheses | {outcomes["root_cause_hypotheses"]} |
| Business risk areas | {outcomes["business_risk_areas"]} |
| High-priority actions | {outcomes["high_priority_actions"]} |
| Owner handoffs | {outcomes["owner_handoffs"]} |
| Agent evaluation scenarios | {outcomes["eval_scenarios"]} |
| Root-cause feedback labels | {outcomes["hypothesis_feedback_labels"]} |
| Recurring incident patterns | {outcomes["incident_pattern_count"]} |
| Observed run traces | {outcomes["observed_trace_count"]} |
| Fallback events captured | {outcomes["fallback_event_count"]} |
| Model telemetry artifact | {outcomes["model_telemetry_artifact"]} |
| Mock LLM calls | {outcomes["mock_model_calls"]} |
| Mock LLM tokens | {outcomes["mock_model_tokens"]} |
| Mock estimated cost USD | {outcomes["mock_estimated_cost_usd"]} |
| Allowed agent tools | {outcomes["tool_allowlist_count"]} |
| Rejected unsafe PostgreSQL queries | {outcomes["postgres_rejected_write_query_count"]} |
| Report verifier rules | {outcomes["verifier_rule_count"]} |
| Agent capability matrix | {outcomes["agent_capability_matrix"]} |
| Agent matrix implemented capabilities | {outcomes["agent_matrix_implemented_capabilities"]} |
| Agent matrix partial maturity areas | {outcomes["agent_matrix_partial_capabilities"]} |
| Agent matrix not-claimed areas | {outcomes["agent_matrix_not_claimed_count"]} |
| Local reviewer demo | {outcomes["local_reviewer_demo"]} |
| Local reviewer seeded rows | {outcomes["local_reviewer_seeded_rows"]} |
| Local reviewer routes | {outcomes["local_reviewer_routes"]} |
| Runnable release packet | {outcomes["runnable_release_packet"]} |
| Runnable release surfaces | {outcomes["runnable_release_surfaces"]} |
| Runnable release acceptance checks | {outcomes["runnable_release_acceptance_checks"]} |
| Runnable release required API paths | {outcomes["runnable_release_required_api_paths"]} |
| External run evidence packet | {outcomes["external_run_evidence_packet"]} |
| External run review paths | {outcomes["external_run_review_paths"]} |
| External run submission fields | {outcomes["external_run_submission_fields"]} |
| External run upgrade rules | {outcomes["external_run_upgrade_rules"]} |
| External reviewer request pack | {outcomes["external_reviewer_request_pack"]} |
| External reviewer request messages | {outcomes["external_reviewer_request_messages"]} |
| External reviewer request run paths | {outcomes["external_reviewer_request_run_paths"]} |
| External reviewer request evidence fields | {outcomes["external_reviewer_request_fields"]} |
| External run quickstart page | {outcomes["external_run_quickstart_page"]} |
| External run quickstart paths | {outcomes["external_run_quickstart_paths"]} |
| External run quickstart fields | {outcomes["external_run_quickstart_fields"]} |
| External reviewer outreach tracker | {outcomes["external_reviewer_outreach_tracker"]} |
| External reviewer outreach queue | {outcomes["external_reviewer_outreach_queue"]} |
| External reviewer outreach not contacted | {outcomes["external_reviewer_outreach_not_contacted"]} |
| External reviewer outreach source messages | {outcomes["external_reviewer_outreach_source_messages"]} |
| External reviewer evidence gate | {outcomes["external_reviewer_evidence_gate"]} |
| External reviewer evidence gate rules | {outcomes["external_reviewer_gate_rules"]} |
| External reviewer evidence gate collected public issues | {outcomes["external_reviewer_gate_collected_issues"]} |
| External reviewer evidence gate accepted issues | {outcomes["external_reviewer_gate_accepted_issues"]} |
| External reviewer evidence gate linked queue entries | {outcomes["external_reviewer_gate_linked_queue"]} |
| Accepted evidence rollup | {outcomes["accepted_evidence_rollup"]} |
| Accepted evidence rollup claimable metrics | {outcomes["accepted_evidence_rollup_claimable_metrics"]} |
| Accepted evidence rollup accepted issues | {outcomes["accepted_evidence_rollup_accepted_issues"]} |
| Accepted evidence rollup blocked claims | {outcomes["accepted_evidence_rollup_blocked_claims"]} |
| Business impact ledger | {outcomes["business_impact_ledger"]} |
| Business impact ledger accepted signals | {outcomes["business_impact_ledger_accepted_signals"]} |
| Reviewer evidence kit | {outcomes["reviewer_evidence_kit"]} |
| Reviewer evidence forms | {outcomes["reviewer_evidence_forms"]} |
| Reviewer evidence script steps | {outcomes["reviewer_evidence_script_steps"]} |
| Resume traction proof | {outcomes["resume_traction_proof"]} |
| Resume traction claimable now | {outcomes["resume_traction_claimable_now"]} |
| Resume traction future claims | {outcomes["resume_traction_future_claims"]} |
| Resume traction blocked claims | {outcomes["resume_traction_blocked_claims"]} |
| Reviewer action queue | {outcomes["reviewer_action_queue"]} |
| Reviewer action tasks | {outcomes["reviewer_action_tasks"]} |
| Reviewer action not-contacted entries | {outcomes["reviewer_action_not_contacted"]} |
| Reviewer action evidence goals | {outcomes["reviewer_action_evidence_goals"]} |
| Reviewer outreach execution pack | {outcomes["reviewer_outreach_execution_pack"]} |
| Reviewer outreach ready messages | {outcomes["reviewer_outreach_ready_messages"]} |
| Reviewer outreach follow-up rules | {outcomes["reviewer_outreach_follow_up_rules"]} |
| Reviewer outreach not-sent entries | {outcomes["reviewer_outreach_not_sent"]} |
| Reviewer outreach evidence goals | {outcomes["reviewer_outreach_evidence_goals"]} |
| Reviewer outreach status board | {outcomes["reviewer_outreach_status_board"]} |
| Reviewer outreach status slots | {outcomes["reviewer_outreach_status_slots"]} |
| Reviewer outreach status stages | {outcomes["reviewer_outreach_status_stages"]} |
| Reviewer outreach status not-sent entries | {outcomes["reviewer_outreach_status_not_sent"]} |
| Reviewer outreach status accepted evidence | {outcomes["reviewer_outreach_status_accepted_evidence"]} |
| Resume outcome metrics | {outcomes["resume_outcome_metrics"]} |
| Resume outcome metrics tracked | {outcomes["resume_outcome_metrics_tracked"]} |
| Resume outcome metrics claimable | {outcomes["resume_outcome_metrics_claimable"]} |
| Resume outcome metrics blocked | {outcomes["resume_outcome_metrics_blocked"]} |
| Public metrics provenance | {outcomes["public_metrics_provenance"]} |
| Public metrics provenance tracked metrics | {outcomes["public_metrics_provenance_tracked"]} |
| Public metrics provenance claimable metrics | {outcomes["public_metrics_provenance_claimable"]} |
| Public metrics provenance blocked or baseline metrics | {outcomes["public_metrics_provenance_blocked_or_baseline"]} |
| Resume outcome action checklist | {outcomes["resume_outcome_action_checklist"]} |
| Resume outcome action count | {outcomes["resume_outcome_action_count"]} |
| Resume outcome next actions needed | {outcomes["resume_outcome_next_actions_needed"]} |
| Resume outcome action accepted public evidence | {outcomes["resume_outcome_action_accepted_public_evidence"]} |
| Reviewer submission hub | {outcomes["reviewer_submission_hub"]} |
| Reviewer submission paths | {outcomes["reviewer_submission_paths"]} |
| Reviewer submission target metrics | {outcomes["reviewer_submission_target_metrics"]} |
| Reviewer submission required fields | {outcomes["reviewer_submission_required_fields"]} |
| First 10 reviewer sprint | {outcomes["first_10_reviewer_sprint"]} |
| First 10 reviewer slots | {outcomes["first_10_reviewer_slots"]} |
| First 10 reviewer issue launch drafts | {outcomes["first_10_reviewer_issue_launch_drafts"]} |
| First 10 reviewer public issue entrypoints | {outcomes["first_10_reviewer_public_issue_entrypoints"]} |
| First 10 reviewer target metrics | {outcomes["first_10_reviewer_target_metrics"]} |
| First 10 reviewer not-sent entries | {outcomes["first_10_reviewer_not_sent"]} |
| First 10 reviewer completed entries | {outcomes["first_10_reviewer_completed"]} |
| First 10 outreach execution log | {outcomes["first_10_outreach_execution_log"]} |
| First 10 outreach copy-ready messages | {outcomes["first_10_outreach_messages"]} |
| First 10 outreach public issue entrypoints | {outcomes["first_10_outreach_public_issue_entrypoints"]} |
| First 10 outreach not-sent entries | {outcomes["first_10_outreach_not_sent"]} |
| First 10 outreach accepted evidence | {outcomes["first_10_outreach_accepted_evidence"]} |
| Outcome collection page | {outcomes["outcome_collection_page"]} |
| Outcome collection actions | {outcomes["outcome_collection_actions"]} |
| Outcome collection submission paths | {outcomes["outcome_collection_submission_paths"]} |
| Outcome collection evidence fields | {outcomes["outcome_collection_evidence_fields"]} |
| Public reviewer call | {outcomes["public_reviewer_call"]} |
| Public reviewer call segments | {outcomes["public_reviewer_call_segments"]} |
| Public reviewer call submission paths | {outcomes["public_reviewer_call_submission_paths"]} |
| Public reviewer call outreach tasks | {outcomes["public_reviewer_call_outreach_tasks"]} |
| Public reviewer call evidence fields | {outcomes["public_reviewer_call_evidence_fields"]} |
| Reviewer share kit | {outcomes["reviewer_share_kit"]} |
| Reviewer share channels | {outcomes["reviewer_share_channels"]} |
| Reviewer share ready messages | {outcomes["reviewer_share_ready_messages"]} |
| Reviewer share linked submission paths | {outcomes["reviewer_share_linked_submission_paths"]} |
| Reviewer share required fields | {outcomes["reviewer_share_required_fields"]} |
| Reviewer share not sent | {outcomes["reviewer_share_not_sent"]} |
| API smoke report | {outcomes["api_smoke_report"]} |
| API smoke checks | {outcomes["api_smoke_checks"]} |
| API smoke passed checks | {outcomes["api_smoke_passed_checks"]} |
| Performance baseline | {outcomes["performance_baseline"]} |
| Performance route benchmarks | {outcomes["performance_benchmark_count"]} |
| Performance measured endpoint calls | {outcomes["performance_measured_endpoint_calls"]} |
| Demo usage baseline | {outcomes["demo_usage_baseline"]} |
| Demo usage tracked funnel steps | {outcomes["demo_usage_tracked_funnel_steps"]} |
| Demo usage entrypoints verified | {outcomes["demo_usage_entrypoints_verified"]} |
| Business-data intake baseline | {outcomes["business_data_intake_baseline"]} |
| Business-data intake endpoints | {outcomes["business_data_intake_endpoints"]} |
| Business-data intake API tests | {outcomes["business_data_intake_tests"]} |
| Business-data intake max rows | {outcomes["business_data_intake_max_rows"]} |
| Business-data intake max columns | {outcomes["business_data_intake_max_columns"]} |
| Community growth baseline | {outcomes["community_growth_baseline"]} |
| Community issue templates | {outcomes["community_issue_templates"]} |
| Community labels | {outcomes["community_labels"]} |
| Community public growth channels | {outcomes["community_public_growth_channels"]} |
| Impact review packet | {outcomes["impact_review_packet"]} |
| Impact review business metrics | {outcomes["impact_review_business_metrics"]} |
| Impact review evidence links | {outcomes["impact_review_evidence_links"]} |
| Business problem casebook | {outcomes["business_problem_casebook"]} |
| Business problem cases | {outcomes["business_problem_cases"]} |
| Business problem detected risks | {outcomes["business_problem_detected_risks"]} |
| Business problem owner handoffs | {outcomes["business_problem_owner_handoffs"]} |
| Business resolution brief | {outcomes["business_resolution_brief"]} |
| Business resolution findings | {outcomes["business_resolution_findings"]} |
| Business resolution risk areas | {outcomes["business_resolution_risk_areas"]} |
| Business resolution high-priority actions | {outcomes["business_resolution_high_priority_actions"]} |
| Business resolution owner handoffs | {outcomes["business_resolution_owner_handoffs"]} |
| Business resolution review request | {outcomes["business_resolution_review_request"]} |
| Business resolution review questions | {outcomes["business_resolution_review_questions"]} |
| Business resolution review external feedback | {outcomes["business_resolution_review_external_feedback"]} |
| Public traction dashboard | {outcomes["public_traction_dashboard"]} |
| Public traction surfaces | {outcomes["public_traction_surfaces"]} |
| Public traction growth channels | {outcomes["public_traction_growth_channels"]} |
| Public traction resume upgrade rules | {outcomes["public_traction_resume_upgrade_rules"]} |
| GitHub traffic snapshot | {outcomes["github_traffic_snapshot"]} |
| GitHub traffic available | {outcomes["github_traffic_available"]} |
| Public availability snapshot | {outcomes["public_availability_snapshot"]} |
| Public availability endpoints | {outcomes["public_availability_endpoint_count"]} |
| Public availability reachable endpoints | {outcomes["public_availability_available_endpoints"]} |
| Public availability successful workflows | {outcomes["public_availability_successful_workflows"]} |
| Live project scorecard | {outcomes["live_project_scorecard"]} |
| Scorecard reviewer paths | {outcomes["scorecard_reviewer_paths"]} |
| OpenAPI required integration endpoints | {outcomes["openapi_required_endpoints"]} |
| OpenAPI paths | {outcomes["openapi_paths"]} |
| Recruiter-safe resume bullets | {outcomes["recruiter_pitch_resume_bullets"]} |
| Recruiter pitch target roles | {outcomes["recruiter_pitch_target_roles"]} |
| Application evidence pack | {outcomes["application_evidence_pack"]} |
| Application evidence links | {outcomes["application_evidence_links"]} |
| GitHub discovery profile | {outcomes["github_discovery_profile"]} |
| GitHub discovery topics | {outcomes["github_discovery_topics"]} |
| GitHub discovery reviewer entrypoints | {outcomes["github_discovery_reviewer_entrypoints"]} |
| Pilot evidence quicklink | {outcomes["pilot_evidence_quicklink"]} |
| Pilot evidence quicklink actions | {outcomes["pilot_evidence_quicklink_actions"]} |
| Pilot evidence quicklink fields | {outcomes["pilot_evidence_quicklink_fields"]} |
| Pilot evidence quicklink target metrics | {outcomes["pilot_evidence_quicklink_target_metrics"]} |
| Pilot launch control room | {outcomes["pilot_launch_control_room"]} |
| Pilot launch public issue threads | {outcomes["pilot_launch_public_issue_threads"]} |
| Pilot launch gates | {outcomes["pilot_launch_gates"]} |
| Pilot launch target outcomes | {outcomes["pilot_launch_target_outcomes"]} |
| Pilot launch reviewer-send paths | {outcomes["pilot_launch_reviewer_send_paths"]} |
| Resume outcome adjudication | {outcomes["resume_outcome_adjudication"]} |
| Resume outcome adjudication categories | {outcomes["resume_outcome_adjudication_categories"]} |
| Resume outcome adjudication blocked categories | {outcomes["resume_outcome_adjudication_blocked_categories"]} |
| Resume outcome adjudication claimable categories | {outcomes["resume_outcome_adjudication_claimable_categories"]} |
| Resume outcome scoreboard | {outcomes["resume_outcome_scoreboard"]} |
| Resume outcome scoreboard claimable now | {outcomes["resume_outcome_scoreboard_claimable_now"]} |
| Resume outcome scoreboard blocked claims | {outcomes["resume_outcome_scoreboard_blocked"]} |
| Resume outcome scoreboard remaining evidence | {outcomes["resume_outcome_scoreboard_remaining_evidence"]} |
| Evidence acceptance checklist | {outcomes["evidence_acceptance_checklist"]} |
| Evidence acceptance items | {outcomes["evidence_acceptance_items"]} |
| Evidence acceptance accepted issues | {outcomes["evidence_acceptance_accepted_issues"]} |
| Evidence acceptance rejected issues | {outcomes["evidence_acceptance_rejected_issues"]} |
| AI Engineer review intake | {outcomes["ai_engineer_review_intake"]} |
| AI Engineer review paths | {outcomes["ai_engineer_review_paths"]} |
| AI Engineer review questions | {outcomes["ai_engineer_review_questions"]} |
| AI Engineer review countable conditions | {outcomes["ai_engineer_review_countable_conditions"]} |
| Pilot outreach messages | {outcomes["pilot_outreach_messages"]} |
| Pilot review paths | {outcomes["pilot_review_paths"]} |
| Pilot program segments | {outcomes["pilot_program_segments"]} |
| Pilot program weeks | {outcomes["pilot_program_weeks"]} |
| Pilot review tracker | {outcomes["pilot_review_tracker"]} |
| Pilot review tracker planned reviews | {outcomes["pilot_review_tracker_planned_reviews"]} |
| Pilot review tracker not-contacted entries | {outcomes["pilot_review_tracker_not_contacted"]} |
| Pilot review tracker resume rules | {outcomes["pilot_review_tracker_resume_rules"]} |
| Pilot conversion board | {outcomes["pilot_conversion_board"]} |
| Pilot conversion stages | {outcomes["pilot_conversion_stages"]} |
| Pilot conversion claimable stages | {outcomes["pilot_conversion_claimable_stages"]} |
| Pilot conversion blocked stages | {outcomes["pilot_conversion_blocked_stages"]} |
| Resume outcome readiness | {outcomes["resume_outcome_readiness"]} |
| Resume outcome readiness stages | {outcomes["resume_outcome_readiness_stages"]} |
| Resume outcome claimable stages | {outcomes["resume_outcome_claimable_stages"]} |
| Resume outcome blocked stages | {outcomes["resume_outcome_blocked_stages"]} |
| Resume outcome missing evidence items | {outcomes["resume_outcome_missing_evidence_items"]} |
| External review evidence ledger | {outcomes["external_review_evidence_ledger"]} |
| External review ledger entries | {outcomes["external_review_ledger_entries"]} |
| External review ledger requirement types | {outcomes["external_review_ledger_requirement_types"]} |
| External review ledger linked reviews | {outcomes["external_review_ledger_linked_reviews"]} |
| Outcome upgrade playbook | {outcomes["outcome_upgrade_playbook"]} |
| Outcome upgrade rules | {outcomes["outcome_upgrade_rules"]} |
| Outcome upgrade blocked rules | {outcomes["outcome_upgrade_blocked_rules"]} |
| Outcome upgrade claimable-now signals | {outcomes["outcome_upgrade_claimable_now"]} |
| Reviewer feedback packet | {outcomes["reviewer_feedback_packet"]} |
| Reviewer feedback tasks | {outcomes["reviewer_feedback_tasks"]} |
| Reviewer feedback evidence questions | {outcomes["reviewer_feedback_questions"]} |
| Reviewer feedback conversion paths | {outcomes["reviewer_feedback_conversion_paths"]} |
| Feedback intake quality | {outcomes["feedback_intake_quality"]} |
| Feedback intake required sections | {outcomes["feedback_intake_required_sections"]} |
| Feedback intake demo paths | {outcomes["feedback_intake_try_paths"]} |
| Feedback intake outcome signals | {outcomes["feedback_intake_outcomes"]} |
| Feedback intake captured evidence groups | {outcomes["feedback_intake_captured_fields"]} |
| Star growth kit | {outcomes["star_growth_kit"]} |
| Star growth required topics | {outcomes["star_growth_required_topics"]} |
| Star growth ethical actions | {outcomes["star_growth_ethical_actions"]} |
| Star growth resume upgrade rules | {outcomes["star_growth_resume_upgrade_rules"]} |
| Business-case intake | {outcomes["business_case_intake"]} |
| Business-case intake required sections | {outcomes["business_case_intake_required_sections"]} |
| Business-case intake tried paths | {outcomes["business_case_intake_try_paths"]} |
| Business-case intake outcome signals | {outcomes["business_case_intake_outcomes"]} |
| Business-case intake captured evidence groups | {outcomes["business_case_intake_captured_fields"]} |
| Business-case intake resume outcome fields | {outcomes["business_case_intake_outcome_fields"]} |
| Business-data replay packet | {outcomes["business_data_replay_packet"]} |
| Business-data replay paths | {outcomes["business_data_replay_paths"]} |
| Business-data replay evidence fields | {outcomes["business_data_replay_evidence_fields"]} |
| Business-data replay safety requirements | {outcomes["business_data_replay_safety_requirements"]} |
| Business replay demo | {outcomes["business_replay_demo"]} |
| Business replay demo rows | {outcomes["business_replay_demo_rows"]} |
| Business replay demo findings | {outcomes["business_replay_demo_findings"]} |
| Business replay demo failed check types | {outcomes["business_replay_demo_check_types"]} |
| Business replay demo rule references | {outcomes["business_replay_demo_rule_references"]} |
| Business replay demo root causes | {outcomes["business_replay_demo_root_causes"]} |
| Real-model runbook | {outcomes["real_model_runbook"]} |
| Current real model runs | {outcomes["real_model_current_runs"]} |
| Real-model run commands | {outcomes["real_model_run_commands"]} |
| Real-model evidence fields | {outcomes["real_model_evidence_fields"]} |
| Real-model acceptance criteria | {outcomes["real_model_acceptance_criteria"]} |
| Real-model safety gates | {outcomes["real_model_safety_gates"]} |
| AI Engineer readiness | {outcomes["ai_engineer_readiness"]} |
| AI Engineer readiness implemented signals | {outcomes["ai_engineer_readiness_implemented_signals"]} |
| AI Engineer readiness partial signals | {outcomes["ai_engineer_readiness_partial_signals"]} |
| AI Engineer readiness not-claimed signals | {outcomes["ai_engineer_readiness_not_claimed_signals"]} |
| Agent maturity audit | {outcomes["agent_maturity_audit"]} |
| Agent maturity audit rows | {outcomes["agent_maturity_audit_rows"]} |
| Agent maturity implemented areas | {outcomes["agent_maturity_implemented_areas"]} |
| Agent maturity partial areas | {outcomes["agent_maturity_partial_areas"]} |
| Agent maturity not-claimed areas | {outcomes["agent_maturity_not_claimed_areas"]} |
| Recommended remediation actions | {outcomes["recommended_actions"]} |
| Implemented LLM agent-readiness capabilities | {outcomes["implemented_agent_capabilities"]} |
| Partial agent-readiness capabilities documented | {outcomes["partial_agent_capabilities"]} |

## Feedback Channels

{channels}

## Resume-Safe Signals

{signals}

## Not Claimed

{not_claimed}
"""


def verify_public_metrics_summary(payload: dict[str, Any]) -> dict[str, Any]:
    metrics = payload["public_metrics"]
    outcomes = payload["verified_project_outcomes"]
    expected_metrics = {
        "stars": 0,
        "forks": 1,
        "test_count": 202,
        "tracked_public_metrics": 8,
        "claimable_public_metrics": 2,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
    }
    for key, expected in expected_metrics.items():
        if metrics.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {metrics.get(key)!r}")
    for key in (
        "github_view_count",
        "github_unique_visitors",
        "github_clone_count",
        "github_unique_cloners",
        "available_public_endpoints",
        "public_endpoint_count",
        "successful_main_branch_workflows",
        "main_branch_workflow_count",
    ):
        if metrics.get(key, -1) < 0:
            raise AssertionError(f"{key} must be non-negative")
    if metrics["github_unique_visitors"] > metrics["github_view_count"]:
        raise AssertionError("unique GitHub visitors cannot exceed views")
    if metrics["github_unique_cloners"] > metrics["github_clone_count"]:
        raise AssertionError("unique GitHub cloners cannot exceed clones")
    if metrics["available_public_endpoints"] > metrics["public_endpoint_count"]:
        raise AssertionError("available public endpoints cannot exceed total endpoints")
    if metrics["successful_main_branch_workflows"] > metrics["main_branch_workflow_count"]:
        raise AssertionError("successful main-branch workflows cannot exceed total workflows")
    expected_outcomes = {
        "support_ticket_issue_categories": 4,
        "root_cause_hypotheses": 3,
        "business_risk_areas": 4,
        "high_priority_actions": 3,
        "owner_handoffs": 4,
        "eval_scenarios": 14,
        "hypothesis_feedback_labels": 3,
        "incident_pattern_count": 3,
        "observed_trace_count": 2,
        "fallback_event_count": 2,
        "model_telemetry_artifact": 1,
        "mock_model_calls": 2,
        "mock_model_tokens": 360,
        "tool_allowlist_count": 9,
        "postgres_rejected_write_query_count": 3,
        "verifier_rule_count": 6,
        "agent_capability_matrix": 1,
        "agent_matrix_implemented_capabilities": 13,
        "agent_matrix_partial_capabilities": 4,
        "agent_matrix_not_claimed_count": 1,
        "local_reviewer_demo": 1,
        "local_reviewer_seeded_rows": 8,
        "local_reviewer_routes": 3,
        "runnable_release_packet": 1,
        "runnable_release_surfaces": 3,
        "runnable_release_acceptance_checks": 4,
        "runnable_release_required_api_paths": 6,
        "external_run_evidence_packet": 1,
        "external_run_review_paths": 3,
        "external_run_submission_fields": 8,
        "external_run_upgrade_rules": 3,
        "external_reviewer_request_pack": 1,
        "external_reviewer_request_messages": 3,
        "external_reviewer_request_run_paths": 3,
        "external_reviewer_request_fields": 8,
        "external_run_quickstart_page": 1,
        "external_run_quickstart_paths": 3,
        "external_run_quickstart_fields": 8,
        "external_reviewer_outreach_tracker": 1,
        "external_reviewer_outreach_queue": 3,
        "external_reviewer_outreach_not_contacted": 3,
        "external_reviewer_outreach_source_messages": 3,
        "external_reviewer_evidence_gate": 1,
        "external_reviewer_gate_rules": 9,
        "external_reviewer_gate_accepted_issues": 0,
        "external_reviewer_gate_linked_queue": 3,
        "accepted_evidence_rollup": 1,
        "accepted_evidence_rollup_claimable_metrics": 5,
        "accepted_evidence_rollup_accepted_issues": 0,
        "accepted_evidence_rollup_blocked_claims": 5,
        "business_impact_ledger": 1,
        "business_impact_ledger_accepted_signals": 0,
        "reviewer_evidence_kit": 1,
        "reviewer_evidence_forms": 5,
        "reviewer_evidence_script_steps": 5,
        "resume_traction_proof": 1,
        "resume_traction_claimable_now": 6,
        "resume_traction_future_claims": 4,
        "resume_traction_blocked_claims": 5,
        "reviewer_action_queue": 1,
        "reviewer_action_tasks": 8,
        "reviewer_action_not_contacted": 8,
        "reviewer_action_evidence_goals": 5,
        "reviewer_outreach_execution_pack": 1,
        "reviewer_outreach_ready_messages": 8,
        "reviewer_outreach_follow_up_rules": 8,
        "reviewer_outreach_not_sent": 8,
        "reviewer_outreach_evidence_goals": 5,
        "reviewer_outreach_status_board": 1,
        "reviewer_outreach_status_slots": 8,
        "reviewer_outreach_status_stages": 5,
        "reviewer_outreach_status_not_sent": 8,
        "reviewer_outreach_status_accepted_evidence": 0,
        "resume_outcome_metrics": 1,
        "resume_outcome_metrics_tracked": 6,
        "resume_outcome_metrics_claimable": 0,
        "resume_outcome_metrics_blocked": 6,
        "public_metrics_provenance": 1,
        "public_metrics_provenance_tracked": 8,
        "public_metrics_provenance_claimable": 2,
        "public_metrics_provenance_blocked_or_baseline": 5,
        "resume_outcome_action_checklist": 1,
        "resume_outcome_action_count": 5,
        "resume_outcome_next_actions_needed": 5,
        "resume_outcome_action_accepted_public_evidence": 0,
        "reviewer_submission_hub": 1,
        "reviewer_submission_paths": 6,
        "reviewer_submission_target_metrics": 6,
        "reviewer_submission_required_fields": 24,
        "first_10_reviewer_sprint": 1,
        "first_10_reviewer_slots": 10,
        "first_10_reviewer_issue_launch_drafts": 10,
        "first_10_reviewer_public_issue_entrypoints": 10,
        "first_10_reviewer_target_metrics": 6,
        "first_10_reviewer_not_sent": 10,
        "first_10_reviewer_completed": 0,
        "first_10_outreach_execution_log": 1,
        "first_10_outreach_messages": 10,
        "first_10_outreach_public_issue_entrypoints": 10,
        "first_10_outreach_not_sent": 10,
        "first_10_outreach_accepted_evidence": 0,
        "outcome_collection_page": 1,
        "outcome_collection_actions": 5,
        "outcome_collection_submission_paths": 6,
        "outcome_collection_evidence_fields": 24,
        "public_reviewer_call": 1,
        "public_reviewer_call_segments": 3,
        "public_reviewer_call_submission_paths": 6,
        "public_reviewer_call_outreach_tasks": 8,
        "public_reviewer_call_evidence_fields": 24,
        "reviewer_share_kit": 1,
        "reviewer_share_channels": 5,
        "reviewer_share_ready_messages": 5,
        "reviewer_share_linked_submission_paths": 6,
        "reviewer_share_required_fields": 24,
        "reviewer_share_not_sent": 5,
        "api_smoke_report": 1,
        "api_smoke_checks": 6,
        "api_smoke_passed_checks": 6,
        "performance_baseline": 1,
        "performance_benchmark_count": 2,
        "performance_measured_endpoint_calls": 24,
        "demo_usage_baseline": 1,
        "demo_usage_tracked_funnel_steps": 5,
        "demo_usage_entrypoints_verified": 6,
        "business_data_intake_baseline": 1,
        "business_data_intake_endpoints": 4,
        "business_data_intake_tests": 6,
        "business_data_intake_max_rows": 10_000,
        "business_data_intake_max_columns": 80,
        "community_growth_baseline": 1,
        "community_issue_templates": 8,
        "community_labels": 10,
        "community_public_growth_channels": 9,
        "impact_review_packet": 1,
        "impact_review_business_metrics": 12,
        "impact_review_evidence_links": 8,
        "business_problem_casebook": 1,
        "business_problem_cases": 1,
        "business_problem_detected_risks": 4,
        "business_problem_owner_handoffs": 4,
        "business_resolution_brief": 1,
        "business_resolution_findings": 5,
        "business_resolution_risk_areas": 4,
        "business_resolution_high_priority_actions": 3,
        "business_resolution_owner_handoffs": 4,
        "business_resolution_review_request": 1,
        "business_resolution_review_questions": 5,
        "business_resolution_review_external_feedback": 0,
        "public_traction_dashboard": 1,
        "public_traction_surfaces": 4,
        "public_traction_growth_channels": 19,
        "public_traction_resume_upgrade_rules": 3,
        "github_traffic_snapshot": 1,
        "public_availability_snapshot": 1,
        "public_availability_endpoint_count": 4,
        "live_project_scorecard": 1,
        "scorecard_reviewer_paths": 23,
        "openapi_required_endpoints": 6,
        "recruiter_pitch_resume_bullets": 3,
        "recruiter_pitch_target_roles": 4,
        "application_evidence_pack": 1,
        "application_evidence_links": 50,
        "github_discovery_profile": 1,
        "github_discovery_topics": 20,
        "github_discovery_reviewer_entrypoints": 6,
        "pilot_evidence_quicklink": 1,
        "pilot_evidence_quicklink_actions": 4,
        "pilot_evidence_quicklink_fields": 17,
        "pilot_evidence_quicklink_target_metrics": 4,
        "pilot_launch_control_room": 1,
        "pilot_launch_public_issue_threads": 4,
        "pilot_launch_gates": 5,
        "pilot_launch_target_outcomes": 4,
        "pilot_launch_reviewer_send_paths": 3,
        "resume_outcome_adjudication": 1,
        "resume_outcome_adjudication_categories": 5,
        "resume_outcome_adjudication_blocked_categories": 5,
        "resume_outcome_adjudication_claimable_categories": 0,
        "resume_outcome_scoreboard": 1,
        "resume_outcome_scoreboard_claimable_now": 6,
        "resume_outcome_scoreboard_blocked": 6,
        "resume_outcome_scoreboard_remaining_evidence": 7,
        "evidence_acceptance_checklist": 1,
        "evidence_acceptance_items": 6,
        "evidence_acceptance_accepted_issues": 0,
        "evidence_acceptance_rejected_issues": 14,
        "ai_engineer_review_intake": 1,
        "ai_engineer_review_paths": 6,
        "ai_engineer_review_questions": 6,
        "ai_engineer_review_countable_conditions": 6,
        "pilot_outreach_messages": 3,
        "pilot_review_paths": 10,
        "pilot_program_segments": 3,
        "pilot_program_weeks": 3,
        "pilot_review_tracker": 1,
        "pilot_review_tracker_planned_reviews": 3,
        "pilot_review_tracker_not_contacted": 3,
        "pilot_review_tracker_resume_rules": 3,
        "pilot_conversion_board": 1,
        "pilot_conversion_stages": 6,
        "pilot_conversion_claimable_stages": 2,
        "pilot_conversion_blocked_stages": 4,
        "resume_outcome_readiness": 1,
        "resume_outcome_readiness_stages": 6,
        "resume_outcome_claimable_stages": 2,
        "resume_outcome_blocked_stages": 4,
        "resume_outcome_missing_evidence_items": 4,
        "external_review_evidence_ledger": 1,
        "external_review_ledger_entries": 0,
        "external_review_ledger_requirement_types": 5,
        "external_review_ledger_linked_reviews": 3,
        "outcome_upgrade_playbook": 1,
        "outcome_upgrade_rules": 5,
        "outcome_upgrade_blocked_rules": 5,
        "outcome_upgrade_claimable_now": 6,
        "resume_claim_upgrade_ledger": 1,
        "resume_claim_upgrade_rows": 6,
        "resume_claim_upgrade_blocked_rows": 6,
        "resume_claim_upgrade_claimable_rows": 0,
        "reviewer_feedback_packet": 1,
        "reviewer_feedback_tasks": 4,
        "reviewer_feedback_questions": 6,
        "reviewer_feedback_conversion_paths": 5,
        "reviewer_funnel_board": 1,
        "reviewer_funnel_stages": 4,
        "reviewer_funnel_open_gaps": 4,
        "reviewer_funnel_remaining_evidence_items": 7,
        "feedback_intake_quality": 1,
        "feedback_intake_required_sections": 7,
        "feedback_intake_try_paths": 4,
        "feedback_intake_outcomes": 4,
        "feedback_intake_captured_fields": 7,
        "star_growth_kit": 1,
        "star_growth_required_topics": 20,
        "star_growth_ethical_actions": 4,
        "star_growth_resume_upgrade_rules": 4,
        "business_case_intake": 1,
        "business_case_intake_required_sections": 8,
        "business_case_intake_try_paths": 5,
        "business_case_intake_outcomes": 8,
        "business_case_intake_captured_fields": 8,
        "business_case_intake_outcome_fields": 9,
        "business_data_replay_packet": 1,
        "business_data_replay_paths": 3,
        "business_data_replay_evidence_fields": 8,
        "business_data_replay_safety_requirements": 5,
        "business_replay_demo": 1,
        "business_replay_demo_rows": 8,
        "business_replay_demo_findings": 5,
        "business_replay_demo_check_types": 4,
        "business_replay_demo_rule_references": 4,
        "business_replay_demo_root_causes": 3,
        "real_model_runbook": 1,
        "real_model_current_runs": 0,
            "real_model_run_commands": 6,
        "real_model_evidence_fields": 15,
        "real_model_acceptance_criteria": 8,
        "real_model_safety_gates": 5,
        "real_model_evidence_capture": 1,
        "real_model_capture_required_fields": 17,
        "real_model_capture_accepted_runs": 0,
        "real_model_capture_blocked_claims": 4,
        "real_model_preflight": 1,
        "real_model_preflight_total_checks": 5,
        "real_model_preflight_ready_checks": 3,
        "real_model_preflight_blocked_checks": 2,
        "ai_engineer_readiness": 1,
        "ai_engineer_readiness_implemented_signals": 8,
        "ai_engineer_readiness_partial_signals": 1,
        "ai_engineer_readiness_not_claimed_signals": 1,
        "agent_maturity_audit": 1,
        "agent_maturity_audit_rows": 20,
        "agent_maturity_implemented_areas": 15,
        "agent_maturity_partial_areas": 4,
        "agent_maturity_not_claimed_areas": 1,
        "recommended_actions": 5,
        "implemented_agent_capabilities": 16,
    }
    for key, expected in expected_outcomes.items():
        if outcomes.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {outcomes.get(key)!r}")
    if outcomes.get("external_reviewer_gate_collected_issues", -1) < 0:
        raise AssertionError("external reviewer gate collected issue count must be non-negative")
    for required in ("external users", "customer feedback", "enterprise production usage"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"public metrics summary must not claim {required}")
    return {"public_metrics_summary_verified": True, **expected_metrics, **expected_outcomes}


def main() -> None:
    payload = build_public_metrics_summary()
    verify_public_metrics_summary(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
