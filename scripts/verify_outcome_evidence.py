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
OPENAPI_PATH = ROOT / "docs" / "openapi.json"
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
    openapi = load_payload(OPENAPI_PATH)
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
            elif metric_name == "public_metrics_summary":
                if public_metrics_summary.get("public_metrics", {}).get("test_count") != 65:
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
        for phrase in ("passing ci tests | 65", "confirmed external users | 0", "forks | 1"):
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
