from scripts.build_external_evidence_triage_board import (
    build_external_evidence_triage_board,
    render_markdown,
    verify_external_evidence_triage_board,
)


def test_external_evidence_triage_board_preserves_zero_resume_outcome_baseline():
    payload = build_external_evidence_triage_board()

    verification = verify_external_evidence_triage_board(payload)
    markdown = render_markdown(payload)

    assert verification["external_evidence_triage_board_verified"] is True
    assert payload["evaluated_issue_count"] == 15
    assert payload["accepted_issue_count"] == 0
    assert payload["claimable_resume_outcome_count"] == 0
    assert payload["waiting_reviewer_issue_count"] == 5
    assert payload["blocked_outcome_claim_count"] == 6
    assert payload["triage_state_counts"]["rejected_needs_external_reviewer"] >= 1
    assert "Self-authored issues do not count as external evidence." in payload["not_claimed"]
    assert "Waiting Reviewer Items" in markdown


def test_external_evidence_triage_board_accepts_claimable_public_evidence():
    gate_payload = {
        "evaluated_issue_count": 1,
        "accepted_issue_count": 1,
        "rejected_issue_count": 0,
        "evaluations": [
            {
                "accepted": True,
                "author": "external-reviewer",
                "counts_toward": ["ai_engineer_review_items"],
                "evidence_type": "ai_engineer_review",
                "failure_reasons": [],
                "issue_number": 31,
                "rejected_counts_toward": [],
                "title": "AI engineer review",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/31",
            }
        ],
    }
    accepted_payload = {
        "accepted_counts": {
            "accepted_real_model_runs": 0,
            "ai_engineer_review_items": 1,
            "business_case_feedback_items": 0,
            "confirmed_external_users": 0,
            "external_feedback_items": 0,
            "reproducible_feedback_items": 0,
        },
        "blocked_outcome_claim_count": 5,
        "claimable_metrics": [
            {
                "claimable": True,
                "current_count": 1,
                "label": "AI Engineer review items",
                "metric": "ai_engineer_review_items",
                "missing_reason": None,
                "resume_wording": "Collected 1 public AI Engineer review item through a gated external review workflow.",
            }
        ],
    }
    materializer_payload = {"safe_current_bullet_count": 4}
    launch_payload = {
        "launch_items": [
            {
                "queue_slot_id": "slot_07_ai_engineer_review",
                "reviewer_profile": "AI engineer",
                "status_board_slot_id": "review_slot_07",
                "submission_url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md",
                "target_metric": "ai_engineer_review_items",
            }
        ]
    }

    payload = build_external_evidence_triage_board(
        gate_payload=gate_payload,
        accepted_payload=accepted_payload,
        materializer_payload=materializer_payload,
        launch_payload=launch_payload,
    )

    assert payload["claimable_resume_outcome_count"] == 1
    assert payload["triage_items"][0]["triage_state"] == "accepted_claimable"
    assert payload["triage_items"][0]["resume_countable_now"] is True
    assert payload["claimable_resume_lines"][0]["resume_wording"].startswith("Collected 1 public")
