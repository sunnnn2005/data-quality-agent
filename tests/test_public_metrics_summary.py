from scripts.build_public_metrics_summary import (
    build_public_metrics_summary,
    render_markdown,
    verify_public_metrics_summary,
)


def test_public_metrics_summary_keeps_resume_metrics_honest():
    payload = build_public_metrics_summary()
    verification = verify_public_metrics_summary(payload)
    markdown = render_markdown(payload)

    assert verification["public_metrics_summary_verified"] is True
    assert payload["public_metrics"]["stars"] == 0
    assert payload["public_metrics"]["forks"] == 1
    assert payload["public_metrics"]["test_count"] == 57
    assert payload["verified_project_outcomes"]["root_cause_hypotheses"] == 3
    assert payload["verified_project_outcomes"]["recommended_actions"] == 5
    assert "Do not claim external users" in payload["resume_policy"]
    assert "Confirmed external users | 0" in markdown
    assert "GitHub stars beyond the current public count" in markdown
