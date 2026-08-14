from scripts.build_reviewer_outcome_ledger import (
    build_reviewer_outcome_ledger,
    render_markdown,
    verify_reviewer_outcome_ledger,
)


def test_reviewer_outcome_ledger_links_outreach_to_resume_claims_without_unlocking_them():
    payload = build_reviewer_outcome_ledger()
    verification = verify_reviewer_outcome_ledger(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_outcome_ledger_verified"] is True
    assert payload["outcome_row_count"] == 5
    assert payload["claimable_row_count"] == 0
    assert payload["blocked_row_count"] == 5
    assert payload["current_sent_count"] == 0
    assert payload["current_public_issue_submitted_count"] == 0
    assert payload["current_accepted_evidence_count"] == 0
    assert payload["next_action_count"] == 5
    assert payload["resume_status"] == "outcome_ledger_ready_not_claimable"
    assert "Reviewer Outcome Ledger" in markdown
    assert "Future Resume Wording" in markdown
    assert "outreach attempts" in payload["not_claimed"][0]


def test_reviewer_outcome_ledger_preserves_sprint_priority_and_public_evidence_gates():
    payload = build_reviewer_outcome_ledger()

    assert [row["metric"] for row in payload["outcome_rows"]] == [
        "ai_engineer_review_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "external_feedback_items",
    ]
    for index, row in enumerate(payload["outcome_rows"], start=1):
        assert row["sprint_day"] == index
        assert row["accepted_evidence_count"] == 0
        assert row["remaining_to_resume_claim"] >= 1
        assert row["status"] == "not_started"
        assert row["resume_claimable_now"] is False
        assert row["current_resume_wording"] is None
        assert row["submission_url"].startswith("https://github.com/")
        assert "public" in row["evidence_gate"].lower()
        assert row["allowed_resume_wording_after_threshold"]
