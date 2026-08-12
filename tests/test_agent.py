from app.agent import DataQualityAgent
from app.data import DATASETS, load_dataset
from app.models import LLMAssessment
from app.tool_agent import DataQualityToolbox, LLMDataQualityAgent


def analyze(dataset_id: str):
    return DataQualityAgent().analyze(DATASETS[dataset_id], load_dataset(dataset_id))


def test_orders_daily_detects_duplicates_missing_values_and_outliers():
    report = analyze("orders_daily")
    checks = {finding.check_name for finding in report.findings}

    assert report.status == "FAIL"
    assert "duplicate_primary_key" in checks
    assert "missing_values" in checks
    assert "numeric_outliers" in checks
    assert report.quality_score < 80
    assert any("idempotent" in step for step in report.recommended_next_steps)


def test_payments_events_detects_freshness_and_negative_amount():
    report = analyze("payments_events")
    checks = {finding.check_name for finding in report.findings}

    assert "freshness_sla" in checks
    assert "negative_amount" in checks
    assert any("scheduler" in cause.lower() or "scheduled" in cause.lower() for cause in report.likely_causes)


def test_customer_profiles_detects_schema_drift_and_missing_fields():
    report = analyze("customer_profiles")
    checks = {finding.check_name for finding in report.findings}

    assert "schema_drift" in checks
    assert "missing_values" in checks
    assert any("schema migration" in cause.lower() for cause in report.likely_causes)


def test_agent_trace_records_tool_calls():
    report = analyze("orders_daily")

    assert any("dataset_profiler" in step for step in report.agent_trace)
    assert any("quality_check_runner" in step for step in report.agent_trace)
    assert any("llm_data_quality_advisor" in step for step in report.agent_trace)


def test_llm_assessment_is_safe_optional_default():
    report = analyze("orders_daily")

    assert report.llm_assessment.enabled is False
    assert report.llm_assessment.error == "OPENAI_API_KEY is not configured"


def test_agent_accepts_structured_llm_assessment():
    class FakeAdvisor:
        name = "llm_data_quality_advisor"

        def assess(self, profile, findings):
            return LLMAssessment(
                enabled=True,
                provider="test",
                model="fake-model",
                summary=f"Reviewed {profile.dataset.id} with {len(findings)} findings.",
                risk_level="HIGH",
                evidence_used=["duplicate_primary_key", "missing_values"],
                suggested_actions=["Create an owner-reviewed remediation ticket."],
                evaluation={"findings_referenced": 2, "unsupported_claims": []},
                cost_estimate_usd=0.0001,
            )

    report = DataQualityAgent(llm_advisor=FakeAdvisor()).analyze(DATASETS["orders_daily"], load_dataset("orders_daily"))

    assert report.llm_assessment.enabled is True
    assert report.llm_assessment.risk_level == "HIGH"
    assert report.llm_assessment.evaluation["findings_referenced"] == 2
    assert any("called llm_data_quality_advisor" in step for step in report.agent_trace)


def test_toolbox_exposes_data_quality_tools():
    toolbox = DataQualityToolbox(DATASETS["orders_daily"], load_dataset("orders_daily"))

    contract = toolbox.dispatch("get_dataset_contract", {})
    profile = toolbox.dispatch("profile_dataset", {})
    checks = toolbox.dispatch("run_quality_checks", {})
    report = toolbox.dispatch("build_quality_report", {})

    assert contract["primary_key"] == DATASETS["orders_daily"].primary_key
    assert profile["row_count"] > 0
    assert len(checks["findings"]) >= 1
    assert report["status"] == "FAIL"
    assert report["llm_assessment"]["enabled"] is False


def test_llm_tool_calling_agent_default_disabled():
    report = LLMDataQualityAgent().run(DATASETS["orders_daily"], load_dataset("orders_daily"))

    assert report.status == "DISABLED"
    assert report.tool_calls == []
    assert report.error == "OPENAI_API_KEY is not configured"


def test_llm_tool_calling_agent_runs_tool_loop():
    class FakeSettings:
        api_key = "test-key"
        base_url = "http://example.test/v1"
        model = "fake-model"
        timeout_seconds = 1
        max_retries = 0

    agent = LLMDataQualityAgent(settings=FakeSettings())
    calls = [
        {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": "call_1",
                                "type": "function",
                                "function": {"name": "profile_dataset", "arguments": "{}"},
                            },
                            {
                                "id": "call_2",
                                "type": "function",
                                "function": {"name": "run_quality_checks", "arguments": "{}"},
                            },
                            {
                                "id": "call_3",
                                "type": "function",
                                "function": {"name": "build_quality_report", "arguments": "{}"},
                            },
                        ],
                    }
                }
            ]
        },
        {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "The dataset fails quality checks due to duplicate keys, missing values, and outliers.",
                    }
                }
            ]
        },
    ]

    def fake_post(_body):
        return calls.pop(0), 1

    agent.advisor._post_with_retries = fake_post

    report = agent.run(DATASETS["orders_daily"], load_dataset("orders_daily"))

    assert report.status == "FAIL"
    assert report.quality_report is not None
    assert [call.tool_name for call in report.tool_calls] == ["profile_dataset", "run_quality_checks", "build_quality_report"]
    assert report.evaluation["used_required_report_tool"] is True
