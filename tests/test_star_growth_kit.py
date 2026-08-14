from scripts.build_star_growth_kit import (
    build_star_growth_kit_payload,
    render_markdown,
    verify_star_growth_kit,
)


def test_star_growth_kit_tracks_ethical_growth_without_inflating_stars():
    payload = build_star_growth_kit_payload()
    verification = verify_star_growth_kit(payload)
    markdown = render_markdown(payload)

    assert verification["star_growth_kit_verified"] is True
    assert payload["current_public_counts"]["stars"] == 0
    assert payload["current_public_counts"]["forks"] == 1
    assert payload["current_public_counts"]["issues_total"] == 25
    assert payload["topic_readiness"]["ready"] is True
    assert len(payload["topic_readiness"]["required_topics"]) == 16
    assert "llm-agent" in payload["topic_readiness"]["current_topics"]
    assert "tool-calling" in payload["topic_readiness"]["current_topics"]
    assert len(payload["ethical_growth_actions"]) == 4
    assert len(payload["resume_upgrade_rules"]) == 4
    assert payload["traffic_snapshot"]["source"] == "GitHub traffic API rolling 14-day window"
    assert "confirmed users" in payload["traffic_snapshot"]["resume_policy"]
    assert "repository interest" in {rule["signal"] for rule in payload["resume_upgrade_rules"]}
    assert all(rule["resume_status"] == "not_claimable_yet" for rule in payload["resume_upgrade_rules"])
    assert "fake or incentivized stars" in payload["not_claimed"]
    assert "confirmed users from traffic alone" in payload["not_claimed"]
    assert "Star Growth Kit" in markdown
    assert "Traffic Snapshot" in markdown
    assert "Topic readiness: `True`" in markdown
