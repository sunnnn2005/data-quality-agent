from collections import OrderedDict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
from uuid import uuid4

from app.models import AgentRunReport, DatasetMemorySummary, QualityReport, StoredRunTrace


MAX_TRACES = 100


class RunTraceStore:
    def __init__(self, max_traces: int = MAX_TRACES, db_path: str | Path | None = None) -> None:
        self.max_traces = max_traces
        self.db_path = Path(db_path) if db_path else self._configured_db_path()
        self._traces: OrderedDict[str, StoredRunTrace] = OrderedDict()
        if self.db_path:
            self._init_db()

    def save_quality_report(self, report: QualityReport) -> QualityReport:
        trace_id = report.trace_id or self._new_trace_id()
        traced_report = report.model_copy(update={"trace_id": trace_id})
        self._save(
            StoredRunTrace(
                trace_id=trace_id,
                dataset_id=report.dataset.id,
                dataset_name=report.dataset.name,
                owner=report.dataset.owner,
                generated_at=report.generated_at,
                status=report.status,
                report_type="quality_report",
                summary={
                    "quality_score": report.quality_score,
                    "row_count": report.row_count,
                    "finding_count": len(report.findings),
                    "finding_checks": sorted({finding.check_name for finding in report.findings}),
                    "business_rule_count": len(report.business_rule_references),
                    "business_rule_ids": [rule.rule_id for rule in report.business_rule_references],
                    "likely_causes": report.likely_causes[:3],
                    "root_cause_hypotheses": [
                        {
                            "title": hypothesis.title,
                            "confidence": hypothesis.confidence,
                            "supporting_checks": hypothesis.supporting_checks,
                        }
                        for hypothesis in report.root_cause_hypotheses[:3]
                    ],
                    "recommended_next_steps": report.recommended_next_steps[:3],
                    "verification_passed": report.verification.passed if report.verification else None,
                    "verification_issue_count": report.verification.issue_count if report.verification else None,
                },
                evaluation={
                    "evidence_support_rate": (
                        report.verification.evidence_support_rate if report.verification else self._evidence_support_rate(report)
                    ),
                    "final_report_attached": True,
                    "verification_passed": report.verification.passed if report.verification else None,
                },
                fallback_status="llm_assessment_disabled" if not report.llm_assessment.enabled else None,
                error=report.llm_assessment.error,
            )
        )
        return traced_report

    def save_agent_report(self, report: AgentRunReport) -> AgentRunReport:
        trace_id = report.trace_id or self._new_trace_id()
        traced_report = report.model_copy(update={"trace_id": trace_id})
        summary = {
            "final_answer_preview": report.final_answer[:240],
            "tool_call_count": len(report.tool_calls),
            "quality_report_attached": report.quality_report is not None,
        }
        if report.quality_report is not None:
            summary.update(
                {
                    "quality_score": report.quality_report.quality_score,
                    "row_count": report.quality_report.row_count,
                    "finding_count": len(report.quality_report.findings),
                    "finding_checks": sorted({finding.check_name for finding in report.quality_report.findings}),
                    "business_rule_count": len(report.quality_report.business_rule_references),
                    "business_rule_ids": [rule.rule_id for rule in report.quality_report.business_rule_references],
                    "root_cause_hypotheses": [
                        {
                            "title": hypothesis.title,
                            "confidence": hypothesis.confidence,
                            "supporting_checks": hypothesis.supporting_checks,
                        }
                        for hypothesis in report.quality_report.root_cause_hypotheses[:3]
                    ],
                    "verification_passed": (
                        report.quality_report.verification.passed if report.quality_report.verification else None
                    ),
                    "verification_issue_count": (
                        report.quality_report.verification.issue_count if report.quality_report.verification else None
                    ),
                }
            )
        self._save(
            StoredRunTrace(
                trace_id=trace_id,
                dataset_id=report.dataset.id,
                dataset_name=report.dataset.name,
                owner=report.dataset.owner,
                generated_at=report.generated_at,
                status=report.status,
                report_type="agent_report",
                summary=summary,
                tool_calls=report.tool_calls,
                evaluation=report.evaluation,
                fallback_status="agent_disabled" if report.status == "DISABLED" else None,
                error=report.error,
            )
        )
        return traced_report

    def get(self, trace_id: str) -> StoredRunTrace | None:
        trace = self._traces.get(trace_id)
        if trace is not None:
            return trace
        if self.db_path is None:
            return None
        return self._get_persisted(trace_id)

    def list_by_dataset(self, dataset_id: str, limit: int = 5) -> DatasetMemorySummary:
        bounded_limit = max(1, min(limit, 20))
        traces = [
            trace
            for trace in sorted(self._traces.values(), key=lambda item: item.generated_at, reverse=True)
            if trace.dataset_id == dataset_id
        ][:bounded_limit]
        if self.db_path:
            persisted = self._list_persisted_by_dataset(dataset_id, bounded_limit)
            seen = {trace.trace_id for trace in traces}
            traces.extend(trace for trace in persisted if trace.trace_id not in seen)
            traces = sorted(traces, key=lambda item: item.generated_at, reverse=True)[:bounded_limit]
        return self._build_memory_summary(dataset_id, traces)

    def _save(self, trace: StoredRunTrace) -> None:
        self._traces[trace.trace_id] = trace
        self._traces.move_to_end(trace.trace_id)
        while len(self._traces) > self.max_traces:
            self._traces.popitem(last=False)
        if self.db_path:
            self._save_persisted(trace)

    def _new_trace_id(self) -> str:
        return f"run_{uuid4().hex[:16]}"

    def _evidence_support_rate(self, report: QualityReport) -> float:
        if not report.findings:
            return 1.0
        supported = sum(1 for finding in report.findings if finding.evidence)
        return round(supported / len(report.findings), 3)

    def _configured_db_path(self) -> Path | None:
        value = os.getenv("TRACE_DB_PATH")
        if not value:
            return None
        return Path(value)

    def _connect(self) -> sqlite3.Connection:
        if self.db_path is None:
            raise RuntimeError("TRACE_DB_PATH is not configured")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS run_traces (
                    trace_id TEXT PRIMARY KEY,
                    dataset_id TEXT NOT NULL,
                    dataset_name TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    generated_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    report_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_run_traces_dataset ON run_traces(dataset_id)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_run_traces_generated_at ON run_traces(generated_at)")

    def _save_persisted(self, trace: StoredRunTrace) -> None:
        payload = trace.model_dump_json()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO run_traces (
                    trace_id,
                    dataset_id,
                    dataset_name,
                    owner,
                    generated_at,
                    status,
                    report_type,
                    payload_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(trace_id) DO UPDATE SET
                    dataset_id = excluded.dataset_id,
                    dataset_name = excluded.dataset_name,
                    owner = excluded.owner,
                    generated_at = excluded.generated_at,
                    status = excluded.status,
                    report_type = excluded.report_type,
                    payload_json = excluded.payload_json
                """,
                (
                    trace.trace_id,
                    trace.dataset_id,
                    trace.dataset_name,
                    trace.owner,
                    trace.generated_at.isoformat(),
                    trace.status,
                    trace.report_type,
                    payload,
                ),
            )

    def _get_persisted(self, trace_id: str) -> StoredRunTrace | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload_json FROM run_traces WHERE trace_id = ?",
                (trace_id,),
            ).fetchone()
        if row is None:
            return None
        return StoredRunTrace.model_validate(json.loads(row[0]))

    def _list_persisted_by_dataset(self, dataset_id: str, limit: int) -> list[StoredRunTrace]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload_json
                FROM run_traces
                WHERE dataset_id = ?
                ORDER BY generated_at DESC
                LIMIT ?
                """,
                (dataset_id, limit),
            ).fetchall()
        return [StoredRunTrace.model_validate(json.loads(row[0])) for row in rows]

    def _build_memory_summary(self, dataset_id: str, traces: list[StoredRunTrace]) -> DatasetMemorySummary:
        check_counts: dict[str, int] = {}
        cause_counts: dict[str, int] = {}
        for trace in traces:
            for check in trace.summary.get("finding_checks", []):
                check_counts[str(check)] = check_counts.get(str(check), 0) + 1
            for hypothesis in trace.summary.get("root_cause_hypotheses", []):
                title = str(hypothesis.get("title", "")).strip()
                if title:
                    cause_counts[title] = cause_counts.get(title, 0) + 1
        return DatasetMemorySummary(
            dataset_id=dataset_id,
            trace_count=len(traces),
            latest_generated_at=traces[0].generated_at if traces else None,
            recurring_checks=self._rank_repeated_items(check_counts),
            recurring_root_causes=self._rank_repeated_items(cause_counts),
            recent_traces=traces,
        )

    def _rank_repeated_items(self, counts: dict[str, int]) -> list[str]:
        return [
            item
            for item, count in sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
            if count > 1
        ][:5]
