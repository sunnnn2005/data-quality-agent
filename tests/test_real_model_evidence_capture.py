from scripts.build_real_model_evidence_capture import (
    build_real_model_evidence_capture_payload,
    render_markdown,
    verify_real_model_evidence_capture,
)


def test_real_model_evidence_capture_preserves_zero_run_baseline():
    payload = build_real_model_evidence_capture_payload()
    verification = verify_real_model_evidence_capture(payload)
    markdown = render_markdown(payload)

    assert verification["real_model_evidence_capture_verified"] is True
    assert payload["evaluated_run_count"] == 0
    assert payload["accepted_real_model_run_count"] == 0
    assert payload["rejected_real_model_run_count"] == 0
    assert payload["current_real_model_runs"] == 0
    assert payload["runbook_evidence_field_count"] == 15
    assert payload["capture_required_field_count"] == 17
    assert payload["claimable_metric_count"] == 4
    assert payload["blocked_outcome_claim_count"] == 4
    assert payload["claimable_metrics"]["real_model_runs"]["claimable"] is False
    assert "trace_id" in payload["capture_required_fields"]
    assert "raw_prompt_logged" in payload["capture_required_fields"]
    assert "real OpenAI model run completed" in payload["not_claimed"]
    assert "Real Model Evidence Capture" in markdown
    assert "Accepted real model runs | 0" in markdown


def test_real_model_evidence_capture_accepts_redacted_tool_calling_run():
    payload = build_real_model_evidence_capture_payload(
        real_runs=[
            {
                "trace_id": "run_001",
                "provider": "openai-compatible",
                "model": "gpt-4o-mini",
                "prompt_version": "tool-agent-v3",
                "dataset_id": "support_tickets",
                "model_call_count": 2,
                "tool_call_count": 4,
                "distinct_tool_count": 4,
                "used_strategy_tool": True,
                "used_required_report_tool": True,
                "final_report_attached": True,
                "total_tokens": 1234,
                "estimated_cost_usd": 0.0012,
                "latency_ms": 1200,
                "verification_passed": True,
                "redaction_status": "redacted",
                "raw_prompt_logged": False,
            }
        ]
    )
    verification = verify_real_model_evidence_capture(payload, expected_current_real_model_runs=1)

    assert verification["real_model_evidence_capture_verified"] is True
    assert payload["evaluated_run_count"] == 1
    assert payload["accepted_real_model_run_count"] == 1
    assert payload["rejected_real_model_run_count"] == 0
    assert payload["blocked_outcome_claim_count"] == 0
    assert payload["claimable_metrics"]["real_model_runs"]["claimable"] is True
    assert payload["claimable_metrics"]["real_model_tool_calling_runs"]["claimable"] is True
    assert payload["claimable_metrics"]["real_model_verified_reports"]["claimable"] is True
    assert payload["claimable_metrics"]["real_model_cost_tracked_runs"]["claimable"] is True
    assert payload["accepted_runs"][0]["trace_id"] == "run_001"
    assert payload["accepted_runs"][0]["tool_call_count"] == 4
