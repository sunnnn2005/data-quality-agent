from pathlib import Path

from scripts.build_evidence_acceptance_checklist import (
    build_evidence_acceptance_checklist,
    render_markdown,
    verify_evidence_acceptance_checklist,
)


ROOT = Path(__file__).resolve().parents[1]


def test_evidence_acceptance_checklist_maps_all_blocked_resume_outcomes():
    payload = build_evidence_acceptance_checklist()
    result = verify_evidence_acceptance_checklist(payload)

    assert result["evidence_acceptance_checklist_verified"] is True
    assert result["acceptance_item_count"] == 6
    assert result["accepted_issue_count"] == 0
    assert {item["current_count"] for item in payload["acceptance_items"]} == {0}
    assert {item["status"] for item in payload["acceptance_items"]} == {"blocked_until_public_evidence"}
    assert "non-owner public GitHub issue" in payload["manual_counting_rule"]


def test_evidence_acceptance_checklist_markdown_keeps_resume_claims_conservative():
    payload = build_evidence_acceptance_checklist()
    markdown = render_markdown(payload)

    assert "# Evidence Acceptance Checklist" in markdown
    assert "`ai_engineer_review_items`" in markdown
    assert "`confirmed_external_users`" in markdown
    assert "`github_stars`" in markdown
    assert "Accepted public reviewer issues | 0" in markdown
    assert "No accepted external reviewer issue exists yet." in markdown


def test_generated_evidence_acceptance_checklist_artifacts_are_current():
    payload = build_evidence_acceptance_checklist()
    verify_evidence_acceptance_checklist(payload)

    generated_json = (ROOT / "docs" / "evidence-acceptance-checklist.json").read_text()
    generated_md = (ROOT / "docs" / "evidence-acceptance-checklist.md").read_text()

    assert '"acceptance_item_count": 6' in generated_json
    assert '"accepted_issue_count": 0' in generated_json
    assert "# Evidence Acceptance Checklist" in generated_md
