from scripts.build_external_review_evidence_ledger import (
    build_external_review_evidence_ledger,
    render_markdown,
    verify_external_review_evidence_ledger,
)


def test_external_review_evidence_ledger_defines_public_proof_before_resume_claims():
    payload = build_external_review_evidence_ledger()
    verification = verify_external_review_evidence_ledger(payload)
    markdown = render_markdown(payload)

    assert verification["external_review_evidence_ledger_verified"] is True
    assert payload["entry_count"] == 0
    assert payload["evidence_requirement_count"] == 4
    assert payload["linked_planned_reviews"] == 3
    assert payload["review_status_counts"]["not_contacted"] == 3
    assert payload["public_counts"]["external_feedback_items"] == 0
    assert payload["public_counts"]["confirmed_external_users"] == 0
    assert payload["public_counts"]["reproducible_feedback_items"] == 0
    assert payload["public_counts"]["business_case_feedback_items"] == 0
    assert payload["resume_status"] == "not_claimable_yet"
    assert {item["evidence_type"] for item in payload["evidence_requirements"]} == {
        "demo_feedback",
        "confirmed_run",
        "business_case_review",
        "reproducible_bug",
    }
    assert "External Review Evidence Ledger" in markdown
    assert "not_claimable_yet" in markdown
