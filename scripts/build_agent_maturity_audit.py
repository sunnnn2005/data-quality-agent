import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AGENT_CAPABILITY_MATRIX_PATH = ROOT / "docs" / "agent-capability-matrix.json"
AI_ENGINEER_READINESS_PATH = ROOT / "docs" / "ai-engineer-readiness.json"
AGENT_READINESS_PATH = ROOT / "docs" / "agent-readiness.json"
REAL_MODEL_PREFLIGHT_PATH = ROOT / "docs" / "real-model-preflight.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "agent-maturity-audit.json"
OUTPUT_MD_PATH = ROOT / "docs" / "agent-maturity-audit.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


AUDIT_ROWS = [
    {
        "area": "Task goal",
        "status": "implemented",
        "evidence": "The agent investigates one dataset and returns quality status, risks, root-cause hypotheses, and remediation actions.",
        "resume_signal": "bounded AI task definition",
    },
    {
        "area": "LLM decision-making",
        "status": "implemented",
        "evidence": "The Chat Completions tool loop uses tool_choice=auto so the model chooses the next tool from the allowlist.",
        "resume_signal": "LLM-driven tool selection",
    },
    {
        "area": "Controlled tools",
        "status": "implemented",
        "evidence": "The toolbox exposes 9 structured allowlisted tools and rejects unknown tool names.",
        "resume_signal": "safe tool calling",
    },
    {
        "area": "Agent loop",
        "status": "implemented",
        "evidence": "Tool results are appended as role=tool messages before the next model step.",
        "resume_signal": "multi-step agent execution",
    },
    {
        "area": "Dynamic execution path",
        "status": "implemented",
        "evidence": "The strategy tool chooses different checks for transaction, support-ticket, customer, and generic tables.",
        "resume_signal": "adaptive data-quality investigation",
    },
    {
        "area": "State management",
        "status": "implemented",
        "evidence": "AgentRunReport stores status, final answer, tool calls, attached report, evaluation, and trace_id.",
        "resume_signal": "stateful agent reporting",
    },
    {
        "area": "Planning and replanning",
        "status": "partial",
        "evidence": "The model can inspect strategy, profile, memory, checks, and report tools iteratively, but there is no explicit editable plan object yet.",
        "next_step": "Add a compact plan state with current hypothesis, next tool, and stop reason after each loop.",
        "resume_signal": "agent planning roadmap",
    },
    {
        "area": "Termination conditions",
        "status": "implemented",
        "evidence": "The loop stops on final model answer, attached quality report, disabled model fallback, or max-round budget.",
        "resume_signal": "bounded autonomous loop",
    },
    {
        "area": "Permissions and safety",
        "status": "implemented",
        "evidence": "The agent is read-only, uses a tool allowlist, limits database access, redacts sensitive fields, and verifies final reports.",
        "resume_signal": "AI safety boundary",
    },
    {
        "area": "Error handling and fallback",
        "status": "implemented",
        "evidence": "Missing OPENAI_API_KEY returns a structured DISABLED fallback instead of failing the API.",
        "resume_signal": "production-minded fallback",
    },
    {
        "area": "Context management",
        "status": "implemented",
        "evidence": "The model receives dataset metadata, profiles, redacted samples, and finding evidence rather than full private tables.",
        "resume_signal": "privacy-aware prompting",
    },
    {
        "area": "Memory",
        "status": "partial",
        "evidence": "The agent can retrieve sanitized prior traces and recurring incident patterns, but feedback labels do not yet update ranking.",
        "next_step": "Use accepted and needs-review hypothesis labels to adjust later root-cause ranking.",
        "resume_signal": "dataset memory",
    },
    {
        "area": "RAG",
        "status": "partial",
        "evidence": "The agent retrieves source-cited local business rules, but embedding/vector search is not implemented yet.",
        "next_step": "Add optional embedding-backed retrieval for larger business-rule and incident documents.",
        "resume_signal": "source-cited retrieval",
    },
    {
        "area": "Structured output",
        "status": "implemented",
        "evidence": "QualityReport and AgentRunReport are Pydantic models with findings, hypotheses, evidence, telemetry, and verification.",
        "resume_signal": "machine-verifiable AI output",
    },
    {
        "area": "Fact/inference separation",
        "status": "implemented",
        "evidence": "The report separates findings, likely causes, root-cause hypotheses, recommended actions, evidence, and limitations.",
        "resume_signal": "evidence-backed reasoning",
    },
    {
        "area": "Guardrails and verification",
        "status": "implemented",
        "evidence": "ReportVerifier checks evidence support, known fields, sensitive terms, unsupported LLM evidence, and score bounds.",
        "resume_signal": "deterministic AI guardrails",
    },
    {
        "area": "Observability",
        "status": "partial",
        "evidence": "Trace ids, tool-call previews, fallback status, latency, token/cost fields, and SQLite trace persistence exist, but there is no full monitoring dashboard.",
        "next_step": "Expose aggregate latency, cost, retry, and per-tool success metrics in a dashboard.",
        "resume_signal": "agent observability",
    },
    {
        "area": "Evaluation",
        "status": "partial",
        "evidence": "Scenario evals cover status accuracy, finding recall, evidence support, fallback, report-tool usage, and latency.",
        "next_step": "Add a larger labeled eval set for tool-choice accuracy, false positives, evidence support, and cost.",
        "resume_signal": "agent evaluation harness",
    },
    {
        "area": "Deployment and versioning",
        "status": "implemented",
        "evidence": "The repo publishes a FastAPI app, Docker image, public demo docs, OpenAPI artifact, CI, release notes, and public evidence checks.",
        "resume_signal": "shipping discipline",
    },
    {
        "area": "Real-model production evidence",
        "status": "not_claimed",
        "evidence": "The repo has a real-model runbook, capture gate, and preflight, but accepted_real_model_run_count is still 0.",
        "next_step": "Run one explicit paid or approved OpenAI-compatible trace, redact it, and pass the capture verifier.",
        "resume_signal": "blocked until real model evidence",
    },
]


