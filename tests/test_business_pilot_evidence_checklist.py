from pathlib import Path

from scripts.build_business_pilot_evidence_checklist import (
    build_business_pilot_evidence_checklist,
    render_markdown,
    verify_business_pilot_evidence_checklist,
)


ROOT = Path(__file__).resolve().parents[1]


def test_business_pilot_evidence_checklist_blocks_outcome_claims_until_public_evidence():
    payload = build_business_pilot_evidence_checklist()
    verification = verify_business_pilot_evidence_checklist(payload)
    markdown = render_markdown(payload)

    assert verification["business_pilot_evidence_checklist_verified"] is True
    assert payload["outcome_track_count"] == 4
    assert payload["template_check_count"] == 5
    assert payload["passed_template_check_count"] == 5
    assert payload["claimable_now"] == []
    assert set(payload["blocked_until_public_evidence"]) == {
        "confirmed_external_users",
        "business_case_feedback_items",
        "reproducible_feedback_items",
        "external_feedback_items",
    }
    assert all(track["minimum_before_claim"] == 1 for track in payload["outcome_tracks"])
    assert all(len(track["required_public_evidence"]) >= 5 for track in payload["outcome_tracks"])
    assert "Business Pilot Evidence Checklist" in markdown
    assert "agent trace" in markdown.lower()
    assert "business impact" in markdown.lower()


def test_generated_business_pilot_evidence_checklist_artifacts_are_current():
    payload = build_business_pilot_evidence_checklist()
    verify_business_pilot_evidence_checklist(payload)

    generated_json = (ROOT / "docs" / "business-pilot-evidence-checklist.json").read_text()
    generated_md = (ROOT / "docs" / "business-pilot-evidence-checklist.md").read_text()

    assert '"outcome_track_count": 4' in generated_json
    assert '"passed_template_check_count": 5' in generated_json
    assert '"claimable_now": []' in generated_json
    assert "# Business Pilot Evidence Checklist" in generated_md
