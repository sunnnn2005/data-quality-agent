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
    assert "python scripts/build_star_growth_kit.py" in run_commands
    assert "python scripts/build_public_metrics_summary.py" in run_commands
    assert "python scripts/build_resume_traction_proof.py" in run_commands
    assert "python scripts/build_reviewer_action_queue.py" in run_commands
    assert "python scripts/build_reviewer_outreach_execution_pack.py" in run_commands
    assert "python scripts/build_resume_outcome_metrics.py" in run_commands
    assert "python scripts/build_reviewer_submission_hub.py" in run_commands
    assert "python scripts/verify_outcome_evidence.py" in run_commands
    assert (
        "tests/test_reviewer_evidence_kit.py tests/test_resume_traction_proof.py "
        "tests/test_reviewer_action_queue.py tests/test_reviewer_outreach_execution_pack.py "
        "tests/test_resume_outcome_metrics.py tests/test_reviewer_submission_hub.py"
    ) in run_commands
    assert run_commands.index("python scripts/build_resume_traction_proof.py") < run_commands.index(
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
    assert run_commands.index("python scripts/build_resume_outcome_metrics.py") < run_commands.index(
        "python scripts/build_reviewer_submission_hub.py"
    )
    assert run_commands.index("python scripts/build_reviewer_submission_hub.py") < run_commands.index(
        "python scripts/build_public_metrics_summary.py"
    )
    assert "stefanzweifel/git-auto-commit-action@v5" in uses
