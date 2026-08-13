from scripts.build_performance_baseline import (
    build_performance_baseline_payload,
    render_markdown,
    verify_performance_baseline,
)


def test_performance_baseline_verifies_local_latency_without_sla_claims():
    payload = build_performance_baseline_payload()
    verification = verify_performance_baseline(payload)
    markdown = render_markdown(payload)

    assert verification["performance_baseline_verified"] is True
    assert verification["benchmark_count"] == 2
    assert verification["measured_endpoint_calls"] == 24
    assert payload["status"] == "PASS"
    assert payload["passed_count"] == 2
    assert {check["path"] for check in payload["checks"]} == {
        "/datasets/orders_daily/quality-report",
        "/datasets/orders_daily/profile",
    }
    assert "No production latency SLA is claimed." in payload["not_claimed"]
    assert "Performance Baseline" in markdown
    assert "No hosted traffic benchmark is claimed." in markdown
