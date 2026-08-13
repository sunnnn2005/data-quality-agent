from collections import OrderedDict
from datetime import datetime, timezone
from uuid import uuid4

from app.models import AgentRunReport, QualityReport, StoredRunTrace


MAX_TRACES = 100


class RunTraceStore:
    def __init__(self, max_traces: int = MAX_TRACES) -> None:
        self.max_traces = max_traces
        self._traces: OrderedDict[str, StoredRunTrace] = OrderedDict()

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
                    "likely_causes": report.likely_causes[:3],
                    "recommended_next_steps": report.recommended_next_steps[:3],
                },
                evaluation={
                    "evidence_support_rate": self._evidence_support_rate(report),
                    "final_report_attached": True,
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
        return self._traces.get(trace_id)

    def _save(self, trace: StoredRunTrace) -> None:
        self._traces[trace.trace_id] = trace
        self._traces.move_to_end(trace.trace_id)
        while len(self._traces) > self.max_traces:
            self._traces.popitem(last=False)

    def _new_trace_id(self) -> str:
        return f"run_{uuid4().hex[:16]}"

    def _evidence_support_rate(self, report: QualityReport) -> float:
        if not report.findings:
            return 1.0
        supported = sum(1 for finding in report.findings if finding.evidence)
        return round(supported / len(report.findings), 3)
