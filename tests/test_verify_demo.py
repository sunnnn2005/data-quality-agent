from scripts.verify_support_ticket_demo import EXPECTED_CHECKS, EXPECTED_RULES, build_report_payload


def test_support_ticket_demo_verifier_matches_expected_artifact():
    payload = build_report_payload()

    assert payload["status"] == "FAIL"
    assert payload["quality_score"] == 24
    assert payload["row_count"] == 8
    assert payload["finding_count"] == 5
    assert len(payload["root_cause_hypotheses"]) == 3
    assert payload["root_cause_hypotheses"][0]["confidence"] >= payload["root_cause_hypotheses"][-1]["confidence"]
    assert payload["root_cause_hypotheses"][0]["evidence"]
    assert EXPECTED_CHECKS <= set(payload["checks"])
    assert EXPECTED_RULES <= set(payload["business_rule_references"])
