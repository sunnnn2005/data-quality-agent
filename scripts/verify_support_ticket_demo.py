import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agent import DataQualityAgent
from app.models import DatasetSummary


CSV_PATH = ROOT / "examples" / "support_tickets.csv"
OUTPUT_PATH = ROOT / "docs" / "verified-support-ticket-result.json"
EXPECTED_CHECKS = {"duplicate_primary_key", "missing_values", "negative_amount", "numeric_outliers"}
EXPECTED_RULES = {"support_tickets:R1", "support_tickets:R2", "support_tickets:R3", "support_tickets:R4"}


def build_report_payload() -> dict[str, Any]:
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
    report = DataQualityAgent().analyze(dataset, frame)
    checks = {finding.check_name for finding in report.findings}
    rules = {reference.rule_id for reference in report.business_rule_references}

    assert report.status == "FAIL"
    assert report.quality_score == 24
    assert report.row_count == 8
    assert EXPECTED_CHECKS <= checks
    assert EXPECTED_RULES <= rules

    return {
        "dataset_id": report.dataset.id,
        "generated_by": "scripts/verify_support_ticket_demo.py",
        "status": report.status,
        "quality_score": report.quality_score,
        "row_count": report.row_count,
        "finding_count": len(report.findings),
        "checks": sorted(checks),
        "business_rule_references": sorted(rules),
        "likely_causes": report.likely_causes,
        "recommended_next_steps": report.recommended_next_steps,
    }


def main() -> None:
    payload = build_report_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
