from scripts.evaluate_resume_outcomes import (
    build_resume_outcome_readiness_payload,
    render_markdown,
    verify_resume_outcome_readiness,
)


def test_resume_outcome_readiness_blocks_unverified_outcome_claims():
    payload = build_resume_outcome_readiness_payload()
    verification = verify_resume_outcome_readiness(payload)
    markdown = render_markdown(payload)

    assert verification["resume_outcome_readiness_verified"] is True
    assert payload["stage_count"] == 6
    assert payload["claimable_stage_count"] == 2
    assert payload["blocked_stage_count"] == 4
    assert len(payload["claimable_resume_lines"]) == 2
    assert len(payload["missing_evidence"]) == 4
    assert any(item["stage"] == "confirmed_external_users" and item["remaining_needed"] == 1 for item in payload["missing_evidence"])
    assert "confirmed_external_feedback" in markdown
    assert "validated business impact" in payload["not_claimed"]
