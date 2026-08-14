import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANDING_PATH = ROOT / "docs" / "review.html"
INDEX_PATH = ROOT / "docs" / "index.html"


def verify_reviewer_landing_page() -> dict[str, int | str | bool]:
    html = LANDING_PATH.read_text()
    index_html = INDEX_PATH.read_text()
    required_fragments = [
        "8-minute public review",
        "Open Demo",
        "Submit Feedback",
        "https://github.com/sunnnn2005/data-quality-agent/issues/17",
        "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md",
        "External feedback starts at zero",
        "200 tests",
        "25 issues",
        "1 fork",
        "external_feedback_items",
        "reproducible_feedback_items",
        "Choose your review path",
        "template=ai_engineer_review.md",
        "template=external_run_review.md",
        "template=business_case_review.md",
        "permission and no-private-data checks",
        "Please do not post raw customer data",
    ]
    required_index_fragments = [
        "Countable reviewer paths",
        "Leave evidence that can become a real resume outcome",
        "template=external_run_review.md",
        "template=demo_feedback.md",
        "template=business_case_review.md",
        "template=ai_engineer_review.md",
        "Star or fork only if the project is genuinely useful",
        "public, non-owner, permissioned, and redacted evidence",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in html]
    missing.extend(fragment for fragment in required_index_fragments if fragment not in index_html)
    if missing:
        raise AssertionError(f"reviewer landing page missing required fragments: {missing}")
    return {
        "reviewer_landing_page_verified": True,
        "required_fragment_count": len(required_fragments) + len(required_index_fragments),
        "public_review_issue": "https://github.com/sunnnn2005/data-quality-agent/issues/17",
        "demo_feedback_template": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md",
        "index_conversion_paths": len(required_index_fragments),
    }


def main() -> None:
    print(json.dumps(verify_reviewer_landing_page(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
