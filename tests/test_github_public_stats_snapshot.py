from scripts.build_github_public_stats_snapshot import (
    build_github_public_stats_snapshot,
    render_markdown,
    verify_github_public_stats_snapshot,
)


def test_github_public_stats_snapshot_records_live_repo_signals_without_inflating_outcomes():
    payload = build_github_public_stats_snapshot(
        {
            "default_branch": "main",
            "forks_count": 1,
            "html_url": "https://github.com/sunnnn2005/data-quality-agent",
            "open_issues_count": 26,
            "pushed_at": "2026-08-14T06:10:36Z",
            "stargazers_count": 0,
            "subscribers_count": 0,
            "visibility": "public",
            "watchers_count": 0,
        }
    )
    verification = verify_github_public_stats_snapshot(payload)
    markdown = render_markdown(payload)

    assert verification["github_public_stats_snapshot_verified"] is True
    assert payload["source_available"] is True
    assert payload["public_stats"] == {
        "forks": 1,
        "open_issues": 26,
        "stars": 0,
        "subscribers": 0,
        "watchers": 0,
    }
    assert "Stars | 0" in markdown
    assert "confirmed users" in payload["resume_policy"]
    assert "customer feedback" in payload["resume_policy"]
    assert "stars above the live public count" in payload["not_claimed"]


def test_github_public_stats_snapshot_handles_unavailable_source():
    payload = build_github_public_stats_snapshot({"error": "CalledProcessError"})
    verification = verify_github_public_stats_snapshot(payload)

    assert verification["github_public_stats_snapshot_verified"] is True
    assert payload["source_available"] is False
    assert payload["public_stats"]["stars"] == 0
    assert payload["public_stats"]["forks"] == 0
