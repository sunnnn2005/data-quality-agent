import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AGENT_READINESS_PATH = ROOT / "docs" / "agent-readiness.json"
CAPABILITY_MATRIX_PATH = ROOT / "docs" / "agent-capability-matrix.json"
REAL_MODEL_RUNBOOK_PATH = ROOT / "docs" / "real-model-runbook.json"
REAL_MODEL_CAPTURE_PATH = ROOT / "docs" / "real-model-evidence-capture.json"
BUSINESS_REPLAY_DEMO_PATH = ROOT / "docs" / "business-replay-demo.json"
APPLICATION_EVIDENCE_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "ai-engineer-readiness.json"
OUTPUT_MD_PATH = ROOT / "docs" / "ai-engineer-readiness.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_ai_engineer_readiness_payload() -> dict[str, Any]:
    agent_readiness = load_json(AGENT_READINESS_PATH)
    capability_matrix = load_json(CAPABILITY_MATRIX_PATH)
    real_model_runbook = load_json(REAL_MODEL_RUNBOOK_PATH)
    real_model_capture = load_json(REAL_MODEL_CAPTURE_PATH)
    business_replay = load_json(BUSINESS_REPLAY_DEMO_PATH)
    application_pack = load_json(APPLICATION_EVIDENCE_PACK_PATH)

    skill_signals = [
        {
            "id": "llm-api-integration",
            "resume_signal": "OpenAI-compatible chat-completions integration",
            "evidence": "app/llm.py supports OPENAI_API_KEY, OPENAI_BASE_URL, model selection, retries, timeouts, JSON response parsing, and cost estimation.",
            "status": "implemented",
        },
        {
            "id": "tool-calling-agent-loop",
            "resume_signal": "LLM tool calling with feedback loop",
            "evidence": "app/tool_agent.py lets the model choose from 7 allowed tools, appends tool results back into messages, and loops until final answer or max step budget.",
            "status": "implemented",
        },
        {
            "id": "business-data-connectors",
            "resume_signal": "Real business-data interface",
            "evidence": "FastAPI exposes /business-data/agent-report for CSV exports and /postgres/support-tickets/agent-report for a read-only PostgreSQL table.",
            "status": "implemented",
        },
        {
            "id": "structured-output",
            "resume_signal": "Structured AI output",
            "evidence": "AgentRunReport and QualityReport are Pydantic response models with findings, hypotheses, recommendations, evidence, verification, telemetry, and trace_id.",
            "status": "implemented",
        },
        {
            "id": "guardrails",
            "resume_signal": "Deterministic report guardrails",
            "evidence": "ReportVerifier checks evidence support, known columns, sensitive terms, unsupported LLM evidence, action coverage, and score bounds.",
            "status": "implemented",
        },
        {
            "id": "observability-cost",
            "resume_signal": "Model observability and cost awareness",
            "evidence": "Agent evaluation records model, provider, prompt version, latency, token usage, estimated cost, retry budget, distinct tools, duplicate tools, and final report attachment.",
            "status": "implemented",
        },
        {
            "id": "safe-fallback",
            "resume_signal": "Safe LLM degradation",
            "evidence": "Without OPENAI_API_KEY, the agent returns DISABLED with an explicit fallback instead of crashing the API.",
            "status": "implemented",
        },
        {
            "id": "eval-harness",
            "resume_signal": "Agent evaluation harness",
            "evidence": "evals/scenarios.jsonl and app/evals.py measure status accuracy, finding recall, evidence support, fallback behavior, report-tool usage, and latency.",
            "status": "implemented",
        },
        {
            "id": "business-rule-retrieval",
            "resume_signal": "Source-cited retrieval for domain rules",
            "evidence": "retrieve_business_rules gives the LLM source-cited local Markdown business rules for support-ticket constraints.",
            "status": "partial",
        },
        {
            "id": "real-model-evidence",
            "resume_signal": "Accepted real-model run evidence",
            "evidence": "Real-model runbook and capture gate exist, but accepted_real_model_run_count is still 0 until a redacted OpenAI-compatible run is captured.",
            "status": "not_claimed",
        },
    ]

    resume_bullet = (
        "Built an OpenAI-compatible data-quality LLM agent for CSV and read-only PostgreSQL business data, "
        f"with {capability_matrix['tool_count']} controlled tools, dynamic tool selection, structured reports, "
        "trace/cost telemetry, deterministic guardrails, safe fallback, and CI-verified evidence artifacts."
    )
    interview_claim = (
        "This project demonstrates AI Engineer intern readiness through API integration, tool calling, "
        "structured output, guardrails, observability, evaluation, and real business-data connectors; it does not yet claim "
        "production users or accepted real-model benchmark runs."
    )
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_ai_engineer_readiness.py",
        "target_role": "AI Engineer Intern",
        "readiness_summary": interview_claim,
        "resume_bullet": resume_bullet,
        "implemented_signal_count": sum(1 for item in skill_signals if item["status"] == "implemented"),
        "partial_signal_count": sum(1 for item in skill_signals if item["status"] == "partial"),
        "not_claimed_signal_count": sum(1 for item in skill_signals if item["status"] == "not_claimed"),
        "skill_signals": skill_signals,
        "evidence_counts": {
            "agent_readiness_implemented": len(agent_readiness["implemented"]),
            "capability_matrix_implemented": capability_matrix["implemented_count"],
            "allowed_tools": capability_matrix["tool_count"],
            "business_replay_rows": business_replay["dataset"]["row_count"],
            "business_replay_findings": business_replay["quality_report_summary"]["finding_count"],
            "real_model_run_commands": real_model_runbook["run_command_count"],
            "real_model_capture_required_fields": real_model_capture["capture_required_field_count"],
            "real_model_capture_accepted_runs": real_model_capture["accepted_real_model_run_count"],
            "application_evidence_links": len(application_pack["application_links"]),
        },
        "resume_safe": [
            resume_bullet,
            "Explained LLM decisions through tool-call traces, evidence-backed findings, verification status, prompt version, token usage, latency, and estimated cost fields.",
        ],
        "not_resume_safe_yet": [
            "Do not claim production users.",
            "Do not claim customer feedback.",
            "Do not claim accepted real-model benchmark runs until accepted_real_model_run_count is greater than 0.",
            "Do not claim embedding-based RAG until a vector retrieval layer is implemented.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    signals = "\n".join(
        f"| {item['resume_signal']} | `{item['status']}` | {item['evidence']} |" for item in payload["skill_signals"]
    )
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["evidence_counts"].items())
    safe = "\n".join(f"- {item}" for item in payload["resume_safe"])
    unsafe = "\n".join(f"- {item}" for item in payload["not_resume_safe_yet"])
    return f"""# AI Engineer Readiness

This generated artifact explains why the project is relevant for {payload["target_role"]} applications while keeping outcome claims honest.

## Summary

{payload["readiness_summary"]}

## Resume Bullet

{payload["resume_bullet"]}

## Skill Signals

| Signal | Status | Evidence |
| --- | --- | --- |
{signals}

## Evidence Counts

| Metric | Value |
| --- | ---: |
{counts}

## Resume-Safe Lines

{safe}

## Not Resume-Safe Yet

{unsafe}
"""


