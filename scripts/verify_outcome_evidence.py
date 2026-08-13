import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "docs" / "outcome-evidence.json"
METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
HISTORY_PATH = ROOT / "docs" / "adoption-history.jsonl"
BUSINESS_IMPACT_PATH = ROOT / "docs" / "business-impact.json"
OUTCOME_SUMMARY_PATH = ROOT / "docs" / "outcome-summary.json"
SUPPORT_TICKET_ARTIFACT_PATH = ROOT / "docs" / "verified-support-ticket-result.json"
PUBLIC_METRICS_SUMMARY_PATH = ROOT / "docs" / "public-metrics-summary.json"
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
LIVE_SCORECARD_PATH = ROOT / "docs" / "live-project-scorecard.json"
OPENAPI_PATH = ROOT / "docs" / "openapi.json"
RECRUITER_PITCH_PATH = ROOT / "docs" / "recruiter-pitch.json"
APPLICATION_EVIDENCE_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
PILOT_OUTREACH_KIT_PATH = ROOT / "docs" / "pilot-outreach-kit.json"
PILOT_PROGRAM_PLAN_PATH = ROOT / "docs" / "pilot-program-plan.json"
PILOT_REVIEW_TRACKER_PATH = ROOT / "docs" / "pilot-review-tracker.json"
FEEDBACK_INTAKE_QUALITY_PATH = ROOT / "docs" / "feedback-intake-quality.json"
STAR_GROWTH_KIT_PATH = ROOT / "docs" / "star-growth-kit.json"
BUSINESS_CASE_INTAKE_PATH = ROOT / "docs" / "business-case-intake.json"
PUBLIC_HEALTH_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "public-evidence-health.yml"
PUBLIC_HEALTH_SCRIPT_PATH = ROOT / "scripts" / "verify_public_evidence_health.py"
RESUME_EVIDENCE_PATH = ROOT / "docs" / "resume-evidence.md"
FEEDBACK_LOG_PATH = ROOT / "docs" / "feedback-log.md"
REQUIRED_CLAIM_FIELDS = {"id", "resume_signal", "claim", "evidence_type", "url", "status"}
FORBIDDEN_UNVERIFIED_TERMS = {"users", "customers", "enterprise production", "github stars gained"}


def load_payload(path: Path) -> dict:
    return json.loads(path.read_text())