def build_agent_maturity_audit() -> dict[str, Any]:
    capability = load_json(AGENT_CAPABILITY_MATRIX_PATH)
    ai_readiness = load_json(AI_ENGINEER_READINESS_PATH)
    readiness = load_json(AGENT_READINESS_PATH)
    preflight = load_json(REAL_MODEL_PREFLIGHT_PATH)
    status_counts = {
        status: sum(1 for row in AUDIT_ROWS if row["status"] == status)
        for status in ("implemented", "partial", "not_claimed")
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_agent_maturity_audit.py",
        "purpose": (
            "Map the project against a practical 20-point LLM agent maturity checklist so resume claims stay "
            "evidence-backed and weak areas remain explicit."
        ),
        "audit_row_count": len(AUDIT_ROWS),
        "status_counts": status_counts,
        "maturity_level": "real_llm_agent_foundation",
        "source_artifacts": [
            "docs/agent-capability-matrix.json",
            "docs/agent-readiness.json",
            "docs/ai-engineer-readiness.json",
            "docs/real-model-preflight.json",
        ],
        "cross_checks": {
            "capability_matrix_implemented": capability["implemented_count"],
            "allowed_tools": capability["tool_count"],
            "ai_engineer_signals": ai_readiness["implemented_signal_count"],
            "agent_readiness_implemented": len(readiness["implemented"]),
            "accepted_real_model_runs": ai_readiness["evidence_counts"]["real_model_capture_accepted_runs"],
            "real_model_preflight_status": preflight["real_model_execution_status"],
        },
        "audit_rows": AUDIT_ROWS,
        "resume_safe_summary": (
            f"Published a 20-point LLM agent maturity audit with {status_counts['implemented']} implemented areas, "
            f"{status_counts['partial']} partial areas, {capability['tool_count']} controlled tools, "
            "structured output, guardrails, traceability, and an explicit zero accepted-real-model-run boundary."
        ),
        "not_claimed": [
            "production users",
            "customer feedback",
            "enterprise deployment",
            "embedding-backed RAG",
            "accepted real-model benchmark run",
            "autonomous write actions",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {area} | {status} | {evidence} | {resume_signal} |".format(**row)
        for row in payload["audit_rows"]
    )
    next_steps = "\n".join(
        f"- {row['area']}: {row['next_step']}"
        for row in payload["audit_rows"]
        if row.get("next_step")
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Agent Maturity Audit

{payload["purpose"]}

## Summary

| Metric | Value |
| --- | ---: |
| Audit rows | {payload["audit_row_count"]} |
| Implemented areas | {payload["status_counts"]["implemented"]} |
| Partial areas | {payload["status_counts"]["partial"]} |
| Not-claimed areas | {payload["status_counts"]["not_claimed"]} |
| Allowed tools | {payload["cross_checks"]["allowed_tools"]} |
| AI Engineer signals | {payload["cross_checks"]["ai_engineer_signals"]} |
| Accepted real-model runs | {payload["cross_checks"]["accepted_real_model_runs"]} |

## Checklist

| Area | Status | Evidence | Resume Signal |
| --- | --- | --- | --- |
{rows}

## Next Upgrades

{next_steps}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_agent_maturity_audit(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["audit_row_count"] != 20:
        raise AssertionError("agent maturity audit must map exactly 20 checklist areas")
    if payload["status_counts"]["implemented"] < 14:
        raise AssertionError("agent maturity audit must preserve at least 14 implemented areas")
    if payload["status_counts"]["partial"] < 4:
        raise AssertionError("agent maturity audit must preserve explicit partial areas")
    if payload["cross_checks"]["allowed_tools"] != 9:
        raise AssertionError("agent maturity audit must cross-check the 9 controlled tools")
    if payload["cross_checks"]["accepted_real_model_runs"] != 0:
        raise AssertionError("agent maturity audit must not claim accepted real-model runs yet")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("tool calling", "guardrails", "structured output", "not_claimed", "evidence-backed"):
        if required not in joined:
            raise AssertionError(f"agent maturity audit must mention {required}")
    return {
        "agent_maturity_audit_verified": True,
        "audit_row_count": payload["audit_row_count"],
        "implemented_area_count": payload["status_counts"]["implemented"],
        "partial_area_count": payload["status_counts"]["partial"],
        "accepted_real_model_runs": payload["cross_checks"]["accepted_real_model_runs"],
    }


def main() -> None:
    payload = build_agent_maturity_audit()
    verify_agent_maturity_audit(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
