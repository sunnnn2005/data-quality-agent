from scripts.build_resume_claim_materializer import (
    build_resume_claim_materializer,
    verify_resume_claim_materializer,
    write_markdown,
)


def test_resume_claim_materializer_blocks_external_outcome_bullets_without_evidence():
    payload = build_resume_claim_materializer()
    verify_resume_claim_materializer(payload)

    assert payload["safe_current_bullet_count"] == 4
    assert payload["future_template_count"] == 6
    assert payload["blocked_claim_count"] == 6
    assert payload["materialized_claim_count"] == 0
    assert payload["accepted_public_evidence_count"] == 0
    assert payload["resume_upgrade_count"] == 0
    assert payload["reviewer_lead_count"] == 9

    future_metrics = {item["metric"] for item in payload["future_bullet_templates"]}
    assert future_metrics == {
        "ai_engineer_review_items",
        "accepted_real_model_runs",
        "business_case_feedback_items",
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
    }
    assert all(not item["materialized"] for item in payload["future_bullet_templates"])
    assert all(item["rendered_bullet"] is None for item in payload["future_bullet_templates"])
    assert "No enterprise deployment is claimed." in payload["not_claimed"]


def test_resume_claim_materializer_markdown_is_recruiter_readable():
    markdown = write_markdown(build_resume_claim_materializer())

    assert "# Resume Claim Materializer" in markdown
    assert "Materialized Outcome Bullets" in markdown
    assert "Blocked Future Templates" in markdown
    assert "None yet. Accepted public evidence count is 0." in markdown
    assert "ai_engineer_review_items" in markdown
    assert "accepted_real_model_runs" in markdown
