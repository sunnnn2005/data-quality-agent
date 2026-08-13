import json
from pathlib import Path
import sys
from datetime import datetime, timezone
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agent import DataQualityAgent
from app.models import DatasetSummary
from app.traces import RunTraceStore


OUTPUT_JSON_PATH = ROOT / "docs" / "incident-pattern-memory.json"
OUTPUT_MD_PATH = ROOT / "docs" / "incident-pattern-memory.md"
CSV_PATH = ROOT / "examples" / "support_tickets.csv"


def build_incident_pattern_memory_payload() -> dict[str, Any]:
    dataset = DatasetSummary(
        id="support_tickets",
        name="Support Tickets",
        owner="support-ops",
        primary_key="ticket_id",
        expected_columns=["ticket_id", "team", "priority", "status", "amount", "created_at"],
        description="Support ticket export used by operations dashboards.",
        last_loaded_at=datetime.now(timezone.utc),
    )
    frame = pd.read_csv(CSV_PATH)
    agent = DataQualityAgent()
    store = RunTraceStore()
    for _ in range(2):
        store.save_quality_report(agent.analyze(dataset, frame))
    memory = store.list_by_dataset(dataset.id, limit=5)
    patterns = [pattern.model_dump(mode="json") for pattern in memory.incident_patterns]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_incident_pattern_memory.py",
        "dataset_id": dataset.id,
        "trace_count": memory.trace_count,
        "incident_pattern_count": len(patterns),
        "patterns": patterns,
        "resume_safe_summary": (
            f"Generated dataset memory that retrieved {len(patterns)} recurring incident patterns "
            f"from {memory.trace_count} sanitized support-ticket traces."
        ),
        "not_claimed": [
            "external production incidents",
            "enterprise incident database",
            "customer-validated root causes",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        (
            f"| `{item['pattern_id']}` | {item['title']} | {item['recurrence_count']} | "
            f"{', '.join(item['supporting_checks'])} | {', '.join(item['evidence_trace_ids'])} |"
        )
        for item in payload["patterns"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Incident Pattern Memory

This generated artifact proves that dataset memory can retrieve recurring incident patterns from sanitized traces. It is a reproducible local case study, not evidence of external production incidents.

| Pattern ID | Title | Recurrence count | Supporting checks | Evidence trace IDs |
| --- | --- | ---: | --- | --- |
{rows}

## Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_incident_pattern_memory(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "trace_count": 2,
        "incident_pattern_count": 3,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    if not payload["patterns"]:
        raise AssertionError("incident pattern memory must include patterns")
    for pattern in payload["patterns"]:
        if pattern["recurrence_count"] < 2:
            raise AssertionError("incident patterns must be recurring")
        if not pattern["supporting_checks"]:
            raise AssertionError("incident patterns must include supporting checks")
        if not pattern["evidence_trace_ids"]:
            raise AssertionError("incident patterns must include evidence trace ids")
        if not pattern["recommended_actions"]:
            raise AssertionError("incident patterns must include recommended actions")
    if "external production incidents" not in payload["not_claimed"]:
        raise AssertionError("incident pattern memory must not claim external production incidents")
    return {"incident_pattern_memory_verified": True, **expected}


def main() -> None:
    payload = build_incident_pattern_memory_payload()
    verify_incident_pattern_memory(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
