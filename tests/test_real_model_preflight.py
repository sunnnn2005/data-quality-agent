from pathlib import Path

from scripts.build_real_model_preflight import (
    build_real_model_preflight_payload,
    render_markdown,
    verify_real_model_preflight,
)


def test_real_model_preflight_blocks_without_key_or_running_api():
    payload = build_real_model_preflight_payload(
        env={},
        api_health={"name": "local_api_health", "ready": False, "status": "unavailable"},
    )
    verification = verify_real_model_preflight(payload)
    markdown = render_markdown(payload)

    assert verification["real_model_preflight_verified"] is True
    assert payload["real_model_execution_status"] == "not_ready"
    assert payload["real_model_run_executed_by_preflight"] is False
    assert payload["total_check_count"] == 5
    assert payload["blocked_check_count"] == 2
    assert "openai_api_key_configured" in payload["blocked_checks"]
    assert "local_api_health" in payload["blocked_checks"]
    assert "business_agent_route_documented" not in payload["blocked_checks"]
    assert "Start the API with OPENAI_API_KEY" in payload["next_real_model_capture_command"]
    assert "Real Model Preflight" in markdown
    assert "never executes a paid model call" in markdown


def test_real_model_preflight_ready_when_all_gates_pass(tmp_path: Path):
    sample = tmp_path / "sample.csv"
    sample.write_text("id,status,amount\n1,open,10\n")
    payload = build_real_model_preflight_payload(
        env={"OPENAI_API_KEY": "present-but-not-printed"},
        api_health={"name": "local_api_health", "ready": True, "status": "ok"},
        sample_csv_path=sample,
    )
    verification = verify_real_model_preflight(payload)

    assert verification["real_model_preflight_verified"] is True
    assert payload["real_model_execution_status"] == "ready_to_execute"
    assert payload["ready_check_count"] == 5
    assert payload["blocked_check_count"] == 0
    assert "capture_real_model_run.py --csv-path sample.csv" in payload["next_real_model_capture_command"]
    assert "present-but-not-printed" not in render_markdown(payload)
