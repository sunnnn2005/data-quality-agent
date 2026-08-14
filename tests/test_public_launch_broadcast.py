from scripts.build_public_launch_broadcast import (
    build_public_launch_broadcast,
    render_markdown,
    verify_public_launch_broadcast,
)


def test_public_launch_broadcast_records_public_comment_without_counting_outcomes():
    payload = build_public_launch_broadcast()
    verification = verify_public_launch_broadcast(payload)
    markdown = render_markdown(payload)

    assert verification["public_launch_broadcast_verified"] is True
    assert payload["broadcast_count"] == 1
    assert payload["published_broadcast_count"] == 1
    assert payload["public_broadcasts"][0]["counts_as_outcome"] is False
    assert "issuecomment-5289908319" in payload["public_broadcasts"][0]["public_url"]
    assert set(payload["current_outcome_counts"].values()) == {0}
    assert "owner-authored launch posts" in markdown
    assert "# Public Launch Broadcast" in markdown
