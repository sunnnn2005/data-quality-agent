from app.agent import DataQualityAgent
from app.data import DATASETS, load_dataset


def analyze(dataset_id: str):
    return DataQualityAgent().analyze(DATASETS[dataset_id], load_dataset(dataset_id))


def test_orders_daily_detects_duplicates_missing_values_and_outliers():
    report = analyze("orders_daily")
    checks = {finding.check_name for finding in report.findings}

    assert report.status == "FAIL"
    assert "duplicate_primary_key" in checks
    assert "missing_values" in checks
    assert "numeric_outliers" in checks
    assert report.quality_score < 80
    assert any("idempotent" in step for step in report.recommended_next_steps)


def test_payments_events_detects_freshness_and_negative_amount():
    report = analyze("payments_events")
    checks = {finding.check_name for finding in report.findings}

    assert "freshness_sla" in checks
    assert "negative_amount" in checks
    assert any("scheduler" in cause.lower() or "scheduled" in cause.lower() for cause in report.likely_causes)


def test_customer_profiles_detects_schema_drift_and_missing_fields():
    report = analyze("customer_profiles")
    checks = {finding.check_name for finding in report.findings}

    assert "schema_drift" in checks
    assert "missing_values" in checks
    assert any("schema migration" in cause.lower() for cause in report.likely_causes)


def test_agent_trace_records_tool_calls():
    report = analyze("orders_daily")

    assert any("dataset_profiler" in step for step in report.agent_trace)
    assert any("quality_check_runner" in step for step in report.agent_trace)
