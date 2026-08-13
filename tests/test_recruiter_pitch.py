from scripts.build_recruiter_pitch import (
    build_recruiter_pitch_payload,
    render_markdown,
    verify_recruiter_pitch,
)


def test_recruiter_pitch_turns_verified_evidence_into_safe_application_language():
    payload = build_recruiter_pitch_payload()
    verification = verify_recruiter_pitch(payload)
    markdown = render_markdown(payload)

    assert verification["recruiter_pitch_verified"] is True
    assert len(payload["resume_bullets"]) == 3
    assert "AI Engineer Intern" in payload["target_roles"]
    assert "Software Engineer Intern" in payload["target_roles"]
    assert verification["evidence_link_count"] == 10
    assert any(link["label"] == "Inspect public traction dashboard" for link in payload["evidence_links"])
    assert any(link["label"] == "Inspect business problem casebook" for link in payload["evidence_links"])
    assert any(link["label"] == "Inspect feedback intake quality" for link in payload["evidence_links"])
    assert payload["honest_baseline"]["stars"] == 0
    assert payload["honest_baseline"]["confirmed_external_users"] == 0
    assert "Recruiter Pitch" in markdown
