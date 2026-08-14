from scripts.build_outcome_pipeline_board import (
    build_outcome_pipeline_board,
    render_markdown,
    verify_outcome_pipeline_board,
)


def test_outcome_pipeline_board_connects_distribution_to_resume_claims():
    payload = build_outcome_pipeline_board()
    verification = verify_outcome_pipeline_board(payload)
    markdown = render_markdown(payload)

    assert verification["outcome_pipeline_board_verified"] is True
    assert payload["pipeline_stage_count"] == 5
    assert payload["complete_stage_count"] == 1
    assert payload["claimable_resume_metric_count"] == 0
    assert payload["current_baseline"]["published_public_broadcasts"] == 1
    assert payload["current_baseline"]["sent_reviewer_messages"] == 0
    assert payload["current_baseline"]["accepted_external_evidence_items"] == 0
    assert "record_reviewer_outreach_event.py" in markdown
    assert "# Outcome Pipeline Board" in markdown
