from scripts.build_public_availability_snapshot import (
    build_public_availability_snapshot,
    render_markdown,
    verify_public_availability_snapshot,
)


def test_public_availability_snapshot_tracks_reachability_without_uptime_claims():
    payload = build_public_availability_snapshot(
        endpoint_results=[
            {
                "id": "public_demo",
                "url": "https://example.test/",
                "expected_text": "Data Quality Agent",
                "surface": "GitHub Pages",
                "status_code": 200,
                "latency_ms": 120,
                "available": True,
                "error": None,
            },
            {
                "id": "reviewer_landing_page",
                "url": "https://example.test/review.html",
                "expected_text": "8-minute public review",
                "surface": "GitHub Pages",
                "status_code": 200,
                "latency_ms": 180,
                "available": True,
                "error": None,
            },
            {
                "id": "openapi_contract",
                "url": "https://example.test/openapi.json",
                "expected_text": "/business-data/agent-report",
                "surface": "GitHub raw artifact",
                "status_code": 200,
                "latency_ms": 90,
                "available": True,
                "error": None,
            },
            {
                "id": "public_metrics",
                "url": "https://example.test/public-metrics-summary.json",
                "expected_text": "resume_safe_signals",
                "surface": "GitHub raw artifact",
                "status_code": 200,
                "latency_ms": 110,
                "available": True,
                "error": None,
            },
        ],
        workflow_runs=[
            {"id": "ci", "workflow": "test.yml", "status": "completed", "conclusion": "success", "verified": True},
            {
                "id": "public_evidence_health",
                "workflow": "public-evidence-health.yml",
                "status": "completed",
                "conclusion": "success",
                "verified": True,
            },
            {
                "id": "container_publish",
                "workflow": "publish-image.yml",
                "status": "completed",
                "conclusion": "success",
                "verified": True,
            },
        ],
    )
    verification = verify_public_availability_snapshot(payload)
    markdown = render_markdown(payload)

    assert verification["public_availability_snapshot_verified"] is True
    assert payload["available_endpoint_count"] == 4
    assert payload["successful_workflow_count"] == 3
    assert payload["max_latency_ms"] == 180
    assert "production uptime SLA" in payload["resume_policy"]
    assert "active users" in payload["resume_policy"]
    assert "Public Availability Snapshot" in markdown
    assert "Available public endpoints | 4 / 4" in markdown


def test_public_availability_snapshot_allows_partial_network_failure():
    payload = build_public_availability_snapshot(
        endpoint_results=[
            {
                "id": "public_demo",
                "url": "https://example.test/",
                "expected_text": "Data Quality Agent",
                "surface": "GitHub Pages",
                "status_code": None,
                "latency_ms": 15000,
                "available": False,
                "error": "TimeoutError",
            },
            {
                "id": "reviewer_landing_page",
                "url": "https://example.test/review.html",
                "expected_text": "8-minute public review",
                "surface": "GitHub Pages",
                "status_code": 200,
                "latency_ms": 100,
                "available": True,
                "error": None,
            },
            {
                "id": "openapi_contract",
                "url": "https://example.test/openapi.json",
                "expected_text": "/business-data/agent-report",
                "surface": "GitHub raw artifact",
                "status_code": 200,
                "latency_ms": 100,
                "available": True,
                "error": None,
            },
            {
                "id": "public_metrics",
                "url": "https://example.test/public-metrics-summary.json",
                "expected_text": "resume_safe_signals",
                "surface": "GitHub raw artifact",
                "status_code": 200,
                "latency_ms": 100,
                "available": True,
                "error": None,
            },
        ],
        workflow_runs=[
            {"id": "ci", "workflow": "test.yml", "status": "completed", "conclusion": "success", "verified": True},
            {
                "id": "public_evidence_health",
                "workflow": "public-evidence-health.yml",
                "status": "completed",
                "conclusion": "success",
                "verified": True,
            },
            {
                "id": "container_publish",
                "workflow": "publish-image.yml",
                "status": "completed",
                "conclusion": "failure",
                "verified": False,
            },
        ],
    )
    verification = verify_public_availability_snapshot(payload)

    assert verification["available_endpoint_count"] == 3
    assert verification["successful_workflow_count"] == 2
    assert payload["not_claimed"] == [
        "production uptime SLA",
        "active users",
        "customer adoption",
        "paid availability monitoring",
    ]
