from scripts.build_contributor_conversion_kit import (
    build_contributor_conversion_kit,
    render_markdown,
    verify_contributor_conversion_kit,
)


def test_contributor_conversion_kit_routes_public_actions_to_resume_evidence():
    payload = build_contributor_conversion_kit()
    verification = verify_contributor_conversion_kit(payload)
    markdown = render_markdown(payload)

    assert verification["contributor_conversion_kit_verified"] is True
    assert payload["conversion_path_count"] == 5
    assert payload["evidence_gate_count"] == 5
    assert payload["contributor_claimable_count"] == 0
    assert payload["current_public_counts"]["stars"] == 0
    assert payload["current_public_counts"]["forks"] == 1
    assert payload["current_public_counts"]["confirmed_external_users"] == 0
    assert payload["current_public_counts"]["external_feedback_items"] == 0
    assert payload["current_public_counts"]["feature_feedback_items_excluded_from_external_claims"] == 8
    assert {item["id"] for item in payload["conversion_paths"]} == {
        "demo_feedback_review",
        "business_data_replay",
        "ai_engineer_review",
        "business_case_review",
        "ethical_star_or_fork",
    }
    ai_review = next(item for item in payload["conversion_paths"] if item["id"] == "ai_engineer_review")
    assert ai_review["entrypoint_url"].endswith("template=ai_engineer_review.md")
    assert "tool-calling loop" in ai_review["copy_ready_message"]
    replay = next(item for item in payload["conversion_paths"] if item["id"] == "business_data_replay")
    assert replay["entrypoint_url"].endswith("template=business_data_replay.md")
    star = next(item for item in payload["conversion_paths"] if item["id"] == "ethical_star_or_fork")
    assert "please do not star it unless it is actually useful" in star["copy_ready_message"]
    assert "public non-owner issue" in payload["counts_only_after"]
    assert "0 contributor-claimable outcomes" in payload["resume_safe_summary"]
    assert "Conversion Paths" in markdown
    assert "Copy-Ready Asks" in markdown
    assert "Not Claimed" in markdown
