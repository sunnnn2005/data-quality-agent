from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "refresh-public-metrics.yml"


def test_refresh_public_metrics_workflow_updates_resume_evidence_sources():
    payload = yaml.safe_load(WORKFLOW_PATH.read_text())

    assert payload["name"] == "Refresh Public Metrics"
    triggers = payload[True]
    assert "workflow_dispatch" in triggers
    assert "schedule" in triggers
    assert payload["permissions"]["contents"] == "write"
    assert payload["permissions"]["issues"] == "read"

    steps = payload["jobs"]["refresh-public-metrics"]["steps"]
    run_commands = "\n".join(step.get("run", "") for step in steps)
    uses = {step.get("uses", "") for step in steps}

    assert "python scripts/update_feedback_metrics.py" in run_commands
    assert "python scripts/update_adoption_metrics.py" in run_commands
    assert "python scripts/build_github_traffic_snapshot.py" in run_commands
    assert "python scripts/build_github_discovery_profile.py" in run_commands
    assert "python scripts/build_star_growth_kit.py" in run_commands
    assert "python scripts/build_public_metrics_provenance.py" in run_commands
    assert "python scripts/build_public_metrics_summary.py" in run_commands
    assert "python scripts/build_resume_traction_proof.py" in run_commands
    assert "python scripts/build_reviewer_action_queue.py" in run_commands
    assert "python scripts/build_reviewer_outreach_execution_pack.py" in run_commands
    assert "python scripts/build_resume_outcome_metrics.py" in run_commands
    assert "python scripts/build_resume_outcome_adjudication.py" in run_commands
    assert "python scripts/build_resume_outcome_action_checklist.py" in run_commands
    assert "python scripts/build_reviewer_submission_hub.py" in run_commands
    assert "python scripts/build_first_10_reviewer_sprint.py" in run_commands
    assert "python scripts/build_pilot_evidence_quicklink.py" in run_commands
    assert "python scripts/build_pilot_launch_control_room.py" in run_commands
    assert "python scripts/build_outcome_pipeline_board.py" in run_commands
    assert "python scripts/build_public_reviewer_call.py" in run_commands
    assert "python scripts/build_reviewer_share_kit.py" in run_commands
    assert "python scripts/build_reviewer_outreach_status_board.py" in run_commands
    assert "python scripts/build_outcome_collection_page.py" in run_commands
    assert "python scripts/build_resume_outcome_scoreboard.py" in run_commands
    assert "tests/test_resume_outcome_scoreboard.py" in run_commands
    assert "python scripts/build_reviewer_send_queue.py" in run_commands
    assert "tests/test_reviewer_send_queue.py" in run_commands
    assert "python scripts/build_first_reviewer_send_kit.py" in run_commands
    assert "tests/test_first_reviewer_send_kit.py" in run_commands
    assert "python scripts/build_first_external_review_card.py" in run_commands
    assert "tests/test_first_external_review_card.py" in run_commands
    assert "python scripts/build_first_feedback_conversion_runbook.py" in run_commands
    assert "tests/test_first_feedback_conversion_runbook.py" in run_commands
    assert "python scripts/build_llm_agent_checklist_verdict.py" in run_commands
    assert "python scripts/verify_outcome_evidence.py" in run_commands
    assert (
        "tests/test_github_discovery_profile.py tests/test_pilot_evidence_quicklink.py tests/test_pilot_launch_control_room.py "
        "tests/test_public_launch_broadcast.py tests/test_outcome_pipeline_board.py tests/test_resume_outcome_adjudication.py "
        "tests/test_first_10_reviewer_sprint.py "
        "tests/test_star_growth_kit.py tests/test_public_metrics_provenance.py tests/test_public_metrics_summary.py "
        "tests/test_business_impact_ledger.py tests/test_reviewer_evidence_kit.py tests/test_resume_traction_proof.py "
        "tests/test_reviewer_action_queue.py tests/test_reviewer_outreach_execution_pack.py "
        "tests/test_reviewer_outreach_status_board.py "
        "tests/test_record_reviewer_outreach_event.py "
        "tests/test_resume_outcome_metrics.py tests/test_resume_outcome_action_checklist.py tests/test_reviewer_submission_hub.py "
        "tests/test_public_reviewer_call.py tests/test_reviewer_share_kit.py tests/test_outcome_collection_page.py"
    ) in run_commands
    assert run_commands.index("python scripts/build_resume_traction_proof.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert run_commands.index("python scripts/build_github_discovery_profile.py") < run_commands.index(
        "python scripts/build_star_growth_kit.py"
    )
    assert run_commands.index("python scripts/build_github_discovery_profile.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert run_commands.index("python scripts/build_reviewer_action_queue.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert run_commands.index("python scripts/build_reviewer_action_queue.py") < run_commands.index(
        "python scripts/build_reviewer_outreach_execution_pack.py"
    )
    assert run_commands.index("python scripts/build_reviewer_outreach_execution_pack.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert run_commands.index("python scripts/build_reviewer_outreach_execution_pack.py") < run_commands.index(
        "python scripts/build_resume_outcome_metrics.py"
    )
    assert run_commands.index("python scripts/build_accepted_evidence_rollup.py") < run_commands.index(
        "python scripts/build_resume_outcome_adjudication.py"
    )
    assert run_commands.index("python scripts/build_resume_outcome_adjudication.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert run_commands.index("python scripts/build_resume_outcome_metrics.py") < run_commands.index(
        "python scripts/build_resume_outcome_action_checklist.py"
    )
    assert run_commands.index("python scripts/build_resume_outcome_action_checklist.py") < run_commands.index(
        "python scripts/build_reviewer_submission_hub.py"
    )
    assert run_commands.index("python scripts/build_reviewer_submission_hub.py") < run_commands.index(
        "python scripts/build_first_10_reviewer_sprint.py"
    )
    assert run_commands.index("python scripts/build_first_10_reviewer_sprint.py") < run_commands.index(
        "python scripts/build_pilot_evidence_quicklink.py"
    )
    assert run_commands.index("python scripts/build_pilot_evidence_quicklink.py") < run_commands.index(
        "python scripts/build_pilot_launch_control_room.py"
    )
    assert run_commands.index("python scripts/build_pilot_launch_control_room.py") < run_commands.index(
        "python scripts/build_public_reviewer_call.py"
    )
    assert run_commands.index("python scripts/build_pilot_launch_control_room.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert run_commands.index("python scripts/build_public_reviewer_call.py") < run_commands.index(
        "python scripts/build_reviewer_share_kit.py"
    )
    assert run_commands.index("python scripts/build_reviewer_share_kit.py") < run_commands.index(
        "python scripts/build_reviewer_outreach_status_board.py"
    )
    assert run_commands.index("python scripts/build_reviewer_outreach_status_board.py") < run_commands.index(
        "python scripts/build_outcome_collection_page.py"
    )
    assert run_commands.index("python scripts/build_outcome_collection_page.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert run_commands.index("python scripts/build_public_metrics_provenance.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert run_commands.index("python scripts/build_resume_claim_upgrade_ledger.py") < run_commands.index(
        "python scripts/build_resume_outcome_scoreboard.py"
    )
    assert run_commands.index("python scripts/build_resume_outcome_scoreboard.py") < run_commands.index(
        "python scripts/build_reviewer_send_queue.py"
    )
    assert run_commands.index("python scripts/build_reviewer_send_queue.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert run_commands.index("python scripts/build_reviewer_quickstart_router.py") < run_commands.index(
        "python scripts/build_first_external_review_card.py"
    )
    assert run_commands.index("python scripts/build_evidence_acceptance_checklist.py") < run_commands.index(
        "python scripts/build_first_external_review_card.py"
    )
    assert run_commands.index("python scripts/build_first_external_review_card.py") < run_commands.index(
        "python scripts/build_first_feedback_conversion_runbook.py"
    )
    assert run_commands.index("python scripts/build_reviewer_send_queue.py") < run_commands.index(
        "python scripts/build_first_feedback_conversion_runbook.py"
    )
    assert run_commands.index("python scripts/build_agent_maturity_audit.py") < run_commands.index(
        "python scripts/build_llm_agent_checklist_verdict.py"
    )
    assert run_commands.index("python scripts/build_llm_agent_checklist_verdict.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert "stefanzweifel/git-auto-commit-action@v5" in uses
