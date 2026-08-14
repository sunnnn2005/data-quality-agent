import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.data import DATASETS, load_dataset
from app.postgres_adapter import PostgresAdapterError, PostgresDatasetAdapter
from app.tool_agent import DataQualityToolbox, LLMDataQualityAgent
from app.traces import RunTraceStore


OUTPUT_JSON_PATH = ROOT / "docs" / "agent-capability-matrix.json"
OUTPUT_MD_PATH = ROOT / "docs" / "agent-capability-matrix.md"


def build_agent_capability_matrix_payload() -> dict[str, Any]:
    dataset = DATASETS["orders_daily"]
    frame = load_dataset(dataset.id)
    toolbox = DataQualityToolbox(dataset, frame, trace_store=RunTraceStore())
    tool_names = [schema["function"]["name"] for schema in toolbox.schemas()]
    strategy = toolbox.dispatch("select_quality_strategy", {})
    safe_agent = LLMDataQualityAgent().run(dataset, frame)
    rejected_queries = _count_rejected_queries()
    capabilities = [
        {
            "id": "explicit-task-goal",
            "question": "Does the agent have a bounded task goal?",
            "status": "implemented",
            "evidence": "LLMDataQualityAgent.run asks the model to investigate one dataset and determine quality status, primary risks, and remediation actions.",
        },
        {
            "id": "llm-decision-making",
            "question": "Does the LLM choose the next step instead of following a fixed path?",
            "status": "implemented",
            "evidence": "The Chat Completions loop exposes tools with tool_choice=auto, and model-selected tool calls determine which toolbox function runs next.",
        },
        {
            "id": "controlled-tools",
            "question": "Are there multiple structured tools with a whitelist?",
            "status": "implemented",
            "evidence": f"{len(tool_names)} allowed tools: {', '.join(tool_names)}.",
        },
        {
            "id": "tool-feedback-loop",
            "question": "Are tool results fed back to the LLM?",
            "status": "implemented",
            "evidence": "Each tool result is appended as a role=tool message before the next model call.",
        },
        {
            "id": "dynamic-path",
            "question": "Can different input shapes trigger different plans?",
            "status": "implemented",
            "evidence": f"select_quality_strategy returned {len(strategy['recommended_checks'])} checks for {dataset.id}: {', '.join(strategy['recommended_checks'])}.",
        },
        {
            "id": "state-management",
            "question": "Does the agent preserve task state and evidence?",
            "status": "implemented",
            "evidence": "AgentRunReport stores status, final_answer, tool_calls, quality_report, evaluation, and trace_id; RunTraceStore persists sanitized run traces when TRACE_DB_PATH is configured.",
        },
        {
            "id": "termination-conditions",
            "question": "Does the loop know when to stop?",
            "status": "implemented",
            "evidence": "The loop stops when the model returns no tool calls, when build_quality_report attaches a final report, or after six rounds.",
        },
        {
            "id": "permission-boundary",
            "question": "Are tool and database permissions bounded?",
            "status": "implemented",
            "evidence": f"Tool dispatch rejects unknown tools, PostgreSQL is read-only, and {rejected_queries} unsafe SQL examples are rejected.",
        },
        {
            "id": "fallback",
            "question": "Does the system degrade safely when the model is unavailable?",
            "status": "implemented",
            "evidence": f"Without OPENAI_API_KEY, the agent returns status={safe_agent.status} instead of failing the API.",
        },
        {
            "id": "context-management",
            "question": "Does the model receive summaries instead of full private tables?",
            "status": "implemented",
            "evidence": "LLM prompt payloads contain dataset metadata, column profiles, redacted samples, and finding evidence rather than raw uploaded files.",
        },
        {
            "id": "structured-output",
            "question": "Is the final output structured and machine-verifiable?",
            "status": "implemented",
            "evidence": "QualityReport and AgentRunReport are Pydantic response models exposed through FastAPI and OpenAPI.",
        },
        {
            "id": "evidence-separation",
            "question": "Are facts, hypotheses, recommendations, and limitations separable?",
            "status": "implemented",
            "evidence": "QualityReport separates findings, likely_causes, root_cause_hypotheses, recommended_next_steps, verification, and llm_assessment.",
        },
        {
            "id": "guardrails",
            "question": "Are final reports checked by deterministic code?",
            "status": "implemented",
            "evidence": "ReportVerifier checks finding evidence, known columns, sensitive terms, LLM evidence support, recommended actions, and score bounds.",
        },
        {
            "id": "observability",
            "question": "Can reviewer inspect traces, model metadata, latency, cost, and fallback status?",
            "status": "partial",
            "evidence": "Run traces, prompt_version, model_call_count, token/cost telemetry, and fallback status exist, but there is no production monitoring dashboard.",
            "next_step": "Add persisted per-model-call telemetry for real model runs and expose aggregate latency/cost dashboards.",
        },
        {
            "id": "memory",
            "question": "Does memory influence future reasoning?",
            "status": "partial",
            "evidence": "retrieve_dataset_memory gives the LLM prior sanitized traces and recurring incident patterns, but accepted feedback labels do not yet tune ranking.",
            "next_step": "Use accepted/needs-review hypothesis feedback to adjust root-cause ranking in later runs.",
        },
        {
            "id": "rag",
            "question": "Does the agent retrieve external knowledge?",
            "status": "partial",
            "evidence": "retrieve_business_rules provides source-cited local Markdown business rules, but there is no embedding/vector search layer yet.",
            "next_step": "Add optional embedding-backed retrieval with permission filtering and source citations.",
        },
        {
            "id": "evaluation",
            "question": "Is there an eval suite proving agent value?",
            "status": "partial",
            "evidence": "The repo has deterministic scenario evals, fallback tests, and tool-planning coverage, but no large labeled real-world eval set.",
            "next_step": "Add 20-30 labeled business-data scenarios measuring tool-choice accuracy, false positives, evidence support, latency, and cost.",
        },
        {
            "id": "human-approval",
            "question": "Are risky actions gated by human approval?",
            "status": "planned",
            "evidence": "The current agent is read-only and recommends actions; it does not execute writes or send tickets.",
            "next_step": "Add an approval boundary before generated SQL, ticket creation, or notification actions.",
        },
        {
            "id": "production-adoption",
            "question": "Is there production usage or external user proof?",
            "status": "not_claimed",
            "evidence": "The public metrics intentionally show zero confirmed external users and no enterprise production deployment claim.",
        },
    ]
    status_counts = _count_statuses(capabilities)
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_agent_capability_matrix.py",
        "agent_definition": "LLM decision-making + controlled tools + stateful loop + dynamic path + bounded permissions + evidence-backed output.",
        "tool_count": len(tool_names),
        "tool_names": tool_names,
        "implemented_count": status_counts["implemented"],
        "partial_count": status_counts["partial"],
        "planned_count": status_counts["planned"],
        "not_claimed_count": status_counts["not_claimed"],
        "capabilities": capabilities,
        "resume_safe_summary": (
            f"Published a CI-verified agent capability matrix showing {status_counts['implemented']} implemented "
            f"LLM-agent capabilities, {status_counts['partial']} partial maturity areas, {len(tool_names)} allowed tools, "
            "safe fallback, read-only business-data boundaries, and no inflated production-user claims."
        ),
        "not_claimed": [
            "external users",
            "customer feedback",
            "enterprise production deployment",
            "paid model benchmark results",
            "autonomous write actions",
        ],
    }


