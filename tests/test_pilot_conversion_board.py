from scripts.build_pilot_conversion_board import build_pilot_conversion_board_payload, verify_pilot_conversion_board


def test_pilot_conversion_board_separates_readiness_from_outcome_claims():
    payload = build_pilot_conversion_board_payload()
    verification = verify_pilot_conversion_board(payload)

    assert verification["pilot_conversion_board_verified"] is True
    assert payload["stage_count"] == 6
    assert payload["claimable_stage_count"] == 2
    assert payload["blocked_stage_count"] == 4
    assert len(payload["current_resume_safe_claims"]) == 2
    assert all(not item["resume_claim_allowed"] for item in payload["stages"] if item["stage"].startswith("confirmed"))
    assert "external users" in payload["not_claimed"]
