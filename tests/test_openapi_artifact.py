from scripts.build_openapi_artifact import (
    REQUIRED_ENDPOINTS,
    build_openapi_payload,
    render_markdown,
    verify_openapi_payload,
)


def test_openapi_artifact_covers_core_integration_endpoints():
    payload = build_openapi_payload()
    verification = verify_openapi_payload(payload)
    markdown = render_markdown(payload)

    assert verification["openapi_contract_verified"] is True
    assert verification["required_endpoint_count"] == 6
    assert verification["path_count"] >= 12
    for _, (_, path) in REQUIRED_ENDPOINTS.items():
        assert path in payload["paths"]
    assert "API Contract" in markdown
    assert "POST /business-data/agent-report" in markdown
