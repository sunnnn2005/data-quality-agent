from scripts.build_resume_live_proof_snapshot import (
    load_json,
    OUTCOME_EVIDENCE_PATH,
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
    assert payload["verified_now"]["passing_test_baseline"] == 245
    assert payload["verified_now"]["verified_resume_claims"] == len(load_json(OUTCOME_EVIDENCE_PATH)["claims"])
    assert payload["verified_now"]["implemented_agent_capabilities"] == 16
    health_count = payload["verified_now"]["public_evidence_health"].split(" ", maxsplit=1)[0]
    passed_count, check_count = (int(value) for value in health_count.split("/", maxsplit=1))
    assert passed_count == check_count
    assert payload["evidence_links"]["business_pilot_issue"].endswith("/issues/31")
    assert "GHCR image" in payload["resume_safe_bullets"][0]
    assert "without claiming completed pilots or enterprise adoption" in payload["resume_safe_bullets"][3]
    assert "confirmed external users" in payload["blocked_until_external_evidence"]
    assert "Self-authored issues" in payload["resume_policy"]
    assert "Resume Live Proof Snapshot" in markdown
    assert "Business Pilot Issue" in markdown
