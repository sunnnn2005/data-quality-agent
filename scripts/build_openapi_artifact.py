import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.main import app


OUTPUT_JSON_PATH = ROOT / "docs" / "openapi.json"
OUTPUT_MD_PATH = ROOT / "docs" / "api-contract.md"

REQUIRED_ENDPOINTS = {
    "POST /business-data/quality-report": ("post", "/business-data/quality-report"),
    "POST /business-data/agent-report": ("post", "/business-data/agent-report"),
    "POST /postgres/support-tickets/agent-report": ("post", "/postgres/support-tickets/agent-report"),
    "GET /datasets/{dataset_id}/memory": ("get", "/datasets/{dataset_id}/memory"),
    "GET /runs/{trace_id}": ("get", "/runs/{trace_id}"),
    "POST /datasets/{dataset_id}/incident-report.md": ("post", "/datasets/{dataset_id}/incident-report.md"),
}


def build_openapi_payload() -> dict[str, Any]:
    return app.openapi()


def render_markdown(payload: dict[str, Any]) -> str:
    endpoint_rows = "\n".join(
        f"| `{label}` | `{payload['paths'][path][method]['operationId']}` |"
        for label, (method, path) in REQUIRED_ENDPOINTS.items()
    )
    return f"""# API Contract

This generated artifact is built from the FastAPI OpenAPI schema. It verifies that the public API surface includes the business-data, agent, trace, memory, and incident-report endpoints used by the demo and resume evidence.

| Contract metric | Value |
| --- | ---: |
| OpenAPI version | `{payload["openapi"]}` |
| API title | `{payload["info"]["title"]}` |
| Paths | {len(payload["paths"])} |
| Required integration endpoints | {len(REQUIRED_ENDPOINTS)} |

## Required Endpoints

| Endpoint | Operation ID |
| --- | --- |
{endpoint_rows}
"""


def verify_openapi_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("info", {}).get("title") != "Data Quality Agent":
        raise AssertionError("OpenAPI title must match the FastAPI app title")
    paths = payload.get("paths", {})
    for label, (method, path) in REQUIRED_ENDPOINTS.items():
        if path not in paths:
            raise AssertionError(f"missing required API path: {path}")
        if method not in paths[path]:
            raise AssertionError(f"missing required API method for {label}")
    if len(paths) < 12:
        raise AssertionError("OpenAPI artifact should expose the documented API surface")
    return {
        "openapi_contract_verified": True,
        "path_count": len(paths),
        "required_endpoint_count": len(REQUIRED_ENDPOINTS),
    }


def main() -> None:
    payload = build_openapi_payload()
    verify_openapi_payload(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(verify_openapi_payload(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
