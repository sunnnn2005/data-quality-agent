import csv
import json
from io import StringIO
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GITIGNORE_PATH = ROOT / ".gitignore"
OUTPUT_JSON_PATH = ROOT / "docs" / "private-reviewer-lead-workflow.json"
OUTPUT_MD_PATH = ROOT / "docs" / "private-reviewer-lead-workflow.md"

PRIVATE_LEAD_PATH = "private/reviewer-leads.csv"
REQUIRED_COLUMNS = [
    "lead_id",
    "reviewer_segment",
    "private_contact_label",
    "channel",
    "target_metric",
    "status",
    "next_action_date",
    "public_evidence_url",
    "permission_to_count",
    "no_private_data_confirmed",
    "notes_private",
]

ALLOWED_STATUSES = [
    "not_contacted",
    "sent",
    "replied_private",
    "public_issue_submitted",
    "accepted_evidence",
    "declined",
]

TARGET_METRICS = [
    "ai_engineer_review_items",
    "confirmed_external_users",
    "external_feedback_items",
    "reproducible_feedback_items",
    "business_case_feedback_items",
    "github_stars",
]


def _gitignore_patterns() -> set[str]:
    return {
        line.strip()
        for line in GITIGNORE_PATH.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


def _example_csv() -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=REQUIRED_COLUMNS)
    writer.writeheader()
    writer.writerow(
        {
            "lead_id": "lead_001",
            "reviewer_segment": "AI engineer or ML systems mentor",
            "private_contact_label": "keep-real-name-private",
            "channel": "LinkedIn",
            "target_metric": "ai_engineer_review_items",
            "status": "not_contacted",
            "next_action_date": "2026-08-15",
            "public_evidence_url": "",
            "permission_to_count": "false",
            "no_private_data_confirmed": "false",
            "notes_private": "Store real contact details only in the local ignored file.",
        }
    )
    return output.getvalue()


def build_private_reviewer_lead_workflow() -> dict[str, Any]:
    ignored = _gitignore_patterns()
    is_private_path_ignored = "private/" in ignored and "private-reviewer-leads.csv" in ignored
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_private_reviewer_lead_workflow.py",
        "purpose": (
            "Give the project a privacy-safe workflow for tracking real reviewer leads locally while publishing only "
            "redacted, permissioned, non-owner evidence after a reviewer submits a public issue."
        ),
        "private_lead_path": PRIVATE_LEAD_PATH,
        "legacy_private_lead_path": "private-reviewer-leads.csv",
        "private_paths_gitignored": is_private_path_ignored,
        "required_column_count": len(REQUIRED_COLUMNS),
        "required_columns": REQUIRED_COLUMNS,
        "allowed_status_count": len(ALLOWED_STATUSES),
        "allowed_statuses": ALLOWED_STATUSES,
        "target_metric_count": len(TARGET_METRICS),
        "target_metrics": TARGET_METRICS,
        "example_csv": _example_csv(),
        "conversion_rules": [
            "Keep real names, emails, phone numbers, and private notes only in the ignored local CSV.",
            "Record a sent event only after a message is actually sent to a real reviewer.",
            "Do not count private replies as resume evidence.",
            "Ask the reviewer to submit a public redacted GitHub issue before any outcome metric can increase.",
            "Run the external reviewer evidence gate before upgrading any resume claim.",
            "Never ask for fake stars, traded stars, raw customer data, secrets, or private production rows.",
        ],
        "record_sent_command_template": (
            "python scripts/record_reviewer_outreach_event.py --slot-id <review_slot_id> --status sent "
            "--reviewer-contact \"<private label or public handle>\" --channel-used <channel>"
        ),
        "public_evidence_command_template": (
            "python scripts/record_reviewer_outreach_event.py --slot-id <review_slot_id> "
            "--status public_issue_submitted --reviewer-contact \"<public handle>\" --channel-used <channel> "
            "--public-evidence-url <github issue url> --permission-to-count --no-private-data-confirmed"
        ),
        "not_claimed": [
            "This workflow does not claim contacted reviewers until real events are recorded.",
            "This workflow does not claim users, feedback, business validation, AI reviews, or GitHub stars.",
            "Private lead rows are not public evidence.",
        ],
        "resume_safe_summary": (
            "Published a privacy-safe reviewer lead workflow with "
            f"{len(REQUIRED_COLUMNS)} required private CSV columns, {len(ALLOWED_STATUSES)} lead statuses, "
            f"{len(TARGET_METRICS)} target outcome metrics, gitignored private lead paths, and zero upgraded outcome claims."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    columns = "\n".join(f"- `{column}`" for column in payload["required_columns"])
    statuses = "\n".join(f"- `{status}`" for status in payload["allowed_statuses"])
    metrics = "\n".join(f"- `{metric}`" for metric in payload["target_metrics"])
    rules = "\n".join(f"- {rule}" for rule in payload["conversion_rules"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Private Reviewer Lead Workflow

This generated workflow lets real reviewer outreach happen without publishing private contacts.

## Purpose

{payload["purpose"]}

## Private File

- Local path: `{payload["private_lead_path"]}`
- Legacy local path: `{payload["legacy_private_lead_path"]}`
- Gitignored: `{payload["private_paths_gitignored"]}`

## Required Columns

{columns}

## Allowed Statuses

{statuses}

## Target Metrics

{metrics}

## Example CSV

```csv
{payload["example_csv"].strip()}
```

## Commands

Record a real send:

```bash
{payload["record_sent_command_template"]}
```

Record a public evidence submission:

```bash
{payload["public_evidence_command_template"]}
```

## Conversion Rules

{rules}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_private_reviewer_lead_workflow(payload: dict[str, Any]) -> dict[str, Any]:
    if not payload["private_paths_gitignored"]:
        raise AssertionError("private reviewer lead paths must be gitignored")
    if payload["required_columns"] != REQUIRED_COLUMNS:
        raise AssertionError("private reviewer lead workflow must expose the exact required columns")
    if payload["allowed_statuses"] != ALLOWED_STATUSES:
        raise AssertionError("private reviewer lead workflow must expose the allowed statuses")
    if payload["target_metrics"] != TARGET_METRICS:
        raise AssertionError("private reviewer lead workflow must expose the target metrics")
    if "raw customer data" not in json.dumps(payload).lower():
        raise AssertionError("workflow must forbid raw customer data")
    if "private lead rows are not public evidence" not in json.dumps(payload).lower():
        raise AssertionError("workflow must not treat private lead rows as public evidence")
    return {
        "private_reviewer_lead_workflow_verified": True,
        "required_column_count": payload["required_column_count"],
        "allowed_status_count": payload["allowed_status_count"],
        "target_metric_count": payload["target_metric_count"],
    }


def main() -> None:
    payload = build_private_reviewer_lead_workflow()
    verify_private_reviewer_lead_workflow(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
