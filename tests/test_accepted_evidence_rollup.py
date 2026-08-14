from scripts.build_accepted_evidence_rollup import (
    build_accepted_evidence_rollup,
    render_markdown,
    verify_accepted_evidence_rollup,
)


def test_accepted_evidence_rollup_preserves_zero_outcome_baseline():
    payload = build_accepted_evidence_rollup()

    verification = verify_accepted_evidence_rollup(payload)

    assert verification["accepted_evidence_rollup_verified"] is True
    assert payload["accepted_issue_count"] == 0
    assert payload["claimable_metric_count"] == 6
    assert payload["blocked_outcome_claim_count"] == 6
    assert payload["accepted_counts"]["accepted_real_model_runs"] == 0
    assert all(item["claimable"] is False for item in payload["claimable_metrics"])
    assert "No accepted external reviewer issue exists yet." in payload["not_claimed"]
    assert "0 confirmed users" in payload["resume_safe_summary"]


def test_accepted_evidence_rollup_turns_valid_gate_counts_into_claimable_metrics():
    gate_payload = {
        "evaluated_issue_count": 1,
        "accepted_issue_count": 1,
        "rejected_issue_count": 0,
        "accepted_counts": {
            "business_case_feedback_items": 0,
            "confirmed_external_users": 1,
            "external_feedback_items": 1,
            "reproducible_feedback_items": 1,
            "ai_engineer_review_items": 1,
            "accepted_real_model_runs": 1,
        },
        "current_public_counts": {
            "business_case_feedback_items": 0,
            "confirmed_external_users": 0,
            "external_feedback_items": 0,
            "reproducible_feedback_items": 0,
            "ai_engineer_review_items": 0,
            "accepted_real_model_runs": 0,
        },
        "linked_outreach_queue_count": 3,
        "evaluations": [
            {
                "issue_number": 31,
                "title": "External run review",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/31",
                "accepted": True,
                "failure_reasons": [],
            }
        ],
    }

    payload = build_accepted_evidence_rollup(gate_payload)
    markdown = render_markdown(payload)

    claimable = {item["metric"]: item for item in payload["claimable_metrics"]}
    assert claimable["confirmed_external_users"]["claimable"] is True
    assert claimable["external_feedback_items"]["resume_wording"]
    assert claimable["ai_engineer_review_items"]["claimable"] is True
    assert claimable["accepted_real_model_runs"]["claimable"] is True
    assert claimable["business_case_feedback_items"]["claimable"] is False
    assert payload["blocked_outcome_claim_count"] == 1
    assert payload["accepted_issue_urls"] == ["https://github.com/sunnnn2005/data-quality-agent/issues/31"]
    assert "Accepted Evidence Rollup" in markdown
