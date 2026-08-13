import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
BUSINESS_DATA_INTAKE_PATH = ROOT / "docs" / "business-data-intake-baseline.json"
REVIEWER_PACKET_PATH = ROOT / "docs" / "reviewer-feedback-packet.json"
REPLAY_TEMPLATE_PATH = ROOT / ".github" / "ISSUE_TEMPLATE" / "business_data_replay.md"
LABELS_PATH = ROOT / ".github" / "labels.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "business-data-replay-packet.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-data-replay-packet.md"
REPLAY_SUBMISSION_URL = (
    "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md"
)


REPLAY_PATHS = [
    {
        "id": "sanitized_csv_upload",
        "audience": "student_developer_or_data_practitioner",
        "data_source": "non-sensitive CSV export",
        "endpoint": "POST /business-data/agent-report",
        "command": (
            "curl -X POST http://127.0.0.1:8000/business-data/agent-report "
            "-F file=@sample.csv -F dataset_name='Replay Dataset' -F owner='reviewer' "
            "-F primary_key='id' -F expected_columns='id,status,amount,created_at'"
        ),
        "counts_toward": "confirmed_external_users",
        "evidence_required": "GitHub issue with dataset shape, command used, status, finding count, and redacted output summary",
    },
    {
        "id": "readonly_postgres_table",
        "audience": "backend_or_data_engineering_reviewer",
        "data_source": "read-only PostgreSQL table or local compose table",
        "endpoint": "POST /postgres/support-tickets/agent-report",
        "command": "docker compose up --build && curl -X POST http://127.0.0.1:8000/postgres/support-tickets/agent-report",
        "counts_toward": "confirmed_external_users",
        "evidence_required": "GitHub issue confirming read-only run, table row count, selected tools, and report status",
    },
    {
        "id": "business_case_replay",
        "audience": "mentor_recruiter_or_data_practitioner",
        "data_source": "anonymized description of a real workflow problem",
        "endpoint": "docs/business-case-intake.md",
        "command": "Open the business-case issue template and submit only anonymized context, tried path, outcome, and permission boundary.",
        "counts_toward": "business_case_feedback_items",
        "evidence_required": "Public business-case issue with business-case label and no raw customer data",
    },
]

REPLAY_EVIDENCE_FIELDS = [
    "path_tried",
    "data_source_type",
    "row_count_or_table_size",
    "selected_tools",
    "report_status",
    "finding_count",
    "usefulness_rating",
    "permission_boundary",
]

