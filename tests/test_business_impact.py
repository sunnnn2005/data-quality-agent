from scripts.verify_business_impact import build_business_impact_payload, verify_business_impact


def test_business_impact_artifact_quantifies_support_ticket_case_study():
    payload = build_business_impact_payload()
    verification = verify_business_impact(payload)

    assert verification["business_impact_verified"] is True
    assert payload["dataset_id"] == "support_tickets"
    assert payload["row_count"] == 8
    assert payload["quality_score"] == 24
    assert payload["issue_category_count"] == 4
    assert payload["root_cause_hypothesis_count"] == 3
    assert payload["top_root_cause_hypotheses"][0]["confidence"] >= payload["top_root_cause_hypotheses"][-1]["confidence"]
    assert payload["affected_column_count"] == 4
    assert payload["business_rule_reference_count"] == 4
    assert payload["business_risk_area_count"] == 4
    assert payload["high_priority_action_count"] == 3
    assert payload["owner_handoff_count"] == 4
    assert payload["remediation_scorecard"]["business_risk_areas"][0]["owner"] == "Data Engineering"
    assert "owner handoffs" in payload["remediation_scorecard"]["resume_safe_outcome"]
    assert "duplicate ticket IDs" in payload["resume_safe_summary"]
    assert "enterprise adoption" in " ".join(payload["not_claimed"]).lower()
