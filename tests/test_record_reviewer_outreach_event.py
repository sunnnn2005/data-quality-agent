import pytest

from scripts.record_reviewer_outreach_event import append_event


def test_append_outreach_event_records_sent_without_counting_resume_outcome():
    payload = {"events": []}
    updated = append_event(
        payload,
        {
            "slot_id": "review_slot_07",
            "status": "sent",
            "reviewer_contact": "mentor-placeholder",
            "channel_used": "LinkedIn",
            "sent_at": "2026-08-14T00:00:00+00:00",
            "event_at": "2026-08-14T00:00:00+00:00",
            "public_evidence_url": None,
            "permission_to_count": False,
            "no_private_data_confirmed": False,
            "note": "Message sent; no public evidence yet.",
        },
    )

    assert len(updated["events"]) == 1
    assert updated["events"][0]["status"] == "sent"
    assert updated["events"][0]["permission_to_count"] is False


def test_append_outreach_event_rejects_public_issue_without_url():
    with pytest.raises(ValueError, match="public_evidence_url"):
        append_event(
            {"events": []},
            {
                "slot_id": "review_slot_07",
                "status": "public_issue_submitted",
                "reviewer_contact": "mentor-placeholder",
                "channel_used": "GitHub",
            },
        )


def test_append_outreach_event_rejects_duplicates():
    event = {
        "slot_id": "review_slot_07",
        "status": "sent",
        "reviewer_contact": "mentor-placeholder",
        "channel_used": "LinkedIn",
    }
    payload = append_event({"events": []}, event)

    with pytest.raises(ValueError, match="duplicate"):
        append_event(payload, event)
