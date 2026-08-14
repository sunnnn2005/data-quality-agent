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
PUBLIC_TRACTION_DASHBOARD_PATH = ROOT / "docs" / "public-traction-dashboard.json"
LIVE_SCORECARD_PATH = ROOT / "docs" / "live-project-scorecard.json"
OPENAPI_PATH = ROOT / "docs" / "openapi.json"
RECRUITER_PITCH_PATH = ROOT / "docs" / "recruiter-pitch.json"
APPLICATION_EVIDENCE_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
PILOT_OUTREACH_KIT_PATH = ROOT / "docs" / "pilot-outreach-kit.json"
PILOT_PROGRAM_PLAN_PATH = ROOT / "docs" / "pilot-program-plan.json"
PILOT_REVIEW_TRACKER_PATH = ROOT / "docs" / "pilot-review-tracker.json"
PILOT_CONVERSION_BOARD_PATH = ROOT / "docs" / "pilot-conversion-board.json"
RESUME_OUTCOME_READINESS_PATH = ROOT / "docs" / "resume-outcome-readiness.json"
EXTERNAL_REVIEW_EVIDENCE_LEDGER_PATH = ROOT / "docs" / "external-review-evidence-ledger.json"
OUTCOME_UPGRADE_PLAYBOOK_PATH = ROOT / "docs" / "outcome-upgrade-playbook.json"
REVIEWER_FEEDBACK_PACKET_PATH = ROOT / "docs" / "reviewer-feedback-packet.json"
REVIEWER_FUNNEL_BOARD_PATH = ROOT / "docs" / "reviewer-funnel-board.json"
FEEDBACK_INTAKE_QUALITY_PATH = ROOT / "docs" / "feedback-intake-quality.json"
STAR_GROWTH_KIT_PATH = ROOT / "docs" / "star-growth-kit.json"
GITHUB_DISCOVERY_PROFILE_PATH = ROOT / "docs" / "github-discovery-profile.json"
PILOT_EVIDENCE_QUICKLINK_PATH = ROOT / "docs" / "pilot-evidence-quicklink.json"
PILOT_LAUNCH_CONTROL_ROOM_PATH = ROOT / "docs" / "pilot-launch-control-room.json"
BUSINESS_CASE_INTAKE_PATH = ROOT / "docs" / "business-case-intake.json"
BUSINESS_DATA_REPLAY_PACKET_PATH = ROOT / "docs" / "business-data-replay-packet.json"
REAL_MODEL_RUNBOOK_PATH = ROOT / "docs" / "real-model-runbook.json"
REAL_MODEL_EVIDENCE_CAPTURE_PATH = ROOT / "docs" / "real-model-evidence-capture.json"
BUSINESS_REPLAY_DEMO_PATH = ROOT / "docs" / "business-replay-demo.json"
RESUME_CLAIM_UPGRADE_LEDGER_PATH = ROOT / "docs" / "resume-claim-upgrade-ledger.json"
PUBLIC_HEALTH_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "public-evidence-health.yml"
PUBLIC_METRICS_REFRESH_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "refresh-public-metrics.yml"
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
    external_run_evidence = load_payload(EXTERNAL_RUN_EVIDENCE_PACKET_PATH)
    external_reviewer_request = load_payload(EXTERNAL_REVIEWER_REQUEST_PACK_PATH)
    external_run_quickstart = load_payload(EXTERNAL_RUN_QUICKSTART_PATH)
    external_reviewer_outreach = load_payload(EXTERNAL_REVIEWER_OUTREACH_TRACKER_PATH)
    external_reviewer_gate = load_payload(EXTERNAL_REVIEWER_EVIDENCE_GATE_PATH)
    accepted_evidence_rollup = load_payload(ACCEPTED_EVIDENCE_ROLLUP_PATH)
    business_impact_ledger = load_payload(BUSINESS_IMPACT_LEDGER_PATH)
    reviewer_evidence_kit = load_payload(REVIEWER_EVIDENCE_KIT_PATH)
    resume_traction_proof = load_payload(RESUME_TRACTION_PROOF_PATH)
    reviewer_action_queue = load_payload(REVIEWER_ACTION_QUEUE_PATH)
    reviewer_outreach_execution = load_payload(REVIEWER_OUTREACH_EXECUTION_PACK_PATH)
    reviewer_outreach_status = load_payload(REVIEWER_OUTREACH_STATUS_BOARD_PATH)
    resume_outcome_metrics = load_payload(RESUME_OUTCOME_METRICS_PATH)
    resume_outcome_action_checklist = load_payload(RESUME_OUTCOME_ACTION_CHECKLIST_PATH)
    reviewer_submission_hub = load_payload(REVIEWER_SUBMISSION_HUB_PATH)
    outcome_collection = load_payload(OUTCOME_COLLECTION_PATH)
    public_reviewer_call = load_payload(PUBLIC_REVIEWER_CALL_PATH)
    reviewer_share_kit = load_payload(REVIEWER_SHARE_KIT_PATH)
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
    pilot_conversion = load_payload(PILOT_CONVERSION_BOARD_PATH)
    resume_outcome_readiness = load_payload(RESUME_OUTCOME_READINESS_PATH)
    external_ledger = load_payload(EXTERNAL_REVIEW_EVIDENCE_LEDGER_PATH)
    outcome_upgrade = load_payload(OUTCOME_UPGRADE_PLAYBOOK_PATH)
    reviewer_packet = load_payload(REVIEWER_FEEDBACK_PACKET_PATH)
    reviewer_funnel = load_payload(REVIEWER_FUNNEL_BOARD_PATH)
    feedback_intake = load_payload(FEEDBACK_INTAKE_QUALITY_PATH)
    star_growth = load_payload(STAR_GROWTH_KIT_PATH)
    github_discovery = load_payload(GITHUB_DISCOVERY_PROFILE_PATH)
    pilot_evidence_quicklink = load_payload(PILOT_EVIDENCE_QUICKLINK_PATH)
    pilot_launch_control_room = load_payload(PILOT_LAUNCH_CONTROL_ROOM_PATH)
    business_case_intake = load_payload(BUSINESS_CASE_INTAKE_PATH)
    replay_packet = load_payload(BUSINESS_DATA_REPLAY_PACKET_PATH)
    real_model_runbook = load_payload(REAL_MODEL_RUNBOOK_PATH)
    real_model_evidence_capture = load_payload(REAL_MODEL_EVIDENCE_CAPTURE_PATH)
    replay_demo = load_payload(BUSINESS_REPLAY_DEMO_PATH)
    claim_upgrade = load_payload(RESUME_CLAIM_UPGRADE_LEDGER_PATH)
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
            elif metric_name == "external_run_evidence_packet":
                external_run_script = (ROOT / "scripts" / "build_external_run_evidence_packet.py").read_text()
                external_run_tests = (ROOT / "tests" / "test_external_run_evidence_packet.py").read_text()
                external_run_template = (ROOT / ".github" / "ISSUE_TEMPLATE" / "external_run_review.md").read_text()
                if external_run_evidence.get("review_path_count") != 3:
                    raise AssertionError("external run evidence packet must define 3 reviewer run paths")
                if external_run_evidence.get("submission_field_count") != 8:
                    raise AssertionError("external run evidence packet must define 8 required submission fields")
                if external_run_evidence.get("upgrade_rule_count") != 3:
                    raise AssertionError("external run evidence packet must define 3 upgrade rules")
                if external_run_evidence.get("current_counts", {}).get("confirmed_external_users") != 0:
                    raise AssertionError("external run evidence packet must preserve zero confirmed-user baseline")
                if external_run_evidence.get("public_collection_issue", {}).get("url", "").endswith("/issues/18") is False:
                    raise AssertionError("external run evidence packet must link public collection issue #18")
                if "external_run_review.md" not in json.dumps(external_run_evidence):
                    raise AssertionError("external run evidence packet must link the external run review issue template")
                if "This can be counted as public external run evidence." not in external_run_template:
                    raise AssertionError("external run review template must collect countable public evidence")
                if (
                    external_run_evidence.get("public_collection_issue", {}).get("counting_status")
                    != "collection_open_not_counted_yet"
                ):
                    raise AssertionError("external run evidence packet must keep the public collection issue uncounted")
                if "permission_to_count_publicly" not in json.dumps(external_run_evidence):
                    raise AssertionError("external run evidence packet must require permission to count publicly")
                if "Do not ask reviewers to upload private business data." not in external_run_evidence.get(
                    "privacy_boundaries", []
                ):
                    raise AssertionError("external run evidence packet must include privacy boundaries")
                if "No external users are claimed yet." not in external_run_evidence.get("not_claimed", []):
                    raise AssertionError("external run evidence packet must not claim external users")
                if "verify_external_run_evidence_packet" not in external_run_script:
                    raise AssertionError("external run evidence packet must have a script verifier")
                if "test_external_run_evidence_packet_defines_public_reviewer_run_proof" not in external_run_tests:
                    raise AssertionError("external run evidence packet must have a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("external_run_evidence_packet claim must use metric_value=1")
            elif metric_name == "external_reviewer_request_pack":
                request_script = (ROOT / "scripts" / "build_external_reviewer_request_pack.py").read_text()
                request_tests = (ROOT / "tests" / "test_external_reviewer_request_pack.py").read_text()
                template_tests = (ROOT / "tests" / "test_external_run_issue_template.py").read_text()
                if external_reviewer_request.get("status") != "outreach_ready_not_counted":
                    raise AssertionError("external reviewer request pack must keep outreach uncounted")
                if external_reviewer_request.get("public_collection_issue", {}).get("number") != 18:
                    raise AssertionError("external reviewer request pack must link issue #18")
                if "external_run_review.md" not in json.dumps(external_reviewer_request):
                    raise AssertionError("external reviewer request pack must link the external run issue template")
                if len(external_reviewer_request.get("outreach_messages", [])) != 3:
                    raise AssertionError("external reviewer request pack must include three outreach messages")
                run_paths = {item.get("run_path") for item in external_reviewer_request.get("outreach_messages", [])}
                if run_paths != {"public_demo_review", "container_smoke_run", "postgres_replay_run"}:
                    raise AssertionError("external reviewer request pack must cover all three run paths")
                if len(external_reviewer_request.get("required_comment_fields", [])) != 8:
                    raise AssertionError("external reviewer request pack must preserve eight evidence fields")
                if external_reviewer_request.get("current_counts", {}).get("confirmed_external_users") != 0:
                    raise AssertionError("external reviewer request pack must preserve zero confirmed-user baseline")
                if "No outreach recipient has completed a run yet." not in external_reviewer_request.get(
                    "not_claimed", []
                ):
                    raise AssertionError("external reviewer request pack must not claim completed runs")
                if "permission_to_count_publicly" not in json.dumps(external_reviewer_request):
                    raise AssertionError("external reviewer request pack must require permission to count publicly")
                if "verify_external_reviewer_request_pack" not in request_script:
                    raise AssertionError("external reviewer request pack must have a script verifier")
                if "test_external_reviewer_request_pack_routes_real_runs_to_issue_18" not in request_tests:
                    raise AssertionError("external reviewer request pack must have a dedicated test")
                if "test_external_run_issue_template_collects_countable_public_evidence" not in template_tests:
                    raise AssertionError("external run issue template must have a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("external_reviewer_request_pack claim must use metric_value=1")
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
                if community_growth.get("issue_template_count") != 8:
                    raise AssertionError("community growth baseline must verify 8 issue templates")
                if "external_run_review.md" not in community_growth.get("issue_templates", []):
                    raise AssertionError("community growth baseline must include the external run review template")
                if community_growth.get("label_count") != 7:
                    raise AssertionError("community growth baseline must verify 7 labels")
                if len(community_growth.get("public_growth_channels", [])) != 9:
                    raise AssertionError("community growth baseline must verify 9 public growth channels")
                if not all(community_growth.get("contribution_paths", {}).values()):
                    raise AssertionError("community growth baseline must verify contribution paths")
                counts = community_growth.get("current_public_counts", {})
                expected_counts = {
                    "stars": 0,
                    "forks": 1,
                    "issues_total": 14,
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
                if traction.get("growth_channel_count") != 19:
                    raise AssertionError("public traction dashboard must verify 19 growth or review channels")
                if traction.get("tracked_funnel_steps") != 5:
                    raise AssertionError("public traction dashboard must verify 5 tracked funnel steps")
                if traction.get("demo_entrypoints_verified") != 6:
                    raise AssertionError("public traction dashboard must verify 6 demo entrypoints")
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
                        "issues_total": 14,
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
                if public_metrics_summary.get("public_metrics", {}).get("test_count") != 149:
                    raise AssertionError("public metrics summary must include the current CI test count")
                if public_metrics_summary.get("public_metrics", {}).get("external_feedback_items") != 0:
                    raise AssertionError("public metrics summary must preserve the zero-feedback baseline")
                if claim.get("metric_value") != 1:
                    raise AssertionError("public_metrics_summary claim must use metric_value=1")
            elif metric_name == "resume_traction_proof":
                traction_proof_script = (ROOT / "scripts" / "build_resume_traction_proof.py").read_text()
                traction_proof_tests = (ROOT / "tests" / "test_resume_traction_proof.py").read_text()
                expected_counts = {
                    "stars": 0,
                    "confirmed_external_users": 0,
                    "external_feedback_items": 0,
                    "reproducible_feedback_items": 0,
                }
                for key, expected in expected_counts.items():
                    if resume_traction_proof.get("public_counts", {}).get(key) != expected:
                        raise AssertionError(f"resume traction proof {key} expected {expected!r}")
                if resume_traction_proof.get("claimable_now_count") != 4:
                    raise AssertionError("resume traction proof must include 4 claimable current signals")
                if resume_traction_proof.get("future_claim_count") != 4:
                    raise AssertionError("resume traction proof must include 4 future outcome claims")
                if resume_traction_proof.get("blocked_claim_count") != 5:
                    raise AssertionError("resume traction proof must include 5 blocked claim rules")
                if not all(
                    item.get("status") == "claimable"
                    for item in resume_traction_proof.get("claimable_now", [])
                ):
                    raise AssertionError("resume traction proof current launch/quality signals must be claimable")
                if not all(
                    item.get("status") == "not_claimable_yet"
                    for item in resume_traction_proof.get("future_claims", [])
                ):
                    raise AssertionError("resume traction proof must keep zero outcome claims blocked")
                blocked = " ".join(resume_traction_proof.get("blocked_claims", [])).lower()
                for required in ("active users", "customer feedback", "production adoption", "github traffic views"):
                    if required not in blocked:
                        raise AssertionError(f"resume traction proof must block {required}")
                if "verify_resume_traction_proof" not in traction_proof_script:
                    raise AssertionError("resume traction proof must include a script verifier")
                if "test_resume_traction_proof_separates_claimable_launch_from_unproven_growth" not in traction_proof_tests:
                    raise AssertionError("resume traction proof must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("resume_traction_proof claim must use metric_value=1")
            elif metric_name == "reviewer_action_queue":
                queue_script = (ROOT / "scripts" / "build_reviewer_action_queue.py").read_text()
                queue_tests = (ROOT / "tests" / "test_reviewer_action_queue.py").read_text()
                expected = {
                    "queue_count": 8,
                    "not_contacted_count": 8,
                    "evidence_goal_count": 5,
                }
                for key, value in expected.items():
                    if reviewer_action_queue.get(key) != value:
                        raise AssertionError(f"reviewer action queue {key} expected {value!r}")
                if reviewer_action_queue.get("status_counts", {}).get("completed") != 0:
                    raise AssertionError("reviewer action queue must not claim completed reviews")
                if reviewer_action_queue.get("status_counts", {}).get("contacted") != 0:
                    raise AssertionError("reviewer action queue must not claim contacted reviewers")
                if reviewer_action_queue.get("resume_status") != "outreach_queue_ready_not_claimable":
                    raise AssertionError("reviewer action queue must keep resume status not claimable")
                required_goals = {
                    "external_feedback_items",
                    "confirmed_external_users",
                    "reproducible_feedback_items",
                    "business_case_feedback_items",
                    "ai_engineer_review_items",
                }
                if set(reviewer_action_queue.get("evidence_goals", [])) != required_goals:
                    raise AssertionError("reviewer action queue must cover all tracked public evidence goals")
                for task in reviewer_action_queue.get("tasks", []):
                    if task.get("status") != "not_contacted":
                        raise AssertionError("reviewer action queue tasks must remain not-contacted until evidence exists")
                    if "github.com/sunnnn2005/data-quality-agent" not in task.get("submission_url", ""):
                        raise AssertionError("reviewer action queue tasks must submit to public GitHub evidence")
                    if "raw customer data" not in task.get("privacy_boundary", "").lower():
                        raise AssertionError("reviewer action queue tasks must include sensitive-data boundaries")
                    if "permission" not in task.get("permission_to_count", "").lower():
                        raise AssertionError("reviewer action queue tasks must require permission to count")
                for blocked in ("active users", "customer feedback", "enterprise production usage"):
                    if blocked not in reviewer_action_queue.get("blocked_resume_claims", []):
                        raise AssertionError(f"reviewer action queue must block {blocked}")
                if "verify_reviewer_action_queue" not in queue_script:
                    raise AssertionError("reviewer action queue must include a script verifier")
                if "test_reviewer_action_queue_turns_traction_goal_into_countable_public_tasks" not in queue_tests:
                    raise AssertionError("reviewer action queue must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("reviewer_action_queue claim must use metric_value=1")
            elif metric_name == "reviewer_outreach_execution_pack":
                outreach_script = (ROOT / "scripts" / "build_reviewer_outreach_execution_pack.py").read_text()
                outreach_tests = (ROOT / "tests" / "test_reviewer_outreach_execution_pack.py").read_text()
                expected = {
                    "outreach_item_count": 8,
                    "ready_message_count": 8,
                    "follow_up_rule_count": 8,
                    "evidence_goal_count": 5,
                }
                for key, value in expected.items():
                    if reviewer_outreach_execution.get(key) != value:
                        raise AssertionError(f"reviewer outreach execution pack {key} expected {value!r}")
                statuses = reviewer_outreach_execution.get("send_status_counts", {})
                if statuses.get("not_sent") != 8:
                    raise AssertionError("reviewer outreach execution pack must preserve 8 not-sent entries")
                if statuses.get("sent") != 0:
                    raise AssertionError("reviewer outreach execution pack must not claim sent outreach")
                if statuses.get("completed") != 0:
                    raise AssertionError("reviewer outreach execution pack must not claim completed outreach")
                if reviewer_outreach_execution.get("resume_status") != "ready_to_send_not_claimable":
                    raise AssertionError("reviewer outreach execution pack must keep resume status not claimable")
                required_goals = {
                    "external_feedback_items",
                    "confirmed_external_users",
                    "reproducible_feedback_items",
                    "business_case_feedback_items",
                    "ai_engineer_review_items",
                }
                if set(reviewer_outreach_execution.get("evidence_goals", [])) != required_goals:
                    raise AssertionError("reviewer outreach execution pack must cover all tracked evidence goals")
                for item in reviewer_outreach_execution.get("outreach_items", []):
                    if item.get("send_status") != "not_sent":
                        raise AssertionError("reviewer outreach items must remain not-sent until manually sent")
                    message = item.get("ready_to_send_message", "")
                    if "{name}" not in message:
                        raise AssertionError("reviewer outreach messages must keep manual personalization placeholder")
                    if "permission" not in message.lower():
                        raise AssertionError("reviewer outreach messages must request permission to count")
                    if "raw customer data" not in message.lower():
                        raise AssertionError("reviewer outreach messages must include private-data boundaries")
                    if "github.com/sunnnn2005/data-quality-agent" not in item.get("submission_url", ""):
                        raise AssertionError("reviewer outreach submissions must point to public GitHub evidence")
                    if item.get("follow_up", {}).get("after_days") != 4:
                        raise AssertionError("reviewer outreach follow-up delay must be deterministic")
                    if "public GitHub issue passes the evidence gate" not in item.get("status_update_rule", ""):
                        raise AssertionError("reviewer outreach completion must depend on public evidence gate")
                rules = " ".join(reviewer_outreach_execution.get("manual_execution_rules", []))
                for required in ("Do not mark a message as sent", "Do not count private replies"):
                    if required not in rules:
                        raise AssertionError(f"reviewer outreach manual rules must include: {required}")
                if "verify_reviewer_outreach_execution_pack" not in outreach_script:
                    raise AssertionError("reviewer outreach execution pack must include a script verifier")
                if (
                    "test_reviewer_outreach_execution_pack_makes_queue_sendable_without_claiming_results"
                    not in outreach_tests
                ):
                    raise AssertionError("reviewer outreach execution pack must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("reviewer_outreach_execution_pack claim must use metric_value=1")
            elif metric_name == "reviewer_outreach_status_board":
                status_script = (ROOT / "scripts" / "build_reviewer_outreach_status_board.py").read_text()
                status_tests = (ROOT / "tests" / "test_reviewer_outreach_status_board.py").read_text()
                expected = {
                    "source_outreach_item_count": 8,
                    "source_share_channel_count": 5,
                    "status_stage_count": 5,
                    "outreach_slot_count": 8,
                    "not_sent_count": 8,
                    "sent_count": 0,
                    "reply_count": 0,
                    "accepted_evidence_count": 0,
                    "resume_upgrade_count": 0,
                }
                for key, value in expected.items():
                    if reviewer_outreach_status.get(key) != value:
                        raise AssertionError(f"reviewer outreach status board {key} expected {value!r}")
                if reviewer_outreach_status.get("resume_status") != "tracking_ready_not_claimable":
                    raise AssertionError("reviewer outreach status board must keep resume status not claimable")
                for value in reviewer_outreach_status.get("current_outcome_counts", {}).values():
                    if value != 0:
                        raise AssertionError("reviewer outreach status board must preserve zero outcome counts")
                for slot in reviewer_outreach_status.get("outreach_slots", []):
                    if slot.get("status") != "not_sent":
                        raise AssertionError("reviewer outreach status board slots must start as not_sent")
                    if slot.get("sent_at") is not None:
                        raise AssertionError("reviewer outreach status board must not fabricate sent timestamps")
                    if slot.get("reply_received") is not False:
                        raise AssertionError("reviewer outreach status board must not fabricate replies")
                    if slot.get("public_evidence_url") is not None:
                        raise AssertionError("reviewer outreach status board must not fabricate public evidence")
                    if slot.get("accepted_by_gate") is not False:
                        raise AssertionError("reviewer outreach status board must not fabricate accepted evidence")
                joined = json.dumps(reviewer_outreach_status, sort_keys=True).lower()
                for required in (
                    "non-owner public github issue",
                    "permission",
                    "self-authored",
                    "private replies",
                    "evidence gate",
                ):
                    if required not in joined:
                        raise AssertionError(f"reviewer outreach status board missing boundary: {required}")
                if "verify_reviewer_outreach_status_board" not in status_script:
                    raise AssertionError("reviewer outreach status board must include a script verifier")
                if "test_reviewer_outreach_status_board_tracks_slots_without_claiming_results" not in status_tests:
                    raise AssertionError("reviewer outreach status board must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("reviewer_outreach_status_board claim must use metric_value=1")
            elif metric_name == "resume_claim_upgrade_ledger":
                claim_script = (ROOT / "scripts" / "build_resume_claim_upgrade_ledger.py").read_text()
                claim_tests = (ROOT / "tests" / "test_resume_claim_upgrade_ledger.py").read_text()
                expected = {
                    "upgrade_row_count": 6,
                    "claimable_row_count": 0,
                    "blocked_row_count": 6,
                }
                for key, value in expected.items():
                    if claim_upgrade.get(key) != value:
                        raise AssertionError(f"resume claim upgrade ledger {key} expected {value!r}")
                for key, value in claim_upgrade.get("current_counts", {}).items():
                    if value != 0:
                        raise AssertionError(f"resume claim upgrade ledger must keep {key} at zero before evidence exists")
                upgrade_metrics = {row.get("metric") for row in claim_upgrade.get("upgrade_rows", [])}
                required_metrics = {
                    "confirmed_external_users",
                    "external_feedback_items",
                    "reproducible_feedback_items",
                    "business_case_feedback_items",
                    "ai_engineer_review_items",
                    "github_stars",
                }
                if upgrade_metrics != required_metrics:
                    raise AssertionError("resume claim upgrade ledger must track all resume outcome metrics")
                if not all(
                    row.get("status") == "blocked_until_public_evidence"
                    for row in claim_upgrade.get("upgrade_rows", [])
                ):
                    raise AssertionError("resume claim upgrade ledger must block all rows before public evidence exists")
                joined = json.dumps(claim_upgrade, sort_keys=True).lower()
                for required in ("permission", "public evidence", "evidence gate", "exact future resume wording"):
                    if required not in joined:
                        raise AssertionError(f"resume claim upgrade ledger missing boundary: {required}")
                if "verify_resume_claim_upgrade_ledger" not in claim_script:
                    raise AssertionError("resume claim upgrade ledger must include a script verifier")
                if "test_resume_claim_upgrade_ledger_blocks_unproven_outcome_claims" not in claim_tests:
                    raise AssertionError("resume claim upgrade ledger must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("resume_claim_upgrade_ledger claim must use metric_value=1")
            elif metric_name == "resume_outcome_metrics":
                outcome_metrics_script = (ROOT / "scripts" / "build_resume_outcome_metrics.py").read_text()
                outcome_metrics_tests = (ROOT / "tests" / "test_resume_outcome_metrics.py").read_text()
                expected = {
                    "tracked_outcome_count": 6,
                    "claimable_outcome_count": 0,
                    "blocked_outcome_count": 6,
                }
                for key, value in expected.items():
                    if resume_outcome_metrics.get(key) != value:
                        raise AssertionError(f"resume outcome metrics {key} expected {value!r}")
                required_metrics = {
                    "confirmed_external_users",
                    "external_feedback_items",
                    "reproducible_feedback_items",
                    "business_case_feedback_items",
                    "ai_engineer_review_items",
                    "github_stars",
                }
                outcomes = {item.get("metric"): item for item in resume_outcome_metrics.get("tracked_outcomes", [])}
                if set(outcomes) != required_metrics:
                    raise AssertionError("resume outcome metrics must track all outcome categories")
                for metric in required_metrics:
                    item = outcomes[metric]
                    if item.get("current_count") != 0:
                        raise AssertionError(f"resume outcome metrics must keep {metric} at zero until evidence exists")
                    if item.get("resume_status") != "not_claimable_yet":
                        raise AssertionError(f"resume outcome metrics must block {metric} at zero")
                    if not item.get("blocked_reason"):
                        raise AssertionError(f"resume outcome metrics must explain why {metric} is blocked")
                if resume_outcome_metrics.get("outreach_readiness", {}).get("ready_message_count") != 8:
                    raise AssertionError("resume outcome metrics must link 8 ready reviewer messages")
                if resume_outcome_metrics.get("outreach_readiness", {}).get("not_sent_count") != 8:
                    raise AssertionError("resume outcome metrics must preserve the zero-sent baseline")
                for required in (
                    "No external users are claimed while confirmed_external_users is zero.",
                    "No customer feedback is claimed while external_feedback_items is zero.",
                    "No real business impact is claimed while business_case_feedback_items is zero.",
                    "No GitHub star growth is claimed while github_stars is zero.",
                    "GitHub traffic is treated as repository interest, not as users.",
                ):
                    if required not in resume_outcome_metrics.get("not_claimed", []):
                        raise AssertionError(f"resume outcome metrics must preserve not-claimed signal: {required}")
                if "verify_resume_outcome_metrics" not in outcome_metrics_script:
                    raise AssertionError("resume outcome metrics must include a script verifier")
                if "test_resume_outcome_metrics_blocks_unproven_outcome_claims" not in outcome_metrics_tests:
                    raise AssertionError("resume outcome metrics must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("resume_outcome_metrics claim must use metric_value=1")
            elif metric_name == "resume_outcome_action_checklist":
                checklist_script = (ROOT / "scripts" / "build_resume_outcome_action_checklist.py").read_text()
                checklist_tests = (ROOT / "tests" / "test_resume_outcome_action_checklist.py").read_text()
                expected = {
                    "tracked_action_count": 5,
                    "next_action_needed_count": 5,
                    "claimable_action_count": 0,
                    "accepted_public_issue_count": 0,
                    "outreach_slot_count": 8,
                    "not_sent_outreach_count": 8,
                }
                for key, value in expected.items():
                    if resume_outcome_action_checklist.get(key) != value:
                        raise AssertionError(f"resume outcome action checklist {key} expected {value!r}")
                required_actions = {
                    "send_first_reviewer_request",
                    "collect_first_public_run_issue",
                    "collect_ai_engineer_review",
                    "collect_business_case",
                    "earn_first_star",
                }
                actions = {item.get("id"): item for item in resume_outcome_action_checklist.get("actions", [])}
                if set(actions) != required_actions:
                    raise AssertionError("resume outcome action checklist must track all next outcome actions")
                for action in actions.values():
                    if action.get("status") != "next_action_needed":
                        raise AssertionError(f"resume outcome action {action.get('id')} must still need proof")
                    if not action.get("completion_check"):
                        raise AssertionError(f"resume outcome action {action.get('id')} must include completion check")
                if "verify_resume_outcome_action_checklist" not in checklist_script:
                    raise AssertionError("resume outcome action checklist must include a script verifier")
                if "test_resume_outcome_action_checklist_turns_blocked_outcomes_into_next_actions" not in checklist_tests:
                    raise AssertionError("resume outcome action checklist must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("resume_outcome_action_checklist claim must use metric_value=1")
            elif metric_name == "reviewer_submission_hub":
                hub_script = (ROOT / "scripts" / "build_reviewer_submission_hub.py").read_text()
                hub_tests = (ROOT / "tests" / "test_reviewer_submission_hub.py").read_text()
                expected = {
                    "submission_path_count": 6,
                    "target_metric_count": 6,
                    "total_required_evidence_fields": 23,
                }
                for key, value in expected.items():
                    if reviewer_submission_hub.get(key) != value:
                        raise AssertionError(f"reviewer submission hub {key} expected {value!r}")
                if reviewer_submission_hub.get("resume_status") != "collection_ready_not_claimable":
                    raise AssertionError("reviewer submission hub must not be claimable by itself")
                required_metrics = {
                    "confirmed_external_users",
                    "external_feedback_items",
                    "reproducible_feedback_items",
                    "business_case_feedback_items",
                    "ai_engineer_review_items",
                    "github_stars",
                }
                actual_metrics = {path.get("target_metric") for path in reviewer_submission_hub.get("submission_paths", [])}
                if actual_metrics != required_metrics:
                    raise AssertionError("reviewer submission hub must map every outcome metric to a submission path")
                for path in reviewer_submission_hub.get("submission_paths", []):
                    if not path.get("submission_url", "").startswith("https://github.com/"):
                        raise AssertionError("reviewer submission hub submissions must use public GitHub URLs")
                    if "Counts only" not in path.get("counting_rule", ""):
                        raise AssertionError("reviewer submission hub must preserve conservative counting rules")
                for status in reviewer_submission_hub.get("tracked_outcome_status", {}).values():
                    if status.get("current_count") != 0 or status.get("resume_status") != "not_claimable_yet":
                        raise AssertionError("reviewer submission hub must preserve zero-count blocked outcomes")
                joined = json.dumps(reviewer_submission_hub, sort_keys=True).lower()
                for required in ("permission", "evidence gate", "no raw production data", "never asks for fake engagement"):
                    if required not in joined:
                        raise AssertionError(f"reviewer submission hub missing safety signal: {required}")
                if "verify_reviewer_submission_hub" not in hub_script:
                    raise AssertionError("reviewer submission hub must include a script verifier")
                if "test_reviewer_submission_hub_maps_every_outcome_to_public_evidence_path" not in hub_tests:
                    raise AssertionError("reviewer submission hub must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("reviewer_submission_hub claim must use metric_value=1")
            elif metric_name == "outcome_collection_page":
                outcome_script = (ROOT / "scripts" / "build_outcome_collection_page.py").read_text()
                outcome_tests = (ROOT / "tests" / "test_outcome_collection_page.py").read_text()
                expected = {
                    "project": "Data Quality Agent",
                    "tracked_action_count": 5,
                    "submission_path_count": 6,
                    "required_evidence_field_count": 23,
                }
                for key, value in expected.items():
                    if outcome_collection.get(key) != value:
                        raise AssertionError(f"outcome collection {key} expected {value!r}")
                counts = outcome_collection.get("current_counts", {})
                for key, expected_value in (
                    ("confirmed_external_users", 0),
                    ("external_feedback_items", 0),
                    ("github_stars", 0),
                    ("passing_tests", 149),
                ):
                    if counts.get(key) != expected_value:
                        raise AssertionError(f"outcome collection {key} expected {expected_value!r}")
                if len(outcome_collection.get("actions", [])) != 5:
                    raise AssertionError("outcome collection must include 5 action cards")
                if len(outcome_collection.get("submission_paths", [])) != 6:
                    raise AssertionError("outcome collection must include 6 submission paths")
                joined = json.dumps(outcome_collection, sort_keys=True).lower()
                for required in ("permission", "public", "raw customer data", "github stars"):
                    if required not in joined:
                        raise AssertionError(f"outcome collection missing boundary: {required}")
                if "verify_outcome_collection_payload" not in outcome_script:
                    raise AssertionError("outcome collection page must include a script verifier")
                if "test_outcome_collection_page_routes_reviewers_to_countable_evidence" not in outcome_tests:
                    raise AssertionError("outcome collection page must include a dedicated test")
                if "OUTPUT_JSON_PATH" not in outcome_script or "OUTPUT_HTML_PATH" not in outcome_script:
                    raise AssertionError("outcome collection must generate both JSON and HTML artifacts")
                if claim.get("metric_value") != 1:
                    raise AssertionError("outcome_collection_page claim must use metric_value=1")
            elif metric_name == "public_reviewer_call":
                call_script = (ROOT / "scripts" / "build_public_reviewer_call.py").read_text()
                call_tests = (ROOT / "tests" / "test_public_reviewer_call.py").read_text()
                expected = {
                    "reviewer_segment_count": 3,
                    "linked_submission_paths": 6,
                    "linked_outreach_tasks": 8,
                    "required_public_evidence_fields": 23,
                }
                for key, value in expected.items():
                    if public_reviewer_call.get(key) != value:
                        raise AssertionError(f"public reviewer call {key} expected {value!r}")
                if public_reviewer_call.get("resume_status") != "public_call_open_not_claimable":
                    raise AssertionError("public reviewer call must not be claimable by itself")
                if public_reviewer_call.get("public_call_issue") != "https://github.com/sunnnn2005/data-quality-agent/issues/19":
                    raise AssertionError("public reviewer call must link issue #19")
                expected_segments = {"technical_reviewer", "business_data_reviewer", "quick_demo_reviewer"}
                actual_segments = {segment.get("id") for segment in public_reviewer_call.get("reviewer_segments", [])}
                if actual_segments != expected_segments:
                    raise AssertionError("public reviewer call must define the expected reviewer segments")
                for value in public_reviewer_call.get("current_counts", {}).values():
                    if value != 0:
                        raise AssertionError("public reviewer call must preserve zero current outcome counts")
                joined = json.dumps(public_reviewer_call, sort_keys=True).lower()
                for required in (
                    "non-owner github evidence",
                    "does not count private dms",
                    "fake github engagement",
                    "blocked while counts are zero",
                ):
                    if required not in joined:
                        raise AssertionError(f"public reviewer call missing boundary: {required}")
                if "verify_public_reviewer_call" not in call_script:
                    raise AssertionError("public reviewer call must include a script verifier")
                if "test_public_reviewer_call_opens_real_evidence_collection_without_claiming_outcomes" not in call_tests:
                    raise AssertionError("public reviewer call must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("public_reviewer_call claim must use metric_value=1")
            elif metric_name == "reviewer_share_kit":
                kit_script = (ROOT / "scripts" / "build_reviewer_share_kit.py").read_text()
                kit_tests = (ROOT / "tests" / "test_reviewer_share_kit.py").read_text()
                expected = {
                    "share_channel_count": 5,
                    "ready_message_count": 5,
                    "linked_submission_paths": 6,
                    "linked_public_call_segments": 3,
                    "required_evidence_fields": 23,
                    "outreach_tasks_linked": 8,
                }
                for key, value in expected.items():
                    if reviewer_share_kit.get(key) != value:
                        raise AssertionError(f"reviewer share kit {key} expected {value!r}")
                if reviewer_share_kit.get("public_call_issue") != "https://github.com/sunnnn2005/data-quality-agent/issues/19":
                    raise AssertionError("reviewer share kit must link issue #19")
                if reviewer_share_kit.get("send_status_counts") != {"not_sent": 5, "sent": 0, "completed": 0}:
                    raise AssertionError("reviewer share kit must not claim sent or completed outreach")
                if reviewer_share_kit.get("resume_status") != "share_ready_not_claimable":
                    raise AssertionError("reviewer share kit must not upgrade outcome claims")
                for value in reviewer_share_kit.get("current_counts", {}).values():
                    if value != 0:
                        raise AssertionError("reviewer share kit must preserve zero current outcome counts")
                joined = json.dumps(reviewer_share_kit, sort_keys=True).lower()
                for required in ("permission", "private data", "does not count private replies", "self-authored", "fake github engagement", "not_sent"):
                    if required not in joined:
                        raise AssertionError(f"reviewer share kit missing boundary: {required}")
                if "verify_reviewer_share_kit" not in kit_script:
                    raise AssertionError("reviewer share kit must include a script verifier")
                if "test_reviewer_share_kit_packages_public_call_without_claiming_outcomes" not in kit_tests:
                    raise AssertionError("reviewer share kit must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("reviewer_share_kit claim must use metric_value=1")
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
                if application_pack.get("verified_outcome_numbers", {}).get("passing_tests") != 149:
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
            elif metric_name == "github_discovery_profile":
                discovery_script = (ROOT / "scripts" / "build_github_discovery_profile.py").read_text()
                discovery_tests = (ROOT / "tests" / "test_github_discovery_profile.py").read_text()
                if github_discovery.get("topic_count") != 16:
                    raise AssertionError("GitHub discovery profile must verify 16 precise topics")
                if len(github_discovery.get("reviewer_entrypoints", [])) != 6:
                    raise AssertionError("GitHub discovery profile must verify 6 reviewer entrypoints")
                if github_discovery.get("discovery_ready") is not True:
                    raise AssertionError("GitHub discovery profile must be discovery-ready")
                counts = github_discovery.get("current_public_counts", {})
                if counts.get("stars") != 0 or counts.get("adoption_metric_stars") != 0:
                    raise AssertionError("GitHub discovery profile must preserve the zero-star baseline")
                for required in ("external users", "customer feedback", "GitHub stars beyond the current public count"):
                    if required not in github_discovery.get("not_claimed", []):
                        raise AssertionError(f"GitHub discovery profile must not claim {required}")
                if "verify_github_discovery_profile" not in discovery_script:
                    raise AssertionError("GitHub discovery profile must include a script verifier")
                if "test_github_discovery_profile_verifies_public_discovery_without_claiming_traction" not in discovery_tests:
                    raise AssertionError("GitHub discovery profile must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("github_discovery_profile claim must use metric_value=1")
            elif metric_name == "pilot_evidence_quicklink":
                quicklink_script = (ROOT / "scripts" / "build_pilot_evidence_quicklink.py").read_text()
                quicklink_tests = (ROOT / "tests" / "test_pilot_evidence_quicklink.py").read_text()
                if pilot_evidence_quicklink.get("action_count") != 3:
                    raise AssertionError("pilot evidence quicklink must verify 3 short evidence actions")
                if pilot_evidence_quicklink.get("total_evidence_fields") != 12:
                    raise AssertionError("pilot evidence quicklink must verify 12 evidence fields")
                if pilot_evidence_quicklink.get("target_metric_count") != 3:
                    raise AssertionError("pilot evidence quicklink must verify 3 target metrics")
                counts = pilot_evidence_quicklink.get("current_counts", {})
                for key in ("external_feedback_items", "confirmed_external_users", "business_case_feedback_items"):
                    if counts.get(key) != 0:
                        raise AssertionError(f"pilot evidence quicklink must preserve zero baseline for {key}")
                for required in ("external users", "customer feedback", "submitted external business cases"):
                    if required not in pilot_evidence_quicklink.get("not_claimed", []):
                        raise AssertionError(f"pilot evidence quicklink must not claim {required}")
                if "verify_pilot_evidence_quicklink" not in quicklink_script:
                    raise AssertionError("pilot evidence quicklink must include a script verifier")
                if "test_pilot_evidence_quicklink_routes_reviewers_to_real_countable_outcomes" not in quicklink_tests:
                    raise AssertionError("pilot evidence quicklink must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("pilot_evidence_quicklink claim must use metric_value=1")
            elif metric_name == "pilot_launch_control_room":
                control_room_script = (ROOT / "scripts" / "build_pilot_launch_control_room.py").read_text()
                control_room_tests = (ROOT / "tests" / "test_pilot_launch_control_room.py").read_text()
                if pilot_launch_control_room.get("public_issue_thread_count") != 4:
                    raise AssertionError("pilot launch control room must verify 4 public issue threads")
                if pilot_launch_control_room.get("launch_gate_count") != 5:
                    raise AssertionError("pilot launch control room must verify 5 launch gates")
                if pilot_launch_control_room.get("target_outcome_count") != 4:
                    raise AssertionError("pilot launch control room must verify 4 target outcome metrics")
                if pilot_launch_control_room.get("reviewer_send_plan_count") != 3:
                    raise AssertionError("pilot launch control room must verify 3 reviewer-send paths")
                if pilot_launch_control_room.get("current_claimable_external_outcomes") != 0:
                    raise AssertionError("pilot launch control room must keep external outcomes unclaimed")
                for required in ("external users", "customer feedback", "business validation"):
                    if required not in pilot_launch_control_room.get("not_claimed", []):
                        raise AssertionError(f"pilot launch control room must not claim {required}")
                if "verify_pilot_launch_control_room" not in control_room_script:
                    raise AssertionError("pilot launch control room must include a script verifier")
                if "test_pilot_launch_control_room_tracks_real_outcome_path_without_claiming_it" not in control_room_tests:
                    raise AssertionError("pilot launch control room must include a dedicated test")
                if claim.get("metric_value") != 1:
                    raise AssertionError("pilot_launch_control_room claim must use metric_value=1")
            elif metric_name == "pilot_outreach_message_count":
                pilot_tests = (ROOT / "tests" / "test_pilot_outreach_kit.py").read_text()
                pilot_script = (ROOT / "scripts" / "build_pilot_outreach_kit.py").read_text()
                if len(pilot_outreach.get("outreach_messages", [])) != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: pilot_outreach_message_count="
                        f"{claim.get('metric_value')} but pilot outreach kit has "
                        f"{len(pilot_outreach.get('outreach_messages', []))}"
                    )
                if len(pilot_outreach.get("review_paths", {})) != 10:
                    raise AssertionError("pilot outreach kit must include ten review paths")
                if not pilot_outreach.get("review_paths", {}).get("public_review_request", "").endswith("/issues/17"):
                    raise AssertionError("pilot outreach kit must link the public review request issue")
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
            elif metric_name == "pilot_conversion_board":
                conversion_tests = (ROOT / "tests" / "test_pilot_conversion_board.py").read_text()
                conversion_script = (ROOT / "scripts" / "build_pilot_conversion_board.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("pilot conversion board claim must use metric_value=1")
                if pilot_conversion.get("stage_count") != 6:
                    raise AssertionError("pilot conversion board must define six stages")
                if pilot_conversion.get("claimable_stage_count") != 2:
                    raise AssertionError("pilot conversion board must define two claimable readiness stages")
                if pilot_conversion.get("blocked_stage_count") != 4:
                    raise AssertionError("pilot conversion board must block four outcome claims")
                blocked_claims = pilot_conversion.get("blocked_resume_claims", [])
                if len(blocked_claims) != 4:
                    raise AssertionError("pilot conversion board must list four blocked outcome claims")
                blocked_stages = {item.get("stage") for item in blocked_claims}
                for required in {
                    "confirmed_external_feedback",
                    "confirmed_external_users",
                    "business_case_validated",
                    "reproducible_replay_confirmed",
                }:
                    if required not in blocked_stages:
                        raise AssertionError(f"pilot conversion board missing blocked stage {required}")
                not_claimed = " ".join(pilot_conversion.get("not_claimed", [])).lower()
                for required in ("external users", "customer feedback", "validated business impact", "production adoption"):
                    if required not in not_claimed:
                        raise AssertionError(f"pilot conversion board must not claim {required}")
                if "verify_pilot_conversion_board" not in conversion_script:
                    raise AssertionError("pilot conversion board script must verify generated board")
                if "test_pilot_conversion_board_separates_readiness_from_outcome_claims" not in conversion_tests:
                    raise AssertionError("pilot conversion board must have a dedicated test")
            elif metric_name == "resume_outcome_readiness":
                readiness_tests = (ROOT / "tests" / "test_resume_outcome_readiness.py").read_text()
                readiness_script = (ROOT / "scripts" / "evaluate_resume_outcomes.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("resume outcome readiness claim must use metric_value=1")
                if resume_outcome_readiness.get("stage_count") != 6:
                    raise AssertionError("resume outcome readiness must evaluate six stages")
                if resume_outcome_readiness.get("claimable_stage_count") != 2:
                    raise AssertionError("resume outcome readiness must keep two claimable readiness stages")
                if resume_outcome_readiness.get("blocked_stage_count") != 4:
                    raise AssertionError("resume outcome readiness must block four stronger outcome stages")
                if len(resume_outcome_readiness.get("missing_evidence", [])) != 4:
                    raise AssertionError("resume outcome readiness must list four missing-evidence items")
                current_counts = resume_outcome_readiness.get("current_public_counts", {})
                expected_counts = {
                    "external_feedback_items": 0,
                    "confirmed_external_users": 0,
                    "business_case_feedback_items": 0,
                    "reproducible_feedback_items": 0,
                }
                for key, expected in expected_counts.items():
                    if current_counts.get(key) != expected:
                        raise AssertionError(f"resume outcome readiness {key} expected {expected!r}")
                missing = {item.get("stage"): item for item in resume_outcome_readiness.get("missing_evidence", [])}
                expected_remaining = {
                    "confirmed_external_feedback": 3,
                    "confirmed_external_users": 1,
                    "business_case_validated": 1,
                    "reproducible_replay_confirmed": 2,
                }
                for stage, remaining in expected_remaining.items():
                    if missing.get(stage, {}).get("remaining_needed") != remaining:
                        raise AssertionError(f"resume outcome readiness {stage} remaining_needed expected {remaining}")
                if "verify_resume_outcome_readiness" not in readiness_script:
                    raise AssertionError("resume outcome readiness script must verify generated payload")
                if "test_resume_outcome_readiness_blocks_unverified_outcome_claims" not in readiness_tests:
                    raise AssertionError("resume outcome readiness must have a dedicated test")
            elif metric_name == "external_review_evidence_ledger":
                ledger_tests = (ROOT / "tests" / "test_external_review_evidence_ledger.py").read_text()
                ledger_script = (ROOT / "scripts" / "build_external_review_evidence_ledger.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("external review evidence ledger claim must use metric_value=1")
                if external_ledger.get("entry_count") != 0:
                    raise AssertionError("external review evidence ledger must start with zero entries")
                if external_ledger.get("evidence_requirement_count") != 5:
                    raise AssertionError("external review evidence ledger must define five evidence types")
                if external_ledger.get("linked_planned_reviews") != 3:
                    raise AssertionError("external review evidence ledger must link three planned reviews")
                if external_ledger.get("resume_status") != "not_claimable_yet":
                    raise AssertionError("external review evidence ledger must not be claimable before proof")
                evidence_types = {item.get("evidence_type") for item in external_ledger.get("evidence_requirements", [])}
                for required in {"demo_feedback", "confirmed_run", "business_case_review", "reproducible_bug", "ai_engineer_review"}:
                    if required not in evidence_types:
                        raise AssertionError(f"external review evidence ledger missing {required}")
                public_counts = external_ledger.get("public_counts", {})
                expected_counts = {
                    "external_feedback_items": 0,
                    "confirmed_external_users": 0,
                    "reproducible_feedback_items": 0,
                    "business_case_feedback_items": 0,
                    "ai_engineer_review_items": 0,
                }
                for key, expected in expected_counts.items():
                    if public_counts.get(key) != expected:
                        raise AssertionError(f"external review evidence ledger {key} expected {expected!r}")
                if "verify_external_review_evidence_ledger" not in ledger_script:
                    raise AssertionError("external review evidence ledger script must verify generated ledger")
                if (
                    "test_external_review_evidence_ledger_defines_public_proof_before_resume_claims"
                    not in ledger_tests
                ):
                    raise AssertionError("external review evidence ledger must have a dedicated test")
            elif metric_name == "outcome_upgrade_playbook":
                upgrade_tests = (ROOT / "tests" / "test_outcome_upgrade_playbook.py").read_text()
                upgrade_script = (ROOT / "scripts" / "build_outcome_upgrade_playbook.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("outcome upgrade playbook claim must use metric_value=1")
                if outcome_upgrade.get("upgrade_rule_count") != 5:
                    raise AssertionError("outcome upgrade playbook must define five upgrade rules")
                if outcome_upgrade.get("blocked_upgrade_rule_count") != 5:
                    raise AssertionError("outcome upgrade playbook must keep all outcome upgrades blocked")
                if outcome_upgrade.get("resume_status") != "baseline_only":
                    raise AssertionError("outcome upgrade playbook must preserve baseline-only resume wording")
                current_counts = outcome_upgrade.get("current_public_counts", {})
                expected_counts = {
                    "stars": 0,
                    "forks": 1,
                    "external_feedback_items": 0,
                    "confirmed_external_users": 0,
                    "reproducible_feedback_items": 0,
                    "business_case_feedback_items": 0,
                }
                for key, expected in expected_counts.items():
                    if current_counts.get(key) != expected:
                        raise AssertionError(f"outcome upgrade playbook {key} expected {expected!r}")
                if any(rule.get("status") != "not_claimable_yet" for rule in outcome_upgrade.get("upgrade_rules", [])):
                    raise AssertionError("outcome upgrade playbook must not mark any upgrade rule as claimable")
                if len(outcome_upgrade.get("claimable_now", [])) != 6:
                    raise AssertionError("outcome upgrade playbook must keep six baseline signals claimable now")
                if "verify_outcome_upgrade_playbook" not in upgrade_script:
                    raise AssertionError("outcome upgrade playbook script must verify generated playbook")
                if (
                    "test_outcome_upgrade_playbook_blocks_resume_outcome_claims_until_public_evidence_exists"
                    not in upgrade_tests
                ):
                    raise AssertionError("outcome upgrade playbook must have a dedicated test")
            elif metric_name == "reviewer_feedback_packet":
                packet_tests = (ROOT / "tests" / "test_reviewer_feedback_packet.py").read_text()
                packet_script = (ROOT / "scripts" / "build_reviewer_feedback_packet.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("reviewer feedback packet claim must use metric_value=1")
                expected = {
                    "reviewer_task_count": 4,
                    "evidence_question_count": 6,
                    "conversion_path_count": 5,
                    "planned_review_slots": 3,
                }
                for key, value in expected.items():
                    if reviewer_packet.get(key) != value:
                        raise AssertionError(f"reviewer feedback packet {key} expected {value!r}")
                counts = reviewer_packet.get("current_public_counts", {})
                for key in (
                    "external_feedback_items",
                    "confirmed_external_users",
                    "reproducible_feedback_items",
                    "business_case_feedback_items",
                    "ai_engineer_review_items",
                ):
                    if counts.get(key) != 0:
                        raise AssertionError(f"reviewer feedback packet must preserve zero {key}")
                if reviewer_packet.get("resume_status") != "collection_ready_not_claimable":
                    raise AssertionError("reviewer feedback packet must not be claimable as feedback yet")
                if "verify_reviewer_feedback_packet" not in packet_script:
                    raise AssertionError("reviewer feedback packet script must verify generated packet")
                if (
                    "test_reviewer_feedback_packet_turns_review_requests_into_metric_aware_public_evidence"
                    not in packet_tests
                ):
                    raise AssertionError("reviewer feedback packet must have a dedicated test")
            elif metric_name == "reviewer_funnel_board":
                funnel_tests = (ROOT / "tests" / "test_reviewer_funnel_board.py").read_text()
                funnel_script = (ROOT / "scripts" / "build_reviewer_funnel_board.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("reviewer funnel board claim must use metric_value=1")
                expected = {
                    "funnel_stage_count": 4,
                    "open_gap_count": 4,
                    "total_remaining_evidence_items": 7,
                    "resume_outcome_blocked_stages": 4,
                    "resume_outcome_claimable_stages": 2,
                }
                for key, value in expected.items():
                    if reviewer_funnel.get(key) != value:
                        raise AssertionError(f"reviewer funnel board {key} expected {value!r}")
                required_metrics = {
                    "external_feedback_items",
                    "reproducible_feedback_items",
                    "confirmed_external_users",
                    "business_case_feedback_items",
                }
                actual_metrics = {stage.get("counts_toward") for stage in reviewer_funnel.get("funnel_stages", [])}
                if actual_metrics != required_metrics:
                    raise AssertionError("reviewer funnel board must cover every public evidence metric")
                if reviewer_funnel.get("resume_status") != "evidence_collection_ready":
                    raise AssertionError("reviewer funnel board must stay in evidence collection status")
                if "verify_reviewer_funnel_board" not in funnel_script:
                    raise AssertionError("reviewer funnel board script must verify generated board")
                if (
                    "test_reviewer_funnel_board_maps_review_activity_to_resume_evidence_gaps"
                    not in funnel_tests
                ):
                    raise AssertionError("reviewer funnel board must have a dedicated test")
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
                    "required_section_count": 8,
                    "required_context_field_count": 3,
                    "required_impact_field_count": 4,
                    "required_project_evidence_field_count": 4,
                    "required_try_path_count": 5,
                    "required_outcome_count": 8,
                    "captured_field_count": 8,
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
                    "Approximate time spent investigating manually:",
                    "Which finding matched the real problem?",
                    "This can be counted as an anonymized business-impact signal.",
                    "Do not quote my organization, name, or raw data.",
                ):
                    if required not in template_text:
                        raise AssertionError(f"business case template missing required prompt: {required}")
                outcome_fields = business_case_intake.get("resume_outcome_fields", [])
                if len(outcome_fields) != 9:
                    raise AssertionError("business case intake must expose 9 resume outcome fields")
                if "manual investigation time" not in outcome_fields:
                    raise AssertionError("business case intake must collect manual investigation time")
                if "verify_business_case_intake" not in case_script:
                    raise AssertionError("business case intake script must verify generated artifact")
                if (
                    "test_business_case_intake_collects_real_problem_context_without_claiming_cases"
                    not in case_tests
                ):
                    raise AssertionError("business case intake must have a dedicated test")
            elif metric_name == "business_data_replay_packet":
                replay_tests = (ROOT / "tests" / "test_business_data_replay_packet.py").read_text()
                replay_script = (ROOT / "scripts" / "build_business_data_replay_packet.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("business data replay packet claim must use metric_value=1")
                expected = {
                    "replay_path_count": 3,
                    "evidence_field_count": 8,
                    "safety_requirement_count": 5,
                }
                for key, value in expected.items():
                    if replay_packet.get(key) != value:
                        raise AssertionError(f"business data replay packet {key} expected {value}")
                boundaries = replay_packet.get("verified_input_boundaries", {})
                expected_boundaries = {
                    "business_data_endpoint_verified": True,
                    "postgres_agent_endpoint_verified": True,
                    "max_rows": 10_000,
                    "max_columns": 80,
                    "csv_only": True,
                    "primary_key_required": True,
                }
                for key, value in expected_boundaries.items():
                    if boundaries.get(key) != value:
                        raise AssertionError(f"business data replay boundary {key} expected {value}")
                counts = replay_packet.get("current_public_counts", {})
                for key in (
                    "external_feedback_items",
                    "confirmed_external_users",
                    "business_case_feedback_items",
                    "reproducible_feedback_items",
                ):
                    if counts.get(key) != 0:
                        raise AssertionError(f"business data replay packet must preserve zero {key}")
                if replay_packet.get("resume_status") != "replay_ready_not_claimable":
                    raise AssertionError("business data replay packet must not be claimable before public evidence")
                for required in (
                    "external replay completed",
                    "real company data analyzed",
                    "enterprise production usage",
                ):
                    if required not in replay_packet.get("not_claimed", []):
                        raise AssertionError(f"business data replay packet must not claim {required}")
                if "verify_business_data_replay_packet" not in replay_script:
                    raise AssertionError("business data replay packet script must verify generated artifact")
                if (
                    "test_business_data_replay_packet_turns_realistic_data_runs_into_public_evidence"
                    not in replay_tests
                ):
                    raise AssertionError("business data replay packet must have a dedicated test")
            elif metric_name == "business_replay_demo":
                demo_tests = (ROOT / "tests" / "test_business_replay_demo.py").read_text()
                demo_script = (ROOT / "scripts" / "build_business_replay_demo.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("business replay demo claim must use metric_value=1")
                dataset = replay_demo.get("dataset", {})
                summary = replay_demo.get("quality_report_summary", {})
                expected = {
                    "row_count": 8,
                    "column_count": 6,
                    "finding_count": 5,
                    "check_count": 4,
                    "business_rule_reference_count": 4,
                    "root_cause_hypothesis_count": 3,
                    "recommended_action_count": 5,
                }
                for key, value in expected.items():
                    source = dataset if key in dataset else summary
                    if source.get(key) != value:
                        raise AssertionError(f"business replay demo {key} expected {value}")
                if summary.get("status") != "FAIL" or summary.get("quality_score") != 24:
                    raise AssertionError("business replay demo must verify expected failing report")
                if summary.get("verification_passed") is not True:
                    raise AssertionError("business replay demo must pass deterministic report verification")
                if dataset.get("contains_real_company_data") is not False or dataset.get("contains_pii") is not False:
                    raise AssertionError("business replay demo must preserve anonymized-data boundaries")
                for required in ("real company data", "external user replay", "customer feedback"):
                    if required not in replay_demo.get("not_claimed", []):
                        raise AssertionError(f"business replay demo must not claim {required}")
                if "verify_business_replay_demo" not in demo_script:
                    raise AssertionError("business replay demo script must verify generated artifact")
                if (
                    "test_business_replay_demo_verifies_anonymized_csv_without_claiming_external_usage"
                    not in demo_tests
                ):
                    raise AssertionError("business replay demo must have a dedicated test")
            elif metric_name == "real_model_runbook":
                runbook_tests = (ROOT / "tests" / "test_real_model_runbook.py").read_text()
                runbook_script = (ROOT / "scripts" / "build_real_model_runbook.py").read_text()
                capture_script = (ROOT / "scripts" / "capture_real_model_run.py").read_text()
                capture_tests = (ROOT / "tests" / "test_capture_real_model_run.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("real model runbook claim must use metric_value=1")
                expected = {
                    "current_real_model_runs": 0,
                    "run_command_count": 5,
                    "evidence_field_count": 15,
                    "acceptance_criteria_count": 8,
                    "safety_gate_count": 5,
                    "tool_count": 7,
                }
                for key, value in expected.items():
                    if real_model_runbook.get(key) != value:
                        raise AssertionError(f"real model runbook {key} expected {value}")
                if real_model_runbook.get("prompt_version") != "tool-agent-v3":
                    raise AssertionError("real model runbook must pin the current prompt version")
                if real_model_runbook.get("resume_status") != "real_model_run_ready_not_claimable":
                    raise AssertionError("real model runbook must not claim a completed real model run")
                routes = set(real_model_runbook.get("openapi_agent_routes", []))
                for required in {"/business-data/agent-report", "/datasets/{dataset_id}/agent-report"}:
                    if required not in routes:
                        raise AssertionError(f"real model runbook missing route {required}")
                for required in (
                    "real OpenAI model run completed",
                    "paid model benchmark results",
                    "production model traffic",
                ):
                    if required not in real_model_runbook.get("not_claimed", []):
                        raise AssertionError(f"real model runbook must not claim {required}")
                if "verify_real_model_runbook" not in runbook_script:
                    raise AssertionError("real model runbook script must verify generated artifact")
                if "capture_real_model_run.py --dataset-id orders_daily --write" not in runbook_script:
                    raise AssertionError("real model runbook must document the capture command")
                if "capture_real_model_run" not in capture_script or "build_capture_record" not in capture_script:
                    raise AssertionError("real model runbook must have a capture CLI")
                if "test_capture_real_model_run_calls_agent_and_trace_endpoints_then_verifies_gate" not in capture_tests:
                    raise AssertionError("real model capture CLI must have a dedicated endpoint test")
                if (
                    "test_real_model_runbook_defines_resume_safe_evidence_gate_without_claiming_paid_run"
                    not in runbook_tests
                ):
                    raise AssertionError("real model runbook must have a dedicated test")
            elif metric_name == "real_model_evidence_capture":
                capture_tests = (ROOT / "tests" / "test_real_model_evidence_capture.py").read_text()
                capture_script = (ROOT / "scripts" / "build_real_model_evidence_capture.py").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("real model evidence capture claim must use metric_value=1")
                expected = {
                    "current_real_model_runs": 0,
                    "runbook_evidence_field_count": 15,
                    "capture_required_field_count": 17,
                    "accepted_real_model_run_count": 0,
                    "blocked_outcome_claim_count": 4,
                }
                for key, value in expected.items():
                    if real_model_evidence_capture.get(key) != value:
                        raise AssertionError(f"real model evidence capture {key} expected {value}")
                for required in ("trace_id", "provider", "model", "tool_call_count", "total_tokens", "raw_prompt_logged"):
                    if required not in real_model_evidence_capture.get("capture_required_fields", []):
                        raise AssertionError(f"real model evidence capture missing {required}")
                for required in (
                    "real OpenAI model run completed",
                    "paid model benchmark results",
                    "production model traffic",
                ):
                    if required not in real_model_evidence_capture.get("not_claimed", []):
                        raise AssertionError(f"real model evidence capture must not claim {required}")
                if "verify_real_model_evidence_capture" not in capture_script:
                    raise AssertionError("real model evidence capture script must verify generated artifact")
                if "test_real_model_evidence_capture_preserves_zero_run_baseline" not in capture_tests:
                    raise AssertionError("real model evidence capture must have a zero-run test")
                if "test_real_model_evidence_capture_accepts_redacted_tool_calling_run" not in capture_tests:
                    raise AssertionError("real model evidence capture must have an accepted-run test")
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
                    "issues_total": 14,
                    "external_feedback_items": 0,
                    "confirmed_external_users": 0,
                }
                for key, expected in expected_counts.items():
                    if counts.get(key) != expected:
                        raise AssertionError(f"star growth kit {key} expected {expected!r}")
                topics = star_growth.get("topic_readiness", {})
                if topics.get("ready") is not True:
                    raise AssertionError("star growth kit must verify topic readiness")
                if len(topics.get("required_topics", [])) != 16:
                    raise AssertionError("star growth kit must verify 16 required topics")
                if len(star_growth.get("ethical_growth_actions", [])) != 4:
                    raise AssertionError("star growth kit must verify 4 ethical growth actions")
                rules = star_growth.get("resume_upgrade_rules", [])
                if len(rules) != 4:
                    raise AssertionError("star growth kit must verify 4 resume upgrade rules")
                if "repository interest" not in {rule.get("signal") for rule in rules}:
                    raise AssertionError("star growth kit must include repository interest upgrade rule")
                traffic_snapshot = star_growth.get("traffic_snapshot", {})
                if traffic_snapshot.get("source") != "GitHub traffic API rolling 14-day window":
                    raise AssertionError("star growth kit must link GitHub traffic snapshot")
                if "confirmed users" not in traffic_snapshot.get("resume_policy", ""):
                    raise AssertionError("star growth kit must separate traffic from confirmed users")
                if not all(rule.get("resume_status") == "not_claimable_yet" for rule in rules):
                    raise AssertionError("star growth kit must keep growth signals not claimable before evidence")
                if "fake or incentivized stars" not in star_growth.get("not_claimed", []):
                    raise AssertionError("star growth kit must explicitly reject fake or incentivized stars")
                if "confirmed users from traffic alone" not in star_growth.get("not_claimed", []):
                    raise AssertionError("star growth kit must not convert traffic into user claims")
                if "verify_star_growth_kit" not in star_script:
                    raise AssertionError("star growth kit must include a script verifier")
                if "test_star_growth_kit_tracks_ethical_growth_without_inflating_stars" not in star_tests:
                    raise AssertionError("star growth kit must include a dedicated test")
            elif metric_name == "external_run_quickstart_page":
                quickstart_script = (ROOT / "scripts" / "build_external_run_quickstart_page.py").read_text()
                quickstart_tests = (ROOT / "tests" / "test_external_run_quickstart_page.py").read_text()
                quickstart_html = (ROOT / "docs" / "external-run-quickstart.html").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("external_run_quickstart_page claim must use metric_value=1")
                if external_run_quickstart.get("review_path_count") != 3:
                    raise AssertionError("external run quickstart must verify 3 run paths")
                if external_run_quickstart.get("submission_field_count") != 8:
                    raise AssertionError("external run quickstart must verify 8 evidence fields")
                if external_run_quickstart.get("upgrade_rule_count") != 3:
                    raise AssertionError("external run quickstart must verify 3 upgrade rules")
                if not external_run_quickstart.get("collection_issue", "").endswith("/issues/18"):
                    raise AssertionError("external run quickstart must link issue #18")
                if not external_run_quickstart.get("review_template", "").endswith(
                    "template=external_run_review.md"
                ):
                    raise AssertionError("external run quickstart must link the external run review template")
                if external_run_quickstart.get("current_counts", {}).get("confirmed_external_users") != 0:
                    raise AssertionError("external run quickstart must preserve zero-user baseline")
                for required in (
                    "Open External Run Review",
                    "Comment on Issue #18",
                    "permission_to_count_publicly",
                    "No private business data",
                    "No external reviewer run is claimed yet.",
                ):
                    if required not in quickstart_html:
                        raise AssertionError(f"external run quickstart page missing {required!r}")
                if "verify_external_run_quickstart_payload" not in quickstart_script:
                    raise AssertionError("external run quickstart script must include a verifier")
                if "test_external_run_quickstart_routes_reviewers_to_countable_public_evidence" not in quickstart_tests:
                    raise AssertionError("external run quickstart must have a dedicated test")
            elif metric_name == "external_reviewer_outreach_tracker":
                outreach_script = (ROOT / "scripts" / "build_external_reviewer_outreach_tracker.py").read_text()
                outreach_tests = (ROOT / "tests" / "test_external_reviewer_outreach_tracker.py").read_text()
                outreach_page = (ROOT / "docs" / "external-reviewer-outreach-tracker.md").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("external_reviewer_outreach_tracker claim must use metric_value=1")
                if external_reviewer_outreach.get("queue_count") != 3:
                    raise AssertionError("external reviewer outreach tracker must verify 3 queue entries")
                if external_reviewer_outreach.get("source_message_count") != 3:
                    raise AssertionError("external reviewer outreach tracker must verify 3 source messages")
                if external_reviewer_outreach.get("quickstart_review_path_count") != 3:
                    raise AssertionError("external reviewer outreach tracker must link 3 quickstart paths")
                if external_reviewer_outreach.get("quickstart_submission_field_count") != 8:
                    raise AssertionError("external reviewer outreach tracker must link 8 evidence fields")
                if external_reviewer_outreach.get("status_counts", {}).get("not_contacted") != 3:
                    raise AssertionError("external reviewer outreach tracker must preserve 3 not-contacted entries")
                if external_reviewer_outreach.get("status_counts", {}).get("contacted") != 0:
                    raise AssertionError("external reviewer outreach tracker must not count unsent outreach")
                if external_reviewer_outreach.get("public_counts", {}).get("external_feedback_items") != 0:
                    raise AssertionError("external reviewer outreach tracker must preserve zero feedback baseline")
                for required in (
                    "A sent message does not count as feedback.",
                    "No outreach message has been sent yet.",
                    "No contacted reviewer is claimed yet.",
                ):
                    if required not in outreach_page:
                        raise AssertionError(f"external reviewer outreach tracker page missing {required!r}")
                if "verify_external_reviewer_outreach_tracker" not in outreach_script:
                    raise AssertionError("external reviewer outreach tracker script must include a verifier")
                if (
                    "test_external_reviewer_outreach_tracker_prepares_countable_review_requests_without_inflation"
                    not in outreach_tests
                ):
                    raise AssertionError("external reviewer outreach tracker must have a dedicated test")
            elif metric_name == "external_reviewer_evidence_gate":
                gate_script = (ROOT / "scripts" / "build_external_reviewer_evidence_gate.py").read_text()
                gate_tests = (ROOT / "tests" / "test_external_reviewer_evidence_gate.py").read_text()
                gate_page = (ROOT / "docs" / "external-reviewer-evidence-gate.md").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("external_reviewer_evidence_gate claim must use metric_value=1")
                if external_reviewer_gate.get("linked_outreach_queue_count") != 3:
                    raise AssertionError("external reviewer evidence gate must link 3 outreach queue entries")
                if external_reviewer_gate.get("accepted_issue_count") != 0:
                    raise AssertionError("external reviewer evidence gate must preserve zero accepted issue baseline")
                if len(external_reviewer_gate.get("gate_rules", [])) != 7:
                    raise AssertionError("external reviewer evidence gate must document 7 validation rules")
                if external_reviewer_gate.get("issue_collection", {}).get("source") != "github_issues":
                    raise AssertionError("external reviewer evidence gate must collect public GitHub issues by default")
                for key in (
                    "external_feedback_items",
                    "confirmed_external_users",
                    "reproducible_feedback_items",
                    "business_case_feedback_items",
                    "ai_engineer_review_items",
                ):
                    if external_reviewer_gate.get("accepted_counts", {}).get(key) != 0:
                        raise AssertionError(f"external reviewer evidence gate must preserve zero {key}")
                for required in (
                    "Self-authored issues do not count as external evidence.",
                    "Reviewer must grant explicit permission before a run or feedback is counted.",
                    "Issues containing sensitive-data risk terms are rejected until redacted.",
                    "The default artifact collects tracked public GitHub issues before applying the evidence gate.",
                ):
                    if required not in external_reviewer_gate.get("gate_rules", []):
                        raise AssertionError(f"external reviewer evidence gate missing rule: {required}")
                    if required not in gate_page:
                        raise AssertionError(f"external reviewer evidence gate page missing {required!r}")
                if "verify_external_reviewer_evidence_gate" not in gate_script:
                    raise AssertionError("external reviewer evidence gate script must include a verifier")
                if "test_external_reviewer_evidence_gate_accepts_complete_public_run_issue" not in gate_tests:
                    raise AssertionError("external reviewer evidence gate must have a complete-run acceptance test")
                if "test_external_reviewer_evidence_gate_rejects_self_authored_missing_permission_or_sensitive_issue" not in gate_tests:
                    raise AssertionError("external reviewer evidence gate must have rejection tests")
            elif metric_name == "accepted_evidence_rollup":
                rollup_script = (ROOT / "scripts" / "build_accepted_evidence_rollup.py").read_text()
                rollup_tests = (ROOT / "tests" / "test_accepted_evidence_rollup.py").read_text()
                rollup_page = (ROOT / "docs" / "accepted-evidence-rollup.md").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("accepted_evidence_rollup claim must use metric_value=1")
                if accepted_evidence_rollup.get("linked_outreach_queue_count") != 3:
                    raise AssertionError("accepted evidence rollup must link 3 outreach queue entries")
                if accepted_evidence_rollup.get("accepted_issue_count") != 0:
                    raise AssertionError("accepted evidence rollup must preserve zero accepted issue baseline")
                if accepted_evidence_rollup.get("claimable_metric_count") != 5:
                    raise AssertionError("accepted evidence rollup must track five claimable metrics")
                if accepted_evidence_rollup.get("blocked_outcome_claim_count") != 5:
                    raise AssertionError("accepted evidence rollup must block five outcome claims at baseline")
                for key in (
                    "external_feedback_items",
                    "confirmed_external_users",
                    "reproducible_feedback_items",
                    "business_case_feedback_items",
                ):
                    if accepted_evidence_rollup.get("accepted_counts", {}).get(key) != 0:
                        raise AssertionError(f"accepted evidence rollup must preserve zero {key}")
                for required in (
                    "No accepted external reviewer issue exists yet.",
                    "No private business data is used as outcome evidence.",
                ):
                    if required not in accepted_evidence_rollup.get("not_claimed", []):
                        raise AssertionError(f"accepted evidence rollup missing not-claimed signal: {required}")
                    if required not in rollup_page:
                        raise AssertionError(f"accepted evidence rollup page missing {required!r}")
                if "verify_accepted_evidence_rollup" not in rollup_script:
                    raise AssertionError("accepted evidence rollup script must include a verifier")
                if "test_accepted_evidence_rollup_preserves_zero_outcome_baseline" not in rollup_tests:
                    raise AssertionError("accepted evidence rollup must have a baseline test")
                if "test_accepted_evidence_rollup_turns_valid_gate_counts_into_claimable_metrics" not in rollup_tests:
                    raise AssertionError("accepted evidence rollup must have a positive-count test")
            elif metric_name == "business_impact_ledger":
                ledger_script = (ROOT / "scripts" / "build_business_impact_ledger.py").read_text()
                ledger_tests = (ROOT / "tests" / "test_business_impact_ledger.py").read_text()
                ledger_page = (ROOT / "docs" / "business-impact-ledger.md").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("business impact ledger claim must use metric_value=1")
                if business_impact_ledger.get("accepted_business_impact_signal_count") != 0:
                    raise AssertionError("business impact ledger must preserve zero accepted business-impact baseline")
                if business_impact_ledger.get("resume_upgrade_rule", {}).get("resume_status") != "not_claimable_yet":
                    raise AssertionError("business impact ledger must not be claimable before accepted evidence")
                for required in (
                    "validated business impact",
                    "raw production data",
                    "revenue saved",
                    "production adoption",
                ):
                    if required not in business_impact_ledger.get("not_claimed", []):
                        raise AssertionError(f"business impact ledger missing not-claimed signal: {required}")
                for required in ("Business Impact Ledger", "Accepted business-impact signals | 0"):
                    if required not in ledger_page:
                        raise AssertionError(f"business impact ledger page missing {required!r}")
                if "verify_business_impact_ledger" not in ledger_script:
                    raise AssertionError("business impact ledger script must include a verifier")
                if "test_business_impact_ledger_preserves_zero_baseline_without_fake_business_claims" not in ledger_tests:
                    raise AssertionError("business impact ledger must have a zero-baseline test")
                if "test_business_impact_ledger_extracts_claimable_accepted_business_case" not in ledger_tests:
                    raise AssertionError("business impact ledger must have a positive accepted-case test")
            elif metric_name == "reviewer_evidence_kit":
                kit_script = (ROOT / "scripts" / "build_reviewer_evidence_kit.py").read_text()
                kit_tests = (ROOT / "tests" / "test_reviewer_evidence_kit.py").read_text()
                kit_page = (ROOT / "docs" / "reviewer-evidence-kit.md").read_text()
                if claim.get("metric_value") != 1:
                    raise AssertionError("reviewer evidence kit claim must use metric_value=1")
                if reviewer_evidence_kit.get("evidence_form_count") != 5:
                    raise AssertionError("reviewer evidence kit must verify five evidence forms")
                if reviewer_evidence_kit.get("reviewer_script_step_count") != 5:
                    raise AssertionError("reviewer evidence kit must verify five script steps")
                if reviewer_evidence_kit.get("resume_status") != "collection_ready_not_claimable":
                    raise AssertionError("reviewer evidence kit must not claim external outcomes yet")
                for key in (
                    "confirmed_external_users",
                    "external_feedback_items",
                    "business_case_feedback_items",
                    "ai_engineer_review_items",
                    "reproducible_feedback_items",
                    "accepted_business_impact_signals",
                ):
                    if reviewer_evidence_kit.get("current_counts", {}).get(key) != 0:
                        raise AssertionError(f"reviewer evidence kit must preserve zero {key}")
                for required in ("Reviewer Evidence Kit", "Public Evidence Forms", "Current Counts"):
                    if required not in kit_page:
                        raise AssertionError(f"reviewer evidence kit page missing {required!r}")
                for required in ("verify_reviewer_evidence_kit", "permission", "private data", "evidence gate"):
                    if required not in kit_script:
                        raise AssertionError(f"reviewer evidence kit script missing {required!r}")
                if "test_reviewer_evidence_kit_gives_countable_public_submission_paths" not in kit_tests:
                    raise AssertionError("reviewer evidence kit must have a dedicated test")
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

    if "public-metrics-refresh" in claim_ids:
        workflow_text = PUBLIC_METRICS_REFRESH_WORKFLOW_PATH.read_text()
        for required in (
            "schedule:",
            "workflow_dispatch:",
            "contents: write",
            "issues: read",
            "scripts/update_feedback_metrics.py",
            "scripts/update_adoption_metrics.py",
            "scripts/build_github_traffic_snapshot.py",
            "scripts/build_star_growth_kit.py",
            "scripts/build_public_metrics_summary.py",
            "scripts/build_reviewer_outreach_execution_pack.py",
            "scripts/build_resume_outcome_metrics.py",
            "scripts/build_resume_outcome_action_checklist.py",
            "scripts/build_reviewer_submission_hub.py",
            "scripts/build_outcome_collection_page.py",
            "scripts/build_public_reviewer_call.py",
            "scripts/build_reviewer_share_kit.py",
            "scripts/build_reviewer_outreach_status_board.py",
            "scripts/verify_outcome_evidence.py",
            "git-auto-commit-action",
        ):
            if required not in workflow_text:
                raise AssertionError(f"public metrics refresh workflow missing {required}")

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
        for phrase in ("passing ci tests | 149", "confirmed external users | 0", "forks | 1"):
            if phrase not in metrics_page:
                raise AssertionError(f"public metrics summary page missing phrase: {phrase}")

    if "community-growth-baseline" in claim_ids:
        if "8 issue templates" not in resume_page or "9 public contribution or feedback channels" not in resume_page:
            raise AssertionError("resume evidence page must reflect the current community growth counts")

    if "public-traction-dashboard" in claim_ids:
        if "19 growth or review channels" not in resume_page:
            raise AssertionError("resume evidence page must reflect the current public traction channel count")

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
