from app.agent import DataQualityAgent
from app.data import DATASETS, load_dataset
from app.models import LLMAssessment
from app.verifier import ReportVerifier


def test_report_verifier_passes_evidence_backed_report():
    report = DataQualityAgent().analyze(DATASETS["orders_daily"], load_dataset("orders_daily"))

    assert report.verification is not None
    assert report.verification.passed is True
    assert report.verification.evidence_support_rate == 1.0
    assert "finding_evidence_required" in report.verification.checked_rules
    assert any("report_verifier" in step for step in report.agent_trace)


def test_report_verifier_flags_unsupported_llm_evidence():
    class FakeAdvisor:
        name = "llm_data_quality_advisor"

        def assess(self, profile, findings):
            return LLMAssessment(
                enabled=True,
                provider="test",
                model="fake-model",
                summary="Unsupported claim inserted by a model.",
                risk_level="HIGH",
                evidence_used=["payment outage from an external incident system"],
                suggested_actions=["Open an incident ticket."],
            )

    report = DataQualityAgent(llm_advisor=FakeAdvisor()).analyze(
        DATASETS["orders_daily"],
        load_dataset("orders_daily"),
    )

    assert report.verification is not None
    assert report.verification.passed is True
    assert any(issue.code == "unsupported_llm_evidence" for issue in report.verification.issues)


def test_report_verifier_flags_missing_evidence_as_high_severity():
    report = DataQualityAgent().analyze(DATASETS["orders_daily"], load_dataset("orders_daily"))
    report.findings[0].evidence = {}

    verification = ReportVerifier().verify(report)

    assert verification.passed is False
    assert any(issue.code == "missing_finding_evidence" for issue in verification.issues)
