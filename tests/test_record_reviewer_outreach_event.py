import pytest

import scripts.build_first_reviewer_send_kit as first_send_builder
import scripts.build_outcome_pipeline_board as pipeline_builder
import scripts.build_reviewer_outreach_status_board as status_builder
import scripts.record_reviewer_outreach_event as recorder
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


def test_refresh_downstream_artifacts_updates_status_and_pipeline_after_sent_event(tmp_path, monkeypatch):
    events_path = tmp_path / "reviewer-outreach-events.json"
    status_json = tmp_path / "reviewer-outreach-status-board.json"
    status_md = tmp_path / "reviewer-outreach-status-board.md"
    pipeline_json = tmp_path / "outcome-pipeline-board.json"
    pipeline_md = tmp_path / "outcome-pipeline-board.md"
    first_send_json = tmp_path / "first-reviewer-send-kit.json"
    first_send_md = tmp_path / "first-reviewer-send-kit.md"

    events_path.write_text(
        """{
  "events": [
    {
      "channel_used": "LinkedIn",
      "event_at": "2026-08-14T00:00:00+00:00",
      "no_private_data_confirmed": false,
      "note": "Message sent; no public evidence yet.",
      "permission_to_count": false,
      "public_evidence_url": null,
      "reviewer_contact": "mentor-placeholder",
      "sent_at": "2026-08-14T00:00:00+00:00",
      "slot_id": "review_slot_07",
      "status": "sent"
    }
  ],
  "purpose": "test"
}
"""
    )

    monkeypatch.setattr(status_builder, "OUTREACH_EVENTS_PATH", events_path)
    monkeypatch.setattr(recorder, "OUTREACH_STATUS_JSON_PATH", status_json)
    monkeypatch.setattr(recorder, "OUTREACH_STATUS_MD_PATH", status_md)
    monkeypatch.setattr(recorder, "OUTCOME_PIPELINE_JSON_PATH", pipeline_json)
    monkeypatch.setattr(recorder, "OUTCOME_PIPELINE_MD_PATH", pipeline_md)
    monkeypatch.setattr(recorder, "FIRST_REVIEWER_SEND_JSON_PATH", first_send_json)
    monkeypatch.setattr(recorder, "FIRST_REVIEWER_SEND_MD_PATH", first_send_md)
    monkeypatch.setattr(pipeline_builder, "OUTREACH_STATUS_PATH", status_json)
    monkeypatch.setattr(first_send_builder, "OUTREACH_STATUS_PATH", status_json)
    monkeypatch.setattr(first_send_builder, "PIPELINE_PATH", pipeline_json)

    summary = recorder.refresh_downstream_artifacts()

    assert summary["refreshed"] is True
    assert summary["status_board_sent_count"] == 1
    assert summary["pipeline_sent_reviewer_messages"] == 1
    assert summary["claimable_resume_metric_count"] == 0
    assert summary["first_send_status"] == "sent"
    assert "review_slot_07" in status_md.read_text()
    assert "| Sent Reviewer Messages | 1 |" in pipeline_md.read_text()
    assert "Claimable resume metrics | 0 | 0" in first_send_md.read_text()
