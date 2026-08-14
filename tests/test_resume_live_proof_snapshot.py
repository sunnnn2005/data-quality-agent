from scripts.build_resume_live_proof_snapshot import (
    build_resume_live_proof_snapshot_payload,
    render_markdown,
    verify_resume_live_proof_snapshot,
)


def test_resume_live_proof_snapshot_is_concise_and_honest():
    payload = build_resume_live_proof_snapshot_payload()
    verification = verify_resume_live_proof_snapshot(payload)
    markdown = render_markdown(payload)

    assert verification["resume_live_proof_snapshot_verified"] is True
    assert verification["resume_safe_bullet_count"] == 4
    assert payload["verified_now"]["passing_test_baseline"] == 225
    assert payload["verified_now"]["verified_resume_claims"] == 94
    assert payload["verified_now"]["implemented_agent_capabilities"] == 16
    assert payload["verified_now"]["public_evidence_health"] == "103/103 public evidence checks passing"
    assert payload["evidence_links"]["business_pilot_issue"].endswith("/issues/31")
    assert "GHCR image" in payload["resume_safe_bullets"][0]
    assert "without claiming completed pilots or enterprise adoption" in payload["resume_safe_bullets"][3]
    assert "confirmed external users" in payload["blocked_until_external_evidence"]
    assert "Self-authored issues" in payload["resume_policy"]
    assert "Resume Live Proof Snapshot" in markdown
    assert "Business Pilot Issue" in markdown
