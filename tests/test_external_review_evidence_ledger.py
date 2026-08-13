from scripts.build_external_review_evidence_ledger import (
    build_external_review_evidence_ledger,
    collect_public_evidence_entries,
    render_markdown,
    verify_external_review_evidence_ledger,
)


def test_external_review_evidence_ledger_defines_public_proof_before_resume_claims():
    payload = build_external_review_evidence_ledger()
    verification = verify_external_review_evidence_ledger(payload)
    markdown = render_markdown(payload)

    assert verification["external_review_evidence_ledger_verified"] is True
    assert payload["entry_count"] == 0
    assert payload["self_authored_planning_excluded"] is True
    assert payload["evidence_counts"]["external_feedback_items"] == 0
    assert payload["evidence_requirement_count"] == 5
    assert payload["linked_planned_reviews"] == 3
    assert payload["review_status_counts"]["not_contacted"] == 3
    assert payload["public_counts"]["external_feedback_items"] == 0
    assert payload["public_counts"]["confirmed_external_users"] == 0
    assert payload["public_counts"]["reproducible_feedback_items"] == 0
    assert payload["public_counts"]["business_case_feedback_items"] == 0
    assert payload["public_counts"]["ai_engineer_review_items"] == 0
    assert payload["resume_status"] == "not_claimable_yet"
    assert {item["evidence_type"] for item in payload["evidence_requirements"]} == {
        "demo_feedback",
        "confirmed_run",
        "business_case_review",
        "reproducible_bug",
        "ai_engineer_review",
    }
    assert "External Review Evidence Ledger" in markdown
    assert "not_claimable_yet" in markdown


def test_external_review_evidence_ledger_counts_only_public_outcome_evidence():
    issues = [
        {
            "number": 17,
            "title": "Review request: collect first public external feedback",
            "url": "https://github.com/sunnnn2005/data-quality-agent/issues/17",
            "state": "OPEN",
            "createdAt": "2026-08-13T16:35:54Z",
            "author": {"login": "sunnnn2005"},
            "labels": [{"name": "feedback"}, {"name": "pilot"}],
        },
        {
            "number": 21,
            "title": "Feedback: replayed the support-ticket demo",
            "url": "https://github.com/sunnnn2005/data-quality-agent/issues/21",
            "state": "OPEN",
            "createdAt": "2026-08-14T10:00:00Z",
            "author": {"login": "external-reviewer"},
            "labels": [{"name": "feedback"}, {"name": "confirmed-user"}],
        },
        {
            "number": 22,
            "title": "AI Engineer review: tool-calling evidence",
            "url": "https://github.com/sunnnn2005/data-quality-agent/issues/22",
            "state": "OPEN",
            "createdAt": "2026-08-14T11:00:00Z",
            "author": {"login": "ai-reviewer"},
            "labels": [{"name": "ai-engineer-review"}],
        },
    ]

    entries = collect_public_evidence_entries(issues)
    payload = build_external_review_evidence_ledger(issues=issues)
    markdown = render_markdown(payload)

    assert [entry["issue_number"] for entry in entries] == [21, 22]
    assert payload["entry_count"] == 2
    assert payload["resume_status"] == "claimable_feedback_exists"
    assert payload["evidence_counts"]["external_feedback_items"] == 1
    assert payload["evidence_counts"]["confirmed_external_users"] == 1
    assert payload["evidence_counts"]["ai_engineer_review_items"] == 1
    assert "external-reviewer" in markdown
    assert "ai-reviewer" in markdown
    assert "issues/21" in markdown
