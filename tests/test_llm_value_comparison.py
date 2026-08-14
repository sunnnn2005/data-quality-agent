from scripts.build_llm_value_comparison import (
    build_llm_value_comparison,
    render_html,
    render_markdown,
    verify_llm_value_comparison,
)


def test_llm_value_comparison_quantifies_adaptive_strategy_lift():
    payload = build_llm_value_comparison()
    verification = verify_llm_value_comparison(payload)
    markdown = render_markdown(payload)
    html = render_html(payload)

    assert verification["llm_value_comparison_verified"] is True
    assert payload["scenario_count"] == 14
    assert payload["fixed_generic_average_recall"] < payload["adaptive_strategy_average_recall"]
    assert payload["absolute_recall_lift"] >= 0.3
    assert payload["improved_scenario_count"] >= 8
    assert "Fixed generic average recall" in markdown
    assert "Adaptive strategy average recall" in markdown
    assert "LLM Value Comparison" in html
    assert "external adoption" in html


def test_llm_value_comparison_is_resume_safe_and_not_user_claiming():
    payload = build_llm_value_comparison()

    assert "paid model benchmark results" in payload["not_claimed"]
    assert "enterprise customer impact" in payload["not_claimed"]
    assert "external adoption" in payload["resume_safe_summary"].lower()
    assert "production users" not in payload["resume_safe_summary"].lower()
    assert all(
        row["adaptive_strategy_recall"] >= row["fixed_generic_recall"]
        for row in payload["comparison_rows"]
    )
