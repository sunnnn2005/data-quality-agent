import json
import time
from datetime import datetime, timezone
from typing import Any, Callable

import pandas as pd

from app.agent import DataQualityAgent
from app.business_rules import BusinessRuleRetriever
from app.checks import QualityCheckRunner
from app.llm import LLMDataQualityAdvisor, LLMSettings
from app.models import AgentRunReport, AgentToolCall, DatasetSummary, QualityReport
from app.profiler import DatasetProfiler
from app.traces import RunTraceStore


ToolFn = Callable[[dict[str, Any]], dict[str, Any]]


class DataQualityToolbox:
    def __init__(
        self,
        dataset: DatasetSummary,
        frame: pd.DataFrame,
        profiler: DatasetProfiler | None = None,
        check_runner: QualityCheckRunner | None = None,
        trace_store: RunTraceStore | None = None,
        rule_retriever: BusinessRuleRetriever | None = None,
    ) -> None:
        self.dataset = dataset
        self.frame = frame
        self.profiler = profiler or DatasetProfiler()
        self.check_runner = check_runner or QualityCheckRunner()
        self.trace_store = trace_store
        self.rule_retriever = rule_retriever or BusinessRuleRetriever()
        self.det_agent = DataQualityAgent(
            profiler=self.profiler,
            check_runner=self.check_runner,
            rule_retriever=self.rule_retriever,
        )

    def schemas(self) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_dataset_contract",
                    "description": "Return dataset owner, primary key, expected columns, freshness metadata, and description.",
                    "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "profile_dataset",
                    "description": "Profile row count, column count, dtypes, missingness, uniqueness, and sample values.",
                    "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "select_quality_strategy",
                    "description": (
                        "Inspect the dataset contract and columns, then recommend which checks and tools should run next. "
                        "Use this before expensive investigation so the agent path can adapt to the business table."
                    ),
                    "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "retrieve_dataset_memory",
                    "description": (
                        "Retrieve recent sanitized run history, recurring failed checks, and recurring root-cause "
                        "patterns for this dataset. Use this when historical evidence could change the investigation "
                        "plan or root-cause ranking."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 10,
                                "description": "Maximum number of recent sanitized traces to inspect.",
                            }
                        },
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "run_quality_checks",
                    "description": "Run schema, freshness, missingness, duplicate-key, volume, domain, and outlier checks.",
                    "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "retrieve_business_rules",
                    "description": (
                        "Retrieve source-cited business rules relevant to the current dataset and quality findings. "
                        "Use this after run_quality_checks when remediation needs business context."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 8,
                                "description": "Maximum number of source-cited business rules to return.",
                            }
                        },
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "build_quality_report",
                    "description": "Build the final deterministic quality report used as the source of truth.",
                    "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
                },
            },
        ]

    def dispatch(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        tools: dict[str, ToolFn] = {
            "get_dataset_contract": self._get_dataset_contract,
            "profile_dataset": self._profile_dataset,
            "select_quality_strategy": self._select_quality_strategy,
            "retrieve_dataset_memory": self._retrieve_dataset_memory,
            "run_quality_checks": self._run_quality_checks,
            "retrieve_business_rules": self._retrieve_business_rules,
            "build_quality_report": self._build_quality_report,
        }
        if tool_name not in tools:
            return {"error": f"unknown tool: {tool_name}"}
        return tools[tool_name](arguments)

    def _get_dataset_contract(self, _: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": self.dataset.id,
            "name": self.dataset.name,
            "owner": self.dataset.owner,
            "primary_key": self.dataset.primary_key,
            "expected_columns": self.dataset.expected_columns,
            "description": self.dataset.description,
            "last_loaded_at": self.dataset.last_loaded_at.isoformat(),
        }

    def _profile_dataset(self, _: dict[str, Any]) -> dict[str, Any]:
        profile = self.profiler.profile(self.dataset, self.frame)
        return profile.model_dump(mode="json")

    def _select_quality_strategy(self, _: dict[str, Any]) -> dict[str, Any]:
        columns = {column.lower() for column in self.frame.columns}
        expected = {column.lower() for column in self.dataset.expected_columns}
        checks = ["schema_required_columns", "missing_values"]
        reason = "General dataset contract checks are required for every table."

        if {"amount", "payment_id"} & columns or {"amount", "payment_id"} & expected:
            checks.extend(["freshness_sla", "negative_amount", "numeric_outliers"])
            reason = "Payment or transaction-like data needs freshness, amount-domain, and outlier checks."
        elif {"ticket_id", "priority", "status"} <= (columns | expected):
            checks.extend(["duplicate_primary_key", "status_priority_consistency", "sla_risk"])
            reason = "Support-ticket data needs identity, workflow-state, priority, and SLA consistency checks."
        elif {"email", "customer_id", "user_id"} & (columns | expected):
            checks.extend(["duplicate_primary_key", "schema_drift", "email_completeness"])
            reason = "Customer or user profile data needs identity, schema, and contact-field checks."
        elif self.dataset.primary_key:
            checks.append("duplicate_primary_key")

        return {
            "dataset_id": self.dataset.id,
            "strategy": reason,
            "recommended_checks": list(dict.fromkeys(checks)),
            "recommended_next_tools": ["profile_dataset", "run_quality_checks", "build_quality_report"],
        }

    def _retrieve_dataset_memory(self, arguments: dict[str, Any]) -> dict[str, Any]:
        if self.trace_store is None:
            return {
                "dataset_id": self.dataset.id,
                "trace_count": 0,
                "recurring_checks": [],
                "recurring_root_causes": [],
                "incident_patterns": [],
                "recent_trace_previews": [],
                "memory_available": False,
                "reason": "No RunTraceStore was provided for this agent run.",
            }

        raw_limit = arguments.get("limit", 5)
        limit = raw_limit if isinstance(raw_limit, int) else 5
        limit = max(1, min(limit, 10))
        memory = self.trace_store.list_by_dataset(self.dataset.id, limit=limit)
        return {
            "dataset_id": memory.dataset_id,
            "trace_count": memory.trace_count,
            "latest_generated_at": memory.latest_generated_at.isoformat() if memory.latest_generated_at else None,
            "recurring_checks": memory.recurring_checks,
            "recurring_root_causes": memory.recurring_root_causes,
            "incident_patterns": [
                {
                    "pattern_id": pattern.pattern_id,
                    "title": pattern.title,
                    "recurrence_count": pattern.recurrence_count,
                    "supporting_checks": pattern.supporting_checks,
                    "recommended_actions": pattern.recommended_actions,
                }
                for pattern in memory.incident_patterns
            ],
            "recent_trace_previews": [
                {
                    "trace_id": trace.trace_id,
                    "status": trace.status,
                    "report_type": trace.report_type,
                    "finding_checks": trace.summary.get("finding_checks", []),
                    "quality_score": trace.summary.get("quality_score"),
                    "verification_passed": trace.summary.get("verification_passed"),
                }
                for trace in memory.recent_traces[:limit]
            ],
            "memory_available": True,
        }

    def _run_quality_checks(self, _: dict[str, Any]) -> dict[str, Any]:
        findings = self.check_runner.run(self.dataset, self.frame)
        return {"findings": [finding.model_dump(mode="json") for finding in findings]}

    def _retrieve_business_rules(self, arguments: dict[str, Any]) -> dict[str, Any]:
        raw_limit = arguments.get("limit", 4)
        limit = raw_limit if isinstance(raw_limit, int) else 4
        limit = max(1, min(limit, 8))
        findings = self.check_runner.run(self.dataset, self.frame)
        rules = self.rule_retriever.retrieve(self.dataset, findings, limit=limit)
        return {
            "dataset_id": self.dataset.id,
            "finding_count": len(findings),
            "rule_count": len(rules),
            "rules": [rule.model_dump(mode="json") for rule in rules],
            "source_cited": all(bool(rule.source) for rule in rules),
        }

    def _build_quality_report(self, _: dict[str, Any]) -> dict[str, Any]:
        report = self.det_agent.analyze(self.dataset, self.frame)
        return report.model_dump(mode="json")


class LLMDataQualityAgent:
    name = "llm_tool_calling_data_quality_agent"
    prompt_version = "tool-agent-v3"

    def __init__(self, settings: LLMSettings | None = None) -> None:
        self.settings = settings or LLMSettings()
        self.advisor = LLMDataQualityAdvisor(self.settings)

    @property
    def enabled(self) -> bool:
        return bool(self.settings.api_key)

    def run(
        self,
        dataset: DatasetSummary,
        frame: pd.DataFrame,
        trace_store: RunTraceStore | None = None,
    ) -> AgentRunReport:
        if not self.enabled:
            return AgentRunReport(
                dataset=dataset,
                generated_at=datetime.now(timezone.utc),
                status="DISABLED",
                final_answer="LLM tool-calling agent is disabled because OPENAI_API_KEY is not configured.",
                tool_calls=[],
                error="OPENAI_API_KEY is not configured",
            )

        toolbox = DataQualityToolbox(dataset, frame, trace_store=trace_store)
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are a data quality LLM agent. Select tools to inspect the dataset before answering. "
                    "Use tool evidence only. Do not invent columns, owners, failures, or private data. "
                    "Use select_quality_strategy to adapt the investigation plan to the dataset shape. "
                    "Use retrieve_dataset_memory when previous sanitized runs can inform root-cause ranking. "
                    "Use retrieve_business_rules after checks when source-cited business context can improve remediation. "
                    "After each tool result, decide whether evidence is sufficient or another tool is needed. "
                    "Before finalizing, call build_quality_report. Final answer must be concise."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Investigate dataset '{dataset.id}'. Determine the data quality status, primary risks, "
                    "and next remediation actions."
                ),
            },
        ]
        tool_calls: list[AgentToolCall] = []
        model_calls: list[dict[str, Any]] = []
        quality_report: QualityReport | None = None
        started = time.monotonic()

        for _ in range(6):
            response, latency_ms = self.advisor._post_with_retries(
                {
                    "model": self.settings.model,
                    "temperature": 0.1,
                    "messages": messages,
                    "tools": toolbox.schemas(),
                    "tool_choice": "auto",
                }
            )
            model_calls.append(self._build_model_call_telemetry(response, latency_ms))
            message = response["choices"][0]["message"]
            requested_tools = message.get("tool_calls") or []
            messages.append(message)
            if not requested_tools:
                final_answer = message.get("content") or ""
                return AgentRunReport(
                    dataset=dataset,
                    generated_at=datetime.now(timezone.utc),
                    status=quality_report.status if quality_report else "ERROR",
                    final_answer=final_answer,
                    tool_calls=tool_calls,
                    quality_report=quality_report,
                    evaluation=self._evaluate(tool_calls, quality_report, started, model_calls),
                )

            for call in requested_tools:
                function = call.get("function", {})
                name = function.get("name", "")
                try:
                    arguments = json.loads(function.get("arguments") or "{}")
                except json.JSONDecodeError:
                    arguments = {}
                result = toolbox.dispatch(name, arguments)
                if name == "build_quality_report" and "quality_score" in result:
                    quality_report = QualityReport.model_validate(result)
                tool_calls.append(
                    AgentToolCall(
                        tool_name=name,
                        arguments=arguments,
                        result_preview=self._preview_result(result),
                    )
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "name": name,
                        "content": json.dumps(result, sort_keys=True),
                    }
                )

        return AgentRunReport(
            dataset=dataset,
            generated_at=datetime.now(timezone.utc),
            status="ERROR",
            final_answer="Agent stopped after reaching the tool-call limit.",
            tool_calls=tool_calls,
            quality_report=quality_report,
            evaluation=self._evaluate(tool_calls, quality_report, started, model_calls),
            error="tool-call limit reached",
        )

    def _build_model_call_telemetry(self, response: dict[str, Any], latency_ms: int) -> dict[str, Any]:
        usage = response.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens")
        completion_tokens = usage.get("completion_tokens")
        total_tokens = usage.get("total_tokens")
        estimated_cost = self.advisor._estimate_cost(usage)
        return {
            "provider": "openai-compatible",
            "model": self.settings.model,
            "prompt_version": self.prompt_version,
            "latency_ms": latency_ms,
            "prompt_tokens": prompt_tokens if isinstance(prompt_tokens, int) else None,
            "completion_tokens": completion_tokens if isinstance(completion_tokens, int) else None,
            "total_tokens": total_tokens if isinstance(total_tokens, int) else None,
            "estimated_cost_usd": estimated_cost,
            "timeout_seconds": self.settings.timeout_seconds,
            "max_retries": self.settings.max_retries,
        }

    def _preview_result(self, result: dict[str, Any]) -> dict[str, Any]:
        if "findings" in result:
            return {"finding_count": len(result["findings"])}
        if "recommended_checks" in result:
            return {
                "strategy": result.get("strategy"),
                "recommended_checks": result.get("recommended_checks", []),
                "recommended_next_tools": result.get("recommended_next_tools", []),
            }
        if "columns" in result:
            return {"row_count": result.get("row_count"), "column_count": result.get("column_count")}
        if "quality_score" in result:
            return {
                "status": result.get("status"),
                "quality_score": result.get("quality_score"),
                "finding_count": len(result.get("findings", [])),
            }
        keys = list(result.keys())[:6]
        return {key: result[key] for key in keys}

    def _evaluate(
        self,
        tool_calls: list[AgentToolCall],
        quality_report: QualityReport | None,
        started: float,
        model_calls: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        names = [call.tool_name for call in tool_calls]
        duplicate_tools = sorted({name for name in names if names.count(name) > 1})
        calls = model_calls or []
        token_counts = [call["total_tokens"] for call in calls if isinstance(call.get("total_tokens"), int)]
        costs = [call["estimated_cost_usd"] for call in calls if isinstance(call.get("estimated_cost_usd"), (int, float))]
        return {
            "latency_ms": int((time.monotonic() - started) * 1000),
            "model": self.settings.model,
            "provider": "openai-compatible" if self.enabled else "disabled",
            "prompt_version": self.prompt_version,
            "model_call_count": len(calls),
            "model_calls": calls,
            "total_tokens": sum(token_counts) if token_counts else None,
            "estimated_cost_usd": round(sum(costs), 6) if costs else None,
            "timeout_seconds": self.settings.timeout_seconds,
            "max_retries": self.settings.max_retries,
            "tool_call_count": len(tool_calls),
            "distinct_tool_count": len(set(names)),
            "duplicate_tools": duplicate_tools,
            "used_strategy_tool": "select_quality_strategy" in names,
            "used_required_report_tool": "build_quality_report" in names,
            "used_profile_tool": "profile_dataset" in names,
            "used_check_tool": "run_quality_checks" in names,
            "used_memory_tool": "retrieve_dataset_memory" in names,
            "used_business_rules_tool": "retrieve_business_rules" in names,
            "final_report_attached": quality_report is not None,
        }
