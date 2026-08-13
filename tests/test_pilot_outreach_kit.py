from scripts.build_pilot_outreach_kit import (
    build_pilot_outreach_kit_payload,
    render_markdown,
    verify_pilot_outreach_kit,
)


def test_pilot_outreach_kit_supports_real_feedback_without_inflating_usage():
    payload = build_pilot_outreach_kit_payload()
    verification = verify_pilot_outreach_kit(payload)
    markdown = render_markdown(payload)

    assert verification["pilot_outreach_kit_verified"] is True
    assert len(payload["target_audiences"]) == 4
    assert len(payload["review_paths"]) == 10
    assert payload["review_paths"]["pilot_feedback_tracker"].endswith("/issues/16")
    assert payload["review_paths"]["public_review_request"].endswith("/issues/17")
    assert len(payload["outreach_messages"]) == 3
    assert payload["success_metrics"]["external_feedback_items"] == 0
    assert payload["success_metrics"]["confirmed_external_users"] == 0
    assert payload["success_metrics"]["target_first_feedback_items"] == 3
    assert "Pilot Outreach Kit" in markdown