def _count_statuses(capabilities: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"implemented": 0, "partial": 0, "planned": 0, "not_claimed": 0}
    for item in capabilities:
        counts[item["status"]] += 1
    return counts


def _count_rejected_queries() -> int:
    adapter = PostgresDatasetAdapter()
    rejected = 0
    for query in (
        "UPDATE support_tickets SET amount = 0 LIMIT 1",
        "SELECT * FROM support_tickets; DROP TABLE support_tickets",
        "SELECT * FROM support_tickets",
    ):
        try:
            adapter._validate_read_only_query(query)
        except PostgresAdapterError:
            rejected += 1
    return rejected


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {question} | {status} | {evidence} | {next_step} |".format(
            question=item["question"],
            status=item["status"],
            evidence=item["evidence"],
            next_step=item.get("next_step", ""),
        )
        for item in payload["capabilities"]
    )
    tools = "\n".join(f"- `{name}`" for name in payload["tool_names"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Agent Capability Matrix

This generated artifact maps Data Quality Agent against a practical LLM-agent checklist. It is intentionally conservative: implemented capabilities are separated from partial, planned, and not-claimed work.

## Summary

| Metric | Value |
| --- | ---: |
| Implemented capabilities | {payload["implemented_count"]} |
| Partial maturity areas | {payload["partial_count"]} |
| Planned capabilities | {payload["planned_count"]} |
| Not-claimed areas | {payload["not_claimed_count"]} |
| Allowed tools | {payload["tool_count"]} |

## Agent Definition

{payload["agent_definition"]}

## Tool Allowlist

{tools}

## Capability Matrix

| Checklist question | Status | Evidence | Next step |
| --- | --- | --- | --- |
{rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_agent_capability_matrix(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "tool_count": 9,
        "implemented_count": 13,
        "partial_count": 4,
        "planned_count": 1,
        "not_claimed_count": 1,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    required_tools = {
        "select_quality_strategy",
        "retrieve_dataset_memory",
        "inspect_primary_key_integrity",
        "analyze_numeric_distribution",
        "retrieve_business_rules",
        "build_quality_report",
    }
    if not required_tools <= set(payload["tool_names"]):
        raise AssertionError("capability matrix is missing required agent tools")
    capability_ids = {item["id"] for item in payload["capabilities"]}
    for required in (
        "llm-decision-making",
        "tool-feedback-loop",
        "dynamic-path",
        "permission-boundary",
        "structured-output",
        "guardrails",
        "production-adoption",
    ):
        if required not in capability_ids:
            raise AssertionError(f"capability matrix missing {required}")
    if "production users" in payload["resume_safe_summary"].lower():
        raise AssertionError("capability matrix must not claim production users")
    for required in ("external users", "enterprise production deployment", "autonomous write actions"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"capability matrix must not claim {required}")
    return {"agent_capability_matrix_verified": True, **expected}


def main() -> None:
    payload = build_agent_capability_matrix_payload()
    verify_agent_capability_matrix(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
