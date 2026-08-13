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
LOCAL_REVIEWER_DEMO_PATH = ROOT / "docs" / "local-reviewer-demo.json"
LIVE_SCORECARD_PATH = ROOT / "docs" / "live-project-scorecard.json"
OPENAPI_PATH = ROOT / "docs" / "openapi.json"
RECRUITER_PITCH_PATH = ROOT / "docs" / "recruiter-pitch.json"
APPLICATION_EVIDENCE_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
PILOT_OUTREACH_KIT_PATH = ROOT / "docs" / "pilot-outreach-kit.json"
PILOT_PROGRAM_PLAN_PATH = ROOT / "docs" / "pilot-program-plan.json"
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
    local_reviewer_demo = load_payload(LOCAL_REVIEWER_DEMO_PATH)
    scorecard = load_payload(LIVE_SCORECARD_PATH)
    openapi = load_payload(OPENAPI_PATH)
    recruiter_pitch = load_payload(RECRUITER_PITCH_PATH)
    application_pack = load_payload(APPLICATION_EVIDENCE_PACK_PATH)
    pilot_outreach = load_payload(PILOT_OUTREACH_KIT_PATH)
    pilot_plan = load_payload(PILOT_PROGRAM_PLAN_PATH)
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
            elif metric_name == "public_metrics_summary":
                if public_metrics_summary.get("public_metrics", {}).get("test_count") != 78:
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
                if application_pack.get("verified_outcome_numbers", {}).get("passing_tests") != 78:
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
                if len(pilot_outreach.get("review_paths", {})) != 7:
                    raise AssertionError("pilot outreach kit must include seven review paths")
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
        for phrase in ("passing ci tests | 78", "confirmed external users | 0", "forks | 1"):
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
