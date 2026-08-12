import json
import time
from datetime import datetime, timezone
from typing import Any, Callable

import pandas as pd

from app.agent import DataQualityAgent
from app.checks import QualityCheckRunner
from app.llm import LLMDataQualityAdvisor, LLMSettings
from app.models import AgentRunReport, AgentToolCall, DatasetSummary, QualityReport
from app.profiler import DatasetProfiler


ToolFn = Callable[[dict[str, Any]], dict[str, Any]]


class DataQualityToolbox:
    def __init__(
        self,
        dataset: DatasetSummary,
        frame: pd.DataFrame,
        profiler: DatasetProfiler | None = None,
        check_runner: QualityCheckRunner | None = None,
    ) -> None:
        self.dataset = dataset
        self.frame = frame
        self.profiler = profiler or DatasetProfiler()
        self.check_runner = check_runner or QualityCheckRunner()
        self.det_agent = DataQualityAgent(profiler=self.profiler, check_runner=self.check_runner)

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
                    "name": "run_quality_checks",
                    "description": "Run schema, freshness, missingness, duplicate-key, volume, domain, and outlier checks.",
                    "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
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
            "run_quality_checks": self._run_quality_checks,
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

    def _run_quality_checks(self, _: dict[str, Any]) -> dict[str, Any]:
        findings = self.check_runner.run(self.dataset, self.frame)
        return {"findings": [finding.model_dump(mode="json") for finding in findings]}

    def _build_quality_report(self, _: dict[str, Any]) -> dict[str, Any]:
        report = self.det_agent.analyze(self.dataset, self.frame)
        return report.model_dump(mode="json")


class LLMDataQualityAgent:
    name = "llm_tool_calling_data_quality_agent"

    def __init__(self, settings: LLMSettings | None = None) -> None:
        self.settings = settings or LLMSettings()
        self.advisor = LLMDataQualityAdvisor(self.settings)

    @property
    def enabled(self) -> bool:
        return bool(self.settings.api_key)

    def run(self, dataset: DatasetSummary, frame: pd.DataFrame) -> AgentRunReport:
        if not self.enabled:
            return AgentRunReport(
                dataset=dataset,
                generated_at=datetime.now(timezone.utc),
                status="DISABLED",
                final_answer="LLM tool-calling agent is disabled because OPENAI_API_KEY is not configured.",
                tool_calls=[],
                error="OPENAI_API_KEY is not configured",
            )

        toolbox = DataQualityToolbox(dataset, frame)
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are a data quality LLM agent. Select tools to inspect the dataset before answering. "
                    "Use tool evidence only. Do not invent columns, owners, failures, or private data. "
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
        quality_report: QualityReport | None = None
        started = time.monotonic()

        for _ in range(6):
            response, _ = self.advisor._post_with_retries(
                {
                    "model": self.settings.model,
                    "temperature": 0.1,
                    "messages": messages,
                    "tools": toolbox.schemas(),
                    "tool_choice": "auto",
                }
            )
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
                    evaluation=self._evaluate(tool_calls, quality_report, started),
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
            evaluation=self._evaluate(tool_calls, quality_report, started),
            error="tool-call limit reached",
        )

    def _preview_result(self, result: dict[str, Any]) -> dict[str, Any]:
        if "findings" in result:
            return {"finding_count": len(result["findings"])}
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
    ) -> dict[str, Any]:
        names = [call.tool_name for call in tool_calls]
        return {
            "latency_ms": int((time.monotonic() - started) * 1000),
            "tool_call_count": len(tool_calls),
            "used_required_report_tool": "build_quality_report" in names,
            "used_profile_tool": "profile_dataset" in names,
            "used_check_tool": "run_quality_checks" in names,
            "final_report_attached": quality_report is not None,
        }
