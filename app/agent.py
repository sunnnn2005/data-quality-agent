from datetime import datetime, timezone

import pandas as pd

from app.checks import QualityCheckRunner
from app.business_rules import BusinessRuleRetriever
from app.llm import LLMDataQualityAdvisor
from app.models import DatasetSummary, QualityFinding, QualityReport, Severity
from app.profiler import DatasetProfiler
from app.verifier import ReportVerifier


class DataQualityAgent:
    def __init__(
        self,
        profiler: DatasetProfiler | None = None,
        check_runner: QualityCheckRunner | None = None,
        rule_retriever: BusinessRuleRetriever | None = None,
        llm_advisor: LLMDataQualityAdvisor | None = None,
        verifier: ReportVerifier | None = None,
    ) -> None:
        self.profiler = profiler or DatasetProfiler()
        self.check_runner = check_runner or QualityCheckRunner()
        self.rule_retriever = rule_retriever or BusinessRuleRetriever()
        self.llm_advisor = llm_advisor or LLMDataQualityAdvisor()
        self.verifier = verifier or ReportVerifier()

    def analyze(self, dataset: DatasetSummary, frame: pd.DataFrame) -> QualityReport:
        trace = [f"loaded dataset {dataset.id} owned by {dataset.owner}"]
        profile = self.profiler.profile(dataset, frame)
        trace.append(f"called {self.profiler.name}: {profile.row_count} rows, {profile.column_count} columns")

        findings = self.check_runner.run(dataset, frame)
        trace.append(f"called {self.check_runner.name}: {len(findings)} quality findings")
        business_rule_references = self.rule_retriever.retrieve(dataset, findings)
        trace.append(f"called {self.rule_retriever.name}: {len(business_rule_references)} business rule references")

        score = self._score(findings)
        llm_assessment = self.llm_advisor.assess(profile, findings)
        if llm_assessment.enabled:
            trace.append(f"called {self.llm_advisor.name}: {llm_assessment.risk_level or 'no risk level'}")
        else:
            trace.append(f"skipped {self.llm_advisor.name}: {llm_assessment.error}")

        report = QualityReport(
            dataset=dataset,
            generated_at=datetime.now(timezone.utc),
            quality_score=score,
            status=self._status(score, findings),
            row_count=len(frame),
            findings=findings,
            business_rule_references=business_rule_references,
            likely_causes=self._likely_causes(findings),
            recommended_next_steps=self._next_steps(findings),
            llm_assessment=llm_assessment,
            agent_trace=trace,
        )
        report.verification = self.verifier.verify(report)
        report.agent_trace.append(f"called {self.verifier.name}: passed={report.verification.passed}")
        return report

    def _score(self, findings: list[QualityFinding]) -> int:
        penalty = 0
        weights = {
            Severity.low: 4,
            Severity.medium: 10,
            Severity.high: 18,
            Severity.critical: 28,
        }
        for finding in findings:
            penalty += weights[finding.severity]
        return max(0, 100 - penalty)

    def _status(self, score: int, findings: list[QualityFinding]) -> str:
        if any(finding.severity == Severity.critical for finding in findings) or score < 70:
            return "FAIL"
        if findings or score < 90:
            return "WARN"
        return "PASS"

    def _likely_causes(self, findings: list[QualityFinding]) -> list[str]:
        checks = {finding.check_name for finding in findings}
        causes = []
        if "schema_drift" in checks or "schema_required_columns" in checks:
            causes.append("Upstream producer changed the table contract without a coordinated schema migration.")
        if "freshness_sla" in checks:
            causes.append("Scheduled extract or warehouse load likely missed its expected run window.")
        if "duplicate_primary_key" in checks:
            causes.append("The ingestion pipeline may be replaying events without idempotent merge logic.")
        if "missing_values" in checks:
            causes.append("Source API or transform logic is producing incomplete fields for required analytics columns.")
        if "numeric_outliers" in checks or "negative_amount" in checks:
            causes.append("Business-rule validation is not separating exceptional transactions from standard facts.")
        if not causes:
            causes.append("No material data quality issue detected in the current sample.")
        return causes

    def _next_steps(self, findings: list[QualityFinding]) -> list[str]:
        if not findings:
            return ["Publish the dataset and keep the standard freshness monitor active."]

        ordered = sorted(findings, key=lambda item: ["LOW", "MEDIUM", "HIGH", "CRITICAL"].index(item.severity.value), reverse=True)
        recommendations = []
        for finding in ordered:
            if finding.recommendation not in recommendations:
                recommendations.append(finding.recommendation)
        recommendations.append("Attach this report to the data incident ticket and assign an owner for each failing check.")
        return recommendations[:5]
