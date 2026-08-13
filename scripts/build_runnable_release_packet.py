import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
LOCAL_REVIEWER_DEMO_PATH = ROOT / "docs" / "local-reviewer-demo.json"
OPENAPI_PATH = ROOT / "docs" / "openapi.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "runnable-release-packet.json"
OUTPUT_MD_PATH = ROOT / "docs" / "runnable-release-packet.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_runnable_release_packet() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    local_demo = load_json(LOCAL_REVIEWER_DEMO_PATH)
    openapi = load_json(OPENAPI_PATH)
    repo = adoption["repo"]
    image = adoption["container_image"]["image"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_runnable_release_packet.py",
        "repo": repo,
        "release": adoption["release"],
        "container_image": adoption["container_image"],
        "public_demo": adoption["public_demo"],
        "runnable_surfaces": [
            {
                "name": "public_demo",
                "type": "hosted_static_demo",
                "url": adoption["public_demo"],
                "verification": "public availability snapshot checks this URL for Data Quality Agent text",
            },
            {
                "name": "ghcr_container",
                "type": "container_image",
                "url": adoption["container_image"]["package_url"],
                "command": f"docker run --rm -p 8000:8000 {image}",
                "verification": "publish-image.yml builds and publishes the GHCR package from main",
            },
            {
                "name": "docker_compose_business_demo",
                "type": "local_postgres_plus_api",
                "url": f"{repo}/blob/main/docker-compose.yml",
                "command": local_demo["reviewer_command"],
                "verification": "local reviewer demo verifies a read-only PostgreSQL user and seeded support-ticket table",
            },
        ],
        "acceptance_checks": [
            {
                "label": "Health check",
                "command": "curl http://127.0.0.1:8000/health",
                "expected": '{"status":"ok","service":"data-quality-agent"}',
            },
            {
                "label": "Deterministic built-in report",
                "command": "curl -X POST http://127.0.0.1:8000/datasets/orders_daily/quality-report",
                "expected": "QualityReport JSON with evidence-backed findings and verification metadata",
            },
            {
                "label": "Read-only PostgreSQL report",
                "command": "curl -X POST http://127.0.0.1:8000/postgres/support-tickets/quality-report",
                "expected": "Report over 8 seeded support-ticket rows with duplicate, missing, negative, and outlier findings",
            },
            {
                "label": "LLM agent fallback route",
                "command": "curl -X POST http://127.0.0.1:8000/postgres/support-tickets/agent-report",
                "expected": "Structured DISABLED fallback when OPENAI_API_KEY is not configured",
            },
        ],
        "openapi_coverage": {
            "path_count": len(openapi["paths"]),
            "published_paths": sorted(openapi["paths"]),
            "required_paths": [
                "/health",
                "/datasets/{dataset_id}/quality-report",
                "/datasets/{dataset_id}/agent-report",
                "/business-data/agent-report",
                "/postgres/support-tickets/agent-report",
                "/runs/{trace_id}",
            ],
        },
        "resume_safe_summary": (
            "Published a runnable release packet covering a public demo, GHCR container command, Docker Compose "
            "PostgreSQL demo, 4 acceptance checks, and a CI-verified OpenAPI surface."
        ),
        "not_claimed": [
            "No package download count is claimed.",
            "No external installs are claimed.",
            "No production deployment is claimed.",
            "No customer usage is claimed.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    surfaces = "\n".join(
        f"| {item['name']} | {item['type']} | [{item['url']}]({item['url']}) | `{item.get('command', '-')}` |"
        for item in payload["runnable_surfaces"]
    )
    checks = "\n".join(
        f"| {item['label']} | `{item['command']}` | {item['expected']} |" for item in payload["acceptance_checks"]
    )
    paths = "\n".join(f"- `{path}`" for path in payload["openapi_coverage"]["required_paths"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Runnable Release Packet

This generated artifact gives reviewers the shortest path to verify that the project is shipped as a runnable system.

## Runnable Surfaces

| Surface | Type | URL | Command |
| --- | --- | --- | --- |
{surfaces}

## Acceptance Checks

| Check | Command | Expected |
| --- | --- | --- |
{checks}

## OpenAPI Coverage

Published path count: {payload["openapi_coverage"]["path_count"]}

Required runnable paths:

{paths}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_runnable_release_packet(payload: dict[str, Any]) -> dict[str, Any]:
    if len(payload["runnable_surfaces"]) != 3:
        raise AssertionError("runnable release packet must expose 3 runnable surfaces")
    if len(payload["acceptance_checks"]) != 4:
        raise AssertionError("runnable release packet must expose 4 acceptance checks")
    commands = " ".join(item.get("command", "") for item in payload["runnable_surfaces"])
    if "docker run" not in commands:
        raise AssertionError("runnable release packet must include a docker run command")
    if "docker compose up --build" not in commands:
        raise AssertionError("runnable release packet must include the compose command")
    openapi_paths = set(payload["openapi_coverage"]["published_paths"])
    for path in payload["openapi_coverage"]["required_paths"]:
        if path not in openapi_paths:
            raise AssertionError(f"missing required OpenAPI path {path}")
    for forbidden in ("download count", "external installs", "production deployment", "customer usage"):
        if forbidden not in " ".join(payload["not_claimed"]).lower():
            raise AssertionError(f"runnable packet must not claim {forbidden}")
    return {
        "runnable_release_packet_verified": True,
        "runnable_surface_count": len(payload["runnable_surfaces"]),
        "acceptance_check_count": len(payload["acceptance_checks"]),
        "openapi_required_path_count": len(payload["openapi_coverage"]["required_paths"]),
    }


def main() -> None:
    payload = build_runnable_release_packet()
    verify_runnable_release_packet(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
