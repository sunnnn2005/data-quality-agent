from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_exposes_countable_reviewer_evidence_path():
    readme = (ROOT / "README.md").read_text()

    assert "## Try It and Leave Countable Evidence" in readme
    assert "https://sunnnn2005.github.io/data-quality-agent/" in readme
    assert "https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html" in readme
    assert "template=business_data_replay.md" in readme
    assert "reviewer quickstart router" in readme.lower()
    assert "first external review card" in readme.lower()
    assert "first feedback conversion runbook" in readme.lower()
    assert "evidence acceptance checklist" in readme.lower()
    assert "reviewer submission hub" in readme.lower()
    assert "outcome pipeline board" in readme.lower()
    assert "reviewer outreach console" in readme.lower()
    assert "first reviewer send kit" in readme.lower()
    assert "### 5 Real Reviewer Tasks" in readme
    assert "First AI reviewer ask" in readme
    assert "https://sunnnn2005.github.io/data-quality-agent/first-ai-reviewer-ask.html" in readme
    assert "AI Engineer review" in readme
    assert "Confirmed external run" in readme
    assert "Reproducible local replay" in readme
    assert "Business-case validation" in readme
    assert "Product feedback" in readme
    assert "ai_engineer_review.md" in readme
    assert "demo_feedback.md" in readme
    assert "business_case_review.md" in readme
    assert "review_slot_07" in readme
    assert "A sent message is distribution evidence, not a resume outcome." in readme
    assert "public, non-owner, permissioned, and redacted" in readme
    assert "24 evidence fields" in readme
    assert "233 automated tests" in readme
