from pathlib import Path

from scripts.build_two_minute_review_card import (
    build_two_minute_review_card,
    render_html,
    render_markdown,
    verify_two_minute_review_card,
)


ROOT = Path(__file__).resolve().parents[1]


def test_two_minute_review_card_shortens_the_first_feedback_path_without_claiming_outcomes():
    payload = build_two_minute_review_card()
    verification = verify_two_minute_review_card(payload)

    assert verification["two_minute_review_card_verified"] is True
    assert payload["time_budget_minutes"] == 2
    assert payload["micro_step_count"] == 3
    assert payload["required_evidence_count"] == 5
    assert all(step["counts_as_outcome"] is False for step in payload["micro_steps"])
    assert all(count == 0 for count in payload["current_counts"].values())
    assert "non-owner GitHub issue" in payload["success_definition"]
    assert "production adoption" in payload["not_claimed"]


def test_two_minute_review_card_outputs_shareable_markdown_and_html():
    payload = build_two_minute_review_card()
    markdown = render_markdown(payload)
    html = render_html(payload)

    assert "# Two-Minute Review Card" in markdown
    assert "Micro-Steps" in markdown
    assert "counts_as_outcome=False" in markdown
    assert "external_feedback_items" in markdown
    assert "<title>Two-Minute Review Card</title>" in html
    assert "Review Data Quality Agent in 2 minutes" in html
    assert "Required evidence" in html


def test_generated_two_minute_review_card_artifacts_are_current():
    payload = build_two_minute_review_card()
    verify_two_minute_review_card(payload)

    generated_json = (ROOT / "docs" / "two-minute-review-card.json").read_text()
    generated_md = (ROOT / "docs" / "two-minute-review-card.md").read_text()
    generated_html = (ROOT / "docs" / "two-minute-review-card.html").read_text()

    assert '"time_budget_minutes": 2' in generated_json
    assert '"micro_step_count": 3' in generated_json
    assert "# Two-Minute Review Card" in generated_md
    assert "<title>Two-Minute Review Card</title>" in generated_html
