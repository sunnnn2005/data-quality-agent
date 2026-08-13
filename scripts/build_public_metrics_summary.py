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
LIVE_SCORECARD_PATH = ROOT / "docs" / "live-project-scorecard.json"
OPENAPI_PATH = ROOT / "docs" / "openapi.json"
RECRUITER_PITCH_PATH = ROOT / "docs" / "recruiter-pitch.json"
APPLICATION_EVIDENCE_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
PILOT_OUTREACH_KIT_PATH = ROOT / "docs" / "pilot-outreach-kit.json"
PILOT_PROGRAM_PLAN_PATH = ROOT / "docs" / "pilot-program-plan.json"
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
    scorecard = load_json(LIVE_SCORECARD_PATH)
    openapi = load_json(OPENAPI_PATH)
    recruiter_pitch = load_json(RECRUITER_PITCH_PATH)
    application_pack = load_json(APPLICATION_EVIDENCE_PACK_PATH)
    pilot_outreach = load_json(PILOT_OUTREACH_KIT_PATH)
    pilot_plan = load_json(PILOT_PROGRAM_PLAN_PATH)
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
            "eval_scenarios": eval_summary["scenario_count"],
            "hypothesis_feedback_labels": hypothesis_feedback["label_count"],
            "incident_pattern_count": incident_memory["incident_pattern_count"],
            "observed_trace_count": observability["observed_trace_count"],
            "fallback_event_count": observability["fallback_event_count"],
            "tool_allowlist_count": safety["tool_allowlist_count"],
            "postgres_rejected_write_query_count": safety["postgres_rejected_write_query_count"],
            "verifier_rule_count": safety["verifier_rule_count"],
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
            "Dataset-level memory retrieval over recent sanitized traces",
            f"{eval_summary['scenario_count']}-scenario agent evaluation harness",
            f"{hypothesis_feedback['label_count']} human-reviewed root-cause feedback labels",
            f"{incident_memory['incident_pattern_count']} recurring incident patterns retrieved from sanitized traces",
            f"{observability['observed_trace_count']} observed run traces with fallback and verification status",
            f"{safety['tool_allowlist_count']} allowed agent tools and {safety['postgres_rejected_write_query_count']} rejected unsafe PostgreSQL queries",
            f"{len(scorecard['reviewer_paths'])} reviewer paths in a CI-verified live project scorecard",
            "CI-verified OpenAPI contract covering 6 integration endpoints",
            f"{len(recruiter_pitch['resume_bullets'])} recruiter-safe resume bullets for {len(recruiter_pitch['target_roles'])} target roles",
            f"{len(application_pack['application_links'])} application evidence links in a recruiter-ready evidence pack",
            f"{len(pilot_outreach['outreach_messages'])} pilot outreach messages and {len(pilot_outreach['review_paths'])} review paths for collecting real feedback",
            f"{len(pilot_plan['participant_segments'])} pilot participant segments across a {len(pilot_plan['weekly_plan'])}-week feedback plan",
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
| Agent evaluation scenarios | {outcomes["eval_scenarios"]} |
| Root-cause feedback labels | {outcomes["hypothesis_feedback_labels"]} |
| Recurring incident patterns | {outcomes["incident_pattern_count"]} |
| Observed run traces | {outcomes["observed_trace_count"]} |
| Fallback events captured | {outcomes["fallback_event_count"]} |
| Allowed agent tools | {outcomes["tool_allowlist_count"]} |
| Rejected unsafe PostgreSQL queries | {outcomes["postgres_rejected_write_query_count"]} |
| Report verifier rules | {outcomes["verifier_rule_count"]} |
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
        "test_count": 71,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
    }
    for key, expected in expected_metrics.items():
        if metrics.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {metrics.get(key)!r}")
    expected_outcomes = {
        "support_ticket_issue_categories": 4,
        "root_cause_hypotheses": 3,
        "eval_scenarios": 3,
        "hypothesis_feedback_labels": 3,
        "incident_pattern_count": 3,
        "observed_trace_count": 2,
        "fallback_event_count": 2,
        "tool_allowlist_count": 5,
        "postgres_rejected_write_query_count": 3,
        "verifier_rule_count": 6,
        "live_project_scorecard": 1,
        "scorecard_reviewer_paths": 5,
        "openapi_required_endpoints": 6,
        "recruiter_pitch_resume_bullets": 3,
        "recruiter_pitch_target_roles": 4,
        "application_evidence_pack": 1,
        "application_evidence_links": 8,
        "pilot_outreach_messages": 3,
        "pilot_review_paths": 7,
        "pilot_program_segments": 3,
        "pilot_program_weeks": 3,
        "recommended_actions": 5,
        "implemented_agent_capabilities": 14,
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
