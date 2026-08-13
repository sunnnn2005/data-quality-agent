from scripts.build_business_impact_ledger import (
    build_business_impact_ledger,
    render_markdown,
    verify_business_impact_ledger,
)


ACCEPTED_BUSINESS_CASE_GATE = {
    "accepted_issue_count": 1,
    "evaluations": [
        {
            "issue_number": 41,
            "title": "Business case: support SLA dashboard",
            "url": "https://github.com/sunnnn2005/data-quality-agent/issues/41",
            "author": "external-reviewer",
            "accepted": True,
            "evidence_type": "business_case_review",
            "extracted_business_impact": {
                "business_context": "support operations weekly SLA dashboard",
                "data_quality_problem": "duplicate ticket IDs caused escalation undercounting",
                "business_impact": "2 hours of manual investigation and 1200 affected tickets",
                "fields_involved": "ticket_id, routing_team, amount",
                "project_evidence_mapping": "duplicate ticket ID finding and owner handoff matched the issue",
            },
        }
    ],
}


def test_business_impact_ledger_preserves_zero_baseline_without_fake_business_claims():
    payload = build_business_impact_ledger()
    verification = verify_business_impact_ledger(payload)
    markdown = render_markdown(payload)

    assert verification["business_impact_ledger_verified"] is True
    assert payload["accepted_business_impact_signal_count"] == 0
    assert payload["accepted_business_cases"] == []
    assert payload["resume_upgrade_rule"]["resume_status"] == "not_claimable_yet"
    assert "validated business impact" in payload["not_claimed"]
    assert "Business Impact Ledger" in markdown


def test_business_impact_ledger_extracts_claimable_accepted_business_case():
    payload = build_business_impact_ledger(ACCEPTED_BUSINESS_CASE_GATE)
    verification = verify_business_impact_ledger(payload)
    markdown = render_markdown(payload)

    assert verification["accepted_business_impact_signal_count"] == 1
    assert payload["resume_upgrade_rule"]["resume_status"] == "claimable_with_linked_evidence"
    assert payload["accepted_business_cases"][0]["issue_number"] == 41
    assert "2 hours" in payload["accepted_business_cases"][0]["business_impact"]
    assert "duplicate ticket ID" in payload["accepted_business_cases"][0]["project_evidence_mapping"]
    assert "support SLA dashboard" in markdown
