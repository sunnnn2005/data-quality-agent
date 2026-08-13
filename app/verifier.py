from __future__ import annotations

from typing import Any

from app.models import QualityReport, ReportVerification, VerificationIssue


SENSITIVE_TERMS = {"ssn", "api_key", "token", "password", "secret"}


class ReportVerifier:
    name = "report_verifier"

    def verify(self, report: QualityReport) -> ReportVerification:
        issues: list[VerificationIssue] = []
        columns = set(report.dataset.expected_columns)
        columns.update(finding.column for finding in report.findings if finding.column)
        check_names = {finding.check_name for finding in report.findings}

        for finding in report.findings:
            if not finding.evidence:
                issues.append(
                    VerificationIssue(
                        code="missing_finding_evidence",
                        severity="HIGH",
                        message=f"Finding '{finding.check_name}' has no tool evidence.",
                    )
                )
            if finding.column and finding.column not in columns:
                issues.append(
                    VerificationIssue(
                        code="unknown_finding_column",
                        severity="HIGH",
                        message=f"Finding '{finding.check_name}' references unknown column '{finding.column}'.",
                    )
                )
            if self._contains_sensitive_value(finding.evidence):
                issues.append(
                    VerificationIssue(
                        code="sensitive_evidence_value",
                        severity="HIGH",
                        message=f"Finding '{finding.check_name}' evidence may contain sensitive data.",
                    )
                )

        if report.llm_assessment.enabled:
            for item in report.llm_assessment.evidence_used:
                text = str(item).lower()
                if not any(check.lower() in text for check in check_names):
                    issues.append(
                        VerificationIssue(
                            code="unsupported_llm_evidence",
                            severity="MEDIUM",
                            message=f"LLM evidence item is not tied to a report finding: {item}",
                        )
                    )

        if not report.recommended_next_steps:
            issues.append(
                VerificationIssue(
                    code="missing_recommended_action",
                    severity="MEDIUM",
                    message="Report has no recommended next steps.",
                )
            )

        if not 0 <= report.quality_score <= 100:
            issues.append(
                VerificationIssue(
                    code="invalid_quality_score",
                    severity="HIGH",
                    message="Quality score must be between 0 and 100.",
                )
            )

        evidence_supported = sum(1 for finding in report.findings if finding.evidence)
        support_rate = evidence_supported / len(report.findings) if report.findings else 1.0
        return ReportVerification(
            passed=not any(issue.severity == "HIGH" for issue in issues),
            issue_count=len(issues),
            evidence_support_rate=round(support_rate, 3),
            checked_rules=[
                "finding_evidence_required",
                "known_column_references",
                "sensitive_value_redaction",
                "llm_evidence_must_match_findings",
                "recommended_actions_required",
                "quality_score_bounds",
            ],
            issues=issues,
        )

    def _contains_sensitive_value(self, value: Any) -> bool:
        if isinstance(value, dict):
            return any(
                str(key).lower() in SENSITIVE_TERMS or self._contains_sensitive_value(item)
                for key, item in value.items()
            )
        if isinstance(value, list):
            return any(self._contains_sensitive_value(item) for item in value)
        text = str(value).lower()
        return any(term in text for term in SENSITIVE_TERMS)
