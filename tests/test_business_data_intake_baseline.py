from scripts.build_business_data_intake_baseline import (
    build_business_data_intake_baseline,
    render_markdown,
    verify_business_data_intake_baseline,
)


def test_business_data_intake_baseline_verifies_realistic_input_paths_without_usage_claims():
    payload = build_business_data_intake_baseline()
    verification = verify_business_data_intake_baseline(payload)
    markdown = render_markdown(payload)

    assert verification["business_data_intake_baseline_verified"] is True
    assert payload["endpoint_count"] == 4
    assert payload["test_count"] == 6
    assert payload["safety_limits"]["max_rows"] == 10_000
    assert payload["safety_limits"]["max_columns"] == 80
    assert payload["safety_limits"]["max_upload_bytes"] == 2_000_000
    assert all(payload["endpoint_verification"].values())
    assert all(payload["tests_verified"].values())
    assert "bounded CSV uploads" in payload["resume_safe_signal"]
    assert "read-only PostgreSQL context" in payload["resume_safe_signal"]
    assert "enterprise production usage" in payload["not_claimed"]
    assert "Business Data Intake Baseline" in markdown
