from scripts.build_pilot_program_plan import (
    build_pilot_program_plan_payload,
    render_markdown,
    verify_pilot_program_plan,
)


def test_pilot_program_plan_defines_feedback_thresholds_before_resume_claims():
    payload = build_pilot_program_plan_payload()
    verification = verify_pilot_program_plan(payload)
    markdown = render_markdown(payload)

    assert verification["pilot_program_plan_verified"] is True
    assert len(payload["participant_segments"]) == 3
    assert len(payload["weekly_plan"]) == 3
    assert payload["success_thresholds"]["current_external_feedback_items"] == 0
    assert payload["success_thresholds"]["current_confirmed_external_users"] == 0
    assert payload["success_thresholds"]["minimum_feedback_items_before_resume_claim"] == 3
    assert payload["success_thresholds"]["minimum_confirmed_users_before_user_claim"] == 1
    assert "Pilot Program Plan" in markdown
