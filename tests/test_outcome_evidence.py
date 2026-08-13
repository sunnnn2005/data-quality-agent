from scripts.verify_outcome_evidence import verify_manifest


def test_outcome_evidence_manifest_is_resume_safe():
    result = verify_manifest()

    assert result["claim_count"] >= 6
    assert result["not_claimed_count"] >= 3
    assert result["resume_evidence_page"] == 1
