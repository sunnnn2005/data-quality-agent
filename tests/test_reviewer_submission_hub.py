from scripts.build_reviewer_submission_hub import (
    build_reviewer_submission_hub,
    render_markdown,
    verify_reviewer_submission_hub,
)


def test_reviewer_submission_hub_maps_every_outcome_to_public_evidence_path():
    payload = build_reviewer_submission_hub()
    verification = verify_reviewer_submission_hub(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_submission_hub_verified"] is True
    assert payload["submission_path_count"] == 7
    assert payload["target_metric_count"] == 7
    assert payload["total_required_evidence_fields"] == 32
    assert payload["resume_status"] == "collection_ready_not_claimable"

    metrics = {path["target_metric"] for path in payload["submission_paths"]}
    assert metrics == {
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "accepted_real_model_runs",
        "github_stars",
    }
    assert all(path["submission_url"].startswith("https://github.com/") for path in payload["submission_paths"])
    assert all("Counts only" in path["counting_rule"] for path in payload["submission_paths"])
    reproducible_path = next(path for path in payload["submission_paths"] if path["target_metric"] == "reproducible_feedback_items")
    assert reproducible_path["submission_url"].endswith("template=business_data_replay.md")
    assert "selected tools shown in the agent trace" in reproducible_path["required_evidence"]
    assert not reproducible_path["submission_url"].endswith("template=bug_report.md")
    real_model_path = next(path for path in payload["submission_paths"] if path["target_metric"] == "accepted_real_model_runs")
    assert real_model_path["submission_url"].endswith("template=real_model_run_review.md")
    assert "total tokens" in real_model_path["required_evidence"]
    assert "estimated cost" in real_model_path["required_evidence"]
    assert "latency" in real_model_path["required_evidence"]
    assert "verification status" in real_model_path["required_evidence"]
    assert all(status["current_count"] == 0 for status in payload["tracked_outcome_status"].values())
    assert all(status["resume_status"] == "not_claimable_yet" for status in payload["tracked_outcome_status"].values())
    assert "never asks for fake engagement" in str(payload).lower()
    assert "Reviewer Submission Hub" in markdown
    assert "Current Outcome Status" in markdown
