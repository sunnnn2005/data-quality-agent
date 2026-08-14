from scripts.build_public_metrics_provenance import (
    build_public_metrics_provenance,
    render_markdown,
    verify_public_metrics_provenance,
)


def test_public_metrics_provenance_explains_claimable_and_blocked_metrics():
    payload = build_public_metrics_provenance()
    verification = verify_public_metrics_provenance(payload)
    markdown = render_markdown(payload)
    metrics = {item["metric"]: item for item in payload["metrics"]}

    assert verification["public_metrics_provenance_verified"] is True
    assert payload["metric_count"] == 8
    assert payload["claimable_metric_count"] == 2
    assert metrics["github_forks"]["resume_status"] == "claimable"
    assert metrics["passing_tests"]["resume_status"] == "claimable"
    assert metrics["github_stars"]["resume_status"] == "baseline_only"
    assert metrics["confirmed_external_users"]["value"] == 0
    assert metrics["confirmed_external_users"]["counts_match_gate"] is True
    assert metrics["external_feedback_items"]["resume_status"] == "blocked_until_accepted_evidence"
    assert metrics["business_case_feedback_items"]["resume_status"] == "blocked_until_accepted_evidence"
    assert metrics["ai_engineer_review_items"]["resume_status"] == "blocked_until_accepted_evidence"
    assert metrics["feature_feedback_items"]["resume_status"] == "tracking_only"
    assert "Public Metrics Provenance" in markdown
    assert "No external users are claimed" in markdown
