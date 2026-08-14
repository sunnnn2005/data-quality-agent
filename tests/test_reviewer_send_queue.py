from scripts.build_reviewer_send_queue import (
    build_reviewer_send_queue,
    render_markdown,
    verify_reviewer_send_queue,
)


def test_reviewer_send_queue_prioritizes_real_evidence_without_claiming_results():
    payload = build_reviewer_send_queue()
    verification = verify_reviewer_send_queue(payload)
    markdown = render_markdown(payload)

    assert verification["reviewer_send_queue_verified"] is True
    assert payload["queue_count"] == 5
    assert payload["not_sent_count"] == 5
    assert payload["sent_count"] == 0
    assert payload["accepted_evidence_count"] == 0
    assert payload["scoreboard_remaining_evidence_items"] == 7
    assert payload["one_click_evidence_url"].endswith("/one-click-evidence-links.html")
    assert payload["next_sends"][0]["target_metric"] == "ai_engineer_review_items"
    assert payload["next_sends"][0]["recommended_channel"] == "LinkedIn DM or mentor email"
    assert payload["one_click_evidence_url"] in payload["next_sends"][0]["copy_ready_message"]
    assert {item["target_metric"] for item in payload["next_sends"]} == {
        "ai_engineer_review_items",
        "business_case_feedback_items",
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
    }
    assert all(item["status"] == "not_sent" for item in payload["next_sends"])
    assert "Only change an item from not_sent to sent" in payload["manual_execution_rule"]
    assert "Reviewer Send Queue" in markdown
    assert "One-click evidence page" in markdown
    assert "zero upgraded resume outcome claims" in payload["resume_safe_summary"]
