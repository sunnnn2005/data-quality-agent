from scripts.build_api_smoke_report import build_api_smoke_report_payload, render_markdown, verify_api_smoke_report


def test_api_smoke_report_verifies_core_routes_without_production_claims():
    payload = build_api_smoke_report_payload()
    verification = verify_api_smoke_report(payload)
    markdown = render_markdown(payload)

    assert verification["api_smoke_report_verified"] is True
    assert payload["deterministic_mode"]["llm_agent_forced_disabled"] is True
    assert payload["check_count"] == 6
    assert payload["passed_count"] == 6
    assert payload["status"] == "PASS"
    assert any(check["path"] == "/datasets/orders_daily/agent-report" for check in payload["checks"])
    assert "API Smoke Report" in markdown
    assert "No production uptime SLA is claimed." in markdown