SAFETY_REQUIREMENTS = [
    "Use non-sensitive, anonymized, or synthetic-but-business-shaped data only.",
    "Do not upload customer names, emails, addresses, tokens, secrets, or raw production exports.",
    "Use read-only database credentials and bounded row limits.",
    "Submit public evidence summaries, not raw data.",
    "Mark whether the replay can be counted as feedback, confirmed run, reproducible issue, or business case.",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_business_data_replay_packet() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    intake = load_json(BUSINESS_DATA_INTAKE_PATH)
    reviewer = load_json(REVIEWER_PACKET_PATH)
    labels = load_json(LABELS_PATH)
    replay_template = REPLAY_TEMPLATE_PATH.read_text()
    current_counts = {
        "external_feedback_items": feedback["external_feedback_items"],
        "confirmed_external_users": feedback["confirmed_external_users"],
        "business_case_feedback_items": feedback["business_case_feedback_items"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
    }
    endpoint_verification = intake["endpoint_verification"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_data_replay_packet.py",
        "purpose": (
            "Give reviewers a safe, repeatable way to replay the agent against their own anonymized business-shaped "
            "CSV or read-only database data, then submit public evidence that can later upgrade resume outcomes."
        ),
        "replay_path_count": len(REPLAY_PATHS),
        "replay_paths": REPLAY_PATHS,
        "evidence_field_count": len(REPLAY_EVIDENCE_FIELDS),
        "evidence_fields": REPLAY_EVIDENCE_FIELDS,
        "safety_requirement_count": len(SAFETY_REQUIREMENTS),
        "safety_requirements": SAFETY_REQUIREMENTS,
        "verified_input_boundaries": {
            "business_data_endpoint_verified": endpoint_verification["csv_agent_report"],
            "postgres_agent_endpoint_verified": endpoint_verification["postgres_agent_report"],
            "max_rows": intake["safety_limits"]["max_rows"],
            "max_columns": intake["safety_limits"]["max_columns"],
            "csv_only": intake["safety_limits"]["csv_only"],
            "primary_key_required": intake["safety_limits"]["primary_key_required"],
        },
        "current_public_counts": current_counts,
        "submission_urls": {
            **{task["counts_toward"]: task["submission_url"] for task in reviewer["reviewer_tasks"]},
            "business_data_replay": REPLAY_SUBMISSION_URL,
        },
        "replay_issue_template": {
            "path": ".github/ISSUE_TEMPLATE/business_data_replay.md",
            "url": REPLAY_SUBMISSION_URL,
            "required_section_count": replay_template.count("## "),
            "required_labels": ["feedback", "confirmed-user", "business-data-replay"],
            "label_verified": any(label["name"] == "business-data-replay" for label in labels),
        },
        "resume_upgrade_rules": [
            {
                "metric": "confirmed_external_users",
                "current_value": feedback["confirmed_external_users"],
                "minimum_before_claim": 1,
                "claim_when_met": "at least one external reviewer replayed the agent on a business-shaped dataset",
            },
            {
                "metric": "business_case_feedback_items",
                "current_value": feedback["business_case_feedback_items"],
                "minimum_before_claim": 1,
                "claim_when_met": "at least one anonymized real-world data-quality problem was reviewed publicly",
            },
            {
                "metric": "reproducible_feedback_items",
                "current_value": feedback["reproducible_feedback_items"],
                "minimum_before_claim": 1,
                "claim_when_met": "at least one reproducible issue or missed quality rule was submitted publicly",
            },
        ],
        "resume_status": "replay_ready_not_claimable",
        "resume_safe_summary": (
            "Published a CI-verified business-data replay packet with 3 safe replay paths, 8 evidence fields, "
            "5 safety requirements, and zero current external replay claims."
        ),
        "not_claimed": [
            "external replay completed",
            "real company data analyzed",
            "customer feedback",
            "enterprise production usage",
            "raw production data stored",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    paths = "\n".join(
        "| {id} | {data_source} | `{endpoint}` | `{counts_toward}` | {evidence_required} |".format(**path)
        for path in payload["replay_paths"]
    )
    commands = "\n\n".join(
        f"### {path['id']}\n\n```bash\n{path['command']}\n```" for path in payload["replay_paths"]
    )
    fields = "\n".join(f"- `{field}`" for field in payload["evidence_fields"])
    safety = "\n".join(f"- {item}" for item in payload["safety_requirements"])
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_public_counts"].items()
    )
    template = payload["replay_issue_template"]
    rules = "\n".join(
        "| {metric} | {current_value} | {minimum_before_claim} | {claim_when_met} |".format(**rule)
        for rule in payload["resume_upgrade_rules"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Business Data Replay Packet

This generated packet gives reviewers a safe way to replay the agent on business-shaped data and submit public evidence without inflating current outcome claims.

## Purpose

{payload["purpose"]}

## Replay Paths

| Path | Data Source | Endpoint | Counts Toward | Evidence Required |
| --- | --- | --- | --- | --- |
{paths}

## Commands

{commands}

## Evidence Fields

{fields}

## Safety Requirements

{safety}

## Current Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Replay Evidence Submission

- Template: [`{template["path"]}`]({template["url"]})
- Required sections: `{template["required_section_count"]}`
- Required labels: `{", ".join(template["required_labels"])}`

## Resume Upgrade Rules

| Metric | Current value | Minimum before claim | Claim when met |
| --- | ---: | ---: | --- |
{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_business_data_replay_packet(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "replay_path_count": 3,
        "evidence_field_count": 8,
        "safety_requirement_count": 5,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    boundaries = payload["verified_input_boundaries"]
    if boundaries["business_data_endpoint_verified"] is not True:
        raise AssertionError("business-data replay packet must verify the business agent endpoint")
    if boundaries["postgres_agent_endpoint_verified"] is not True:
        raise AssertionError("business-data replay packet must verify the PostgreSQL agent endpoint")
    if boundaries["max_rows"] != 10_000 or boundaries["max_columns"] != 80:
        raise AssertionError("business-data replay packet must preserve bounded input limits")
    if boundaries["csv_only"] is not True or boundaries["primary_key_required"] is not True:
        raise AssertionError("business-data replay packet must verify CSV and primary-key constraints")
    if payload["current_public_counts"] != {
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "business_case_feedback_items": 0,
        "reproducible_feedback_items": 0,
    }:
        raise AssertionError("business-data replay packet must preserve current zero external replay counts")
    if payload["resume_status"] != "replay_ready_not_claimable":
        raise AssertionError("business-data replay packet must not claim external replay before evidence")
    template = payload["replay_issue_template"]
    if template["url"] != REPLAY_SUBMISSION_URL:
        raise AssertionError("business-data replay packet must link the dedicated replay issue template")
    if template["required_section_count"] < 8:
        raise AssertionError("business-data replay issue template must collect the full evidence packet")
    if template["label_verified"] is not True:
        raise AssertionError("business-data replay label must be configured")
    if set(template["required_labels"]) != {"feedback", "confirmed-user", "business-data-replay"}:
        raise AssertionError("business-data replay template must use feedback, confirmed-user, and replay labels")
    required_counts = {"confirmed_external_users", "business_case_feedback_items"}
    if not required_counts <= set(payload["submission_urls"]):
        raise AssertionError("business-data replay packet must link submission URLs for replay and business-case evidence")
    for path in payload["replay_paths"]:
        if path["counts_toward"] not in payload["submission_urls"]:
            raise AssertionError(f"replay path missing submission route for {path['counts_toward']}")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("real company data analyzed", "external replay completed", "enterprise production usage"):
        if forbidden not in joined:
            raise AssertionError(f"business-data replay packet must explicitly not claim {forbidden}")
    return {"business_data_replay_packet_verified": True, **expected}


def main() -> None:
    payload = build_business_data_replay_packet()
    verify_business_data_replay_packet(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
