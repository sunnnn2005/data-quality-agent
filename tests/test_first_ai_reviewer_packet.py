from scripts.build_first_ai_reviewer_packet import (
    build_first_ai_reviewer_packet,
    render_markdown,
    verify_first_ai_reviewer_packet,
)


def test_first_ai_reviewer_packet_gives_one_countable_review_path_without_claiming_it():
    payload = build_first_ai_reviewer_packet()
    verification = verify_first_ai_reviewer_packet(payload)
    markdown = render_markdown(payload)

    assert verification["first_ai_reviewer_packet_verified"] is True
    assert payload["target_metric"] == "ai_engineer_review_items"
    assert payload["current_count"] == 0
    assert payload["required_count"] == 1
    assert payload["resume_status"] == "ready_to_send_not_claimable"
    assert len(payload["inspection_targets"]) == 5
    assert len(payload["optional_local_checks"]) == 3
    assert len(payload["review_questions"]) == 5
    assert payload["current_ai_engineer_signal_count"] == 8
    assert payload["current_agent_maturity_implemented"] == 15
    assert payload["current_agent_maturity_partial"] == 4
    assert any(item["path"] == "app/tool_agent.py" for item in payload["inspection_targets"])
    assert any(item["path"] == "app/models.py" for item in payload["inspection_targets"])
    assert "template=ai_engineer_review.md" in payload["submission_url"]
    assert "accepted AI Engineer review" in payload["not_claimed"]
    assert "First AI Reviewer Packet" in markdown
    assert "Locked until a non-owner public review issue passes the evidence gate" in markdown
