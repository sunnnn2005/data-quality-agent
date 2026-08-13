from scripts.build_eval_summary import build_eval_summary_payload, render_markdown, verify_eval_summary


def test_eval_summary_publishes_resume_safe_agent_metrics():
    payload = build_eval_summary_payload()
    verification = verify_eval_summary(payload)
    markdown = render_markdown(payload)

    assert verification["eval_summary_verified"] is True
    assert payload["scenario_count"] == 3
    assert payload["deterministic_baseline"]["finding_recall"] == 1.0
    assert payload["deterministic_baseline"]["evidence_support_rate"] == 1.0
    assert payload["tool_agent_disabled_fallback"]["fallback_success_rate"] == 1.0
    assert payload["tool_planning_coverage"]["available_tool_count"] == 7
    assert payload["tool_planning_coverage"]["required_tools_present"] is True
    assert payload["tool_planning_coverage"]["scenario_strategy_recommendation_recall"] >= 0.88
    assert "paid model benchmark results" in payload["not_claimed"]
    assert "Evaluation Summary" in markdown
    assert "Tool-agent disabled fallback success | 1.0" in markdown
    assert "Available agent tools | 7" in markdown


def test_eval_summary_verifies_tool_planning_coverage_for_agent_claims():
    payload = build_eval_summary_payload()
    tool_planning = payload["tool_planning_coverage"]

    assert "select_quality_strategy" in tool_planning["tool_names"]
    assert "retrieve_dataset_memory" in tool_planning["tool_names"]
    assert "retrieve_business_rules" in tool_planning["tool_names"]
    assert "build_quality_report" in tool_planning["tool_names"]
    assert len(tool_planning["scenario_strategy_rows"]) == 3
    assert all(row["matched_expected_findings"] for row in tool_planning["scenario_strategy_rows"])
