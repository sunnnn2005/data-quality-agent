from scripts.build_github_discovery_profile import (
    build_github_discovery_profile,
    render_markdown,
    verify_github_discovery_profile,
)


def test_github_discovery_profile_verifies_public_discovery_without_claiming_traction():
    payload = build_github_discovery_profile()
    verification = verify_github_discovery_profile(payload)
    markdown = render_markdown(payload)

    assert verification["github_discovery_profile_verified"] is True
    assert payload["is_private"] is False
    assert payload["discovery_ready"] is True
    assert payload["topic_count"] == 20
    assert "agentic-ai" in payload["topics"]
    assert "ai-engineering" in payload["topics"]
    assert "evaluation" in payload["topics"]
    assert "llm-agent" in payload["topics"]
    assert "observability" in payload["topics"]
    assert "tool-calling" in payload["topics"]
    assert "data-reliability" in payload["topics"]
    assert payload["current_public_counts"]["stars"] == 0
    assert payload["current_public_counts"]["adoption_metric_stars"] == 0
    assert len(payload["reviewer_entrypoints"]) == 6
    assert "external users" in payload["not_claimed"]
    assert "customer feedback" in payload["not_claimed"]
    assert "GitHub Discovery Profile" in markdown
    assert "Discovery ready: `True`" in markdown
