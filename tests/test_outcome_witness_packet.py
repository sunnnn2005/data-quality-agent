from scripts.build_outcome_witness_packet import (
    build_outcome_witness_packet,
    render_markdown,
    verify_outcome_witness_packet,
)


def test_outcome_witness_packet_turns_reviewers_into_countable_public_tasks():
    payload = build_outcome_witness_packet()
    verification = verify_outcome_witness_packet(payload)
    markdown = render_markdown(payload)

    assert verification["outcome_witness_packet_verified"] is True
    assert payload["witness_card_count"] == 5
    assert payload["target_metric_count"] == 5
    assert payload["total_required_evidence_fields"] == 22
    assert payload["resume_outcome_upgraded"] is False
    assert all(value == 0 for value in payload["current_public_counts"].values())

    metrics = {card["target_metric"] for card in payload["witness_cards"]}
    assert metrics == {
        "ai_engineer_review_items",
        "confirmed_external_users",
        "external_feedback_items",
        "business_case_feedback_items",
        "reproducible_feedback_items",
    }
    assert all(card["submission_url"].startswith("https://github.com/") for card in payload["witness_cards"])
    assert all("Counts only" in card["counting_rule"] for card in payload["witness_cards"])
    assert all("permission" in card["permission_sentence"].lower() for card in payload["witness_cards"])
    assert all("no raw customer data" in card["no_private_data_sentence"] for card in payload["witness_cards"])
    assert "non-owner public GitHub issue passes the evidence gate" in str(payload)
    assert "Witness cards are invitations, not users or feedback." in payload["not_claimed"]
    assert "Outcome Witness Packet" in markdown
    assert "Current Public Counts" in markdown


def test_outcome_witness_packet_rejects_unverified_resume_upgrade():
    payload = build_outcome_witness_packet()
    payload["resume_outcome_upgraded"] = True

    try:
        verify_outcome_witness_packet(payload)
    except AssertionError as exc:
        assert "must not upgrade resume outcomes" in str(exc)
    else:
        raise AssertionError("expected witness packet verification to reject resume upgrade")
