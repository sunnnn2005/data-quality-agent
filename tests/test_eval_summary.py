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
    assert "paid model benchmark results" in payload["not_claimed"]
    assert "Evaluation Summary" in markdown
    assert "Tool-agent disabled fallback success | 1.0" in markdown
