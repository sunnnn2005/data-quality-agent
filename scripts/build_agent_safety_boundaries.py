import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.data import DATASETS, load_dataset
from app.llm import LLMDataQualityAdvisor
from app.postgres_adapter import PostgresAdapterError, PostgresDatasetAdapter
from app.profiler import DatasetProfiler
from app.tool_agent import DataQualityToolbox, LLMDataQualityAgent
from app.verifier import ReportVerifier


OUTPUT_JSON_PATH = ROOT / "docs" / "agent-safety-boundaries.json"
OUTPUT_MD_PATH = ROOT / "docs" / "agent-safety-boundaries.md"


def build_agent_safety_boundaries_payload() -> dict[str, Any]:
    dataset = DATASETS["orders_daily"]
    frame = load_dataset(dataset.id)
    profile = DatasetProfiler().profile(dataset, frame)
    toolbox = DataQualityToolbox(dataset, frame)
    advisor = LLMDataQualityAdvisor()
    redacted = advisor._redact({"email": "student@example.com", "safe_count": 4})
    rejected_queries = _count_rejected_queries()
    verifier_rules = ReportVerifier().verify(toolbox.det_agent.analyze(dataset, frame)).checked_rules
    tool_names = [item["function"]["name"] for item in toolbox.schemas()]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_agent_safety_boundaries.py",
        "tool_allowlist_count": len(tool_names),
        "tool_allowlist": tool_names,
        "postgres_rejected_write_query_count": rejected_queries,
        "postgres_row_limit": PostgresDatasetAdapter().row_limit,
        "postgres_max_row_limit": 10_000,
        "llm_sensitive_redaction_verified": redacted["email"] == "[REDACTED]",
        "agent_disabled_fallback_verified": LLMDataQualityAgent().run(dataset, frame).status == "DISABLED",
        "verifier_rule_count": len(verifier_rules),
        "verifier_rules": verifier_rules,
        "prompt_payload_column_count": len(advisor._build_prompt_payload(profile, [])["columns"]),
        "resume_safe_summary": (
            "Generated a safety-boundary artifact covering tool allowlists, read-only PostgreSQL query limits, "
            "sensitive-field redaction, disabled-agent fallback, and deterministic report verification rules."
        ),
        "not_claimed": [
            "formal security audit",
            "penetration test",
            "SOC 2 compliance",
        ],
    }


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
    tools = "\n".join(f"- `{item}`" for item in payload["tool_allowlist"])
    rules = "\n".join(f"- `{item}`" for item in payload["verifier_rules"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Agent Safety Boundaries

This generated artifact summarizes the local safety boundaries around the LLM agent. It is not a formal security audit.

## Verified Boundaries

| Boundary | Value |
| --- | ---: |
| Tool allowlist count | {payload["tool_allowlist_count"]} |
| Rejected unsafe PostgreSQL queries | {payload["postgres_rejected_write_query_count"]} |
| Default PostgreSQL row limit | {payload["postgres_row_limit"]} |
| Verifier rule count | {payload["verifier_rule_count"]} |
| Sensitive redaction verified | {payload["llm_sensitive_redaction_verified"]} |
| Disabled-agent fallback verified | {payload["agent_disabled_fallback_verified"]} |

## Tool Allowlist

{tools}

## Verifier Rules

{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_agent_safety_boundaries(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "tool_allowlist_count": 6,
        "postgres_rejected_write_query_count": 3,
        "verifier_rule_count": 6,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    if payload["postgres_row_limit"] <= 0 or payload["postgres_row_limit"] > payload["postgres_max_row_limit"]:
        raise AssertionError("PostgreSQL row limit must be bounded")
    if payload["llm_sensitive_redaction_verified"] is not True:
        raise AssertionError("LLM prompt payload must redact sensitive fields")
    if payload["agent_disabled_fallback_verified"] is not True:
        raise AssertionError("agent must return a safe disabled fallback without model credentials")
    for required_tool in ("select_quality_strategy", "run_quality_checks", "build_quality_report"):
        if required_tool not in payload["tool_allowlist"]:
            raise AssertionError(f"tool allowlist missing {required_tool}")
    for required in ("finding_evidence_required", "sensitive_value_redaction", "quality_score_bounds"):
        if required not in payload["verifier_rules"]:
            raise AssertionError(f"verifier rules missing {required}")
    if "formal security audit" not in payload["not_claimed"]:
        raise AssertionError("safety artifact must not claim a formal security audit")
    return {"agent_safety_boundaries_verified": True, **expected}


def main() -> None:
    payload = build_agent_safety_boundaries_payload()
    verify_agent_safety_boundaries(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
