from pathlib import Path

from scripts.build_first_external_review_card import (
    build_first_external_review_card,
    render_html,
    render_markdown,
    verify_first_external_review_card,
)


ROOT = Path(__file__).resolve().parents[1]


def test_first_external_review_card_routes_reviewers_without_claiming_outcomes():
    payload = build_first_external_review_card()
    result = verify_first_external_review_card(payload)

    assert result["first_external_review_card_verified"] is True
    assert result["primary_route_count"] == 3
    assert payload["current_counts"] == {
        "ai_engineer_review_items": 0,
        "confirmed_external_users": 0,
        "external_feedback_items": 0,
    }
    assert payload["target_metrics"] == [
        "ai_engineer_review_items",
        "confirmed_external_users",
        "external_feedback_items",
    ]
    assert "5-12 minutes" in payload["copy_ready_message"]
    assert "non-owner public GitHub issue" in payload["counting_rule"]
    assert "production adoption" in payload["not_claimed"]


def test_first_external_review_card_outputs_shareable_markdown_and_html():
    payload = build_first_external_review_card()
    markdown = render_markdown(payload)
    html = render_html(payload)

    assert "# First External Review Card" in markdown
    assert "Copy-Ready Message" in markdown
    assert "external_feedback_items" in markdown
    assert "confirmed_external_users" in markdown
    assert "ai_engineer_review_items" in markdown
    assert "<title>First External Review Card</title>" in html
    assert "Review Data Quality Agent in 5-12 minutes" in html
    assert "Submit public evidence" in html
    assert "Counting rule" in html


def test_generated_first_external_review_card_artifacts_are_current():
    payload = build_first_external_review_card()
    verify_first_external_review_card(payload)

    generated_json = (ROOT / "docs" / "first-external-review-card.json").read_text()
    generated_md = (ROOT / "docs" / "first-external-review-card.md").read_text()
    generated_html = (ROOT / "docs" / "first-external-review-card.html").read_text()

    assert "https://sunnnn2005.github.io/data-quality-agent/first-external-review-card.html" in generated_json
    assert "# First External Review Card" in generated_md
    assert "<title>First External Review Card</title>" in generated_html
