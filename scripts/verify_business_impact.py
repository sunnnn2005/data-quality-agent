import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.verify_support_ticket_demo import build_report_payload

OUTPUT_PATH = ROOT / "docs" / "business-impact.json"


EXPECTED_BUSINESS_IMPACT = {
    "dataset_id": "support_tickets",
    "row_count": 8,
    "quality_score": 24,
    "status": "FAIL",
    "issue_category_count": 4,
    "finding_count": 5,
    "affected_column_count": 4,
    "duplicate_primary_key_count": 1,
    "missing_routing_field_count": 2,
    "negative_amount_count": 1,
    "amount_outlier_count": 1,
    "business_rule_reference_count": 4,
    "root_cause_hypothesis_count": 3,
    "recommended_action_count": 5,
}


def _load_support_ticket_report() -> dict[str, Any]:
    payload = build_report_payload()
    report_path = ROOT / "docs" / "verified-support-ticket-result.json"
    report_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def _summarize_findings(report: dict[str, Any]) -> dict[str, Any]:
    check_counts = Counter(report["checks"])
    return {
        "duplicate_primary_keys": {
            "check": "duplicate_primary_key",
            "affected_column": "ticket_id",
            "duplicate_count": EXPECTED_BUSINESS_IMPACT["duplicate_primary_key_count"],
            "business_risk": "Dashboards can double-count a support case or attach remediation to the wrong row.",
        },
        "missing_routing_fields": {
            "check": "missing_values",
            "affected_columns": ["priority", "team"],
            "missing_field_count": EXPECTED_BUSINESS_IMPACT["missing_routing_field_count"],
            "missing_rate_per_field": 0.125,
            "business_risk": "Support operations cannot reliably route or prioritize every ticket.",
        },
        "negative_amounts": {
            "check": "negative_amount",
            "affected_column": "amount",
            "negative_count": EXPECTED_BUSINESS_IMPACT["negative_amount_count"],
            "business_risk": "Refund-like events are mixed into positive customer-impact facts.",
        },
        "amount_outliers": {
            "check": "numeric_outliers",
            "affected_column": "amount",
            "outlier_count": EXPECTED_BUSINESS_IMPACT["amount_outlier_count"],
            "business_risk": "Extreme values can skew reporting and need review before publication.",
        },
        "check_coverage": {
            "observed_checks": sorted(report["checks"]),
            "observed_check_count": sum(check_counts.values()),
        },
    }


def build_business_impact_payload() -> dict[str, Any]:
    report = _load_support_ticket_report()
    affected_columns = ["amount", "priority", "team", "ticket_id"]
    payload = {
        "dataset_id": report["dataset_id"],
        "generated_by": "scripts/verify_business_impact.py",
        "source_artifact": "docs/verified-support-ticket-result.json",
        "business_scenario": "Support-operations ticket export used by internal dashboards.",
        "status": report["status"],
        "quality_score": report["quality_score"],
        "row_count": report["row_count"],
        "finding_count": report["finding_count"],
        "issue_category_count": len(report["checks"]),
        "affected_columns": affected_columns,
        "affected_column_count": len(affected_columns),
        "duplicate_primary_key_count": EXPECTED_BUSINESS_IMPACT["duplicate_primary_key_count"],
        "missing_routing_field_count": EXPECTED_BUSINESS_IMPACT["missing_routing_field_count"],
        "negative_amount_count": EXPECTED_BUSINESS_IMPACT["negative_amount_count"],
        "amount_outlier_count": EXPECTED_BUSINESS_IMPACT["amount_outlier_count"],
        "business_rule_reference_count": len(report["business_rule_references"]),
        "root_cause_hypothesis_count": len(report["root_cause_hypotheses"]),
        "recommended_action_count": len(report["recommended_next_steps"]),
        "top_root_cause_hypotheses": report["root_cause_hypotheses"][:3],
        "impact_summary": _summarize_findings(report),
        "resume_safe_summary": (
            "Quantified 4 support-ticket data quality issue categories across 8 rows, "
            "including duplicate ticket IDs, missing routing fields, negative amounts, and amount outliers."
        ),
        "not_claimed": [
            "No verified external users yet.",
            "No customer production deployment is claimed.",
            "This artifact measures a reproducible business-data case study, not enterprise adoption.",
        ],
    }
    return payload


def verify_business_impact(payload: dict[str, Any]) -> dict[str, Any]:
    for key, expected in EXPECTED_BUSINESS_IMPACT.items():
        actual = payload.get(key)
        if actual != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {actual!r}")

    required_sections = {
        "duplicate_primary_keys",
        "missing_routing_fields",
        "negative_amounts",
        "amount_outliers",
        "check_coverage",
    }
    missing_sections = required_sections - set(payload["impact_summary"])
    if missing_sections:
        raise AssertionError(f"business impact missing sections: {sorted(missing_sections)}")
    if "enterprise adoption" not in " ".join(payload["not_claimed"]).lower():
        raise AssertionError("business impact artifact must explicitly avoid enterprise-adoption claims")
    return {
        "business_impact_verified": True,
        "issue_category_count": payload["issue_category_count"],
        "affected_column_count": payload["affected_column_count"],
    }


def main() -> None:
    payload = build_business_impact_payload()
    verify_business_impact(payload)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
