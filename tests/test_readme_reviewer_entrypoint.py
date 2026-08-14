from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_exposes_countable_reviewer_evidence_path():
    readme = (ROOT / "README.md").read_text()

    assert "## Try It and Leave Countable Evidence" in readme
    assert "https://sunnnn2005.github.io/data-quality-agent/" in readme
    assert "https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html" in readme
    assert "template=business_data_replay.md" in readme
    assert "reviewer quickstart router" in readme.lower()
    assert "evidence acceptance checklist" in readme.lower()
    assert "reviewer submission hub" in readme.lower()
    assert "public, non-owner, permissioned, and redacted" in readme
    assert "24 evidence fields" in readme
    assert "165 automated tests" in readme
