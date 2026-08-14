from scripts.build_pilot_evidence_quicklink import (
    build_pilot_evidence_quicklink,
    render_html,
    render_markdown,
    verify_pilot_evidence_quicklink,
)


def test_pilot_evidence_quicklink_routes_reviewers_to_real_countable_outcomes():
    payload = build_pilot_evidence_quicklink()
    verification = verify_pilot_evidence_quicklink(payload)
    html = render_html(payload)
    markdown = render_markdown(payload)

    assert verification["pilot_evidence_quicklink_verified"] is True
    assert payload["action_count"] == 4
    assert payload["target_metric_count"] == 4
    assert payload["total_evidence_fields"] == 17
    assert payload["current_counts"]["external_feedback_items"] == 0
    assert payload["current_counts"]["confirmed_external_users"] == 0
    assert payload["current_counts"]["reproducible_feedback_items"] == 0
    assert payload["current_counts"]["business_case_feedback_items"] == 0
    assert "Try the public demo" in html
    assert "Run the container or local demo" in html
    assert "Replay business-shaped data" in html
    assert "template=business_data_replay.md" in html
    assert "Submit an anonymized business problem" in markdown
    assert "selected tools shown in the agent trace" in markdown
    assert "external users" in payload["not_claimed"]
    assert "external reproducible replays" in payload["not_claimed"]
