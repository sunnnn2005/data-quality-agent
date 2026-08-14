from pathlib import Path

from scripts.build_ai_engineer_reviewer_card import (
    build_ai_engineer_reviewer_card,
    render_markdown,
    verify_ai_engineer_reviewer_card,
)


ROOT = Path(__file__).resolve().parents[1]


def test_ai_engineer_reviewer_card_routes_external_review_without_claiming_it():
    payload = build_ai_engineer_reviewer_card()
    result = verify_ai_engineer_reviewer_card(payload)

    assert result["ai_engineer_reviewer_card_verified"] is True
    assert payload["target_metric"] == "ai_engineer_review_items"
    assert payload["current_count"] == 0
    assert payload["inspection_target_count"] == 6
    assert payload["command_count"] == 3
    assert payload["review_prompt_count"] == 5
    assert payload["outcome_badge_snapshot"]["ai_review"] == "0 accepted"
    assert payload["resume_status"] == "review_card_ready_not_claimable"


def test_ai_engineer_reviewer_card_markdown_is_a_low_friction_review_path():
    payload = build_ai_engineer_reviewer_card()
    markdown = render_markdown(payload)

    assert "# AI Engineer Reviewer Card" in markdown
    assert "`app/tool_agent.py`" in markdown
    assert "`app/postgres_adapter.py`" in markdown
    assert "Submit Public Review" in markdown
    assert "Current accepted reviews | 0" in markdown
    assert "No external AI Engineer review has been accepted yet." in markdown


def test_generated_ai_engineer_reviewer_card_artifacts_are_current():
    payload = build_ai_engineer_reviewer_card()
    verify_ai_engineer_reviewer_card(payload)

    generated_json = (ROOT / "docs" / "ai-engineer-reviewer-card.json").read_text()
    generated_md = (ROOT / "docs" / "ai-engineer-reviewer-card.md").read_text()

    assert '"inspection_target_count": 6' in generated_json
    assert '"target_metric": "ai_engineer_review_items"' in generated_json
    assert "# AI Engineer Reviewer Card" in generated_md
