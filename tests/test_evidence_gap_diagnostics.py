from scripts.build_evidence_gap_diagnostics import (
    build_evidence_gap_diagnostics,
    render_markdown,
    verify_evidence_gap_diagnostics,
)


def test_evidence_gap_diagnostics_explains_why_current_issues_do_not_count():
    payload = build_evidence_gap_diagnostics()
    verify_evidence_gap_diagnostics(payload)

    assert payload["accepted_issue_count"] == 0
    assert payload["rejected_issue_count"] > 0
    assert payload["self_authored_rejection_count"] > 0
    assert payload["accepted_counts"]["confirmed_external_users"] == 0
    assert payload["accepted_counts"]["ai_engineer_review_items"] == 0
    assert len(payload["nearest_unlock_paths"]) == 3
    assert any(item["target_metric"] == "ai_engineer_review_items" for item in payload["nearest_unlock_paths"])
    assert any(item["reason"] == "self-authored issue" for item in payload["top_failure_reasons"])
    assert "Self-authored planning issues remain excluded from outcome metrics." in payload["not_claimed"]


def test_evidence_gap_diagnostics_markdown_gives_reviewer_next_steps():
    markdown = render_markdown(build_evidence_gap_diagnostics())

    assert "# Evidence Gap Diagnostics" in markdown
    assert "Top Failure Reasons" in markdown
    assert "Evidence Type Gaps" in markdown
    assert "Nearest Unlock Paths" in markdown
    assert "issues/new?template=ai_engineer_review.md" in markdown
