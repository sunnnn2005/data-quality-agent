from scripts.build_public_outcome_intake_dashboard import (
    build_public_outcome_intake_dashboard,
    render_html,
    render_markdown,
    verify_public_outcome_intake_dashboard,
)


def test_public_outcome_intake_dashboard_separates_claimable_proof_from_blocked_outcomes():
    payload = build_public_outcome_intake_dashboard()
    verification = verify_public_outcome_intake_dashboard(payload)
    markdown = render_markdown(payload)
    html = render_html(payload)

    assert verification["public_outcome_intake_dashboard_verified"] is True
    assert payload["claimable_signal_count"] == 4
    assert payload["blocked_intake_path_count"] == 5
    assert payload["accepted_external_evidence_count"] == 0
    assert payload["github_stars"] == 0
    assert payload["github_forks"] == 1
    assert payload["public_health_status"] == "PASS"
    assert "Claimable Public Proof" in markdown
    assert "Intake Paths For Real Outcomes" in markdown
    assert "Submit Evidence For Real Outcomes" in html
    assert "Resume-Safe Bullets Now" in html


def test_public_outcome_intake_dashboard_routes_each_missing_metric_to_public_evidence():
    payload = build_public_outcome_intake_dashboard()

    assert [item["metric"] for item in payload["blocked_intake_paths"]] == [
        "ai_engineer_review_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "external_feedback_items",
    ]
    for item in payload["blocked_intake_paths"]:
        assert item["current"] == 0
        assert item["required"] >= 1
        assert item["remaining"] == item["required"]
        assert item["submission_url"].startswith("https://github.com/")
        assert "public" in item["evidence_gate"].lower()
        assert item["future_resume_wording"]
    assert "Page views" in payload["counting_rule"]
    assert any("No confirmed external users" in item for item in payload["not_claimed"])
    assert any("No GitHub stars beyond" in item for item in payload["not_claimed"])