def validate_url(value: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise AssertionError(f"invalid evidence url: {value}")


def verify_manifest() -> dict[str, int]:
    evidence = load_payload(EVIDENCE_PATH)
    metrics = load_payload(METRICS_PATH)
    feedback_metrics = load_payload(FEEDBACK_METRICS_PATH)
    business_impact = load_payload(BUSINESS_IMPACT_PATH)
    outcome_summary = load_payload(OUTCOME_SUMMARY_PATH)
    support_ticket_artifact = load_payload(SUPPORT_TICKET_ARTIFACT_PATH)
    public_metrics_summary = load_payload(PUBLIC_METRICS_SUMMARY_PATH)
    agent_readiness = load_payload(AGENT_READINESS_PATH)
    eval_summary = load_payload(EVAL_SUMMARY_PATH)
    hypothesis_feedback = load_payload(HYPOTHESIS_FEEDBACK_PATH)
    incident_memory = load_payload(INCIDENT_PATTERN_MEMORY_PATH)
    observability = load_payload(AGENT_OBSERVABILITY_PATH)
    safety = load_payload(AGENT_SAFETY_PATH)
    capability_matrix = load_payload(AGENT_CAPABILITY_MATRIX_PATH)
    local_reviewer_demo = load_payload(LOCAL_REVIEWER_DEMO_PATH)
    api_smoke_report = load_payload(API_SMOKE_REPORT_PATH)
    performance_baseline = load_payload(PERFORMANCE_BASELINE_PATH)
    demo_usage_baseline = load_payload(DEMO_USAGE_BASELINE_PATH)
    business_data_intake = load_payload(BUSINESS_DATA_INTAKE_BASELINE_PATH)
    community_growth = load_payload(COMMUNITY_GROWTH_BASELINE_PATH)
    impact_review = load_payload(IMPACT_REVIEW_PACKET_PATH)
    business_casebook = load_payload(BUSINESS_PROBLEM_CASEBOOK_PATH)
    traction = load_payload(PUBLIC_TRACTION_DASHBOARD_PATH)
    scorecard = load_payload(LIVE_SCORECARD_PATH)
    openapi = load_payload(OPENAPI_PATH)
    recruiter_pitch = load_payload(RECRUITER_PITCH_PATH)
    application_pack = load_payload(APPLICATION_EVIDENCE_PACK_PATH)
    pilot_outreach = load_payload(PILOT_OUTREACH_KIT_PATH)
    pilot_plan = load_payload(PILOT_PROGRAM_PLAN_PATH)
    pilot_tracker = load_payload(PILOT_REVIEW_TRACKER_PATH)
    feedback_intake = load_payload(FEEDBACK_INTAKE_QUALITY_PATH)
    star_growth = load_payload(STAR_GROWTH_KIT_PATH)
    business_case_intake = load_payload(BUSINESS_CASE_INTAKE_PATH)
    history = [json.loads(line) for line in HISTORY_PATH.read_text().splitlines() if line.strip()]
    resume_page = RESUME_EVIDENCE_PATH.read_text().lower()
    feedback_log = FEEDBACK_LOG_PATH.read_text().lower()
    claims = evidence.get("claims", [])
    if len(claims) < 6:
        raise AssertionError("outcome evidence manifest must include at least six public claims")

    claim_ids = set()
    for claim in claims:
        missing = REQUIRED_CLAIM_FIELDS - set(claim)
        if missing:
            raise AssertionError(f"claim {claim.get('id')} missing fields: {sorted(missing)}")
        if claim["id"] in claim_ids:
            raise AssertionError(f"duplicate claim id: {claim['id']}")
        claim_ids.add(claim["id"])
        if claim["status"] != "verified":
            raise AssertionError(f"claim {claim['id']} must not be marked as a resume signal until verified")
        validate_url(claim["url"])

        text = f"{claim['resume_signal']} {claim['claim']}".lower()
        for forbidden in FORBIDDEN_UNVERIFIED_TERMS:
            if forbidden in text and claim["id"] != "adoption-baseline":
                raise AssertionError(f"claim {claim['id']} uses unverified outcome language: {forbidden}")

        metric_name = claim.get("metric_name")
        if metric_name:
            if metric_name == "external_feedback_items":
                if feedback_metrics.get("external_feedback_items") != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: external_feedback_items={claim.get('metric_value')} "
                        f"but feedback metrics has {feedback_metrics.get('external_feedback_items')}"
                    )
            elif metric_name == "support_ticket_issue_categories":
                if business_impact.get("issue_category_count") != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: {metric_name}={claim.get('metric_value')} "
                        f"but business impact has {business_impact.get('issue_category_count')}"
                    )
            elif metric_name == "implemented_agent_capabilities":
                if len(agent_readiness.get("implemented", [])) != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: implemented_agent_capabilities="
                        f"{claim.get('metric_value')} but agent readiness has "
                        f"{len(agent_readiness.get('implemented', []))}"
                    )
            elif metric_name == "recommended_action_count":
                actions = outcome_summary.get("verified_outcomes", {}).get("recommended_action_count")
                if actions != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: recommended_action_count={claim.get('metric_value')} "
                        f"but outcome summary has {actions}"
                    )
            elif metric_name == "business_remediation_scorecard":
                remediation_scorecard = business_impact.get("remediation_scorecard", {})
                outcomes = outcome_summary.get("verified_outcomes", {})
                if business_impact.get("business_risk_area_count") != 4:
                    raise AssertionError("business remediation scorecard must verify 4 business risk areas")
                if business_impact.get("high_priority_action_count") != 3:
                    raise AssertionError("business remediation scorecard must verify 3 high-priority actions")
                if business_impact.get("owner_handoff_count") != 4:
                    raise AssertionError("business remediation scorecard must verify 4 owner handoffs")
                if outcomes.get("business_risk_area_count") != 4:
                    raise AssertionError("outcome summary must include business risk area count")
                if "owner handoffs" not in remediation_scorecard.get("resume_safe_outcome", ""):
                    raise AssertionError("business remediation scorecard must include owner-handoff evidence")
                if claim.get("metric_value") != 1:
                    raise AssertionError("business_remediation_scorecard claim must use metric_value=1")
            elif metric_name == "local_reviewer_demo":
                local_demo_script = (ROOT / "scripts" / "build_local_reviewer_demo.py").read_text()
                local_demo_tests = (ROOT / "tests" / "test_local_reviewer_demo.py").read_text()
                if local_reviewer_demo.get("seeded_business_table", {}).get("row_count") != 8:
                    raise AssertionError("local reviewer demo must verify 8 seeded rows")
                if len(local_reviewer_demo.get("reviewer_routes", [])) != 3:
                    raise AssertionError("local reviewer demo must verify 3 review routes")
                if local_reviewer_demo.get("read_only_database", {}).get("readonly_user") != "readonly_agent":
                    raise AssertionError("local reviewer demo must verify read-only database user")
                if local_reviewer_demo.get("reviewer_command") != "docker compose up --build":
                    raise AssertionError("local reviewer demo must document the compose command")
                if "external reviewer completion" not in " ".join(local_reviewer_demo.get("not_claimed", [])).lower():
                    raise AssertionError("local reviewer demo must not claim external reviewer completion")
                if "verify_local_reviewer_demo" not in local_demo_script:
                    raise AssertionError("local reviewer demo must include a script verifier")
                if "test_local_reviewer_demo_documents_seeded_compose_path_without_usage_claims" not in local_demo_tests:
                    raise AssertionError("local reviewer demo must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("local_reviewer_demo claim must use metric_value=1")
            elif metric_name == "api_smoke_report":
                smoke_script = (ROOT / "scripts" / "build_api_smoke_report.py").read_text()
                smoke_tests = (ROOT / "tests" / "test_api_smoke_report.py").read_text()
                if api_smoke_report.get("check_count") != 6:
                    raise AssertionError("API smoke report must verify 6 route checks")
                if api_smoke_report.get("passed_count") != 6 or api_smoke_report.get("status") != "PASS":
                    raise AssertionError("API smoke report must pass every route")
                paths = {check.get("path") for check in api_smoke_report.get("checks", [])}
                for required in {"/health", "/datasets/orders_daily/quality-report", "/datasets/orders_daily/agent-report"}:
                    if required not in paths:
                        raise AssertionError(f"API smoke report missing {required}")
                if "production uptime sla" not in " ".join(api_smoke_report.get("not_claimed", [])).lower():
                    raise AssertionError("API smoke report must not claim production uptime SLA")
                if "verify_api_smoke_report" not in smoke_script:
                    raise AssertionError("API smoke report must include a script verifier")
                if "test_api_smoke_report_verifies_core_routes_without_production_claims" not in smoke_tests:
                    raise AssertionError("API smoke report must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("api_smoke_report claim must use metric_value=1")
            elif metric_name == "performance_baseline":
                perf_script = (ROOT / "scripts" / "build_performance_baseline.py").read_text()
                perf_tests = (ROOT / "tests" / "test_performance_baseline.py").read_text()
                if performance_baseline.get("benchmark_count") != 2:
                    raise AssertionError("performance baseline must verify 2 route benchmarks")
                if performance_baseline.get("passed_count") != 2 or performance_baseline.get("status") != "PASS":
                    raise AssertionError("performance baseline must pass every benchmark")
                measured_calls = sum(check.get("iterations", 0) for check in performance_baseline.get("checks", []))
                if measured_calls != 24:
                    raise AssertionError("performance baseline must include 24 measured endpoint calls")
                paths = {check.get("path") for check in performance_baseline.get("checks", [])}
                for required in {"/datasets/orders_daily/quality-report", "/datasets/orders_daily/profile"}:
                    if required not in paths:
                        raise AssertionError(f"performance baseline missing {required}")
                if "production latency sla" not in " ".join(performance_baseline.get("not_claimed", [])).lower():
                    raise AssertionError("performance baseline must not claim production latency SLA")
                if "verify_performance_baseline" not in perf_script:
                    raise AssertionError("performance baseline must include a script verifier")
                if "test_performance_baseline_verifies_local_latency_without_sla_claims" not in perf_tests:
                    raise AssertionError("performance baseline must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("performance_baseline claim must use metric_value=1")
            elif metric_name == "demo_usage_baseline":
                usage_script = (ROOT / "scripts" / "build_demo_usage_baseline.py").read_text()
                usage_tests = (ROOT / "tests" / "test_demo_usage_baseline.py").read_text()
                entrypoints = demo_usage_baseline.get("demo_entrypoints_verified", {})
                if not entrypoints or not all(entrypoints.values()):
                    raise AssertionError("demo usage baseline must verify demo entrypoints")
                if len(demo_usage_baseline.get("tracked_usage_funnel", [])) != 5:
                    raise AssertionError("demo usage baseline must verify 5 tracked funnel steps")
                counts = demo_usage_baseline.get("tracked_counts", {})
                expected_counts = {
                    "stars": 0,
                    "forks": 1,
                    "external_feedback_items": 0,
                    "confirmed_external_users": 0,
                    "reproducible_feedback_items": 0,
                }
                for key, expected in expected_counts.items():
                    if counts.get(key) != expected:
                        raise AssertionError(f"demo usage baseline {key} expected {expected!r}")
                not_claimed = " ".join(demo_usage_baseline.get("not_claimed", [])).lower()
                for required in ("visitor analytics", "external users", "customer feedback", "production adoption"):
                    if required not in not_claimed:
                        raise AssertionError(f"demo usage baseline must not claim {required}")
                if "verify_demo_usage_baseline" not in usage_script:
                    raise AssertionError("demo usage baseline must include a script verifier")
                if "test_demo_usage_baseline_tracks_public_funnel_without_usage_claims" not in usage_tests:
                    raise AssertionError("demo usage baseline must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("demo_usage_baseline claim must use metric_value=1")
            elif metric_name == "business_data_intake_baseline":
                intake_script = (ROOT / "scripts" / "build_business_data_intake_baseline.py").read_text()
                intake_tests = (ROOT / "tests" / "test_business_data_intake_baseline.py").read_text()
                if business_data_intake.get("endpoint_count") != 4:
                    raise AssertionError("business data intake baseline must verify 4 endpoints")
                if business_data_intake.get("test_count") != 6:
                    raise AssertionError("business data intake baseline must verify 6 API tests")
                if not all(business_data_intake.get("endpoint_verification", {}).values()):
                    raise AssertionError("business data intake baseline must verify every endpoint")
                limits = business_data_intake.get("safety_limits", {})
                expected_limits = {
                    "max_upload_bytes": 2_000_000,
                    "max_rows": 10_000,
                    "max_columns": 80,
                    "csv_only": True,
                    "primary_key_required": True,
                    "empty_file_rejected": True,
                }
                for key, expected in expected_limits.items():
                    if limits.get(key) != expected:
                        raise AssertionError(f"business data intake {key} expected {expected!r}")
                not_claimed = " ".join(business_data_intake.get("not_claimed", [])).lower()
                for required in ("production datasets", "uploaded csv rows", "enterprise production usage"):
                    if required not in not_claimed:
                        raise AssertionError(f"business data intake baseline must not claim {required}")
                if "verify_business_data_intake_baseline" not in intake_script:
                    raise AssertionError("business data intake baseline must include a script verifier")
                if (
                    "test_business_data_intake_baseline_verifies_realistic_input_paths_without_usage_claims"
                    not in intake_tests
                ):
                    raise AssertionError("business data intake baseline must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("business_data_intake_baseline claim must use metric_value=1")
            elif metric_name == "community_growth_baseline":
                community_script = (ROOT / "scripts" / "build_community_growth_baseline.py").read_text()
                community_tests = (ROOT / "tests" / "test_community_growth_baseline.py").read_text()
                if community_growth.get("issue_template_count") != 5:
                    raise AssertionError("community growth baseline must verify 5 issue templates")
                if community_growth.get("label_count") != 6:
                    raise AssertionError("community growth baseline must verify 6 labels")
                if len(community_growth.get("public_growth_channels", [])) != 6:
                    raise AssertionError("community growth baseline must verify 6 public growth channels")
                if not all(community_growth.get("contribution_paths", {}).values()):
                    raise AssertionError("community growth baseline must verify contribution paths")
                counts = community_growth.get("current_public_counts", {})
                expected_counts = {
                    "stars": 0,
                    "forks": 1,
                    "issues_total": 11,
                    "external_feedback_items": 0,
                    "confirmed_external_users": 0,
                    "reproducible_feedback_items": 0,
                }
                for key, expected in expected_counts.items():
                    if counts.get(key) != expected:
                        raise AssertionError(f"community growth baseline {key} expected {expected!r}")
                for required in ("external contributors", "community adoption", "external users", "customer feedback"):
                    if required not in community_growth.get("not_claimed", []):
                        raise AssertionError(f"community growth baseline must not claim {required}")
                if "verify_community_growth_baseline" not in community_script:
                    raise AssertionError("community growth baseline must include a script verifier")
                if (
                    "test_community_growth_baseline_verifies_public_contribution_paths_without_adoption_claims"
                    not in community_tests
                ):
                    raise AssertionError("community growth baseline must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("community_growth_baseline claim must use metric_value=1")
            elif metric_name == "impact_review_packet":
                impact_script = (ROOT / "scripts" / "build_impact_review_packet.py").read_text()
                impact_tests = (ROOT / "tests" / "test_impact_review_packet.py").read_text()
                if impact_review.get("business_metric_count") != 12:
                    raise AssertionError("impact review packet must verify 12 business metrics")
                if impact_review.get("evidence_link_count") != 8:
                    raise AssertionError("impact review packet must verify 8 evidence links")
                metrics_payload = impact_review.get("business_metrics", {})
                expected_metrics = {
                    "rows_analyzed": 8,
                    "quality_score": 24,
                    "status": "FAIL",
                    "issue_categories": 4,
                    "findings": 5,
                    "affected_columns": 4,
                    "recommended_actions": 5,
                    "root_cause_hypotheses": 3,
                    "business_rule_references": 4,
                    "business_risk_areas": 4,
                    "high_priority_actions": 3,
                    "owner_handoffs": 4,
                }
                for key, expected in expected_metrics.items():
                    if metrics_payload.get(key) != expected:
                        raise AssertionError(f"impact review packet {key} expected {expected!r}")
                for required in (
                    "external users",
                    "customer feedback",
                    "production deployment",
                    "production financial impact avoided",
                    "company adoption",
                ):
                    if required not in impact_review.get("not_claimed", []):
                        raise AssertionError(f"impact review packet must not claim {required}")
                if "verify_impact_review_packet" not in impact_script:
                    raise AssertionError("impact review packet must include a script verifier")
                if (
                    "test_impact_review_packet_summarizes_business_evidence_without_adoption_claims"
                    not in impact_tests
                ):
                    raise AssertionError("impact review packet must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("impact_review_packet claim must use metric_value=1")
            elif metric_name == "business_problem_casebook":
                casebook_script = (ROOT / "scripts" / "build_business_problem_casebook.py").read_text()
                casebook_tests = (ROOT / "tests" / "test_business_problem_casebook.py").read_text()
                if business_casebook.get("business_case_count") != 1:
                    raise AssertionError("business problem casebook must verify 1 business case")
                if business_casebook.get("detected_risk_count") != 4:
                    raise AssertionError("business problem casebook must verify 4 detected business risks")
                if business_casebook.get("owner_handoff_count") != 4:
                    raise AssertionError("business problem casebook must verify 4 owner handoffs")
                if business_casebook.get("evidence_link_count") != 5:
                    raise AssertionError("business problem casebook must verify 5 evidence links")
                case = business_casebook.get("casebook", [{}])[0]
                outputs = case.get("agent_outputs", {})
                expected_outputs = {
                    "quality_score": 24,
                    "status": "FAIL",
                    "finding_count": 5,
                    "business_rule_reference_count": 4,
                    "root_cause_hypothesis_count": 3,
                    "recommended_action_count": 5,
                    "owner_handoff_count": 4,
                }
                for key, expected in expected_outputs.items():
                    if outputs.get(key) != expected:
                        raise AssertionError(f"business problem casebook {key} expected {expected!r}")
                for required in (
                    "real customer dataset",
                    "external users",
                    "customer feedback",
                    "production deployment",
                    "production financial impact avoided",
                ):
                    if required not in business_casebook.get("not_claimed", []):
                        raise AssertionError(f"business problem casebook must not claim {required}")
                if "verify_business_problem_casebook" not in casebook_script:
                    raise AssertionError("business problem casebook must include a script verifier")
                if (
                    "test_business_problem_casebook_explains_enterprise_problem_without_usage_claims"
                    not in casebook_tests
                ):
                    raise AssertionError("business problem casebook must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("business_problem_casebook claim must use metric_value=1")
            elif metric_name == "public_traction_dashboard":
                traction_script = (ROOT / "scripts" / "build_public_traction_dashboard.py").read_text()
                traction_tests = (ROOT / "tests" / "test_public_traction_dashboard.py").read_text()
                if traction.get("traction_surface_count") != 4:
                    raise AssertionError("public traction dashboard must verify 4 traction surfaces")
                if traction.get("growth_channel_count") != 15:
                    raise AssertionError("public traction dashboard must verify 15 growth or review channels")
                if traction.get("tracked_funnel_steps") != 5:
                    raise AssertionError("public traction dashboard must verify 5 tracked funnel steps")
                if traction.get("demo_entrypoints_verified") != 4:
                    raise AssertionError("public traction dashboard must verify 4 demo entrypoints")
                if len(traction.get("resume_upgrade_rules", [])) != 3:
                    raise AssertionError("public traction dashboard must verify 3 resume upgrade rules")
                if not all(
                    rule.get("resume_status") == "not_claimable_yet"
                    for rule in traction.get("resume_upgrade_rules", [])
                ):
                    raise AssertionError("public traction dashboard must keep zero-traction rules not claimable")
                counts = traction.get("public_counts", {})
                expected_counts = {
                    "stars": 0,
                    "forks": 1,
                        "issues_total": 11,
                    "external_feedback_items": 0,
                    "confirmed_external_users": 0,
                    "reproducible_feedback_items": 0,
                }
                for key, expected in expected_counts.items():
                    if counts.get(key) != expected:
                        raise AssertionError(f"public traction dashboard {key} expected {expected!r}")
                for required in (
                    "external users",
                    "customer feedback",
                    "production adoption",
                    "GitHub star growth beyond the current public count",
                ):
                    if required not in traction.get("not_claimed", []):
                        raise AssertionError(f"public traction dashboard must not claim {required}")
                if "verify_public_traction_dashboard" not in traction_script:
                    raise AssertionError("public traction dashboard must include a script verifier")
                if (
                    "test_public_traction_dashboard_tracks_growth_surfaces_without_inflating_traction"
                    not in traction_tests
                ):
                    raise AssertionError("public traction dashboard must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("public_traction_dashboard claim must use metric_value=1")
            elif metric_name == "public_metrics_summary":
                if public_metrics_summary.get("public_metrics", {}).get("test_count") != 91:
                    raise AssertionError("public metrics summary must include the current CI test count")
                if public_metrics_summary.get("public_metrics", {}).get("external_feedback_items") != 0:
                    raise AssertionError("public metrics summary must preserve the zero-feedback baseline")
                if claim.get("metric_value") != 1:
                    raise AssertionError("public_metrics_summary claim must use metric_value=1")
            elif metric_name == "persistent_trace_audit":
                trace_tests = (ROOT / "tests" / "test_traces.py").read_text()
                trace_source = (ROOT / "app" / "traces.py").read_text()
                if "test_run_trace_store_can_persist_sanitized_trace_across_instances" not in trace_tests:
                    raise AssertionError("persistent trace audit must have a dedicated persistence test")
                if "TRACE_DB_PATH" not in trace_source or "sqlite3" not in trace_source:
                    raise AssertionError("persistent trace audit must use the SQLite-backed TRACE_DB_PATH path")
                if claim.get("metric_value") != 1:
                    raise AssertionError("persistent_trace_audit claim must use metric_value=1")
            elif metric_name == "dataset_memory_retrieval":
                trace_tests = (ROOT / "tests" / "test_traces.py").read_text()
                api_tests = (ROOT / "tests" / "test_api.py").read_text()
                trace_source = (ROOT / "app" / "traces.py").read_text()
                api_source = (ROOT / "app" / "main.py").read_text()
                if "test_run_trace_store_retrieves_dataset_memory_from_persisted_traces" not in trace_tests:
                    raise AssertionError("dataset memory must have a dedicated persisted trace retrieval test")
                if "test_dataset_memory_endpoint_returns_recent_trace_summary_without_raw_rows" not in api_tests:
                    raise AssertionError("dataset memory must have an API test that checks sanitized retrieval")
                if "list_by_dataset" not in trace_source or "DatasetMemorySummary" not in trace_source:
                    raise AssertionError("dataset memory must be backed by RunTraceStore.list_by_dataset")
                if "/datasets/{dataset_id}/memory" not in api_source:
                    raise AssertionError("dataset memory must expose the /datasets/{dataset_id}/memory route")
                if claim.get("metric_value") != 1:
                    raise AssertionError("dataset_memory_retrieval claim must use metric_value=1")
            elif metric_name == "memory_informed_planning":
                agent_tests = (ROOT / "tests" / "test_agent.py").read_text()
                agent_source = (ROOT / "app" / "tool_agent.py").read_text()
                api_source = (ROOT / "app" / "main.py").read_text()
                if "retrieve_dataset_memory" not in agent_source:
                    raise AssertionError("memory-informed planning must expose retrieve_dataset_memory")
                if "used_memory_tool" not in agent_source:
                    raise AssertionError("memory-informed planning must be recorded in agent evaluation")
                if "test_llm_tool_calling_agent_can_use_memory_to_inform_planning" not in agent_tests:
                    raise AssertionError("memory-informed planning must have a dedicated LLM tool-loop test")
                if "trace_store=trace_store" not in api_source:
                    raise AssertionError("agent API routes must inject the shared trace store")
                if claim.get("metric_value") != 1:
                    raise AssertionError("memory_informed_planning claim must use metric_value=1")
            elif metric_name == "source_cited_business_rule_tool":
                agent_tests = (ROOT / "tests" / "test_agent.py").read_text()
                agent_source = (ROOT / "app" / "tool_agent.py").read_text()
                rules_source = (ROOT / "app" / "business_rules.py").read_text()
                if "retrieve_business_rules" not in agent_source:
                    raise AssertionError("source-cited business-rule retrieval must expose retrieve_business_rules")
                if "used_business_rules_tool" not in agent_source:
                    raise AssertionError("business-rule tool use must be recorded in agent evaluation")
                if "BusinessRuleRetriever" not in agent_source:
                    raise AssertionError("business-rule tool must reuse BusinessRuleRetriever")
                if "test_llm_tool_calling_agent_can_retrieve_business_rules_after_checks" not in agent_tests:
                    raise AssertionError("business-rule tool must have a dedicated LLM tool-loop test")
                if "test_toolbox_retrieves_source_cited_business_rules" not in agent_tests:
                    raise AssertionError("business-rule tool must have a direct toolbox test")
                if "source=f\"" not in rules_source:
                    raise AssertionError("business-rule retrieval must produce source citations")
                if claim.get("metric_value") != 1:
                    raise AssertionError("source_cited_business_rule_tool claim must use metric_value=1")
            elif metric_name == "root_cause_hypothesis_count":
                hypotheses = support_ticket_artifact.get("root_cause_hypotheses", [])
                if len(hypotheses) != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: root_cause_hypothesis_count="
                        f"{claim.get('metric_value')} but support-ticket artifact has {len(hypotheses)}"
                    )
                if not all(item.get("evidence") and item.get("supporting_checks") for item in hypotheses):
                    raise AssertionError("root-cause hypotheses must include evidence and supporting checks")
            elif metric_name == "eval_scenario_count":
                eval_tests = (ROOT / "tests" / "test_eval_summary.py").read_text()
                eval_script = (ROOT / "scripts" / "build_eval_summary.py").read_text()
                if eval_summary.get("scenario_count") != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: eval_scenario_count="
                        f"{claim.get('metric_value')} but eval summary has {eval_summary.get('scenario_count')}"
                    )
                if eval_summary.get("deterministic_baseline", {}).get("finding_recall") != 1.0:
                    raise AssertionError("eval summary must include deterministic finding recall")
                if "verify_eval_summary" not in eval_script:
                    raise AssertionError("eval summary script must verify generated metrics")
                if "test_eval_summary_publishes_resume_safe_agent_metrics" not in eval_tests:
                    raise AssertionError("eval summary must have a dedicated test")
            elif metric_name == "tool_planning_eval":
                eval_tests = (ROOT / "tests" / "test_eval_summary.py").read_text()
                eval_script = (ROOT / "scripts" / "build_eval_summary.py").read_text()
                planning = eval_summary.get("tool_planning_coverage", {})
                if planning.get("available_tool_count") != 7:
                    raise AssertionError("tool-planning eval must verify the 7-tool allowlist")
                if planning.get("required_tools_present") is not True:
                    raise AssertionError("tool-planning eval must verify required tools are present")
                if planning.get("scenario_strategy_recommendation_recall", 0) < 0.88:
                    raise AssertionError("tool-planning eval must meet the strategy recommendation threshold")
                for tool in ("select_quality_strategy", "retrieve_dataset_memory", "retrieve_business_rules"):
                    if tool not in planning.get("tool_names", []):
                        raise AssertionError(f"tool-planning eval missing agent tool: {tool}")
                if "build_tool_planning_coverage" not in eval_script:
                    raise AssertionError("eval summary script must build tool-planning coverage")
                if "test_eval_summary_verifies_tool_planning_coverage_for_agent_claims" not in eval_tests:
                    raise AssertionError("tool-planning eval must have a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("tool_planning_eval claim must use metric_value=1")
            elif metric_name == "hypothesis_feedback_label_count":
                feedback_tests = (ROOT / "tests" / "test_hypothesis_feedback.py").read_text()
                feedback_script = (ROOT / "scripts" / "build_hypothesis_feedback.py").read_text()
                if hypothesis_feedback.get("label_count") != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: hypothesis_feedback_label_count="
                        f"{claim.get('metric_value')} but feedback artifact has {hypothesis_feedback.get('label_count')}"
                    )
                if hypothesis_feedback.get("accepted_count") != 2:
                    raise AssertionError("hypothesis feedback must include accepted labels")
                if hypothesis_feedback.get("needs_review_count") != 1:
                    raise AssertionError("hypothesis feedback must include needs-review labels")
                if "verify_hypothesis_feedback" not in feedback_script:
                    raise AssertionError("hypothesis feedback script must verify generated labels")
                if "test_hypothesis_feedback_labels_root_cause_hypotheses_without_external_claims" not in feedback_tests:
                    raise AssertionError("hypothesis feedback must have a dedicated test")
            elif metric_name == "incident_pattern_count":
                incident_tests = (ROOT / "tests" / "test_incident_pattern_memory.py").read_text()
                incident_script = (ROOT / "scripts" / "build_incident_pattern_memory.py").read_text()
                if incident_memory.get("incident_pattern_count") != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: incident_pattern_count="
                        f"{claim.get('metric_value')} but incident memory has "
                        f"{incident_memory.get('incident_pattern_count')}"
                    )
                if incident_memory.get("trace_count") != 2:
                    raise AssertionError("incident pattern memory must be generated from repeated traces")
                if not all(item.get("evidence_trace_ids") for item in incident_memory.get("patterns", [])):
                    raise AssertionError("incident pattern memory must include evidence trace ids")
                if "external production incidents" not in incident_memory.get("not_claimed", []):
                    raise AssertionError("incident pattern memory must not claim external production incidents")
                if "verify_incident_pattern_memory" not in incident_script:
                    raise AssertionError("incident pattern memory script must verify generated patterns")
                if "test_incident_pattern_memory_retrieves_recurring_sanitized_patterns" not in incident_tests:
                    raise AssertionError("incident pattern memory must have a dedicated test")
            elif metric_name == "observed_trace_count":
                observability_tests = (ROOT / "tests" / "test_agent_observability.py").read_text()
                observability_script = (ROOT / "scripts" / "build_agent_observability.py").read_text()
                if observability.get("observed_trace_count") != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: observed_trace_count="
                        f"{claim.get('metric_value')} but observability has "
                        f"{observability.get('observed_trace_count')}"
                    )
                if observability.get("fallback_event_count") != 2:
                    raise AssertionError("agent observability must capture disabled fallback events")
                if "agent_disabled" not in observability.get("fallback_statuses", []):
                    raise AssertionError("agent observability must capture agent_disabled fallback status")
                if "production monitoring dashboard" not in observability.get("not_claimed", []):
                    raise AssertionError("agent observability must not claim production monitoring")
                if "verify_agent_observability" not in observability_script:
                    raise AssertionError("agent observability script must verify generated metrics")
                if "test_agent_observability_artifact_tracks_trace_fallback_and_memory" not in observability_tests:
                    raise AssertionError("agent observability must have a dedicated test")
            elif metric_name == "model_telemetry_artifact":
                observability_tests = (ROOT / "tests" / "test_agent_observability.py").read_text()
                observability_script = (ROOT / "scripts" / "build_agent_observability.py").read_text()
                telemetry = observability.get("model_telemetry", {})
                if telemetry.get("model_call_count") != 2:
                    raise AssertionError("model telemetry artifact must verify model call count")
                if telemetry.get("total_tokens") != 360:
                    raise AssertionError("model telemetry artifact must verify token count")
                if telemetry.get("estimated_cost_usd") != 0.000081:
                    raise AssertionError("model telemetry artifact must verify estimated cost")
                if telemetry.get("prompt_version") != "tool-agent-v3":
                    raise AssertionError("model telemetry artifact must verify prompt version")
                if telemetry.get("raw_prompt_logged") is not False:
                    raise AssertionError("model telemetry artifact must prove raw prompts are not logged")
                if "_run_mock_telemetry_agent" not in observability_script:
                    raise AssertionError("observability script must build deterministic model telemetry")
                if "test_llm_tool_calling_agent_records_model_telemetry_without_raw_prompt" not in (
                    ROOT / "tests" / "test_agent.py"
                ).read_text():
                    raise AssertionError("model telemetry must have a dedicated agent test")
                if "Mock total tokens | 360" not in (ROOT / "docs" / "agent-observability.md").read_text():
                    raise AssertionError("agent observability page must show model token telemetry")
                if "paid model benchmark results" not in observability.get("not_claimed", []):
                    raise AssertionError("model telemetry artifact must not claim paid benchmark results")
                if claim.get("metric_value") != 1:
                    raise AssertionError("model_telemetry_artifact claim must use metric_value=1")
            elif metric_name == "tool_allowlist_count":
                safety_tests = (ROOT / "tests" / "test_agent_safety_boundaries.py").read_text()
                safety_script = (ROOT / "scripts" / "build_agent_safety_boundaries.py").read_text()
                if safety.get("tool_allowlist_count") != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: tool_allowlist_count="
                        f"{claim.get('metric_value')} but safety artifact has "
                        f"{safety.get('tool_allowlist_count')}"
                    )
                if safety.get("postgres_rejected_write_query_count") != 3:
                    raise AssertionError("agent safety artifact must verify rejected unsafe PostgreSQL queries")
                if safety.get("llm_sensitive_redaction_verified") is not True:
                    raise AssertionError("agent safety artifact must verify sensitive-field redaction")
                if safety.get("agent_disabled_fallback_verified") is not True:
                    raise AssertionError("agent safety artifact must verify disabled fallback")
                if "formal security audit" not in safety.get("not_claimed", []):
                    raise AssertionError("agent safety artifact must not claim a formal security audit")
                if "verify_agent_safety_boundaries" not in safety_script:
                    raise AssertionError("agent safety script must verify generated boundaries")
                if "test_agent_safety_boundaries_capture_tool_permissions_and_guardrails" not in safety_tests:
                    raise AssertionError("agent safety boundaries must have a dedicated test")
            elif metric_name == "agent_capability_matrix":
                matrix_tests = (ROOT / "tests" / "test_agent_capability_matrix.py").read_text()
                matrix_script = (ROOT / "scripts" / "build_agent_capability_matrix.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("agent capability matrix claim must use metric_value=1")
                if capability_matrix.get("tool_count") != 7:
                    raise AssertionError("agent capability matrix must verify seven allowed tools")
                if capability_matrix.get("implemented_count") != 13:
                    raise AssertionError("agent capability matrix must verify 13 implemented capabilities")
                if capability_matrix.get("partial_count") != 4:
                    raise AssertionError("agent capability matrix must preserve partial maturity areas")
                if capability_matrix.get("not_claimed_count") != 1:
                    raise AssertionError("agent capability matrix must preserve explicit not-claimed areas")
                if "enterprise production deployment" not in capability_matrix.get("not_claimed", []):
                    raise AssertionError("agent capability matrix must not claim production deployment")
                capability_ids = {item.get("id") for item in capability_matrix.get("capabilities", [])}
                for required in ("llm-decision-making", "tool-feedback-loop", "dynamic-path", "production-adoption"):
                    if required not in capability_ids:
                        raise AssertionError(f"agent capability matrix missing {required}")
                if "verify_agent_capability_matrix" not in matrix_script:
                    raise AssertionError("agent capability matrix script must verify generated metrics")
                if "test_agent_capability_matrix_maps_real_agent_requirements_without_inflation" not in matrix_tests:
                    raise AssertionError("agent capability matrix must have a dedicated test")
            elif metric_name == "live_project_scorecard":
                scorecard_tests = (ROOT / "tests" / "test_live_project_scorecard.py").read_text()
                scorecard_script = (ROOT / "scripts" / "build_live_project_scorecard.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("live project scorecard claim must use metric_value=1")
                scorecard_claim_count = scorecard.get("headline_metrics", {}).get("verified_resume_claims")
                if scorecard_claim_count != len(claims):
                    raise AssertionError(
                        "live project scorecard must summarize the current claim count: "
                        f"scorecard={scorecard_claim_count}, claims={len(claims)}"
                    )
                if scorecard.get("live_footprint", {}).get("stars") != 0:
                    raise AssertionError("live project scorecard must preserve the zero-star baseline")
                if scorecard.get("live_footprint", {}).get("confirmed_external_users") != 0:
                    raise AssertionError("live project scorecard must preserve the zero-user baseline")
                if not all(scorecard.get("claim_coverage", {}).values()):
                    raise AssertionError("live project scorecard must cover core public evidence claims")
                if "verify_live_project_scorecard" not in scorecard_script:
                    raise AssertionError("live project scorecard script must verify generated metrics")
                if "test_live_project_scorecard_summarizes_public_resume_evidence_without_inflation" not in scorecard_tests:
                    raise AssertionError("live project scorecard must have a dedicated test")
            elif metric_name == "openapi_required_endpoint_count":
                openapi_tests = (ROOT / "tests" / "test_openapi_artifact.py").read_text()
                openapi_script = (ROOT / "scripts" / "build_openapi_artifact.py").read_text()
                required_paths = {
                    "/business-data/quality-report": "post",
                    "/business-data/agent-report": "post",
                    "/postgres/support-tickets/agent-report": "post",
                    "/datasets/{dataset_id}/memory": "get",
                    "/runs/{trace_id}": "get",
                    "/datasets/{dataset_id}/incident-report.md": "post",
                }
                paths = openapi.get("paths", {})
                for path, method in required_paths.items():
                    if method not in paths.get(path, {}):
                        raise AssertionError(f"OpenAPI artifact missing {method.upper()} {path}")
                if len(required_paths) != claim.get("metric_value"):
                    raise AssertionError("OpenAPI required endpoint count must match the claim")
                if "verify_openapi_payload" not in openapi_script:
                    raise AssertionError("OpenAPI artifact script must verify generated schema")
                if "test_openapi_artifact_covers_core_integration_endpoints" not in openapi_tests:
                    raise AssertionError("OpenAPI artifact must have a dedicated test")
            elif metric_name == "recruiter_pitch_resume_bullets":
                pitch_tests = (ROOT / "tests" / "test_recruiter_pitch.py").read_text()
                pitch_script = (ROOT / "scripts" / "build_recruiter_pitch.py").read_text()
                if len(recruiter_pitch.get("resume_bullets", [])) != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: recruiter_pitch_resume_bullets="
                        f"{claim.get('metric_value')} but recruiter pitch has "
                        f"{len(recruiter_pitch.get('resume_bullets', []))}"
                    )
                if len(recruiter_pitch.get("target_roles", [])) != 4:
                    raise AssertionError("recruiter pitch must cover four target roles")
                if recruiter_pitch.get("honest_baseline", {}).get("stars") != 0:
                    raise AssertionError("recruiter pitch must preserve the zero-star baseline")
                if recruiter_pitch.get("honest_baseline", {}).get("confirmed_external_users") != 0:
                    raise AssertionError("recruiter pitch must preserve the zero-user baseline")
                for required in ("external users", "customer feedback"):
                    if required not in recruiter_pitch.get("not_claimed", []):
                        raise AssertionError(f"recruiter pitch must not claim {required}")
                if "verify_recruiter_pitch" not in pitch_script:
                    raise AssertionError("recruiter pitch script must verify generated language")
                if "test_recruiter_pitch_turns_verified_evidence_into_safe_application_language" not in pitch_tests:
                    raise AssertionError("recruiter pitch must have a dedicated test")
            elif metric_name == "application_evidence_link_count":
                pack_tests = (ROOT / "tests" / "test_application_evidence_pack.py").read_text()
                pack_script = (ROOT / "scripts" / "build_application_evidence_pack.py").read_text()
                if len(application_pack.get("application_links", {})) != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: application_evidence_link_count="
                        f"{claim.get('metric_value')} but application evidence pack has "
                        f"{len(application_pack.get('application_links', {}))}"
                    )
                if application_pack.get("verified_outcome_numbers", {}).get("passing_tests") != 91:
                    raise AssertionError("application evidence pack must include current passing test count")
                if application_pack.get("verified_outcome_numbers", {}).get("verified_resume_claims") != len(claims):
                    raise AssertionError("application evidence pack must summarize current claim count")
                if application_pack.get("honest_baseline", {}).get("stars") != 0:
                    raise AssertionError("application evidence pack must preserve the zero-star baseline")
                if application_pack.get("honest_baseline", {}).get("confirmed_external_users") != 0:
                    raise AssertionError("application evidence pack must preserve the zero-user baseline")
                if "verify_application_evidence_pack" not in pack_script:
                    raise AssertionError("application evidence pack script must verify generated language")
                if "test_application_evidence_pack_gives_recruiters_verified_review_path" not in pack_tests:
                    raise AssertionError("application evidence pack must have a dedicated test")
            elif metric_name == "pilot_outreach_message_count":
                pilot_tests = (ROOT / "tests" / "test_pilot_outreach_kit.py").read_text()
                pilot_script = (ROOT / "scripts" / "build_pilot_outreach_kit.py").read_text()
                if len(pilot_outreach.get("outreach_messages", [])) != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: pilot_outreach_message_count="
                        f"{claim.get('metric_value')} but pilot outreach kit has "
                        f"{len(pilot_outreach.get('outreach_messages', []))}"
                    )
                if len(pilot_outreach.get("review_paths", {})) != 9:
                    raise AssertionError("pilot outreach kit must include nine review paths")
                if pilot_outreach.get("success_metrics", {}).get("external_feedback_items") != 0:
                    raise AssertionError("pilot outreach kit must preserve current feedback baseline")
                if pilot_outreach.get("success_metrics", {}).get("confirmed_external_users") != 0:
                    raise AssertionError("pilot outreach kit must preserve current user baseline")
                if "verify_pilot_outreach_kit" not in pilot_script:
                    raise AssertionError("pilot outreach kit script must verify generated messages")
                if "test_pilot_outreach_kit_supports_real_feedback_without_inflating_usage" not in pilot_tests:
                    raise AssertionError("pilot outreach kit must have a dedicated test")
            elif metric_name == "pilot_program_segment_count":
                plan_tests = (ROOT / "tests" / "test_pilot_program_plan.py").read_text()
                plan_script = (ROOT / "scripts" / "build_pilot_program_plan.py").read_text()
                if len(pilot_plan.get("participant_segments", [])) != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: pilot_program_segment_count="
                        f"{claim.get('metric_value')} but pilot plan has "
                        f"{len(pilot_plan.get('participant_segments', []))}"
                    )
                if len(pilot_plan.get("weekly_plan", [])) != 3:
                    raise AssertionError("pilot program plan must include a three-week plan")
                thresholds = pilot_plan.get("success_thresholds", {})
                if thresholds.get("current_external_feedback_items") != 0:
                    raise AssertionError("pilot program plan must preserve current feedback baseline")
                if thresholds.get("current_confirmed_external_users") != 0:
                    raise AssertionError("pilot program plan must preserve current user baseline")
                if thresholds.get("minimum_feedback_items_before_resume_claim") != 3:
                    raise AssertionError("pilot program plan must require three feedback items before feedback claims")
                if "verify_pilot_program_plan" not in plan_script:
                    raise AssertionError("pilot program plan script must verify generated plan")
                if "test_pilot_program_plan_defines_feedback_thresholds_before_resume_claims" not in plan_tests:
                    raise AssertionError("pilot program plan must have a dedicated test")
            elif metric_name == "pilot_review_tracker":
                tracker_tests = (ROOT / "tests" / "test_pilot_review_tracker.py").read_text()
                tracker_script = (ROOT / "scripts" / "build_pilot_review_tracker.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("pilot review tracker claim must use metric_value=1")
                if pilot_tracker.get("planned_review_count") != 3:
                    raise AssertionError("pilot review tracker must include three planned reviews")
                if pilot_tracker.get("status_counts", {}).get("not_contacted") != 3:
                    raise AssertionError("pilot review tracker must preserve not-contacted baseline")
                if pilot_tracker.get("status_counts", {}).get("feedback_received") != 0:
                    raise AssertionError("pilot review tracker must not count feedback before public evidence")
                public_counts = pilot_tracker.get("public_counts", {})
                expected_counts = {
                    "external_feedback_items": 0,
                    "confirmed_external_users": 0,
                    "business_case_feedback_items": 0,
                }
                for key, expected in expected_counts.items():
                    if public_counts.get(key) != expected:
                        raise AssertionError(f"pilot review tracker {key} expected {expected!r}")
                if any(item.get("counts_toward_resume") for item in pilot_tracker.get("planned_reviews", [])):
                    raise AssertionError("pilot review tracker must not count planned reviews toward resume")
                if len(pilot_tracker.get("resume_upgrade_rules", [])) != 3:
                    raise AssertionError("pilot review tracker must include three resume-upgrade rules")
                if "verify_pilot_review_tracker" not in tracker_script:
                    raise AssertionError("pilot review tracker script must verify generated tracker")
                if (
                    "test_pilot_review_tracker_tracks_planned_reviews_without_counting_unverified_feedback"
                    not in tracker_tests
                ):
                    raise AssertionError("pilot review tracker must have a dedicated test")
            elif metric_name == "feedback_intake_quality":
                intake_tests = (ROOT / "tests" / "test_feedback_intake_quality.py").read_text()
                intake_script = (ROOT / "scripts" / "build_feedback_intake_quality.py").read_text()
                template_text = (ROOT / ".github" / "ISSUE_TEMPLATE" / "demo_feedback.md").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("feedback intake quality claim must use metric_value=1")
                expected = {
                    "required_section_count": 5,
                    "required_try_path_count": 5,
                    "required_outcome_count": 4,
                    "captured_field_count": 5,
                }
                for key, value in expected.items():
                    if feedback_intake.get(key) != value:
                        raise AssertionError(f"feedback intake {key} expected {value}")
                if not all(feedback_intake.get("captured_fields", {}).values()):
                    raise AssertionError("feedback intake must verify all captured field groups")
                if feedback_intake.get("current_public_counts", {}).get("external_feedback_items") != 0:
                    raise AssertionError("feedback intake must preserve zero external feedback baseline")
                if feedback_intake.get("current_public_counts", {}).get("confirmed_external_users") != 0:
                    raise AssertionError("feedback intake must preserve zero confirmed-user baseline")
                for required in ("Public demo page", "CSV upload endpoint", "LLM tool-calling route", "Command or URL used:"):
                    if required not in template_text:
                        raise AssertionError(f"feedback template missing required prompt: {required}")
                if "verify_feedback_intake_quality" not in intake_script:
                    raise AssertionError("feedback intake script must verify generated artifact")
                if "test_feedback_intake_quality_verifies_public_feedback_template_without_usage_claims" not in intake_tests:
                    raise AssertionError("feedback intake must have a dedicated test")
            elif metric_name == "business_case_intake":
                case_tests = (ROOT / "tests" / "test_business_case_intake.py").read_text()
                case_script = (ROOT / "scripts" / "build_business_case_intake.py").read_text()
                template_text = (ROOT / ".github" / "ISSUE_TEMPLATE" / "business_case_review.md").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("business case intake claim must use metric_value=1")
                expected = {
                    "required_section_count": 6,
                    "required_context_field_count": 3,
                    "required_try_path_count": 5,
                    "required_outcome_count": 5,
                    "captured_field_count": 6,
                }
                for key, value in expected.items():
                    if business_case_intake.get(key) != value:
                        raise AssertionError(f"business case intake {key} expected {value}")
                if not all(business_case_intake.get("captured_fields", {}).values()):
                    raise AssertionError("business case intake must verify all captured field groups")
                if business_case_intake.get("tracking_label") != "business-case":
                    raise AssertionError("business case intake must use the business-case label")
                if business_case_intake.get("current_public_counts", {}).get("business_case_feedback_items") != 0:
                    raise AssertionError("business case intake must preserve zero submitted-case baseline")
                if business_case_intake.get("current_public_counts", {}).get("confirmed_external_users") != 0:
                    raise AssertionError("business case intake must preserve zero confirmed-user baseline")
                for required in (
                    "Industry or team:",
                    "Workflow affected:",
                    "Data source type:",
                    "Do not quote my organization, name, or raw data.",
                ):
                    if required not in template_text:
                        raise AssertionError(f"business case template missing required prompt: {required}")
                if "verify_business_case_intake" not in case_script:
                    raise AssertionError("business case intake script must verify generated artifact")
                if (
                    "test_business_case_intake_collects_real_problem_context_without_claiming_cases"
                    not in case_tests
                ):
                    raise AssertionError("business case intake must have a dedicated test")
            elif metric_name == "star_growth_kit":
                star_script = (ROOT / "scripts" / "build_star_growth_kit.py").read_text()
                star_tests = (ROOT / "tests" / "test_star_growth_kit.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("star growth kit claim must use metric_value=1")
                counts = star_growth.get("current_public_counts", {})
                expected_counts = {
                    "stars": 0,
                    "forks": 1,
                    "watchers": 0,
                    "issues_total": 11,
                    "external_feedback_items": 0,
                    "confirmed_external_users": 0,
                }
                for key, expected in expected_counts.items():
                    if counts.get(key) != expected:
                        raise AssertionError(f"star growth kit {key} expected {expected!r}")
                topics = star_growth.get("topic_readiness", {})
                if topics.get("ready") is not True:
                    raise AssertionError("star growth kit must verify topic readiness")
                if len(topics.get("required_topics", [])) != 6:
                    raise AssertionError("star growth kit must verify 6 required topics")
                if len(star_growth.get("ethical_growth_actions", [])) != 4:
                    raise AssertionError("star growth kit must verify 4 ethical growth actions")
                rules = star_growth.get("resume_upgrade_rules", [])
                if len(rules) != 3:
                    raise AssertionError("star growth kit must verify 3 resume upgrade rules")
                if not all(rule.get("resume_status") == "not_claimable_yet" for rule in rules):
                    raise AssertionError("star growth kit must keep growth signals not claimable before evidence")
                if "fake or incentivized stars" not in star_growth.get("not_claimed", []):
                    raise AssertionError("star growth kit must explicitly reject fake or incentivized stars")
                if "verify_star_growth_kit" not in star_script:
                    raise AssertionError("star growth kit must include a script verifier")
                if "test_star_growth_kit_tracks_ethical_growth_without_inflating_stars" not in star_tests:
                    raise AssertionError("star growth kit must include a dedicated test")
            elif metrics.get(metric_name) != claim.get("metric_value"):
                raise AssertionError(
                    f"claim {claim['id']} metric mismatch: {metric_name}={claim.get('metric_value')} "
                    f"but adoption metrics has {metrics.get(metric_name)}"
                )
        if claim["id"] not in resume_page:
            raise AssertionError(f"resume evidence page must mention claim id or anchor text: {claim['id']}")

    if "public-evidence-health" in claim_ids:
        workflow_text = PUBLIC_HEALTH_WORKFLOW_PATH.read_text()
        script_text = PUBLIC_HEALTH_SCRIPT_PATH.read_text()
        if "schedule:" not in workflow_text or "workflow_dispatch:" not in workflow_text:
            raise AssertionError("public evidence health workflow must support scheduled and manual runs")
        for required in ["public-demo", "business-impact-artifact", "github-release"]:
            if required not in script_text:
                raise AssertionError(f"public evidence health script must check {required}")

    if "postgres-agent-route" in claim_ids:
        script_text = PUBLIC_HEALTH_SCRIPT_PATH.read_text()
        if "postgres-agent-route" not in script_text:
            raise AssertionError("public evidence health script must check postgres-agent-route")
        if "/postgres/support-tickets/agent-report" not in script_text:
            raise AssertionError("public evidence health script must verify the PostgreSQL agent route path")

    if "agent-readiness" in claim_ids:
        readiness_page = (ROOT / "docs" / "agent-readiness.md").read_text().lower()
        if len(agent_readiness.get("implemented", [])) < 9:
            raise AssertionError("agent readiness must document at least nine implemented capabilities")
        if len(agent_readiness.get("partial", [])) < 4:
            raise AssertionError("agent readiness must document partial capabilities instead of overstating maturity")
        if len(agent_readiness.get("planned", [])) < 3:
            raise AssertionError("agent readiness must include concrete planned upgrades")
        for required in ("external users", "customer feedback", "enterprise production deployment"):
            if required not in agent_readiness.get("not_claimed", []):
                raise AssertionError(f"agent readiness must not claim {required}")
            if required not in readiness_page:
                raise AssertionError(f"agent readiness page must mention not-claimed signal: {required}")

    if "outcome-summary" in claim_ids:
        summary_page = (ROOT / "docs" / "outcome-summary.md").read_text().lower()
        required_phrases = [
            "support operations dashboard data",
            "issue categories | 4",
            "recommended actions | 5",
            "no verified external users yet",
        ]
        for phrase in required_phrases:
            if phrase not in summary_page:
                raise AssertionError(f"outcome summary page missing phrase: {phrase}")

    if "public-metrics-summary" in claim_ids:
        metrics_page = (ROOT / "docs" / "public-metrics-summary.md").read_text().lower()
        for phrase in ("passing ci tests | 91", "confirmed external users | 0", "forks | 1"):
            if phrase not in metrics_page:
                raise AssertionError(f"public metrics summary page missing phrase: {phrase}")

    not_claimed = {item["metric"] for item in evidence.get("not_claimed", [])}
    for required in {"users", "customer_feedback", "production_company_usage"}:
        if required not in not_claimed:
            raise AssertionError(f"missing explicit not_claimed entry for {required}")
        if required.replace("_", " ") not in resume_page and required not in resume_page:
            raise AssertionError(f"resume evidence page must mention not-claimed signal: {required}")

    if "external feedback items | 0" not in feedback_log:
        raise AssertionError("feedback log must keep an explicit zero external feedback baseline")
    if "confirmed external users | 0" not in feedback_log:
        raise AssertionError("feedback log must keep an explicit zero external user baseline")
    for key in ("external_feedback_items", "confirmed_external_users", "reproducible_feedback_items"):
        if metrics.get(key) != feedback_metrics.get(key):
            raise AssertionError(f"adoption metrics {key} must match feedback metrics")
    if not history:
        raise AssertionError("adoption history must include at least one point")
    latest = history[-1]
    for key in ("stars", "forks", "watchers", "issues_total", "test_count"):
        if latest.get(key) != metrics.get(key):
            raise AssertionError(f"adoption history latest {key} must match adoption metrics")

    return {
        "claim_count": len(claims),
        "not_claimed_count": len(not_claimed),
        "resume_evidence_page": 1,
        "feedback_log": 1,
        "adoption_history_count": len(history),
    }


def main() -> None:
    print(json.dumps(verify_manifest(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
