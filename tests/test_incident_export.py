from app.agent import DataQualityAgent
from app.data import DATASETS, load_dataset
from app.incident_export import render_incident_markdown


def test_incident_markdown_separates_facts_evidence_actions_and_limits():
    report = DataQualityAgent().analyze(DATASETS["orders_daily"], load_dataset("orders_daily"))
    markdown = render_incident_markdown(report)

    assert markdown.startswith("# Data Quality Incident: Daily Orders")
    assert "## Facts" in markdown
    assert "## Evidence" in markdown
    assert "## Verification" in markdown
    assert "## Likely Causes" in markdown
    assert "## Root Cause Hypotheses" in markdown
    assert "## Recommended Actions" in markdown
    assert "## Limitations" in markdown
    assert "Evidence support rate: `1.0`" in markdown
    assert "Confidence: `" in markdown
    assert "Supporting checks:" in markdown
    assert "`duplicate_primary_key`" in markdown
    assert "The agent does not write to production systems" in markdown
