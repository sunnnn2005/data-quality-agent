from scripts.build_one_click_evidence_links import (
    build_one_click_evidence_links,
    render_html,
    render_markdown,
    verify_one_click_evidence_links,
)


def test_one_click_evidence_links_prefill_public_permissioned_issues():
    payload = build_one_click_evidence_links()
    verification = verify_one_click_evidence_links(payload)
    markdown = render_markdown(payload)
    html = render_html(payload)

    assert verification["one_click_evidence_links_verified"] is True
    assert payload["link_count"] == 4
    assert payload["target_metric_count"] == 4
    assert payload["accepted_issue_count"] == 0
    assert payload["claimable_resume_metric_count"] == 0
    assert all(value == 0 for value in payload["current_public_counts"].values())
    assert all("issues/new" in item["issue_url"] for item in payload["links"])
    assert all("I+give+permission" in item["issue_url"] for item in payload["links"])
    assert "one-click issue link is not evidence by itself" in payload["counting_rule"]
    assert "# One-Click Evidence Links" in markdown
    assert "Open prefilled GitHub issue" in html


def test_one_click_evidence_links_cover_reviewer_facing_outcomes_only():
    payload = build_one_click_evidence_links()

    assert {item["target_metric"] for item in payload["links"]} == {
        "ai_engineer_review_items",
        "business_case_feedback_items",
        "confirmed_external_users",
        "external_feedback_items",
    }
    assert "github_stars" not in {item["target_metric"] for item in payload["links"]}
    assert "all_outcome_metrics" not in {item["target_metric"] for item in payload["links"]}
