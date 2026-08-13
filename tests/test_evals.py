from app.evals import evaluate_deterministic, evaluate_tool_agent, load_scenarios
from app.tool_agent import LLMDataQualityAgent


def test_evaluation_scenarios_load_from_jsonl():
    scenarios = load_scenarios()

    assert len(scenarios) >= 14
    assert {scenario.dataset_id for scenario in scenarios} >= {"orders_daily", "payments_events", "customer_profiles"}


def test_deterministic_eval_scores_known_quality_scenarios():
    result = evaluate_deterministic()

    assert result["name"] == "deterministic"
    assert result["scenario_count"] == 14
    assert result["status_accuracy"] == 1.0
    assert result["finding_recall"] == 1.0
    assert result["evidence_support_rate"] == 1.0
    assert result["fallback_success_rate"] == 1.0
    assert result["final_report_attachment_rate"] == 1.0


def test_tool_agent_eval_records_disabled_fallback_without_model_key():
    result = evaluate_tool_agent(LLMDataQualityAgent())

    assert result["name"] == "tool_agent"
    assert result["scenario_count"] == 14
    assert result["status_accuracy"] == 1.0
    assert result["fallback_success_rate"] == 1.0
    assert result["required_report_tool_rate"] == 0.0
    assert result["final_report_attachment_rate"] == 0.0
