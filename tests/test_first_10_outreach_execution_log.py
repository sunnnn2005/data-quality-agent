from scripts.build_first_10_outreach_execution_log import (
    build_first_10_outreach_execution_log,
    render_markdown,
    verify_first_10_outreach_execution_log,
)


def test_first_10_outreach_execution_log_is_actionable_without_claiming_results():
    payload = build_first_10_outreach_execution_log()
    result = verify_first_10_outreach_execution_log(payload)
    markdown = render_markdown(payload)

    assert result["first_10_outreach_execution_log_verified"] is True
    assert payload["entry_count"] == 10
    assert payload["public_issue_entrypoint_count"] == 10
    assert payload["sent_count"] == 0
    assert payload["accepted_evidence_count"] == 0
    assert payload["resume_status"] == "execution_ready_not_claimable"
    assert "slot_07_ai_engineer_review" in markdown
    assert "Copy-ready message" in markdown
    assert "zero claimable external outcomes" in payload["resume_safe_summary"]
