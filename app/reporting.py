from app.models import QualityReport

def report_to_text(report: QualityReport) -> str:
    lines = [
        f"Status: {report.status}",
        f"Score: {report.quality_score}",
        "",
        "Findings:",
    ]

    if report.findings:
        for finding in report.findings:
            column = f" ({finding.column})" if finding.column else ""
            lines.append(
                f"- [{finding.severity.value}] {finding.check_name}{column}: "
                f"{finding.message}"
            )
    else:
        lines.append("- No quality findings.")

    lines.append("")
    lines.append("Likely Causes:")
    for cause in report.likely_causes:
        lines.append(f"- {cause}")

    lines.append("")
    lines.append("Next Steps:")
    for step in report.recommended_next_steps:
        lines.append(f"- {step}")

    return "\n".join(lines)