def verify_ai_engineer_readiness(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["target_role"] != "AI Engineer Intern":
        raise AssertionError("target role must be AI Engineer Intern")
    if payload["implemented_signal_count"] != 8:
        raise AssertionError("AI readiness must verify 8 implemented signals")
    if payload["partial_signal_count"] != 1:
        raise AssertionError("AI readiness must preserve 1 partial signal")
    if payload["not_claimed_signal_count"] != 1:
        raise AssertionError("AI readiness must preserve 1 not-claimed signal")
    counts = payload["evidence_counts"]
    expected_counts = {
        "allowed_tools": 7,
        "business_replay_rows": 8,
        "business_replay_findings": 5,
        "real_model_capture_accepted_runs": 0,
        "application_evidence_links": 31,
    }
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {counts.get(key)!r}")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("tool calling", "structured", "guardrails", "trace", "cost", "postgresql"):
        if required not in joined:
            raise AssertionError(f"AI readiness missing required signal: {required}")
    for forbidden in ("production users", "customer feedback", "accepted real-model benchmark runs"):
        if forbidden not in joined:
            raise AssertionError(f"AI readiness must explicitly block claim: {forbidden}")
    if "gained github stars" in joined:
        raise AssertionError("AI readiness must not claim GitHub star growth")
    return {
        "ai_engineer_readiness_verified": True,
        "implemented_signal_count": payload["implemented_signal_count"],
        "partial_signal_count": payload["partial_signal_count"],
        "not_claimed_signal_count": payload["not_claimed_signal_count"],
    }


def main() -> None:
    payload = build_ai_engineer_readiness_payload()
    verify_ai_engineer_readiness(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
