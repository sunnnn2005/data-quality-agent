from scripts.build_pilot_launch_control_room import (
    build_pilot_launch_control_room,
    render_markdown,
    verify_pilot_launch_control_room,
)


def test_pilot_launch_control_room_tracks_real_outcome_path_without_claiming_it():
    payload = build_pilot_launch_control_room()
    verification = verify_pilot_launch_control_room(payload)
    markdown = render_markdown(payload)

    assert verification["pilot_launch_control_room_verified"] is True
    assert payload["quicklink_action_count"] == 4
    assert payload["public_issue_thread_count"] == 4
    assert payload["launch_gate_count"] == 5
    assert payload["ready_gate_count"] == 3
    assert payload["blocked_gate_count"] == 2
    assert payload["target_outcome_count"] == 4
    assert payload["reviewer_send_plan_count"] == 3
    assert payload["current_claimable_external_outcomes"] == 0
    assert "external_feedback_items" in markdown
    assert "confirmed_external_users" in markdown
    assert "business_case_feedback_items" in markdown
    assert "github_stars" in markdown
    assert "external users" in payload["not_claimed"]
