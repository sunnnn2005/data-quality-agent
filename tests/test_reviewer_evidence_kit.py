from scripts.build_reviewer_evidence_kit import (
    build_reviewer_evidence_kit,
    render_markdown,
    verify_reviewer_evidence_kit,
)


def test_reviewer_evidence_kit_gives_countable_public_submission_paths():
    payload = build_reviewer_evidence_kit()
    verification = verify_reviewer_evidence_kit(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_evidence_kit_verified"] is True
    assert payload["evidence_form_count"] == 5
    assert payload["reviewer_script_step_count"] == 5
    assert payload["resume_status"] == "collection_ready_not_claimable"
    assert payload["current_counts"]["confirmed_external_users"] == 0
    assert payload["current_counts"]["external_feedback_items"] == 0
    assert payload["current_counts"]["business_case_feedback_items"] == 0
    assert payload["current_counts"]["accepted_business_impact_signals"] == 0
    assert {form["template"] for form in payload["evidence_forms"]} == {
        "external_run_review.md",
        "demo_feedback.md",
        "business_case_review.md",
        "ai_engineer_review.md",
        "bug_report.md",
    }
    assert "Reviewer Evidence Kit" in markdown
    assert "validated business impact" in payload["not_claimed"]
