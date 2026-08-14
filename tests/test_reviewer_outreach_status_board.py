from scripts.build_reviewer_outreach_status_board import (
    apply_outreach_events,
    build_reviewer_outreach_status_board,
    calculate_conversion_metrics,
    render_markdown,
    verify_reviewer_outreach_status_board,
)


def test_reviewer_outreach_status_board_tracks_slots_without_claiming_results():
    payload = build_reviewer_outreach_status_board()
    verification = verify_reviewer_outreach_status_board(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_outreach_status_board_verified"] is True
    assert payload["outreach_slot_count"] == 9
    assert payload["status_stage_count"] == 5
    assert payload["not_sent_count"] == 9
    assert payload["sent_count"] == 0
    assert payload["reply_count"] == 0
    assert payload["accepted_evidence_count"] == 0
    assert payload["resume_upgrade_count"] == 0
    assert payload["conversion_metrics"]["tracked_slot_count"] == 9
    assert payload["conversion_metrics"]["contacted_count"] == 0
    assert payload["conversion_metrics"]["contact_rate"] == 0
    assert payload["conversion_metrics"]["remaining_contacts_to_first_public_issue"] == 1
    assert payload["conversion_metrics"]["resume_claim_status"] == "blocked_until_public_evidence"
    assert payload["next_resume_unlock_count"] == 5
    assert payload["blocked_unlock_count"] == 5
    assert payload["resume_status"] == "tracking_ready_not_claimable"
    assert all(slot["status"] == "not_sent" for slot in payload["outreach_slots"])
    assert all(slot["public_evidence_url"] is None for slot in payload["outreach_slots"])
    assert all(slot["accepted_by_gate"] is False for slot in payload["outreach_slots"])
    assert all(unlock["claimable_now"] is False for unlock in payload["next_resume_unlocks"])
    assert set(payload["current_outcome_counts"].values()) == {0}
    assert "private replies are notes only" in str(payload).lower()
    assert "non-owner public GitHub issue" in str(payload)
    assert "# Reviewer Outreach Status Board" in markdown
    assert "Conversion Metrics" in markdown
    assert "Next Resume Unlocks" in markdown


def test_conversion_metrics_update_without_unlocking_resume_claims():
    payload = build_reviewer_outreach_status_board()
    slots = payload["outreach_slots"]
    apply_outreach_events(
        slots,
        [
            {
                "slot_id": "review_slot_01",
                "status": "sent",
                "reviewer_contact": "peer-a",
                "channel_used": "LinkedIn",
                "sent_at": "2026-08-14T00:00:00+00:00",
                "event_at": "2026-08-14T00:00:00+00:00",
            },
            {
                "slot_id": "review_slot_02",
                "status": "replied_private",
                "reviewer_contact": "peer-b",
                "channel_used": "Email",
                "sent_at": "2026-08-14T00:00:00+00:00",
                "event_at": "2026-08-15T00:00:00+00:00",
            },
            {
                "slot_id": "review_slot_03",
                "status": "public_issue_submitted",
                "reviewer_contact": "peer-c",
                "channel_used": "GitHub",
                "sent_at": "2026-08-14T00:00:00+00:00",
                "event_at": "2026-08-16T00:00:00+00:00",
                "public_evidence_url": "https://github.com/sunnnn2005/data-quality-agent/issues/99",
                "permission_to_count": True,
                "no_private_data_confirmed": True,
            },
        ],
    )

    metrics = calculate_conversion_metrics(slots)

    assert metrics["contacted_count"] == 3
    assert metrics["private_reply_count"] == 1
    assert metrics["public_issue_count"] == 1
    assert metrics["contact_rate"] == 0.3333
    assert metrics["private_reply_rate_from_contacted"] == 0.3333
    assert metrics["public_issue_rate_from_contacted"] == 0.3333
    assert metrics["accepted_evidence_count"] == 0
    assert metrics["accepted_evidence_rate_from_public_issues"] == 0.0
    assert metrics["remaining_contacts_to_first_public_issue"] == 0
    assert metrics["resume_claim_status"] == "blocked_until_public_evidence"
