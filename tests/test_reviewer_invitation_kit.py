from scripts.build_reviewer_invitation_kit import (
    build_reviewer_invitation_kit_payload,
    render_markdown,
    verify_reviewer_invitation_kit,
)


def test_reviewer_invitation_kit_routes_copy_ready_messages_to_public_evidence():
    payload = build_reviewer_invitation_kit_payload()
    verification = verify_reviewer_invitation_kit(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_invitation_kit_verified"] is True
    assert len(payload["invitation_targets"]) == 5
    assert {item["funnel_stage"] for item in payload["invitation_targets"]} == {
        "visit_public_demo",
        "run_local_replay",
        "confirm_external_use",
        "submit_business_case",
    }
    assert payload["current_baseline"]["external_feedback_items"] == 0
    assert payload["current_baseline"]["confirmed_external_users"] == 0
    assert payload["success_thresholds"]["resume_feedback_signal"] == 3
    assert payload["success_thresholds"]["confirmed_external_user_signal"] == 1
    assert all("issues/new" in item["submission_url"] for item in payload["invitation_targets"])
    assert "Reviewer Invitation Kit" in markdown
    assert "copy-ready messages" in markdown
