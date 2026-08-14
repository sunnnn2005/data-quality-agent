from scripts.build_public_traction_dashboard import (
    build_public_traction_dashboard_payload,
    render_markdown,
    verify_public_traction_dashboard,
)


def test_public_traction_dashboard_tracks_growth_surfaces_without_inflating_traction():
    payload = build_public_traction_dashboard_payload()
    verification = verify_public_traction_dashboard(payload)
    markdown = render_markdown(payload)

    assert verification["public_traction_dashboard_verified"] is True
    assert payload["traction_surface_count"] == 4
    assert payload["growth_channel_count"] == 21
    assert any(item["name"] == "pilot_feedback_tracker" for item in payload["growth_channels"])
    assert any(item["name"] == "External run review issue" for item in payload["growth_channels"])
    assert any(item["name"] == "AI Engineer review issue" for item in payload["growth_channels"])
    assert any(item["name"] == "Real model run review issue" for item in payload["growth_channels"])
    assert payload["tracked_funnel_steps"] == 5
    assert payload["demo_entrypoints_verified"] == 7
    assert payload["public_counts"]["stars"] == 0
    assert payload["public_counts"]["forks"] == 1
    assert payload["public_counts"]["issues_total"] >= 12
    assert payload["public_counts"]["confirmed_external_users"] == 0
    assert payload["public_counts"]["external_feedback_items"] == 0
    assert len(payload["resume_upgrade_rules"]) == 3
    assert all(rule["resume_status"] == "not_claimable_yet" for rule in payload["resume_upgrade_rules"])
    assert "Public Traction Dashboard" in markdown
    assert "GitHub star growth beyond the current public count" in markdown
