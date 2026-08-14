from pathlib import Path

from scripts.build_first_feedback_conversion_runbook import (
    build_first_feedback_conversion_runbook,
    render_markdown,
    verify_first_feedback_conversion_runbook,
)


ROOT = Path(__file__).resolve().parents[1]


def test_first_feedback_conversion_runbook_turns_outreach_into_gated_evidence():
    payload = build_first_feedback_conversion_runbook()
    result = verify_first_feedback_conversion_runbook(payload)

    assert result["first_feedback_conversion_runbook_verified"] is True
    assert payload["sprint_step_count"] == 5
    assert payload["first_send"]["target_metric"] == "ai_engineer_review_items"
    assert payload["first_send"]["recommended_channel"] == "LinkedIn DM or mentor email"
    assert len(payload["first_unlock_options"]) == 3
    assert {item["metric"] for item in payload["first_unlock_options"]} == {
        "ai_engineer_review_items",
        "confirmed_external_users",
        "external_feedback_items",
    }
    assert all(value == 0 for value in payload["current_counts"].values())
    assert payload["sprint_steps"][-1]["counts_as_resume_outcome"] is True
    assert all(step["counts_as_resume_outcome"] is False for step in payload["sprint_steps"][:-1])


def test_first_feedback_conversion_runbook_markdown_is_copy_ready_and_honest():
    payload = build_first_feedback_conversion_runbook()
    markdown = render_markdown(payload)

    assert "# First Feedback Conversion Runbook" in markdown
    assert "Five-Step Conversion Workflow" in markdown
    assert "First Unlock Options" in markdown
    assert "record_reviewer_outreach_event.py" in markdown
    assert "Counts as resume outcome: `False`" in markdown
    assert "Counts as resume outcome: `True`" in markdown
    assert "zero resume upgrades" in markdown
    assert "production adoption" in markdown


def test_generated_first_feedback_conversion_runbook_artifacts_are_current():
    payload = build_first_feedback_conversion_runbook()
    verify_first_feedback_conversion_runbook(payload)

    generated_json = (ROOT / "docs" / "first-feedback-conversion-runbook.json").read_text()
    generated_md = (ROOT / "docs" / "first-feedback-conversion-runbook.md").read_text()

    assert '"sprint_step_count": 5' in generated_json
    assert '"target_metric": "ai_engineer_review_items"' in generated_json
    assert "# First Feedback Conversion Runbook" in generated_md
