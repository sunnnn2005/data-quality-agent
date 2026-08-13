from app.agent import DataQualityAgent
from app.data import DATASETS, load_dataset
from app.models import LLMAssessment
from app.tool_agent import DataQualityToolbox, LLMDataQualityAgent
from app.traces import RunTraceStore


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
    assert report.root_cause_hypotheses
    assert report.root_cause_hypotheses[0].confidence >= report.root_cause_hypotheses[-1].confidence
    assert report.root_cause_hypotheses[0].supporting_checks
    assert report.root_cause_hypotheses[0].evidence


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
    strategy = toolbox.dispatch("select_quality_strategy", {})

    assert contract["primary_key"] == DATASETS["orders_daily"].primary_key
    assert profile["row_count"] > 0
    assert len(checks["findings"]) >= 1
    assert report["status"] == "FAIL"
    assert report["llm_assessment"]["enabled"] is False
    assert report["root_cause_hypotheses"]
    assert strategy["recommended_next_tools"] == ["profile_dataset", "run_quality_checks", "build_quality_report"]


def test_toolbox_retrieves_sanitized_dataset_memory():
    dataset = DATASETS["orders_daily"]
    store = RunTraceStore()
    historical_report = DataQualityAgent().analyze(dataset, load_dataset(dataset.id))
    store.save_quality_report(historical_report)
    store.save_quality_report(historical_report)
    toolbox = DataQualityToolbox(dataset, load_dataset(dataset.id), trace_store=store)

    memory = toolbox.dispatch("retrieve_dataset_memory", {"limit": 5})

    assert memory["memory_available"] is True
    assert memory["trace_count"] == 2
    assert "duplicate_primary_key" in memory["recurring_checks"]
    assert memory["incident_patterns"]
    assert memory["recent_trace_previews"]
    assert "agent_trace" not in str(memory)


def test_toolbox_retrieves_source_cited_business_rules():
    frame = load_dataset("orders_daily").rename(columns={"order_id": "ticket_id", "order_total": "amount"})
    dataset = DATASETS["orders_daily"].model_copy(
        update={
            "id": "support_tickets",
            "name": "Support Tickets",
            "owner": "support-ops",
            "primary_key": "ticket_id",
            "expected_columns": ["ticket_id", "team", "priority", "status", "amount"],
            "description": "Support ticket export used by operations dashboards.",
        }
    )
    toolbox = DataQualityToolbox(dataset, frame)

    rules = toolbox.dispatch("retrieve_business_rules", {"limit": 3})

    assert rules["rule_count"] >= 1
    assert rules["source_cited"] is True
    assert all(rule["source"].startswith("business-rules/support_tickets.md#") for rule in rules["rules"])
    assert any("support_tickets:R1" == rule["rule_id"] for rule in rules["rules"])


def test_toolbox_selects_different_quality_strategies_by_dataset_shape():
    payments_strategy = DataQualityToolbox(DATASETS["payments_events"], load_dataset("payments_events")).dispatch(
        "select_quality_strategy", {}
    )
    customer_strategy = DataQualityToolbox(DATASETS["customer_profiles"], load_dataset("customer_profiles")).dispatch(
        "select_quality_strategy", {}
    )

    assert "negative_amount" in payments_strategy["recommended_checks"]
    assert "numeric_outliers" in payments_strategy["recommended_checks"]
    assert "email_completeness" in customer_strategy["recommended_checks"]
    assert payments_strategy["strategy"] != customer_strategy["strategy"]


def test_agent_ranks_root_cause_hypotheses_with_evidence():
    report = analyze("payments_events")
    hypotheses = report.root_cause_hypotheses

    assert hypotheses
    assert [item.confidence for item in hypotheses] == sorted(
        [item.confidence for item in hypotheses],
        reverse=True,
    )
    assert any("freshness_sla" in item.supporting_checks for item in hypotheses)
    assert any("negative_amount" in item.supporting_checks for item in hypotheses)
    assert all(item.evidence for item in hypotheses)
    assert all(item.recommended_action for item in hypotheses)


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


