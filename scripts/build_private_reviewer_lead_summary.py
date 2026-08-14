import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_private_reviewer_lead_workflow import (
    ALLOWED_STATUSES,
    PRIVATE_LEAD_PATH,
    REQUIRED_COLUMNS,
    TARGET_METRICS,
)


PRIVATE_LEADS_CSV_PATH = ROOT / PRIVATE_LEAD_PATH
OUTPUT_JSON_PATH = ROOT / "docs" / "private-reviewer-lead-summary.json"
OUTPUT_MD_PATH = ROOT / "docs" / "private-reviewer-lead-summary.md"
SENSITIVE_COLUMNS = {"private_contact_label", "notes_private"}


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise AssertionError("private reviewer lead CSV columns must match the published workflow schema")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def _validate_row(row: dict[str, str], index: int) -> list[str]:
    errors: list[str] = []
    if not row["lead_id"]:
        errors.append(f"row {index}: lead_id is required")
    if not row["reviewer_segment"]:
        errors.append(f"row {index}: reviewer_segment is required")
    if row["status"] not in ALLOWED_STATUSES:
        errors.append(f"row {index}: unsupported status {row['status']!r}")
    if row["target_metric"] not in TARGET_METRICS:
        errors.append(f"row {index}: unsupported target_metric {row['target_metric']!r}")
    if row["status"] in {"public_issue_submitted", "accepted_evidence"} and not row["public_evidence_url"]:
        errors.append(f"row {index}: public evidence statuses require public_evidence_url")
    if row["status"] == "accepted_evidence":
        if row["permission_to_count"].lower() != "true":
            errors.append(f"row {index}: accepted_evidence requires permission_to_count=true")
        if row["no_private_data_confirmed"].lower() != "true":
            errors.append(f"row {index}: accepted_evidence requires no_private_data_confirmed=true")
    return errors


def build_private_reviewer_lead_summary(path: Path = PRIVATE_LEADS_CSV_PATH) -> dict[str, Any]:
    rows = _read_csv_rows(path)
    validation_errors: list[str] = []
    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()
    for index, row in enumerate(rows, start=2):
        validation_errors.extend(_validate_row(row, index))
        lead_id = row.get("lead_id", "")
        if lead_id in seen_ids:
            duplicate_ids.add(lead_id)
        if lead_id:
            seen_ids.add(lead_id)
    for lead_id in sorted(duplicate_ids):
        validation_errors.append(f"duplicate lead_id: {lead_id}")

    status_counts = Counter(row["status"] for row in rows)
    metric_counts = Counter(row["target_metric"] for row in rows)
    due_next_count = sum(1 for row in rows if row.get("next_action_date"))
    public_evidence_count = sum(1 for row in rows if row.get("public_evidence_url"))
    accepted_ready_count = sum(
        1
        for row in rows
        if row.get("status") == "accepted_evidence"
        and row.get("permission_to_count", "").lower() == "true"
        and row.get("no_private_data_confirmed", "").lower() == "true"
        and row.get("public_evidence_url")
    )

    redacted_preview = [
        {
            "lead_id": row["lead_id"],
            "reviewer_segment": row["reviewer_segment"],
            "channel": row["channel"],
            "target_metric": row["target_metric"],
            "status": row["status"],
            "next_action_date": row["next_action_date"],
            "has_public_evidence_url": bool(row["public_evidence_url"]),
            "permission_to_count": row["permission_to_count"].lower() == "true",
            "no_private_data_confirmed": row["no_private_data_confirmed"].lower() == "true",
        }
        for row in rows[:10]
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_private_reviewer_lead_summary.py",
        "purpose": (
            "Validate the ignored local reviewer lead CSV and publish only a redacted progress summary that can guide "
            "real outreach without leaking private contacts or upgrading resume outcomes."
        ),
        "private_source_path": PRIVATE_LEAD_PATH,
        "private_source_exists": path.exists(),
        "lead_count": len(rows),
        "status_counts": {status: status_counts.get(status, 0) for status in ALLOWED_STATUSES},
        "target_metric_counts": {metric: metric_counts.get(metric, 0) for metric in TARGET_METRICS},
        "due_next_action_count": due_next_count,
        "public_evidence_url_count": public_evidence_count,
        "accepted_ready_count": accepted_ready_count,
        "validation_error_count": len(validation_errors),
        "validation_errors": validation_errors,
        "redacted_preview": redacted_preview,
        "redacted_preview_count": len(redacted_preview),
        "sensitive_columns_excluded": sorted(SENSITIVE_COLUMNS),
        "resume_outcome_upgraded": False,
        "not_claimed": [
            "Private lead rows are not public evidence.",
            "Private reviewer names, emails, handles, and notes are not published.",
            "No users, feedback, business validation, AI reviews, or GitHub stars are claimed from this summary.",
        ],
        "resume_safe_summary": (
            f"Published a privacy-preserving reviewer lead summary with {len(rows)} local private leads, "
            f"{public_evidence_count} public evidence URLs, {accepted_ready_count} evidence-ready rows, "
            f"{len(validation_errors)} validation errors, and zero resume outcome upgrades."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    status_rows = "\n".join(
        f"| `{status}` | {count} |" for status, count in payload["status_counts"].items()
    )
    metric_rows = "\n".join(
        f"| `{metric}` | {count} |" for metric, count in payload["target_metric_counts"].items()
    )
    errors = "\n".join(f"- {error}" for error in payload["validation_errors"]) or "- None"
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Private Reviewer Lead Summary

This generated summary validates the local private reviewer lead CSV and publishes only redacted progress.

## Source

- Private path: `{payload["private_source_path"]}`
- Source exists locally: `{payload["private_source_exists"]}`
- Lead count: `{payload["lead_count"]}`
- Sensitive columns excluded: `{', '.join(payload["sensitive_columns_excluded"])}`

## Status Counts

| Status | Count |
| --- | ---: |
{status_rows}

## Target Metric Counts

| Metric | Count |
| --- | ---: |
{metric_rows}

## Validation

- Public evidence URLs: `{payload["public_evidence_url_count"]}`
- Evidence-ready rows: `{payload["accepted_ready_count"]}`
- Validation errors: `{payload["validation_error_count"]}`

{errors}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_private_reviewer_lead_summary(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["resume_outcome_upgraded"] is not False:
        raise AssertionError("private lead summary must not upgrade resume outcomes")
    if payload["sensitive_columns_excluded"] != sorted(SENSITIVE_COLUMNS):
        raise AssertionError("private lead summary must exclude sensitive columns")
    serialized = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("notes_private", "private_contact_label"):
        if forbidden in serialized and forbidden not in payload["sensitive_columns_excluded"]:
            raise AssertionError(f"private lead summary leaked sensitive column {forbidden}")
    if "private lead rows are not public evidence" not in serialized:
        raise AssertionError("private lead summary must state private rows are not public evidence")
    if payload["accepted_ready_count"] > payload["public_evidence_url_count"]:
        raise AssertionError("accepted-ready rows cannot exceed public evidence URL rows")
    return {
        "private_reviewer_lead_summary_verified": True,
        "lead_count": payload["lead_count"],
        "public_evidence_url_count": payload["public_evidence_url_count"],
        "accepted_ready_count": payload["accepted_ready_count"],
        "validation_error_count": payload["validation_error_count"],
    }


def main() -> None:
    payload = build_private_reviewer_lead_summary()
    verify_private_reviewer_lead_summary(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
