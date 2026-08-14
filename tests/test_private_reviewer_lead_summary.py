import csv

from scripts.build_private_reviewer_lead_summary import (
    build_private_reviewer_lead_summary,
    render_markdown,
    verify_private_reviewer_lead_summary,
)
from scripts.build_private_reviewer_lead_workflow import REQUIRED_COLUMNS


def _write_private_leads(path, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def test_private_reviewer_lead_summary_validates_redacted_progress(tmp_path):
    private_csv = tmp_path / "reviewer-leads.csv"
    _write_private_leads(
        private_csv,
        [
            {
                "lead_id": "lead_001",
                "reviewer_segment": "AI engineer mentor",
                "private_contact_label": "mentor email hidden",
                "channel": "LinkedIn",
                "target_metric": "ai_engineer_review_items",
                "status": "sent",
                "next_action_date": "2026-08-16",
                "public_evidence_url": "",
                "permission_to_count": "false",
                "no_private_data_confirmed": "false",
                "notes_private": "private notes must not be published",
            },
            {
                "lead_id": "lead_002",
                "reviewer_segment": "data analyst peer",
                "private_contact_label": "peer handle hidden",
                "channel": "Discord",
                "target_metric": "business_case_feedback_items",
                "status": "accepted_evidence",
                "next_action_date": "2026-08-17",
                "public_evidence_url": "https://github.com/sunnnn2005/data-quality-agent/issues/99",
                "permission_to_count": "true",
                "no_private_data_confirmed": "true",
                "notes_private": "business context stays private",
            },
        ],
    )

    payload = build_private_reviewer_lead_summary(private_csv)
    verification = verify_private_reviewer_lead_summary(payload)
    markdown = render_markdown(payload)

    assert verification["private_reviewer_lead_summary_verified"] is True
    assert payload["lead_count"] == 2
    assert payload["status_counts"]["sent"] == 1
    assert payload["status_counts"]["accepted_evidence"] == 1
    assert payload["target_metric_counts"]["ai_engineer_review_items"] == 1
    assert payload["public_evidence_url_count"] == 1
    assert payload["accepted_ready_count"] == 1
    assert payload["validation_error_count"] == 0
    assert payload["resume_outcome_upgraded"] is False
    assert "notes_private" not in str(payload["redacted_preview"])
    assert "private_contact_label" not in str(payload["redacted_preview"])
    assert "# Private Reviewer Lead Summary" in markdown


def test_private_reviewer_lead_summary_reports_schema_and_gate_errors(tmp_path):
    private_csv = tmp_path / "reviewer-leads.csv"
    _write_private_leads(
        private_csv,
        [
            {
                "lead_id": "lead_001",
                "reviewer_segment": "AI engineer mentor",
                "private_contact_label": "hidden",
                "channel": "LinkedIn",
                "target_metric": "ai_engineer_review_items",
                "status": "accepted_evidence",
                "next_action_date": "2026-08-16",
                "public_evidence_url": "",
                "permission_to_count": "false",
                "no_private_data_confirmed": "false",
                "notes_private": "private",
            }
        ],
    )

    payload = build_private_reviewer_lead_summary(private_csv)

    assert payload["validation_error_count"] == 3
    assert "public evidence statuses require public_evidence_url" in " ".join(payload["validation_errors"])
    assert payload["accepted_ready_count"] == 0
