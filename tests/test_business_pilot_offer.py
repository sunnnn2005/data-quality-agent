from pathlib import Path

from scripts.build_business_pilot_offer import (
    build_business_pilot_offer,
    render_html,
    render_markdown,
    verify_business_pilot_offer,
)


ROOT = Path(__file__).resolve().parents[1]


def test_business_pilot_offer_defines_safe_path_to_real_outcomes_without_claiming_them():
    payload = build_business_pilot_offer()
    verification = verify_business_pilot_offer(payload)

    assert verification["business_pilot_offer_verified"] is True
    assert payload["pilot_scope_count"] == 4
    assert payload["eligible_data_source_count"] == 4
    assert payload["evidence_gate_count"] == 6
    assert payload["pilot_status"] == "ready_to_invite_not_validated"
    assert all(count == 0 for count in payload["current_public_counts"].values())
    assert "completed pilot" in payload["not_claimed"]
    assert "production deployment" in payload["not_claimed"]
    assert payload["submission_paths"]["business_data_replay"].endswith("template=business_data_replay.md")
    assert payload["submission_paths"]["business_case_review"].endswith("template=business_case_review.md")


def test_business_pilot_offer_outputs_public_markdown_and_html():
    payload = build_business_pilot_offer()
    markdown = render_markdown(payload)
    html = render_html(payload)

    assert "# Business Pilot Offer" in markdown
    assert "Evidence Gates" in markdown
    assert "Current Public Counts" in markdown
    assert "<title>Business Pilot Offer</title>" in html
    assert "Business Data Pilot Offer" in html
    assert "Pilot-ready, not pilot-validated yet" in html


def test_generated_business_pilot_offer_artifacts_are_current():
    payload = build_business_pilot_offer()
    verify_business_pilot_offer(payload)

    generated_json = (ROOT / "docs" / "business-pilot-offer.json").read_text()
    generated_md = (ROOT / "docs" / "business-pilot-offer.md").read_text()
    generated_html = (ROOT / "docs" / "business-pilot-offer.html").read_text()

    assert '"pilot_scope_count": 4' in generated_json
    assert '"evidence_gate_count": 6' in generated_json
    assert "# Business Pilot Offer" in generated_md
    assert "<title>Business Pilot Offer</title>" in generated_html
