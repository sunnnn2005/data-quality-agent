from scripts.build_first_external_proof_action_sheet import (
    build_first_external_proof_action_sheet,
    render_html,
    render_markdown,
    verify_first_external_proof_action_sheet,
)


def test_first_external_proof_action_sheet_prioritizes_real_external_evidence_without_claiming_it():
    payload = build_first_external_proof_action_sheet()
    verification = verify_first_external_proof_action_sheet(payload)
    markdown = render_markdown(payload)
    html = render_html(payload)

    assert verification["first_external_proof_action_sheet_verified"] is True
    assert payload["primary_target_metric"] == "ai_engineer_review_items"
    assert payload["current_accepted_external_evidence"] == 0
    assert payload["current_github_stars"] == 0
    assert payload["current_confirmed_external_users"] == 0
    assert payload["reviewer_target_count"] == 3
    assert payload["required_success_field_count"] == 6
    assert "First External Proof Action Sheet" in markdown
    assert "Today Execution Order" in markdown
    assert "Submit evidence" in html
    assert "Locked Resume Line" in html


def test_first_external_proof_action_sheet_has_copy_messages_recorders_and_boundaries():
    payload = build_first_external_proof_action_sheet()

    target_metrics = {target["target_metric"] for target in payload["reviewer_targets"]}
    assert target_metrics == {
        "ai_engineer_review_items",
        "external_feedback_items",
        "reproducible_feedback_items",
    }
    assert payload["reviewer_targets"][0]["target_metric"] == "ai_engineer_review_items"
    assert all("record_reviewer_outreach_event.py" in target["record_sent_command"] for target in payload["reviewer_targets"])
    assert all(target["submission_url"].startswith("https://github.com/") for target in payload["reviewer_targets"])
    assert "distribution evidence only" in payload["counting_boundary"]
    assert "zero until a non-owner public GitHub issue passes" in payload["counting_boundary"]
    assert any("No AI Engineer review is claimed" in item for item in payload["not_claimed"])
    assert "zero upgraded resume outcomes" in payload["resume_safe_summary"]
