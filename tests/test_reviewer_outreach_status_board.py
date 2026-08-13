from scripts.build_reviewer_outreach_status_board import (
    build_reviewer_outreach_status_board,
    render_markdown,
    verify_reviewer_outreach_status_board,
)


def test_reviewer_outreach_status_board_tracks_slots_without_claiming_results():
    payload = build_reviewer_outreach_status_board()
    verification = verify_reviewer_outreach_status_board(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_outreach_status_board_verified"] is True
    assert payload["outreach_slot_count"] == 8
    assert payload["status_stage_count"] == 5
    assert payload["not_sent_count"] == 8
    assert payload["sent_count"] == 0
    assert payload["reply_count"] == 0
    assert payload["accepted_evidence_count"] == 0
    assert payload["resume_upgrade_count"] == 0
    assert payload["resume_status"] == "tracking_ready_not_claimable"
    assert all(slot["status"] == "not_sent" for slot in payload["outreach_slots"])
    assert all(slot["public_evidence_url"] is None for slot in payload["outreach_slots"])
    assert all(slot["accepted_by_gate"] is False for slot in payload["outreach_slots"])
    assert set(payload["current_outcome_counts"].values()) == {0}
    assert "private replies are notes only" in str(payload).lower()
    assert "non-owner public GitHub issue" in str(payload)
    assert "# Reviewer Outreach Status Board" in markdown
