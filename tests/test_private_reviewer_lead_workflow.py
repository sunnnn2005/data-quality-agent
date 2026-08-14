from scripts.build_private_reviewer_lead_workflow import (
    build_private_reviewer_lead_workflow,
    render_markdown,
    verify_private_reviewer_lead_workflow,
)


def test_private_reviewer_lead_workflow_keeps_contacts_out_of_public_repo():
    payload = build_private_reviewer_lead_workflow()
    verification = verify_private_reviewer_lead_workflow(payload)
    markdown = render_markdown(payload)

    assert verification["private_reviewer_lead_workflow_verified"] is True
    assert payload["private_paths_gitignored"] is True
    assert payload["required_column_count"] == 11
    assert payload["allowed_status_count"] == 6
    assert payload["target_metric_count"] == 6
    assert "private_contact_label" in payload["required_columns"]
    assert "public_issue_submitted" in payload["allowed_statuses"]
    assert "ai_engineer_review_items" in payload["target_metrics"]
    assert "private lead rows are not public evidence" in str(payload).lower()
    assert "record_reviewer_outreach_event.py" in payload["record_sent_command_template"]
    assert "# Private Reviewer Lead Workflow" in markdown
    assert "```csv" in markdown
