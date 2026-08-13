from scripts.build_demo_usage_baseline import (
    build_demo_usage_baseline_payload,
    render_markdown,
    verify_demo_usage_baseline,
)


def test_demo_usage_baseline_tracks_public_funnel_without_usage_claims():
    payload = build_demo_usage_baseline_payload()
    verification = verify_demo_usage_baseline(payload)
    markdown = render_markdown(payload)

    assert verification["demo_usage_baseline_verified"] is True
    assert verification["tracked_funnel_steps"] == 5
    assert payload["tracked_counts"]["stars"] == 0
    assert payload["tracked_counts"]["forks"] == 1
    assert payload["tracked_counts"]["external_feedback_items"] == 0
    assert payload["tracked_counts"]["confirmed_external_users"] == 0
    assert all(payload["demo_entrypoints_verified"].values())
    assert {item["step"] for item in payload["tracked_usage_funnel"]} == {
        "view_public_demo",
        "submit_feedback_issue",
        "confirmed_external_user",
        "star_repository",
        "fork_repository",
    }
    assert "No visitor analytics are claimed" in payload["not_claimed"][0]
    assert "Demo Usage Baseline" in markdown
    assert "No external users are claimed." in markdown
