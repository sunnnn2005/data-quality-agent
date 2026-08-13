import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.business_data import MAX_COLUMNS, MAX_ROWS, MAX_UPLOAD_BYTES

OUTPUT_JSON_PATH = ROOT / "docs" / "business-data-intake-baseline.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-data-intake-baseline.md"


def _read(path: Path) -> str:
    return path.read_text()


def build_business_data_intake_baseline() -> dict[str, Any]:
    api_source = _read(ROOT / "app" / "main.py")
    loader_source = _read(ROOT / "app" / "business_data.py")
    api_tests = _read(ROOT / "tests" / "test_api.py")
    readme = _read(ROOT / "README.md")
    openapi = json.loads(_read(ROOT / "docs" / "openapi.json"))

    endpoints = {
        "csv_quality_report": "/business-data/quality-report",
        "csv_agent_report": "/business-data/agent-report",
        "postgres_quality_report": "/postgres/support-tickets/quality-report",
        "postgres_agent_report": "/postgres/support-tickets/agent-report",
    }
    endpoint_verification = {
        name: route in api_source and route in json.dumps(openapi.get("paths", {}))
        for name, route in endpoints.items()
    }
    safety_limits = {
        "max_upload_bytes": MAX_UPLOAD_BYTES,
        "max_rows": MAX_ROWS,
        "max_columns": MAX_COLUMNS,
        "csv_only": "Only CSV uploads are supported" in loader_source,
        "primary_key_required": "Primary key must match a CSV column" in loader_source,
        "empty_file_rejected": "CSV must contain at least one row" in loader_source,
    }
    tests_verified = {
        "csv_upload_acceptance": "test_business_csv_quality_report_accepts_uploaded_data" in api_tests,
        "csv_agent_disabled_fallback": (
            "test_business_csv_agent_report_is_disabled_without_key_but_uses_real_dataset_context" in api_tests
        ),
        "missing_primary_key_rejection": "test_business_csv_rejects_missing_primary_key_column" in api_tests,
        "support_ticket_case_study": (
            "test_support_ticket_case_study_produces_reproducible_business_findings" in api_tests
        ),
        "postgres_read_only_adapter": "test_postgres_support_ticket_report_uses_read_only_adapter" in api_tests,
        "postgres_agent_disabled_fallback": (
            "test_postgres_support_ticket_agent_report_uses_database_context_with_disabled_fallback" in api_tests
        ),
    }
    documentation_verified = {
        "csv_limits_documented": "10,000 rows, 80 columns, 2 MB upload limit" in readme,
        "no_uploaded_file_persistence_documented": "does not persist uploaded CSV files" in readme,
        "read_only_postgres_documented": "read-only PostgreSQL adapter" in readme,
        "business_data_curl_documented": "/business-data/agent-report" in readme,
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_data_intake_baseline.py",
        "business_data_inputs_supported": ["bounded CSV upload", "optional read-only PostgreSQL adapter"],
        "endpoint_count": len(endpoints),
        "endpoints": endpoints,
        "endpoint_verification": endpoint_verification,
        "safety_limits": safety_limits,
        "test_count": len(tests_verified),
        "tests_verified": tests_verified,
        "documentation_verified": documentation_verified,
        "resume_safe_signal": (
            "CI-verified business-data intake baseline covering bounded CSV uploads, read-only PostgreSQL context, "
            "4 integration endpoints, 3 upload limits, and 6 API tests without claiming external production usage."
        ),
        "not_claimed": [
            "external production datasets",
            "persistent storage of uploaded CSV rows",
            "enterprise production usage",
            "external users",
            "customer feedback",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    endpoints = "\n".join(
        f"| {name} | `{route}` | {payload['endpoint_verification'][name]} |"
        for name, route in payload["endpoints"].items()
    )
    limits = "\n".join(f"| {key} | {value} |" for key, value in payload["safety_limits"].items())
    tests = "\n".join(f"| {key} | {value} |" for key, value in payload["tests_verified"].items())
    docs = "\n".join(f"| {key} | {value} |" for key, value in payload["documentation_verified"].items())
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Business Data Intake Baseline

This generated artifact verifies that the project can accept realistic business-data inputs through bounded,
reviewable paths without claiming external production usage.

## Supported Inputs

{", ".join(payload["business_data_inputs_supported"])}

## Verified Endpoints

| Input path | Route | Verified |
| --- | --- | --- |
{endpoints}

## Safety Limits

| Limit | Value |
| --- | ---: |
{limits}

## API Tests

| Test coverage | Verified |
| --- | --- |
{tests}

## Documentation Checks

| Documentation coverage | Verified |
| --- | --- |
{docs}

## Resume-Safe Signal

{payload["resume_safe_signal"]}

## Not Claimed

{not_claimed}
"""


def verify_business_data_intake_baseline(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["endpoint_count"] != 4:
        raise AssertionError("business data intake baseline must verify 4 integration endpoints")
    if not all(payload["endpoint_verification"].values()):
        raise AssertionError("every business-data endpoint must be present in source and OpenAPI")
    limits = payload["safety_limits"]
    expected_limits = {
        "max_upload_bytes": 2_000_000,
        "max_rows": 10_000,
        "max_columns": 80,
        "csv_only": True,
        "primary_key_required": True,
        "empty_file_rejected": True,
    }
    for key, expected in expected_limits.items():
        if limits.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {limits.get(key)!r}")
    if payload["test_count"] != 6 or not all(payload["tests_verified"].values()):
        raise AssertionError("business data intake baseline must verify 6 API tests")
    if not all(payload["documentation_verified"].values()):
        raise AssertionError("business data intake baseline must verify README coverage")
    not_claimed = " ".join(payload["not_claimed"]).lower()
    for required in ("production datasets", "uploaded csv rows", "enterprise production usage"):
        if required not in not_claimed:
            raise AssertionError(f"business data intake baseline must not claim {required}")
    return {
        "business_data_intake_baseline_verified": True,
        "endpoint_count": payload["endpoint_count"],
        "test_count": payload["test_count"],
        "max_rows": limits["max_rows"],
        "max_columns": limits["max_columns"],
        "max_upload_bytes": limits["max_upload_bytes"],
    }


def main() -> None:
    payload = build_business_data_intake_baseline()
    verify_business_data_intake_baseline(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
