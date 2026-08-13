from scripts.build_github_traffic_snapshot import (
    build_github_traffic_snapshot,
    render_markdown,
    verify_github_traffic_snapshot,
)


def test_github_traffic_snapshot_separates_interest_from_users():
    payload = build_github_traffic_snapshot(
        {
            "views": {"count": 9, "uniques": 3, "views": []},
            "clones": {"count": 79, "uniques": 50, "clones": []},
            "referrers": [{"referrer": "github.com", "count": 6, "uniques": 3}],
            "paths": [{"path": "/sunnnn2005/data-quality-agent", "title": "Overview", "count": 3, "uniques": 3}],
        }
    )
    verification = verify_github_traffic_snapshot(payload)
    markdown = render_markdown(payload)

    assert verification["github_traffic_snapshot_verified"] is True
    assert payload["traffic_available"] is True
    assert payload["views"]["count"] == 9
    assert payload["views"]["uniques"] == 3
    assert payload["clones"]["count"] == 79
    assert payload["clones"]["uniques"] == 50
    assert payload["traffic_metrics"] == {
        "view_count": 9,
        "unique_visitors": 3,
        "clone_count": 79,
        "unique_cloners": 50,
    }
    assert "confirmed users" in payload["resume_policy"]
    assert "customer feedback" in payload["resume_policy"]
    assert "GitHub Traffic Snapshot" in markdown
    assert "Unique cloners | 50" in markdown


def test_github_traffic_snapshot_handles_unavailable_traffic():
    payload = build_github_traffic_snapshot(
        {
            "views": {"error": "CalledProcessError"},
            "clones": {"error": "CalledProcessError"},
            "referrers": [],
            "paths": [],
        }
    )
    verification = verify_github_traffic_snapshot(payload)

    assert verification["github_traffic_snapshot_verified"] is True
    assert payload["traffic_available"] is False
    assert payload["views"]["count"] == 0
    assert payload["clones"]["count"] == 0
    assert payload["traffic_metrics"]["unique_cloners"] == 0
