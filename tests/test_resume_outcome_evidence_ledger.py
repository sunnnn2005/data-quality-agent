from scripts.build_resume_outcome_evidence_ledger import (
    build_resume_outcome_evidence_ledger,
    render_markdown,
    verify_resume_outcome_evidence_ledger,
)


def test_resume_outcome_evidence_ledger_separates_claimable_and_blocked_outcomes():
    payload = build_resume_outcome_evidence_ledger()
    verification = verify_resume_outcome_evidence_ledger(payload)
    markdown = render_markdown(payload)

    assert verification["resume_outcome_evidence_ledger_verified"] is True
    assert payload["claimable_now_count"] == 4
    assert payload["in_pipeline_count"] == 2
    assert payload["blocked_until_evidence_count"] == 5
    assert payload["outreach_slot_count"] == 8
    assert payload["accepted_public_evidence_count"] == 0
    assert payload["resume_upgrade_count"] == 0
    assert payload["public_counts"]["confirmed_external_users"] == 0
    assert payload["public_counts"]["external_feedback_items"] == 0
    assert payload["public_counts"]["ai_engineer_review_items"] == 0
    assert payload["public_counts"]["stars"] == 0
    assert any(item["signal"] == "ci_quality" for item in payload["claimable_now"])
    assert any(item["metric"] == "ai_engineer_review_items" for item in payload["blocked_until_evidence"])
    assert "record_reviewer_outreach_event.py" in " ".join(payload["manual_update_commands"])
    assert "Resume Outcome Evidence Ledger" in markdown
    assert "Blocked Until Public Evidence" in markdown
