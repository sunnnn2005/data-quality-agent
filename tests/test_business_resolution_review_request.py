from scripts.build_business_resolution_review_request import (
    build_business_resolution_review_request,
    render_markdown,
    verify_business_resolution_review_request,
)


def test_business_resolution_review_request_opens_public_gate_without_counting_it():
    payload = build_business_resolution_review_request()
    verification = verify_business_resolution_review_request(payload)
    markdown = render_markdown(payload)

    assert verification["business_resolution_review_request_verified"] is True
    assert payload["review_issue"].endswith("/issues/30")
    assert len(payload["review_questions"]) == 5
    assert payload["brief_signal_counts"]["findings"] == 5
    assert payload["brief_signal_counts"]["business_risk_areas"] == 4
    assert payload["brief_signal_counts"]["high_priority_actions"] == 3
    assert payload["brief_signal_counts"]["owner_handoffs"] == 4
    assert payload["evidence_gate"]["self_authored_issue_counts_as_feedback"] is False
    assert payload["evidence_gate"]["current_external_feedback_items"] == 0
    assert payload["evidence_gate"]["current_confirmed_external_users"] == 0
    assert "issue #30" in markdown
    assert "Self-authored issue counts as feedback | `False`" in markdown
