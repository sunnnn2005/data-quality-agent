from scripts.build_reviewer_outreach_console import (
    build_reviewer_outreach_console,
    render_html,
    verify_reviewer_outreach_console,
)


def test_reviewer_outreach_console_exposes_copy_ready_asks_without_claiming_outcomes():
    payload = build_reviewer_outreach_console()
    verification = verify_reviewer_outreach_console(payload)
    html = render_html(payload)

    assert verification["reviewer_outreach_console_verified"] is True
    assert payload["send_count"] == 5
    assert payload["not_sent_count"] == 5
    assert payload["sent_count"] == 0
    assert payload["accepted_evidence_count"] == 0
    assert payload["resume_upgrade_count"] == 0
    assert payload["sends"][0]["target_metric"] == "ai_engineer_review_items"
    assert "--slot-id review_slot_07" in payload["sends"][0]["record_sent_command"]
    assert "Reviewer outreach console" in html
    assert "Open submission form" in html
    assert "Record after real send" in html
    assert "Do not include raw business rows" in html
