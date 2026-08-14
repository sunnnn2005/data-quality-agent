from scripts.build_outcome_proof_page import (
    build_outcome_proof_page,
    render_html,
    render_markdown,
    verify_outcome_proof_page,
)


def test_outcome_proof_page_separates_claimable_and_blocked_outcomes():
    payload = build_outcome_proof_page()
    verification = verify_outcome_proof_page(payload)
    markdown = render_markdown(payload)
    html = render_html(payload)

    assert verification["outcome_proof_page_verified"] is True
    assert payload["claimable_card_count"] == 6
    assert payload["blocked_card_count"] == 6
    assert payload["reviewer_action_count"] == 5
    assert payload["public_health_status"] == "PASS"
    assert payload["public_health_check_count"] >= 90
    assert payload["current_public_counts"]["confirmed_external_users"] == 0
    assert payload["current_public_counts"]["external_feedback_items"] == 0
    assert payload["current_public_counts"]["github_stars"] == 0
    assert {item["id"] for item in payload["reviewer_actions"]} == {
        "demo_feedback_review",
        "business_data_replay",
        "ai_engineer_review",
        "business_case_review",
        "ethical_star_or_fork",
    }
    assert "outreach attempts do not count" in payload["counting_rule"]
    assert "Traffic" in payload["counting_rule"]
    assert "Verified Now" in markdown
    assert "Blocked Until Evidence" in markdown
    assert "Help Unlock Real Outcomes" in html
    assert "Open evidence path" in html


def test_outcome_proof_page_uses_public_urls_for_reviewers():
    payload = build_outcome_proof_page()

    assert payload["proof_page_url"].endswith("/outcome-proof-page.html")
    assert all(item["evidence_url"].startswith("https://") for item in payload["claimable_cards"])
    assert all(item["entrypoint_url"].startswith("https://") for item in payload["reviewer_actions"])
    non_star_actions = [item for item in payload["reviewer_actions"] if item["id"] != "ethical_star_or_fork"]
    assert all("issues/new?template=" in item["entrypoint_url"] for item in non_star_actions)
