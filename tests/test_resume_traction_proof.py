from scripts.build_resume_traction_proof import (
    build_resume_traction_proof,
    render_markdown,
    verify_resume_traction_proof,
)


def test_resume_traction_proof_separates_claimable_launch_from_unproven_growth():
    payload = build_resume_traction_proof()
    verification = verify_resume_traction_proof(payload)
    markdown = render_markdown(payload)

    assert verification["resume_traction_proof_verified"] is True
    assert payload["claimable_now_count"] == 4
    assert payload["future_claim_count"] == 4
    assert payload["blocked_claim_count"] == 5
    assert payload["public_counts"]["stars"] == 0
    assert payload["public_counts"]["confirmed_external_users"] == 0
    assert payload["public_counts"]["external_feedback_items"] == 0
    assert payload["linked_public_traction_surfaces"] == 4
    assert payload["linked_growth_channels"] == 19
    assert all(item["status"] == "claimable" for item in payload["claimable_now"])
    assert all(item["status"] == "not_claimable_yet" for item in payload["future_claims"])
    assert "Launched a public GitHub Pages demo" in markdown
    assert "Do not claim active users" in markdown
    assert "Do not convert GitHub traffic views into user counts" in markdown
