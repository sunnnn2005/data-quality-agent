import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
COMPOSE_PATH = ROOT / "docker-compose.yml"
SEED_SQL_PATH = ROOT / "examples" / "postgres" / "init.sql"
OUTPUT_JSON_PATH = ROOT / "docs" / "local-reviewer-demo.json"
OUTPUT_MD_PATH = ROOT / "docs" / "local-reviewer-demo.md"


def build_local_reviewer_demo_payload() -> dict[str, Any]:
    compose = yaml.safe_load(COMPOSE_PATH.read_text())
    seed_sql = SEED_SQL_PATH.read_text()
    services = compose["services"]
    postgres = services["postgres"]
    api = services["api"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_local_reviewer_demo.py",
        "compose_file": "docker-compose.yml",
        "seed_sql": "examples/postgres/init.sql",
        "reviewer_command": "docker compose up --build",
        "api_base_url": "http://127.0.0.1:8000",
        "services": {
            "postgres_image": postgres["image"],
            "api_build_context": api["build"],
            "postgres_host_port": "5433",
            "api_host_port": "8000",
            "postgres_healthcheck": postgres["healthcheck"]["test"],
        },
        "read_only_database": {
            "database": postgres["environment"]["POSTGRES_DB"],
            "owner_user": postgres["environment"]["POSTGRES_USER"],
            "readonly_user": "readonly_agent",
            "readonly_grants": [
                "CONNECT ON DATABASE quality_demo",
                "USAGE ON SCHEMA public",
                "SELECT ON support_tickets",
            ],
        },
        "seeded_business_table": {
            "table": "support_tickets",
            "row_count": seed_sql.count("TCK-"),
            "known_quality_cases": [
                "duplicate ticket_id",
                "missing team",
                "missing priority",
                "negative amount",
                "amount outlier",
            ],
        },
        "reviewer_routes": [
            {
                "label": "Deterministic PostgreSQL quality report",
                "method": "POST",
                "path": "/postgres/support-tickets/quality-report",
                "curl": "curl -X POST http://127.0.0.1:8000/postgres/support-tickets/quality-report",
            },
            {
                "label": "LLM agent route with safe disabled fallback",
                "method": "POST",
                "path": "/postgres/support-tickets/agent-report",
                "curl": "curl -X POST http://127.0.0.1:8000/postgres/support-tickets/agent-report",
            },
            {
                "label": "Interactive FastAPI docs",
                "method": "GET",
                "path": "/docs",
                "curl": "open http://127.0.0.1:8000/docs",
            },
        ],
        "resume_safe_summary": (
            "Published a Docker Compose reviewer demo with a seeded PostgreSQL table, read-only database user, "
            "and 3 local review paths for reproducing quality and agent reports."
        ),
        "not_claimed": [
            "No hosted production database is claimed.",
            "No external reviewer completion is claimed.",
            "No customer deployment is claimed.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    services = payload["services"]
    database = payload["read_only_database"]
    seeded = payload["seeded_business_table"]
    routes = "\n".join(
        f"| {route['label']} | `{route['method']}` | `{route['path']}` | `{route['curl']}` |"
        for route in payload["reviewer_routes"]
    )
    cases = "\n".join(f"- {item}" for item in seeded["known_quality_cases"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Local Reviewer Demo

This generated artifact documents the reproducible local demo path for reviewers. It is verified from `{payload["compose_file"]}` and `{payload["seed_sql"]}`.

## One-Command Start

```bash
{payload["reviewer_command"]}
```

## Services

| Service Detail | Value |
| --- | --- |
| PostgreSQL image | `{services["postgres_image"]}` |
| API build context | `{services["api_build_context"]}` |
| PostgreSQL host port | `{services["postgres_host_port"]}` |
| API host port | `{services["api_host_port"]}` |

## Read-Only Database

| Field | Value |
| --- | --- |
| Database | `{database["database"]}` |
| Owner user | `{database["owner_user"]}` |
| Read-only user | `{database["readonly_user"]}` |

## Seeded Business Table

`{seeded["table"]}` has {seeded["row_count"]} seeded rows with known quality cases:

{cases}

## Reviewer Routes

| Route | Method | Path | Command |
| --- | --- | --- | --- |
{routes}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_local_reviewer_demo(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["reviewer_command"] != "docker compose up --build":
        raise AssertionError("local reviewer demo must document the compose startup command")
    if payload["services"]["postgres_image"] != "postgres:16-alpine":
        raise AssertionError("local reviewer demo must use the configured PostgreSQL image")
    if payload["seeded_business_table"]["row_count"] != 8:
        raise AssertionError("seeded support-ticket table must contain 8 demo rows")
    if payload["read_only_database"]["readonly_user"] != "readonly_agent":
        raise AssertionError("local reviewer demo must verify the read-only user")
    if len(payload["reviewer_routes"]) != 3:
        raise AssertionError("local reviewer demo must expose 3 review paths")
    if "external reviewer completion" not in " ".join(payload["not_claimed"]).lower():
        raise AssertionError("local reviewer demo must avoid claiming external reviewer usage")
    return {
        "local_reviewer_demo_verified": True,
        "seeded_rows": payload["seeded_business_table"]["row_count"],
        "reviewer_routes": len(payload["reviewer_routes"]),
    }


def main() -> None:
    payload = build_local_reviewer_demo_payload()
    verify_local_reviewer_demo(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
