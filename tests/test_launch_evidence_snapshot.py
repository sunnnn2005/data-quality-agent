from pathlib import Path

from scripts.build_launch_evidence_snapshot import (
    build_launch_evidence_snapshot,
    render_markdown,
    verify_launch_evidence_snapshot,
)


ROOT = Path(__file__).resolve().parents[1]


def test_launch_evidence_snapshot_summarizes_public_launch_without_adoption_claims():
    payload = build_launch_evidence_snapshot()
    result = verify_launch_evidence_snapshot(payload)

    assert result["launch_evidence_snapshot_verified"] is True
    assert payload["launch_surface_count"] == 5
    assert payload["public_availability"]["available_endpoint_count"] == 4
    assert payload["public_availability"]["successful_workflow_count"] == 3
    assert payload["application_pack"]["passing_tests"] == 199
    assert payload["public_github_stats"]["stars"] == 0
    assert payload["public_github_stats"]["forks"] == 1
    assert payload["review_path"]["current_count"] == 0
    assert payload["claimable_now_count"] == 5
    assert payload["blocked_claim_count"] == 5


def test_launch_evidence_snapshot_markdown_is_recruiter_readable():
    payload = build_launch_evidence_snapshot()
    markdown = render_markdown(payload)

    assert "# Launch Evidence Snapshot" in markdown
    assert "Public Launch Surfaces" in markdown
    assert "AI Engineer Review Path" in markdown
    assert "Claimable Now" in markdown
    assert "Blocked Claims" in markdown
    assert "does not prove users" in markdown


def test_launch_evidence_snapshot_allows_current_ci_run_to_be_in_progress():
    payload = build_launch_evidence_snapshot()
    payload["public_availability"]["successful_workflow_count"] = 0
    payload["claimable_now"][1] = "0/3 main-branch workflows successful at snapshot time"
    payload["resume_safe_summary"] = payload["resume_safe_summary"].replace(
        "3/3 successful workflows",
        "0/3 successful workflows",
    )

    result = verify_launch_evidence_snapshot(payload)

    assert result["launch_evidence_snapshot_verified"] is True
    assert payload["public_availability"]["successful_workflow_count"] == 0


def test_generated_launch_evidence_snapshot_artifacts_are_current():
    payload = build_launch_evidence_snapshot()
    verify_launch_evidence_snapshot(payload)

    generated_json = (ROOT / "docs" / "launch-evidence-snapshot.json").read_text()
    generated_md = (ROOT / "docs" / "launch-evidence-snapshot.md").read_text()

    assert '"launch_surface_count": 5' in generated_json
    assert '"stars": 0' in generated_json
    assert "# Launch Evidence Snapshot" in generated_md
