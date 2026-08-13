from app.models import QualityReport


def render_incident_markdown(report: QualityReport) -> str:
    lines = [
        f"# Data Quality Incident: {report.dataset.name}",
        "",
        "## Summary",
        "",
        f"- Status: `{report.status}`",
        f"- Quality score: `{report.quality_score}`",
        f"- Dataset owner: `{report.dataset.owner}`",
        f"- Row count: `{report.row_count}`",
        f"- Trace ID: `{report.trace_id or 'not recorded'}`",
        "",
        "## Facts",
        "",
    ]

    if report.findings:
        for finding in report.findings:
            location = f" on `{finding.column}`" if finding.column else ""
            lines.append(f"- `{finding.severity.value}` `{finding.check_name}`{location}: {finding.message}")
    else:
        lines.append("- No failing quality checks were detected.")

    lines.extend(["", "## Evidence", ""])
    for finding in report.findings:
        if finding.evidence:
            evidence = ", ".join(f"{key}={value}" for key, value in finding.evidence.items())
            lines.append(f"- `{finding.check_name}`: {evidence}")

    if not report.findings:
        lines.append("- No evidence required.")

    if report.verification:
        lines.extend(["", "## Verification", ""])
        lines.append(f"- Passed: `{report.verification.passed}`")
        lines.append(f"- Evidence support rate: `{report.verification.evidence_support_rate}`")
        lines.append(f"- Checked rules: {', '.join(f'`{rule}`' for rule in report.verification.checked_rules)}")
        if report.verification.issues:
            for issue in report.verification.issues:
                lines.append(f"- `{issue.severity}` `{issue.code}`: {issue.message}")
        else:
            lines.append("- No verification issues found.")

    lines.extend(["", "## Likely Causes", ""])
    for cause in report.likely_causes:
        lines.append(f"- {cause}")

    if report.root_cause_hypotheses:
        lines.extend(["", "## Root Cause Hypotheses", ""])
        for index, hypothesis in enumerate(report.root_cause_hypotheses, start=1):
            checks = ", ".join(f"`{check}`" for check in hypothesis.supporting_checks)
            lines.append(f"{index}. {hypothesis.title}")
            lines.append(f"   - Confidence: `{hypothesis.confidence}`")
            lines.append(f"   - Supporting checks: {checks}")
            for evidence in hypothesis.evidence:
                lines.append(f"   - Evidence: {evidence}")
            lines.append(f"   - Recommended action: {hypothesis.recommended_action}")

    lines.extend(["", "## Recommended Actions", ""])
    for step in report.recommended_next_steps:
        lines.append(f"- {step}")

    if report.business_rule_references:
        lines.extend(["", "## Business Rule References", ""])
        for reference in report.business_rule_references:
            lines.append(f"- `{reference.rule_id}`: {reference.title} ({reference.source})")

    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- This report is generated from the provided dataset sample and deterministic checks.",
            "- The agent does not write to production systems or modify source data.",
            "- Model-generated assessment is optional; deterministic findings remain the source of truth.",
            "",
        ]
    )
    return "\n".join(lines)
