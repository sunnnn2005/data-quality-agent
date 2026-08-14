from scripts.build_pilot_reviewer_crm import (
    build_pilot_reviewer_crm,
    render_markdown,
    verify_pilot_reviewer_crm,
)


def test_pilot_reviewer_crm_turns_outcomes_into_executable_leads():
    payload = build_pilot_reviewer_crm()
    verification = verify_pilot_reviewer_crm(payload)
    markdown = render_markdown(payload)

    assert verification["pilot_reviewer_crm_verified"] is True
    assert payload["lead_count"] == 8
    assert payload["priority_metric_count"] == 5
    assert payload["week_count"] == 3
    assert payload["recorded_outreach_event_count"] == 0
    assert payload["accepted_public_evidence_count"] == 0
    assert payload["resume_upgrade_count"] == 0
    assert payload["leads"][0]["target_metric"] == "ai_engineer_review_items"
    assert payload["target_counts"]["business_case_feedback_items"] == 2
    assert any("record_reviewer_outreach_event.py" in lead["record_sent_command"] for lead in payload["leads"])
    assert "Pilot Reviewer CRM" in markdown
    assert "Three-Week Sprint" in markdown
