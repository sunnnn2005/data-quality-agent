import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from app.agent import DataQualityAgent
from app.models import DatasetSummary


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "examples" / "support_tickets.csv"
OUTPUT_JSON_PATH = ROOT / "docs" / "business-replay-demo.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-replay-demo.md"


def build_business_replay_demo() -> dict[str, Any]:
    frame = pd.read_csv(CSV_PATH)
    dataset = DatasetSummary(
        id="support_tickets",
        name="Support Tickets Replay",
        owner="support-ops",
        primary_key="ticket_id",
        expected_columns=["ticket_id", "team", "priority", "status", "amount", "created_at"],
        description="Anonymized business-shaped support-ticket CSV used to replay the data-quality agent.",
        last_loaded_at=datetime.now(timezone.utc),
    )
    report = DataQualityAgent().analyze(dataset, frame)
    checks = sorted({finding.check_name for finding in report.findings})
    severities = sorted({finding.severity.value for finding in report.findings})
    root_causes = [
        {
            "title": hypothesis.title,
            "confidence": hypothesis.confidence,
            "supporting_checks": hypothesis.supporting_checks,
        }
        for hypothesis in report.root_cause_hypotheses
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_replay_demo.py",
        "dataset": {
            "path": "examples/support_tickets.csv",
            "row_count": int(report.row_count),
            "column_count": int(len(frame.columns)),
            "primary_key": dataset.primary_key,
            "expected_columns": dataset.expected_columns,
            "contains_real_company_data": False,
            "contains_pii": False,
        },
        "replay_command": (
            "curl -X POST http://127.0.0.1:8000/business-data/quality-report "
            "-F file=@examples/support_tickets.csv "
            "-F dataset_name='Support Tickets Replay' "
            "-F owner='support-ops' "
            "-F primary_key='ticket_id' "
            "-F expected_columns='ticket_id,team,priority,status,amount,created_at'"
        ),
        "quality_report_summary": {
            "status": report.status,
            "quality_score": report.quality_score,
            "finding_count": len(report.findings),
            "check_count": len(checks),
            "checks": checks,
            "severities": severities,
            "business_rule_reference_count": len(report.business_rule_references),
            "root_cause_hypothesis_count": len(report.root_cause_hypotheses),
            "recommended_action_count": len(report.recommended_next_steps),
            "verification_passed": report.verification.passed if report.verification else False,
            "verification_issue_count": report.verification.issue_count if report.verification else None,
        },
        "root_cause_hypotheses": root_causes,
        "resume_safe_summary": (
            "Published a reproducible business-shaped CSV replay demo that verifies 8 rows, 5 findings, "
            "4 failed check types, 4 business-rule references, 3 root-cause hypotheses, and deterministic report verification."
        ),
        "not_claimed": [
            "real company data",
            "external user replay",
            "customer feedback",
            "production incident resolved",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    dataset = payload["dataset"]
    summary = payload["quality_report_summary"]
    checks = "\n".join(f"- `{check}`" for check in summary["checks"])
    root_causes = "\n".join(
        f"- {item['title']} (`confidence={item['confidence']}`, checks={', '.join(item['supporting_checks'])})"
        for item in payload["root_cause_hypotheses"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Business Replay Demo

This generated artifact proves the business-data path can replay an anonymized support-ticket CSV and produce a verified deterministic report. It does not claim real company data, external users, or customer feedback.

## Dataset

| Field | Value |
| --- | --- |
| Path | `{dataset["path"]}` |
| Rows | {dataset["row_count"]} |
| Columns | {dataset["column_count"]} |
| Primary key | `{dataset["primary_key"]}` |
| Contains real company data | `{dataset["contains_real_company_data"]}` |
| Contains PII | `{dataset["contains_pii"]}` |

## Replay Command

```bash
{payload["replay_command"]}
```

## Verified Report Summary

| Metric | Value |
| --- | ---: |
| Status | `{summary["status"]}` |
| Quality score | {summary["quality_score"]} |
| Findings | {summary["finding_count"]} |
| Failed check types | {summary["check_count"]} |
| Business-rule references | {summary["business_rule_reference_count"]} |
| Root-cause hypotheses | {summary["root_cause_hypothesis_count"]} |
| Recommended actions | {summary["recommended_action_count"]} |
| Verification passed | `{summary["verification_passed"]}` |

## Checks

{checks}

## Root-Cause Hypotheses

{root_causes}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_business_replay_demo(payload: dict[str, Any]) -> dict[str, Any]:
    dataset = payload["dataset"]
    summary = payload["quality_report_summary"]
    expected = {
        "row_count": 8,
        "column_count": 6,
        "finding_count": 5,
        "check_count": 4,
        "business_rule_reference_count": 4,
        "root_cause_hypothesis_count": 3,
        "recommended_action_count": 5,
    }
    for key, value in expected.items():
        source = dataset if key in dataset else summary
        if source.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {source.get(key)!r}")
    if summary["status"] != "FAIL":
        raise AssertionError("business replay demo must expose failing quality status")
    if summary["quality_score"] != 24:
        raise AssertionError("business replay demo must verify expected quality score")
    if summary["verification_passed"] is not True:
        raise AssertionError("business replay demo must pass deterministic verification")
    for required in {"duplicate_primary_key", "missing_values", "negative_amount", "numeric_outliers"}:
        if required not in summary["checks"]:
            raise AssertionError(f"business replay demo missing check {required}")
    if dataset["contains_real_company_data"] is not False or dataset["contains_pii"] is not False:
        raise AssertionError("business replay demo must preserve anonymized-data boundaries")
    for required in ("real company data", "external user replay", "customer feedback"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"business replay demo must not claim {required}")
    return {"business_replay_demo_verified": True, **expected}


def main() -> None:
    payload = build_business_replay_demo()
    verify_business_replay_demo(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
