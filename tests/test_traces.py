from app.agent import DataQualityAgent
from app.data import DATASETS, load_dataset
from app.traces import RunTraceStore


def test_run_trace_store_can_persist_sanitized_trace_across_instances(tmp_path):
    db_path = tmp_path / "agent-runs.sqlite"
    dataset = DATASETS["orders_daily"]
    report = DataQualityAgent().analyze(dataset, load_dataset(dataset.id))

    first_store = RunTraceStore(max_traces=1, db_path=db_path)
    traced_report = first_store.save_quality_report(report)

    second_store = RunTraceStore(max_traces=1, db_path=db_path)
    restored = second_store.get(traced_report.trace_id)

    assert restored is not None
    assert restored.trace_id == traced_report.trace_id
    assert restored.dataset_id == dataset.id
    assert restored.report_type == "quality_report"
    assert restored.summary["finding_count"] >= 1
    assert restored.evaluation["final_report_attached"] is True
    assert "agent_trace" not in restored.model_dump_json()


def test_run_trace_store_retrieves_dataset_memory_from_persisted_traces(tmp_path):
    db_path = tmp_path / "agent-runs.sqlite"
    dataset = DATASETS["orders_daily"]
    report = DataQualityAgent().analyze(dataset, load_dataset(dataset.id))

    first_store = RunTraceStore(db_path=db_path)
    first_store.save_quality_report(report)
    first_store.save_quality_report(report)

    second_store = RunTraceStore(db_path=db_path)
    memory = second_store.list_by_dataset(dataset.id, limit=5)

    assert memory.dataset_id == dataset.id
    assert memory.trace_count == 2
    assert memory.latest_generated_at is not None
    assert "duplicate_primary_key" in memory.recurring_checks
    assert memory.recurring_root_causes
    assert all(trace.dataset_id == dataset.id for trace in memory.recent_traces)
    assert "agent_trace" not in memory.model_dump_json()
