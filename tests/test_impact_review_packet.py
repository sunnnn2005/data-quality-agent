from scripts.build_impact_review_packet import (
    build_impact_review_packet_payload,
    render_markdown,
    verify_impact_review_packet,
)


def test_impact_review_packet_summarizes_business_evidence_without_adoption_claims():
    payload = build_impact_review_packet_payload()
    verification = verify_impact_review_packet(payload)
    markdown = render_markdown(payload)

    assert verification["impact_review_packet_verified"] is True
    assert payload["business_metric_count"] == 12
    assert payload["evidence_link_count"] == 8
    assert payload["business_metrics"]["rows_analyzed"] == 8
    assert payload["business_metrics"]["quality_score"] == 24
    assert payload["business_metrics"]["status"] == "FAIL"
    assert payload["business_metrics"]["recommended_actions"] == 5
    assert payload["business_metrics"]["owner_handoffs"] == 4
    assert payload["current_public_counts"]["confirmed_external_users"] == 0
    assert "production financial impact avoided" in payload["not_claimed"]
    assert "Impact Review Packet" in markdown
