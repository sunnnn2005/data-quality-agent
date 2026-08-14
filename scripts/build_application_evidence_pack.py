import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCORECARD_PATH = ROOT / "docs" / "live-project-scorecard.json"
RECRUITER_PITCH_PATH = ROOT / "docs" / "recruiter-pitch.json"
PUBLIC_METRICS_PATH = ROOT / "docs" / "public-metrics-summary.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "application-evidence-pack.json"
OUTPUT_MD_PATH = ROOT / "docs" / "application-evidence-pack.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_application_evidence_pack_payload() -> dict[str, Any]:
    scorecard = load_json(SCORECARD_PATH)
    recruiter_pitch = load_json(RECRUITER_PITCH_PATH)
    public_metrics = load_json(PUBLIC_METRICS_PATH)
    headline = scorecard["headline_metrics"]
    footprint = scorecard["live_footprint"]
    outcomes = public_metrics["verified_project_outcomes"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_application_evidence_pack.py",
        "audience": ["recruiters", "hiring managers", "technical interviewers"],
        "target_roles": recruiter_pitch["target_roles"],
        "one_line_project_proof": (
            "Public, containerized LLM data-quality agent with CI-verified evidence artifacts, "
            f"{headline['passing_tests']} tests, {headline['verified_resume_claims']} verified resume claims, "
            "and honest adoption baselines."
        ),
        "application_links": {
            "demo": scorecard["public_demo"],
            "github_repo": scorecard["repo"],
            "container_image": f"https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent",
            "recruiter_pitch": f"{scorecard['repo']}/blob/main/docs/recruiter-pitch.md",
            "live_scorecard": f"{scorecard['repo']}/blob/main/docs/live-project-scorecard.md",
            "resume_evidence": f"{scorecard['repo']}/blob/main/docs/resume-evidence.md",
            "impact_review_packet": f"{scorecard['repo']}/blob/main/docs/impact-review-packet.md",
            "business_problem_casebook": f"{scorecard['repo']}/blob/main/docs/business-problem-casebook.md",
            "business_resolution_brief": f"{scorecard['repo']}/blob/main/docs/business-resolution-brief.md",
            "business_resolution_review_request": f"{scorecard['repo']}/blob/main/docs/business-resolution-review-request.md",
            "public_traction_dashboard": f"{scorecard['repo']}/blob/main/docs/public-traction-dashboard.md",
            "feedback_intake_quality": f"{scorecard['repo']}/blob/main/docs/feedback-intake-quality.md",
            "business_data_replay_packet": f"{scorecard['repo']}/blob/main/docs/business-data-replay-packet.md",
            "business_replay_demo": f"{scorecard['repo']}/blob/main/docs/business-replay-demo.md",
            "ai_engineer_readiness": f"{scorecard['repo']}/blob/main/docs/ai-engineer-readiness.md",
            "ai_engineer_review_intake": f"{scorecard['repo']}/blob/main/docs/ai-engineer-review-intake.md",
            "real_model_runbook": f"{scorecard['repo']}/blob/main/docs/real-model-runbook.md",
            "real_model_evidence_capture": f"{scorecard['repo']}/blob/main/docs/real-model-evidence-capture.md",
            "agent_capability_matrix": f"{scorecard['repo']}/blob/main/docs/agent-capability-matrix.md",
            "api_contract": f"{scorecard['repo']}/blob/main/docs/api-contract.md",
            "public_metrics": f"{scorecard['repo']}/blob/main/docs/public-metrics-summary.md",
            "resume_outcome_readiness": f"{scorecard['repo']}/blob/main/docs/resume-outcome-readiness.md",
            "reviewer_feedback_packet": f"{scorecard['repo']}/blob/main/docs/reviewer-feedback-packet.md",
            "reviewer_funnel_board": f"{scorecard['repo']}/blob/main/docs/reviewer-funnel-board.md",
            "external_run_evidence_packet": f"{scorecard['repo']}/blob/main/docs/external-run-evidence-packet.md",
            "external_run_quickstart": "https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html",
            "external_reviewer_outreach_tracker": f"{scorecard['repo']}/blob/main/docs/external-reviewer-outreach-tracker.md",
            "external_reviewer_evidence_gate": f"{scorecard['repo']}/blob/main/docs/external-reviewer-evidence-gate.md",
            "accepted_evidence_rollup": f"{scorecard['repo']}/blob/main/docs/accepted-evidence-rollup.md",
            "business_impact_ledger": f"{scorecard['repo']}/blob/main/docs/business-impact-ledger.md",
            "reviewer_evidence_kit": f"{scorecard['repo']}/blob/main/docs/reviewer-evidence-kit.md",
            "resume_traction_proof": f"{scorecard['repo']}/blob/main/docs/resume-traction-proof.md",
            "reviewer_action_queue": f"{scorecard['repo']}/blob/main/docs/reviewer-action-queue.md",
            "reviewer_outreach_execution_pack": f"{scorecard['repo']}/blob/main/docs/reviewer-outreach-execution-pack.md",
            "reviewer_outreach_status_board": f"{scorecard['repo']}/blob/main/docs/reviewer-outreach-status-board.md",
            "resume_outcome_metrics": f"{scorecard['repo']}/blob/main/docs/resume-outcome-metrics.md",
            "resume_outcome_action_checklist": f"{scorecard['repo']}/blob/main/docs/resume-outcome-action-checklist.md",
            "reviewer_submission_hub": f"{scorecard['repo']}/blob/main/docs/reviewer-submission-hub.md",
            "outcome_collection": "https://sunnnn2005.github.io/data-quality-agent/outcome-collection.html",
            "public_reviewer_call": f"{scorecard['repo']}/blob/main/docs/public-reviewer-call.md",
            "reviewer_share_kit": f"{scorecard['repo']}/blob/main/docs/reviewer-share-kit.md",
            "resume_claim_upgrade_ledger": f"{scorecard['repo']}/blob/main/docs/resume-claim-upgrade-ledger.md",
            "resume_outcome_scoreboard": f"{scorecard['repo']}/blob/main/docs/resume-outcome-scoreboard.md",
            "evidence_acceptance_checklist": f"{scorecard['repo']}/blob/main/docs/evidence-acceptance-checklist.md",
            "github_discovery_profile": f"{scorecard['repo']}/blob/main/docs/github-discovery-profile.md",
            "pilot_evidence_quicklink": "https://sunnnn2005.github.io/data-quality-agent/pilot-evidence-quicklink.html",
            "pilot_launch_control_room": f"{scorecard['repo']}/blob/main/docs/pilot-launch-control-room.md",
            "resume_outcome_adjudication": f"{scorecard['repo']}/blob/main/docs/resume-outcome-adjudication.md",
            "first_10_reviewer_sprint": f"{scorecard['repo']}/blob/main/docs/first-10-reviewer-sprint.md",
            "first_10_outreach_execution_log": f"{scorecard['repo']}/blob/main/docs/first-10-outreach-execution-log.md",
        },
        "verified_outcome_numbers": {
            "passing_tests": headline["passing_tests"],
            "verified_resume_claims": headline["verified_resume_claims"],
            "implemented_agent_capabilities": headline["implemented_agent_capabilities"],
            "agent_tools_allowed": headline["agent_tools_allowed"],
            "openapi_required_endpoints": headline["openapi_required_endpoints"],
            "support_ticket_issue_categories": headline["support_ticket_issue_categories"],
            "rejected_unsafe_postgres_queries": headline["unsafe_postgres_queries_rejected"],
            "impact_review_business_metrics": outcomes["impact_review_business_metrics"],
            "impact_review_evidence_links": outcomes["impact_review_evidence_links"],
            "business_problem_cases": outcomes["business_problem_cases"],
            "business_problem_detected_risks": outcomes["business_problem_detected_risks"],
            "business_resolution_findings": outcomes["business_resolution_findings"],
            "business_resolution_risk_areas": outcomes["business_resolution_risk_areas"],
            "business_resolution_high_priority_actions": outcomes["business_resolution_high_priority_actions"],
            "business_resolution_owner_handoffs": outcomes["business_resolution_owner_handoffs"],
            "business_resolution_review_request": outcomes["business_resolution_review_request"],
            "business_resolution_review_questions": outcomes["business_resolution_review_questions"],
            "business_resolution_review_external_feedback": outcomes["business_resolution_review_external_feedback"],
            "public_traction_surfaces": outcomes["public_traction_surfaces"],
            "public_traction_growth_channels": outcomes["public_traction_growth_channels"],
            "feedback_intake_required_sections": outcomes["feedback_intake_required_sections"],
            "feedback_intake_captured_fields": outcomes["feedback_intake_captured_fields"],
            "business_data_replay_paths": outcomes["business_data_replay_paths"],
            "business_data_replay_evidence_fields": outcomes["business_data_replay_evidence_fields"],
            "business_replay_demo_rows": outcomes["business_replay_demo_rows"],
            "business_replay_demo_findings": outcomes["business_replay_demo_findings"],
            "business_replay_demo_check_types": outcomes["business_replay_demo_check_types"],
            "resume_outcome_claimable_stages": outcomes["resume_outcome_claimable_stages"],
            "resume_outcome_blocked_stages": outcomes["resume_outcome_blocked_stages"],
            "resume_outcome_missing_evidence_items": outcomes["resume_outcome_missing_evidence_items"],
            "reviewer_funnel_stages": outcomes["reviewer_funnel_stages"],
            "reviewer_funnel_remaining_evidence_items": outcomes["reviewer_funnel_remaining_evidence_items"],
            "accepted_evidence_rollup_claimable_metrics": outcomes["accepted_evidence_rollup_claimable_metrics"],
            "accepted_evidence_rollup_blocked_claims": outcomes["accepted_evidence_rollup_blocked_claims"],
            "business_impact_ledger_accepted_signals": outcomes["business_impact_ledger_accepted_signals"],
            "reviewer_evidence_forms": outcomes["reviewer_evidence_forms"],
            "reviewer_evidence_script_steps": outcomes["reviewer_evidence_script_steps"],
            "resume_traction_claimable_now": outcomes["resume_traction_claimable_now"],
            "resume_traction_future_claims": outcomes["resume_traction_future_claims"],
            "resume_traction_blocked_claims": outcomes["resume_traction_blocked_claims"],
            "reviewer_action_tasks": outcomes["reviewer_action_tasks"],
            "reviewer_action_evidence_goals": outcomes["reviewer_action_evidence_goals"],
            "reviewer_action_not_contacted": outcomes["reviewer_action_not_contacted"],
            "reviewer_outreach_ready_messages": outcomes["reviewer_outreach_ready_messages"],
            "reviewer_outreach_follow_up_rules": outcomes["reviewer_outreach_follow_up_rules"],
            "reviewer_outreach_not_sent": outcomes["reviewer_outreach_not_sent"],
            "reviewer_outreach_status_slots": outcomes["reviewer_outreach_status_slots"],
            "reviewer_outreach_status_stages": outcomes["reviewer_outreach_status_stages"],
            "reviewer_outreach_status_accepted_evidence": outcomes["reviewer_outreach_status_accepted_evidence"],
            "resume_outcome_metrics_tracked": outcomes["resume_outcome_metrics_tracked"],
            "resume_outcome_metrics_claimable": outcomes["resume_outcome_metrics_claimable"],
            "resume_outcome_metrics_blocked": outcomes["resume_outcome_metrics_blocked"],
            "resume_outcome_action_count": outcomes["resume_outcome_action_count"],
            "resume_outcome_next_actions_needed": outcomes["resume_outcome_next_actions_needed"],
            "reviewer_submission_paths": outcomes["reviewer_submission_paths"],
            "reviewer_submission_required_fields": outcomes["reviewer_submission_required_fields"],
            "outcome_collection_actions": outcomes["outcome_collection_actions"],
            "outcome_collection_submission_paths": outcomes["outcome_collection_submission_paths"],
            "outcome_collection_evidence_fields": outcomes["outcome_collection_evidence_fields"],
            "public_reviewer_call_segments": outcomes["public_reviewer_call_segments"],
            "public_reviewer_call_outreach_tasks": outcomes["public_reviewer_call_outreach_tasks"],
            "public_reviewer_call_evidence_fields": outcomes["public_reviewer_call_evidence_fields"],
            "reviewer_share_channels": outcomes["reviewer_share_channels"],
            "reviewer_share_ready_messages": outcomes["reviewer_share_ready_messages"],
            "reviewer_share_linked_submission_paths": outcomes["reviewer_share_linked_submission_paths"],
            "reviewer_share_required_fields": outcomes["reviewer_share_required_fields"],
            "reviewer_share_not_sent": outcomes["reviewer_share_not_sent"],
            "resume_claim_upgrade_rows": outcomes["resume_claim_upgrade_rows"],
            "resume_claim_upgrade_blocked_rows": outcomes["resume_claim_upgrade_blocked_rows"],
            "resume_claim_upgrade_claimable_rows": outcomes["resume_claim_upgrade_claimable_rows"],
            "resume_outcome_scoreboard_claimable_now": outcomes["resume_outcome_scoreboard_claimable_now"],
            "resume_outcome_scoreboard_blocked": outcomes["resume_outcome_scoreboard_blocked"],
            "resume_outcome_scoreboard_remaining_evidence": outcomes["resume_outcome_scoreboard_remaining_evidence"],
            "evidence_acceptance_items": outcomes["evidence_acceptance_items"],
            "evidence_acceptance_accepted_issues": outcomes["evidence_acceptance_accepted_issues"],
            "evidence_acceptance_rejected_issues": outcomes["evidence_acceptance_rejected_issues"],
            "github_discovery_topics": outcomes["github_discovery_topics"],
            "github_discovery_reviewer_entrypoints": outcomes["github_discovery_reviewer_entrypoints"],
            "pilot_evidence_quicklink_actions": outcomes["pilot_evidence_quicklink_actions"],
            "pilot_evidence_quicklink_fields": outcomes["pilot_evidence_quicklink_fields"],
            "pilot_evidence_quicklink_target_metrics": outcomes["pilot_evidence_quicklink_target_metrics"],
            "pilot_launch_public_issue_threads": outcomes["pilot_launch_public_issue_threads"],
            "pilot_launch_gates": outcomes["pilot_launch_gates"],
            "pilot_launch_target_outcomes": outcomes["pilot_launch_target_outcomes"],
            "pilot_launch_reviewer_send_paths": outcomes["pilot_launch_reviewer_send_paths"],
            "resume_outcome_adjudication_categories": outcomes["resume_outcome_adjudication_categories"],
            "resume_outcome_adjudication_blocked_categories": outcomes["resume_outcome_adjudication_blocked_categories"],
            "resume_outcome_adjudication_claimable_categories": outcomes["resume_outcome_adjudication_claimable_categories"],
            "first_10_reviewer_slots": outcomes["first_10_reviewer_slots"],
            "first_10_reviewer_public_issue_entrypoints": outcomes["first_10_reviewer_public_issue_entrypoints"],
            "first_10_reviewer_target_metrics": outcomes["first_10_reviewer_target_metrics"],
            "first_10_reviewer_not_sent": outcomes["first_10_reviewer_not_sent"],
            "first_10_reviewer_completed": outcomes["first_10_reviewer_completed"],
            "first_10_outreach_messages": outcomes["first_10_outreach_messages"],
            "first_10_outreach_public_issue_entrypoints": outcomes["first_10_outreach_public_issue_entrypoints"],
            "first_10_outreach_not_sent": outcomes["first_10_outreach_not_sent"],
            "first_10_outreach_accepted_evidence": outcomes["first_10_outreach_accepted_evidence"],
            "real_model_run_commands": outcomes["real_model_run_commands"],
            "real_model_evidence_fields": outcomes["real_model_evidence_fields"],
            "real_model_capture_required_fields": outcomes["real_model_capture_required_fields"],
            "real_model_capture_accepted_runs": outcomes["real_model_capture_accepted_runs"],
            "real_model_capture_blocked_claims": outcomes["real_model_capture_blocked_claims"],
            "recruiter_safe_resume_bullets": outcomes["recruiter_pitch_resume_bullets"],
            "target_roles": outcomes["recruiter_pitch_target_roles"],
        },
        "resume_bullets": recruiter_pitch["resume_bullets"],
        "email_attachment_note": (
            "I included the project link because the repository has a public demo, runnable container, "
            "OpenAPI contract, CI-verified evidence page, and a generated scorecard that keeps adoption claims honest."
        ),
        "interview_opening": recruiter_pitch["thirty_second_pitch"],
        "evidence_review_order": [
            "Open the public demo to see the product-style result.",
            "Open the live scorecard for the current tests, claims, release, container, and adoption baseline.",
            "Open the recruiter pitch for resume bullets and interview framing.",
            "Open the AI Engineer readiness page, OpenAPI contract, and safety boundaries for implementation depth.",
            "Open public metrics to verify stars, forks, feedback, and not-claimed signals.",
        ],
        "honest_baseline": {
            "stars": footprint["stars"],
            "forks": footprint["forks"],
            "confirmed_external_users": footprint["confirmed_external_users"],
            "external_feedback_items": footprint["external_feedback_items"],
        },
        "not_claimed": scorecard["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    links = "\n".join(f"- {label.replace('_', ' ').title()}: [{url}]({url})" for label, url in payload["application_links"].items())
    numbers = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["verified_outcome_numbers"].items())
    bullets = "\n".join(f"- {item}" for item in payload["resume_bullets"])
    review_order = "\n".join(f"{index}. {item}" for index, item in enumerate(payload["evidence_review_order"], start=1))
    baseline = "\n".join(f"- `{key}`: {value}" for key, value in payload["honest_baseline"].items())
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    roles = ", ".join(payload["target_roles"])
    return f"""# Application Evidence Pack

This generated pack gives recruiters and interviewers a compact review path for {roles}.

## One-Line Project Proof

{payload["one_line_project_proof"]}

## Application Links

{links}

## Verified Outcome Numbers

| Metric | Value |
| --- | ---: |
{numbers}

## Resume Bullets

{bullets}

## Email Attachment Note

{payload["email_attachment_note"]}

## Interview Opening

{payload["interview_opening"]}

## Evidence Review Order

{review_order}

## Honest Baseline

{baseline}

## Not Claimed

{not_claimed}
"""


def verify_application_evidence_pack(payload: dict[str, Any]) -> dict[str, Any]:
    scorecard = load_json(SCORECARD_PATH)
    expected = {
        "application_link_count": 50,
        "resume_bullet_count": 3,
        "target_role_count": 4,
        "passing_tests": 250,
        "verified_resume_claims": scorecard["headline_metrics"]["verified_resume_claims"],
    }
    if len(payload["application_links"]) != expected["application_link_count"]:
        raise AssertionError("application evidence pack must include 50 application links")
    if len(payload["resume_bullets"]) != expected["resume_bullet_count"]:
        raise AssertionError("application evidence pack must include 3 resume bullets")
    if len(payload["target_roles"]) != expected["target_role_count"]:
        raise AssertionError("application evidence pack must include 4 target roles")
    numbers = payload["verified_outcome_numbers"]
    for key in ("passing_tests", "verified_resume_claims"):
        if numbers.get(key) != expected[key]:
            raise AssertionError(f"{key} expected {expected[key]!r}, got {numbers.get(key)!r}")
    for key, expected_value in {
        "business_resolution_findings": 5,
        "business_resolution_risk_areas": 4,
        "business_resolution_high_priority_actions": 3,
        "business_resolution_owner_handoffs": 4,
        "business_resolution_review_request": 1,
        "business_resolution_review_questions": 5,
        "business_resolution_review_external_feedback": 0,
    }.items():
        if numbers.get(key) != expected_value:
            raise AssertionError(f"{key} expected {expected_value!r}, got {numbers.get(key)!r}")
    if payload["honest_baseline"]["stars"] != 0:
        raise AssertionError("application evidence pack must preserve current star baseline")
    if payload["honest_baseline"]["confirmed_external_users"] != 0:
        raise AssertionError("application evidence pack must preserve current user baseline")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("production users", "customer traction", "earned github stars"):
        if forbidden in joined:
            raise AssertionError(f"application evidence pack must not claim {forbidden}")
    for required in ("external users", "customer feedback", "enterprise production usage"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"application evidence pack must not claim {required}")
    return {"application_evidence_pack_verified": True, **expected}


def main() -> None:
    payload = build_application_evidence_pack_payload()
    verify_application_evidence_pack(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
