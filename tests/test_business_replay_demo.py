from scripts.build_business_replay_demo import (
    build_business_replay_demo,
    render_markdown,
    verify_business_replay_demo,
)


def test_business_replay_demo_verifies_anonymized_csv_without_claiming_external_usage():
    payload = build_business_replay_demo()
    verification = verify_business_replay_demo(payload)
    markdown = render_markdown(payload)

    assert verification["business_replay_demo_verified"] is True
    assert payload["dataset"]["row_count"] == 8
    assert payload["dataset"]["contains_real_company_data"] is False
    assert payload["dataset"]["contains_pii"] is False
    assert payload["quality_report_summary"]["status"] == "FAIL"
    assert payload["quality_report_summary"]["quality_score"] == 24
    assert payload["quality_report_summary"]["finding_count"] == 5
    assert payload["quality_report_summary"]["check_count"] == 4
    assert payload["quality_report_summary"]["business_rule_reference_count"] == 4
    assert payload["quality_report_summary"]["root_cause_hypothesis_count"] == 3
    assert payload["quality_report_summary"]["verification_passed"] is True
    assert "external user replay" in payload["not_claimed"]
    assert "Business Replay Demo" in markdown
    assert "examples/support_tickets.csv" in markdown
