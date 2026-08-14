from scripts.build_first_outcome_evidence_request import (
    build_first_outcome_evidence_request,
    render_html,
    render_markdown,
    verify_first_outcome_evidence_request,
)


def test_first_outcome_evidence_request_targets_first_ai_engineer_review_without_claiming_it():
    payload = build_first_outcome_evidence_request()
    verification = verify_first_outcome_evidence_request(payload)
    markdown = render_markdown(payload)
    html = render_html(payload)

    assert verification["first_outcome_evidence_request_verified"] is True
    assert payload["target_metric"] == "ai_engineer_review_items"
    assert payload["current_count"] == 0
    assert payload["required_count"] == 1
    assert payload["remaining_to_unlock"] == 1
    assert payload["accepted_external_evidence_count"] == 0
    assert payload["resume_status"] == "first_external_outcome_request_ready_not_claimable"
    assert "First Outcome Evidence Request" in markdown
    assert "Copy-Ready Message" in markdown
    assert "Submit public review" in html
    assert "Locked until the public evidence gate passes" in html


def test_first_outcome_evidence_request_has_review_targets_submission_and_boundaries():
    payload = build_first_outcome_evidence_request()

    assert len(payload["inspection_targets"]) == 6
    assert len(payload["review_prompts"]) == 5
    assert len(payload["required_public_fields"]) >= 4
    assert payload["submission_url"].startswith("https://github.com/")
    assert payload["public_tracking_issue_url"].startswith("https://github.com/")
    assert "{name}" in payload["copy_ready_message"]
    assert "--slot-id review_slot_07" in payload["record_sent_command"]
    assert "not evidence by itself" in payload["counting_boundary"]
    assert any("No AI Engineer review has been accepted yet." in item for item in payload["not_claimed"])
    assert any("future resume line is locked" in item.lower() for item in payload["not_claimed"])
