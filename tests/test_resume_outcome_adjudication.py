from scripts.build_resume_outcome_adjudication import (
    build_resume_outcome_adjudication,
    render_markdown,
    verify_resume_outcome_adjudication,
)


def test_resume_outcome_adjudication_keeps_strong_resume_claims_evidence_gated():
    payload = build_resume_outcome_adjudication()
    verification = verify_resume_outcome_adjudication(payload)
    markdown = render_markdown(payload)

    assert verification["resume_outcome_adjudication_verified"] is True
    assert payload["claim_category_count"] == 5
    assert payload["claimable_category_count"] == 0
    assert payload["blocked_category_count"] == 5
    assert payload["accepted_issue_count"] == 0
    assert payload["launch_control_room"]["public_issue_thread_count"] == 4
    assert "confirmed_external_users" in markdown
    assert "external_feedback_items" in markdown
    assert "business_case_feedback_items" in markdown
    assert "ai_engineer_review_items" in markdown
    assert "Unlock Condition" in markdown
    assert "external users" in payload["not_claimed"]
