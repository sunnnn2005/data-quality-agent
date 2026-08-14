from scripts.build_business_impact_validation_plan import (
    build_business_impact_validation_plan,
    render_markdown,
    verify_business_impact_validation_plan,
)


def test_business_impact_validation_plan_maps_business_metrics_without_claiming_adoption():
    payload = build_business_impact_validation_plan()
    verification = verify_business_impact_validation_plan(payload)
    markdown = render_markdown(payload)

    assert verification["business_impact_validation_plan_verified"] is True
    assert payload["current_demo_baseline"]["quality_score"] == 24
    assert payload["current_demo_baseline"]["findings"] == 5
    assert payload["current_demo_baseline"]["business_risk_areas"] == 4
    assert payload["current_demo_baseline"]["owner_handoffs"] == 4
    assert payload["current_demo_baseline"]["external_validated_business_cases"] == 0
    assert payload["validation_metric_count"] == 5
    assert payload["pilot_step_count"] == 5
    assert payload["minimum_resume_upgrade_gate"]["resume_claim_allowed"] is False
    assert payload["minimum_resume_upgrade_gate"]["requires_business_workflow_mapping"] is True
    assert len(payload["future_resume_lines_after_evidence"]) == 5
    assert "validated business impact" in payload["not_claimed"]
    assert "manual time saved" in payload["not_claimed"]
    assert "Business Impact Validation Plan" in markdown
    assert "Minimum Resume Upgrade Gate" in markdown
