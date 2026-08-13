from scripts.build_outcome_upgrade_playbook import (
    build_outcome_upgrade_playbook,
    render_markdown,
    verify_outcome_upgrade_playbook,
)


def test_outcome_upgrade_playbook_blocks_resume_outcome_claims_until_public_evidence_exists():
    payload = build_outcome_upgrade_playbook()
    verification = verify_outcome_upgrade_playbook(payload)
    markdown = render_markdown(payload)

    assert verification["outcome_upgrade_playbook_verified"] is True
    assert payload["upgrade_rule_count"] == 5
    assert payload["blocked_upgrade_rule_count"] == 5
    assert payload["resume_status"] == "baseline_only"
    assert payload["current_public_counts"]["stars"] == 0
    assert payload["current_public_counts"]["confirmed_external_users"] == 0
    assert payload["current_public_counts"]["external_feedback_items"] == 0
    assert payload["current_public_counts"]["business_case_feedback_items"] == 0
    assert all(rule["status"] == "not_claimable_yet" for rule in payload["upgrade_rules"])
    assert {rule["id"] for rule in payload["upgrade_rules"]} == {
        "first_confirmed_external_run",
        "pilot_feedback_signal",
        "reproducible_bug_signal",
        "business_case_signal",
        "github_interest_signal",
    }
    assert "Public GitHub Pages demo" in payload["claimable_now"]
    assert "Outcome Upgrade Playbook" in markdown
    assert "not_claimable_yet" in markdown
