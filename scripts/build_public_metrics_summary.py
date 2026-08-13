import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTCOME_SUMMARY_PATH = ROOT / "docs" / "outcome-summary.json"
AGENT_READINESS_PATH = ROOT / "docs" / "agent-readiness.json"
EVAL_SUMMARY_PATH = ROOT / "docs" / "eval-summary.json"
HYPOTHESIS_FEEDBACK_PATH = ROOT / "docs" / "hypothesis-feedback.json"
INCIDENT_PATTERN_MEMORY_PATH = ROOT / "docs" / "incident-pattern-memory.json"
AGENT_OBSERVABILITY_PATH = ROOT / "docs" / "agent-observability.json"
AGENT_SAFETY_PATH = ROOT / "docs" / "agent-safety-boundaries.json"
AGENT_CAPABILITY_MATRIX_PATH = ROOT / "docs" / "agent-capability-matrix.json"
LOCAL_REVIEWER_DEMO_PATH = ROOT / "docs" / "local-reviewer-demo.json"
API_SMOKE_REPORT_PATH = ROOT / "docs" / "api-smoke-report.json"
PERFORMANCE_BASELINE_PATH = ROOT / "docs" / "performance-baseline.json"
DEMO_USAGE_BASELINE_PATH = ROOT / "docs" / "demo-usage-baseline.json"
BUSINESS_DATA_INTAKE_BASELINE_PATH = ROOT / "docs" / "business-data-intake-baseline.json"
COMMUNITY_GROWTH_BASELINE_PATH = ROOT / "docs" / "community-growth-baseline.json"
IMPACT_REVIEW_PACKET_PATH = ROOT / "docs" / "impact-review-packet.json"
BUSINESS_PROBLEM_CASEBOOK_PATH = ROOT / "docs" / "business-problem-casebook.json"
PUBLIC_TRACTION_DASHBOARD_PATH = ROOT / "docs" / "public-traction-dashboard.json"
LIVE_PROJECT_SCORECARD_PATH = ROOT / "docs" / "live-project-scorecard.json"
OPENAPI_PATH = ROOT / "docs" / "openapi.json"
RECRUITER_PITCH_PATH = ROOT / "docs" / "recruiter-pitch.json"
APPLICATION_EVIDENCE_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
PILOT_OUTREACH_KIT_PATH = ROOT / "docs" / "pilot-outreach-kit.json"
PILOT_PROGRAM_PLAN_PATH = ROOT / "docs" / "pilot-program-plan.json"
PILOT_REVIEW_TRACKER_PATH = ROOT / "docs" / "pilot-review-tracker.json"
EXTERNAL_REVIEW_EVIDENCE_LEDGER_PATH = ROOT / "docs" / "external-review-evidence-ledger.json"
OUTCOME_UPGRADE_PLAYBOOK_PATH = ROOT / "docs" / "outcome-upgrade-playbook.json"
REVIEWER_FEEDBACK_PACKET_PATH = ROOT / "docs" / "reviewer-feedback-packet.json"
FEEDBACK_INTAKE_QUALITY_PATH = ROOT / "docs" / "feedback-intake-quality.json"
STAR_GROWTH_KIT_PATH = ROOT / "docs" / "star-growth-kit.json"
BUSINESS_CASE_INTAKE_PATH = ROOT / "docs" / "business-case-intake.json"
BUSINESS_DATA_REPLAY_PACKET_PATH = ROOT / "docs" / "business-data-replay-packet.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "public-metrics-summary.json"
OUTPUT_MD_PATH = ROOT / "docs" / "public-metrics-summary.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_public_metrics_summary() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    outcome = load_json(OUTCOME_SUMMARY_PATH)
    readiness = load_json(AGENT_READINESS_PATH)
    eval_summary = load_json(EVAL_SUMMARY_PATH)
    hypothesis_feedback = load_json(HYPOTHESIS_FEEDBACK_PATH)
    incident_memory = load_json(INCIDENT_PATTERN_MEMORY_PATH)
    observability = load_json(AGENT_OBSERVABILITY_PATH)
    safety = load_json(AGENT_SAFETY_PATH)
    capability_matrix = load_json(AGENT_CAPABILITY_MATRIX_PATH)
    local_demo = load_json(LOCAL_REVIEWER_DEMO_PATH)
    api_smoke = load_json(API_SMOKE_REPORT_PATH)
    performance = load_json(PERFORMANCE_BASELINE_PATH)
    demo_usage = load_json(DEMO_USAGE_BASELINE_PATH)
    business_data_intake = load_json(BUSINESS_DATA_INTAKE_BASELINE_PATH)
    community_growth = load_json(COMMUNITY_GROWTH_BASELINE_PATH)
    impact_review = load_json(IMPACT_REVIEW_PACKET_PATH)
    business_casebook = load_json(BUSINESS_PROBLEM_CASEBOOK_PATH)
    traction = load_json(PUBLIC_TRACTION_DASHBOARD_PATH)
    scorecard = load_json(LIVE_PROJECT_SCORECARD_PATH)
    openapi = load_json(OPENAPI_PATH)
    recruiter_pitch = load_json(RECRUITER_PITCH_PATH)
    application_pack = load_json(APPLICATION_EVIDENCE_PACK_PATH)
    pilot_outreach = load_json(PILOT_OUTREACH_KIT_PATH)
    pilot_plan = load_json(PILOT_PROGRAM_PLAN_PATH)
    pilot_tracker = load_json(PILOT_REVIEW_TRACKER_PATH)
    external_ledger = load_json(EXTERNAL_REVIEW_EVIDENCE_LEDGER_PATH)
    outcome_upgrade = load_json(OUTCOME_UPGRADE_PLAYBOOK_PATH)
    reviewer_packet = load_json(REVIEWER_FEEDBACK_PACKET_PATH)
    feedback_intake = load_json(FEEDBACK_INTAKE_QUALITY_PATH)
    star_growth = load_json(STAR_GROWTH_KIT_PATH)
    business_case_intake = load_json(BUSINESS_CASE_INTAKE_PATH)
    replay_packet = load_json(BUSINESS_DATA_REPLAY_PACKET_PATH)
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
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
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
            "local_reviewer_demo": 1,
            "local_reviewer_seeded_rows": local_demo["seeded_business_table"]["row_count"],
            "local_reviewer_routes": len(local_demo["reviewer_routes"]),
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
            "public_traction_dashboard": 1,
            "public_traction_surfaces": traction["traction_surface_count"],
            "public_traction_growth_channels": traction["growth_channel_count"],
            "public_traction_resume_upgrade_rules": len(traction["resume_upgrade_rules"]),
            "live_project_scorecard": 1,
            "scorecard_reviewer_paths": len(scorecard["reviewer_paths"]),
            "openapi_required_endpoints": 6,
            "openapi_paths": len(openapi["paths"]),
            "recruiter_pitch_resume_bullets": len(recruiter_pitch["resume_bullets"]),
            "recruiter_pitch_target_roles": len(recruiter_pitch["target_roles"]),
            "application_evidence_pack": 1,
            "application_evidence_links": len(application_pack["application_links"]),
            "pilot_outreach_messages": len(pilot_outreach["outreach_messages"]),
            "pilot_review_paths": len(pilot_outreach["review_paths"]),
            "pilot_program_segments": len(pilot_plan["participant_segments"]),
            "pilot_program_weeks": len(pilot_plan["weekly_plan"]),
            "pilot_review_tracker": 1,
            "pilot_review_tracker_planned_reviews": pilot_tracker["planned_review_count"],
            "pilot_review_tracker_not_contacted": pilot_tracker["status_counts"]["not_contacted"],
            "pilot_review_tracker_resume_rules": len(pilot_tracker["resume_upgrade_rules"]),
            "external_review_evidence_ledger": 1,
            "external_review_ledger_entries": external_ledger["entry_count"],
            "external_review_ledger_requirement_types": external_ledger["evidence_requirement_count"],
            "external_review_ledger_linked_reviews": external_ledger["linked_planned_reviews"],
            "outcome_upgrade_playbook": 1,
            "outcome_upgrade_rules": outcome_upgrade["upgrade_rule_count"],
            "outcome_upgrade_blocked_rules": outcome_upgrade["blocked_upgrade_rule_count"],
            "outcome_upgrade_claimable_now": len(outcome_upgrade["claimable_now"]),
            "reviewer_feedback_packet": 1,
            "reviewer_feedback_tasks": reviewer_packet["reviewer_task_count"],
            "reviewer_feedback_questions": reviewer_packet["evidence_question_count"],
            "reviewer_feedback_conversion_paths": reviewer_packet["conversion_path_count"],
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
            "business_data_replay_packet": 1,
            "business_data_replay_paths": replay_packet["replay_path_count"],
            "business_data_replay_evidence_fields": replay_packet["evidence_field_count"],
            "business_data_replay_safety_requirements": replay_packet["safety_requirement_count"],
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
                f"Reviewer feedback packet with {reviewer_packet['reviewer_task_count']} task paths, "
                f"{reviewer_packet['evidence_question_count']} evidence questions, and "
                f"{reviewer_packet['conversion_path_count']} metric conversion paths"
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
                f"Public traction dashboard with {traction['traction_surface_count']} live project surfaces, "
                f"{traction['growth_channel_count']} growth or review channels, "
                f"{traction['tracked_funnel_steps']} tracked funnel steps, and "
                f"{len(traction['resume_upgrade_rules'])} resume upgrade rules"
            ),
            f"{len(scorecard['reviewer_paths'])} reviewer paths in a CI-verified live project scorecard",
            "CI-verified OpenAPI contract covering 6 integration endpoints",
            f"{len(recruiter_pitch['resume_bullets'])} recruiter-safe resume bullets for {len(recruiter_pitch['target_roles'])} target roles",
            f"{len(application_pack['application_links'])} application evidence links in a recruiter-ready evidence pack",
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
                f"{len(star_growth['resume_upgrade_rules'])} resume upgrade rules without inflating current stars"
            ),
            (
                f"Business-case intake path with {business_case_intake['required_section_count']} required sections, "
                f"{business_case_intake['required_try_path_count']} tried paths, "
                f"{business_case_intake['required_outcome_count']} outcome signals, and "
                f"{business_case_intake['captured_field_count']} captured evidence groups"
            ),
            (
                f"Business-data replay packet with {replay_packet['replay_path_count']} safe replay paths, "
                f"{replay_packet['evidence_field_count']} evidence fields, "
                f"{replay_packet['safety_requirement_count']} safety requirements, and zero current external replay claims"
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
| External feedback items | {metrics["external_feedback_items"]} |
| Confirmed external users | {metrics["confirmed_external_users"]} |
| Reproducible feedback items | {metrics["reproducible_feedback_items"]} |

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
| Public traction dashboard | {outcomes["public_traction_dashboard"]} |
| Public traction surfaces | {outcomes["public_traction_surfaces"]} |
| Public traction growth channels | {outcomes["public_traction_growth_channels"]} |
| Public traction resume upgrade rules | {outcomes["public_traction_resume_upgrade_rules"]} |
| Live project scorecard | {outcomes["live_project_scorecard"]} |
| Scorecard reviewer paths | {outcomes["scorecard_reviewer_paths"]} |
| OpenAPI required integration endpoints | {outcomes["openapi_required_endpoints"]} |
| OpenAPI paths | {outcomes["openapi_paths"]} |
| Recruiter-safe resume bullets | {outcomes["recruiter_pitch_resume_bullets"]} |
| Recruiter pitch target roles | {outcomes["recruiter_pitch_target_roles"]} |
| Application evidence pack | {outcomes["application_evidence_pack"]} |
| Application evidence links | {outcomes["application_evidence_links"]} |
| Pilot outreach messages | {outcomes["pilot_outreach_messages"]} |
| Pilot review paths | {outcomes["pilot_review_paths"]} |
| Pilot program segments | {outcomes["pilot_program_segments"]} |
| Pilot program weeks | {outcomes["pilot_program_weeks"]} |
| Pilot review tracker | {outcomes["pilot_review_tracker"]} |
| Pilot review tracker planned reviews | {outcomes["pilot_review_tracker_planned_reviews"]} |
| Pilot review tracker not-contacted entries | {outcomes["pilot_review_tracker_not_contacted"]} |
| Pilot review tracker resume rules | {outcomes["pilot_review_tracker_resume_rules"]} |
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
| Business-data replay packet | {outcomes["business_data_replay_packet"]} |
| Business-data replay paths | {outcomes["business_data_replay_paths"]} |
| Business-data replay evidence fields | {outcomes["business_data_replay_evidence_fields"]} |
| Business-data replay safety requirements | {outcomes["business_data_replay_safety_requirements"]} |
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
        "test_count": 95,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
    }
    for key, expected in expected_metrics.items():
        if metrics.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {metrics.get(key)!r}")
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
        "tool_allowlist_count": 7,
        "postgres_rejected_write_query_count": 3,
        "verifier_rule_count": 6,
        "agent_capability_matrix": 1,
        "agent_matrix_implemented_capabilities": 13,
        "agent_matrix_partial_capabilities": 4,
        "agent_matrix_not_claimed_count": 1,
        "local_reviewer_demo": 1,
        "local_reviewer_seeded_rows": 8,
        "local_reviewer_routes": 3,
        "api_smoke_report": 1,
        "api_smoke_checks": 6,
        "api_smoke_passed_checks": 6,
        "performance_baseline": 1,
        "performance_benchmark_count": 2,
        "performance_measured_endpoint_calls": 24,
        "demo_usage_baseline": 1,
        "demo_usage_tracked_funnel_steps": 5,
        "demo_usage_entrypoints_verified": 5,
        "business_data_intake_baseline": 1,
        "business_data_intake_endpoints": 4,
        "business_data_intake_tests": 6,
        "business_data_intake_max_rows": 10_000,
        "business_data_intake_max_columns": 80,
        "community_growth_baseline": 1,
        "community_issue_templates": 5,
        "community_labels": 6,
        "community_public_growth_channels": 6,
        "impact_review_packet": 1,
        "impact_review_business_metrics": 12,
        "impact_review_evidence_links": 8,
        "business_problem_casebook": 1,
        "business_problem_cases": 1,
        "business_problem_detected_risks": 4,
        "business_problem_owner_handoffs": 4,
        "public_traction_dashboard": 1,
        "public_traction_surfaces": 4,
        "public_traction_growth_channels": 15,
        "public_traction_resume_upgrade_rules": 3,
        "live_project_scorecard": 1,
        "scorecard_reviewer_paths": 12,
        "openapi_required_endpoints": 6,
        "recruiter_pitch_resume_bullets": 3,
        "recruiter_pitch_target_roles": 4,
        "application_evidence_pack": 1,
        "application_evidence_links": 14,
        "pilot_outreach_messages": 3,
        "pilot_review_paths": 9,
        "pilot_program_segments": 3,
        "pilot_program_weeks": 3,
        "pilot_review_tracker": 1,
        "pilot_review_tracker_planned_reviews": 3,
        "pilot_review_tracker_not_contacted": 3,
        "pilot_review_tracker_resume_rules": 3,
        "external_review_evidence_ledger": 1,
        "external_review_ledger_entries": 0,
        "external_review_ledger_requirement_types": 4,
        "external_review_ledger_linked_reviews": 3,
        "outcome_upgrade_playbook": 1,
        "outcome_upgrade_rules": 5,
        "outcome_upgrade_blocked_rules": 5,
        "outcome_upgrade_claimable_now": 6,
        "reviewer_feedback_packet": 1,
        "reviewer_feedback_tasks": 3,
        "reviewer_feedback_questions": 5,
        "reviewer_feedback_conversion_paths": 4,
        "feedback_intake_quality": 1,
        "feedback_intake_required_sections": 5,
        "feedback_intake_try_paths": 5,
        "feedback_intake_outcomes": 4,
        "feedback_intake_captured_fields": 5,
        "star_growth_kit": 1,
        "star_growth_required_topics": 6,
        "star_growth_ethical_actions": 4,
        "star_growth_resume_upgrade_rules": 3,
        "business_case_intake": 1,
        "business_case_intake_required_sections": 6,
        "business_case_intake_try_paths": 5,
        "business_case_intake_outcomes": 5,
        "business_case_intake_captured_fields": 6,
        "business_data_replay_packet": 1,
        "business_data_replay_paths": 3,
        "business_data_replay_evidence_fields": 8,
        "business_data_replay_safety_requirements": 5,
        "recommended_actions": 5,
        "implemented_agent_capabilities": 16,
    }
    for key, expected in expected_outcomes.items():
        if outcomes.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {outcomes.get(key)!r}")
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
