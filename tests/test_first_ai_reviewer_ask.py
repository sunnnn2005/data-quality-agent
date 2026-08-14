from pathlib import Path

from scripts.build_first_ai_reviewer_ask import (
    build_first_ai_reviewer_ask,
    render_html,
    render_markdown,
    verify_first_ai_reviewer_ask,
)


ROOT = Path(__file__).resolve().parents[1]


def test_first_ai_reviewer_ask_targets_the_first_countable_ai_review_path():
    payload = build_first_ai_reviewer_ask()
    verification = verify_first_ai_reviewer_ask(payload)

    assert verification["first_ai_reviewer_ask_verified"] is True
    assert payload["target_metric"] == "ai_engineer_review_items"
    assert payload["status_board_slot_id"] == "review_slot_07"
    assert payload["source_outreach_status"] == "not_sent"
    assert payload["inspection_target_count"] == 4
    assert payload["review_question_count"] == 4
    assert payload["current_claimable_ai_reviews"] == 0
    assert "I give permission for this public issue to be counted" in payload["permission_sentence"]
    assert "page view does not count" in payload["counting_boundary"]


def test_first_ai_reviewer_ask_outputs_shareable_markdown_and_html():
    payload = build_first_ai_reviewer_ask()
    markdown = render_markdown(payload)
    html = render_html(payload)

    assert "# First AI Reviewer Ask" in markdown
    assert "app/agent.py" in markdown
    assert "docs/agent-safety-boundaries.md" in markdown
    assert "Submit AI review" in html
    assert "<title>First AI Reviewer Ask</title>" in html
    assert "Review the LLM agent design in 8-15 minutes" in html


def test_generated_first_ai_reviewer_ask_artifacts_are_current():
    payload = build_first_ai_reviewer_ask()
    verify_first_ai_reviewer_ask(payload)

    generated_json = (ROOT / "docs" / "first-ai-reviewer-ask.json").read_text()
    generated_md = (ROOT / "docs" / "first-ai-reviewer-ask.md").read_text()
    generated_html = (ROOT / "docs" / "first-ai-reviewer-ask.html").read_text()

    assert '"status_board_slot_id": "review_slot_07"' in generated_json
    assert '"inspection_target_count": 4' in generated_json
    assert "# First AI Reviewer Ask" in generated_md
    assert "<title>First AI Reviewer Ask</title>" in generated_html
