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
    assert len(payload["invitation_targets"]) == 6
    assert payload["invitation_count"] == 6
    assert payload["distinct_funnel_stage_count"] == 5
    assert payload["public_evidence_path_count"] == 5
    assert payload["one_click_evidence_links"]["link_count"] == 4
    assert payload["one_click_evidence_links"]["target_metric_count"] == 4
    assert payload["one_click_evidence_links"]["accepted_issue_count"] == 0
    assert payload["one_click_evidence_links"]["claimable_resume_metric_count"] == 0
    assert payload["short_share_card"]["primary_url"].endswith("/one-click-evidence-links.html")
    assert "8-12 minutes" in payload["short_share_card"]["title"]
    assert "8-12 minutes" in payload["short_share_card"]["copy_message"]
    assert "Opening a one-click issue link is not evidence by itself" in payload["short_share_card"]["counts_only_after"]
    assert {item["funnel_stage"] for item in payload["invitation_targets"]} == {
        "visit_public_demo",
        "run_local_replay",
        "confirm_external_use",
        "submit_business_case",
        "ai_engineer_review",
    }
    assert payload["current_baseline"]["external_feedback_items"] == 0
    assert payload["current_baseline"]["confirmed_external_users"] == 0
    assert payload["current_baseline"]["ai_engineer_review_items"] == 0
    assert payload["public_review_request"]["issue_number"] == 17
    assert payload["public_review_request"]["url"].endswith("/issues/17")
    assert payload["success_thresholds"]["resume_feedback_signal"] == 3
    assert payload["success_thresholds"]["confirmed_external_user_signal"] == 1
    assert payload["success_thresholds"]["ai_engineer_review_signal"] == 1
    assert any(item["counts_toward"] == "ai_engineer_review_items" for item in payload["invitation_targets"])
    assert all("issues/new" in item["submission_url"] for item in payload["invitation_targets"])
    assert any("one-click evidence page" in item["message"] for item in payload["invitation_targets"])
    assert "Reviewer Invitation Kit" in markdown
    assert "copy-ready messages" in markdown
    assert "One-Click Reviewer Share Card" in markdown
    assert "Claimable resume metric count: 0" in markdown