def test_llm_tool_calling_agent_replans_across_tool_feedback():
    class FakeSettings:
        api_key = "test-key"
        base_url = "http://example.test/v1"
        model = "fake-model"
        timeout_seconds = 1
        max_retries = 0

    agent = LLMDataQualityAgent(settings=FakeSettings())
    requested_tools = []
    calls = [
        {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": "call_strategy",
                                "type": "function",
                                "function": {"name": "select_quality_strategy", "arguments": "{}"},
                            }
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
                        "tool_calls": [
                            {
                                "id": "call_profile",
                                "type": "function",
                                "function": {"name": "profile_dataset", "arguments": "{}"},
                            },
                            {
                                "id": "call_checks",
                                "type": "function",
                                "function": {"name": "run_quality_checks", "arguments": "{}"},
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
                        "tool_calls": [
                            {
                                "id": "call_report",
                                "type": "function",
                                "function": {"name": "build_quality_report", "arguments": "{}"},
                            }
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
                        "content": "The support-ticket dataset fails due to missing fields and duplicate identifiers.",
                    }
                }
            ]
        },
    ]

    def fake_post(body):
        tool_results_seen = [message for message in body["messages"] if message.get("role") == "tool"]
        if tool_results_seen:
            assert any("recommended_checks" in message["content"] for message in tool_results_seen)
        response = calls.pop(0)
        requested_tools.extend(
            call["function"]["name"]
            for call in response["choices"][0]["message"].get("tool_calls", [])
        )
        return response, 1

    agent.advisor._post_with_retries = fake_post

    report = agent.run(DATASETS["payments_events"], load_dataset("payments_events"))

    assert requested_tools == [
        "select_quality_strategy",
        "profile_dataset",
        "run_quality_checks",
        "build_quality_report",
    ]
    assert report.status == "FAIL"
    assert report.evaluation["used_strategy_tool"] is True
    assert report.evaluation["distinct_tool_count"] == 4
    assert "negative_amount" in report.tool_calls[0].result_preview.get("recommended_checks", [])


def test_llm_tool_calling_agent_can_use_memory_to_inform_planning():
    class FakeSettings:
        api_key = "test-key"
        base_url = "http://example.test/v1"
        model = "fake-model"
        timeout_seconds = 1
        max_retries = 0

    dataset = DATASETS["orders_daily"]
    store = RunTraceStore()
    historical_report = DataQualityAgent().analyze(dataset, load_dataset(dataset.id))
    store.save_quality_report(historical_report)
    store.save_quality_report(historical_report)

    agent = LLMDataQualityAgent(settings=FakeSettings())
    calls = [
        {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": "call_memory",
                                "type": "function",
                                "function": {"name": "retrieve_dataset_memory", "arguments": '{"limit": 5}'},
                            }
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
                        "tool_calls": [
                            {
                                "id": "call_strategy",
                                "type": "function",
                                "function": {"name": "select_quality_strategy", "arguments": "{}"},
                            },
                            {
                                "id": "call_report",
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
                        "content": "Recurring duplicate keys should be prioritized because memory shows repeated failures.",
                    }
                }
            ]
        },
    ]

    def fake_post(body):
        tool_results_seen = [message for message in body["messages"] if message.get("role") == "tool"]
        if tool_results_seen:
            joined_results = " ".join(message["content"] for message in tool_results_seen)
            assert "recurring_checks" in joined_results
            assert "duplicate_primary_key" in joined_results
        return calls.pop(0), 1

    agent.advisor._post_with_retries = fake_post

    report = agent.run(dataset, load_dataset(dataset.id), trace_store=store)

    assert report.status == "FAIL"
    assert [call.tool_name for call in report.tool_calls] == [
        "retrieve_dataset_memory",
        "select_quality_strategy",
        "build_quality_report",
    ]
    assert report.evaluation["used_memory_tool"] is True
    assert report.tool_calls[0].result_preview["trace_count"] == 2


def test_llm_tool_calling_agent_can_retrieve_business_rules_after_checks():
    class FakeSettings:
        api_key = "test-key"
        base_url = "http://example.test/v1"
        model = "fake-model"
        timeout_seconds = 1
        max_retries = 0

    frame = load_dataset("orders_daily").rename(columns={"order_id": "ticket_id", "order_total": "amount"})
    dataset = DATASETS["orders_daily"].model_copy(
        update={
            "id": "support_tickets",
            "name": "Support Tickets",
            "owner": "support-ops",
            "primary_key": "ticket_id",
            "expected_columns": ["ticket_id", "team", "priority", "status", "amount"],
            "description": "Support ticket export used by operations dashboards.",
        }
    )
    agent = LLMDataQualityAgent(settings=FakeSettings())
    calls = [
        {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": "call_checks",
                                "type": "function",
                                "function": {"name": "run_quality_checks", "arguments": "{}"},
                            },
                            {
                                "id": "call_rules",
                                "type": "function",
                                "function": {"name": "retrieve_business_rules", "arguments": '{"limit": 3}'},
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
                        "tool_calls": [
                            {
                                "id": "call_report",
                                "type": "function",
                                "function": {"name": "build_quality_report", "arguments": "{}"},
                            }
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
                        "content": "Business rules show duplicate ticket IDs can distort SLA reporting.",
                    }
                }
            ]
        },
    ]

    def fake_post(body):
        tool_results_seen = [message for message in body["messages"] if message.get("role") == "tool"]
        if tool_results_seen:
            joined_results = " ".join(message["content"] for message in tool_results_seen)
            assert "support_tickets:R1" in joined_results
            assert "source_cited" in joined_results
        return calls.pop(0), 1

    agent.advisor._post_with_retries = fake_post

    report = agent.run(dataset, frame)

    assert report.status == "FAIL"
    assert [call.tool_name for call in report.tool_calls] == [
        "run_quality_checks",
        "retrieve_business_rules",
        "build_quality_report",
    ]
    assert report.evaluation["used_business_rules_tool"] is True
    assert report.tool_calls[1].result_preview["rule_count"] >= 1
