from scripts.build_agent_maturity_audit import (
    build_agent_maturity_audit,
    render_markdown,
    verify_agent_maturity_audit,
)


def test_agent_maturity_audit_maps_agent_claims_to_evidence():
    payload = build_agent_maturity_audit()
    verification = verify_agent_maturity_audit(payload)
    markdown = render_markdown(payload)

    assert verification["agent_maturity_audit_verified"] is True
    assert payload["audit_row_count"] == 20
    assert payload["status_counts"]["implemented"] == 15
    assert payload["status_counts"]["partial"] == 4
    assert payload["status_counts"]["not_claimed"] == 1
    assert payload["cross_checks"]["allowed_tools"] == 9
    assert payload["cross_checks"]["capability_matrix_implemented"] == 13
    assert payload["cross_checks"]["agent_readiness_implemented"] == 16
    assert payload["cross_checks"]["accepted_real_model_runs"] == 0
    assert payload["cross_checks"]["real_model_preflight_status"] == "not_ready"
    assert {row["area"] for row in payload["audit_rows"]} >= {
        "LLM decision-making",
        "Controlled tools",
        "Agent loop",
        "Planning and replanning",
        "RAG",
        "Real-model production evidence",
    }
    assert any(
        row["status"] == "implemented" and row["area"] == "Planning and replanning"
        for row in payload["audit_rows"]
    )
    assert any(row["status"] == "partial" and row["area"] == "RAG" for row in payload["audit_rows"])
    assert any(row["status"] == "not_claimed" and row["area"] == "Real-model production evidence" for row in payload["audit_rows"])
    assert "20-point LLM agent maturity audit" in payload["resume_safe_summary"]
    assert "accepted real-model benchmark run" in payload["not_claimed"]
    assert "Agent Maturity Audit" in markdown
    assert "Next Upgrades" in markdown
