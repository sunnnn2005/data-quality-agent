from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "external_run_review.md"


def test_external_run_issue_template_collects_countable_public_evidence():
    text = TEMPLATE.read_text()

    assert "name: External run review" in text
    assert "labels: feedback,pilot,reproducible" in text
    assert "## Reviewer role" in text
    assert "## Path tried" in text
    assert "Public demo review" in text
    assert "GHCR container smoke run" in text
    assert "Docker Compose PostgreSQL replay" in text
    assert "## Commands or URLs used" in text
    assert "## Observed result" in text
    assert "## Permission to count publicly" in text
    assert "This can be counted as public external run evidence." in text
    assert "This can be counted as external feedback." in text
    assert "This can be counted as a reproducible local replay" in text
    assert "private business data, secrets, customer names, emails, addresses, or raw production rows" in text
