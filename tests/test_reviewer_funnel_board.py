from scripts.build_reviewer_funnel_board import (
    build_reviewer_funnel_board_payload,
    render_markdown,
    verify_reviewer_funnel_board,
)


def test_reviewer_funnel_board_maps_review_activity_to_resume_evidence_gaps():
    payload = build_reviewer_funnel_board_payload()
    verification = verify_reviewer_funnel_board(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_funnel_board_verified"] is True
    assert payload["funnel_stage_count"] == 4
    assert payload["open_gap_count"] == 4
    assert payload["total_remaining_evidence_items"] == 7
    assert payload["resume_status"] == "evidence_collection_ready"
    assert {stage["counts_toward"] for stage in payload["funnel_stages"]} == {
        "external_feedback_items",
        "reproducible_feedback_items",
        "confirmed_external_users",
        "business_case_feedback_items",
    }
    assert "Reviewer Funnel Board" in markdown
    assert "needs_public_evidence" in markdown
