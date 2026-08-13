from scripts.build_community_growth_baseline import (
    build_community_growth_baseline,
    render_markdown,
    verify_community_growth_baseline,
)


def test_community_growth_baseline_verifies_public_contribution_paths_without_adoption_claims():
    payload = build_community_growth_baseline()
    verification = verify_community_growth_baseline(payload)
    markdown = render_markdown(payload)

    assert verification["community_growth_baseline_verified"] is True
    assert payload["issue_template_count"] == 6
    assert payload["label_count"] == 7
    assert len(payload["public_growth_channels"]) == 7
    assert "business_data_replay.md" in payload["issue_templates"]
    assert "business-data-replay" in payload["required_labels"]
    assert payload["current_public_counts"]["stars"] == 0
    assert payload["current_public_counts"]["forks"] == 1
    assert payload["current_public_counts"]["external_feedback_items"] == 0
    assert all(payload["contribution_paths"].values())
    assert "external contributors" in payload["not_claimed"]
    assert "community adoption" in payload["not_claimed"]
    assert "Community Growth Baseline" in markdown
