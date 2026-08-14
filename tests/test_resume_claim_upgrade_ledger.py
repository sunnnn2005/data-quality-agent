from scripts.build_resume_claim_upgrade_ledger import (
    build_resume_claim_upgrade_ledger,
    render_markdown,
    verify_resume_claim_upgrade_ledger,
)


def test_resume_claim_upgrade_ledger_blocks_unproven_outcome_claims():
    payload = build_resume_claim_upgrade_ledger()
    verification = verify_resume_claim_upgrade_ledger(payload)
    markdown = render_markdown(payload)

    assert verification["resume_claim_upgrade_ledger_verified"] is True
    assert payload["upgrade_row_count"] == 6
    assert payload["claimable_row_count"] == 0
    assert payload["blocked_row_count"] == 6
    assert payload["current_counts"]["confirmed_external_users"] == 0
    assert payload["current_counts"]["external_feedback_items"] == 0
    assert payload["current_counts"]["ai_engineer_review_items"] == 0
    assert payload["current_counts"]["business_case_feedback_items"] == 0
    assert payload["current_counts"]["github_stars"] == 0
    assert {row["metric"] for row in payload["upgrade_rows"]} == {
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "github_stars",
    }
    assert all(row["status"] == "blocked_until_public_evidence" for row in payload["upgrade_rows"])
    assert "Resume Claim Upgrade Ledger" in markdown
    assert "Allowed wording after threshold" in markdown
