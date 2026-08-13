import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANDING_PATH = ROOT / "docs" / "review.html"


def verify_reviewer_landing_page() -> dict[str, int | str | bool]:
    html = LANDING_PATH.read_text()
    required_fragments = [
        "8-minute public review",
        "Open Demo",
        "Submit Feedback",
        "https://github.com/sunnnn2005/data-quality-agent/issues/17",
        "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md",
        "External feedback starts at zero",
        "107 tests",
        "12 issues",
        "1 fork",
        "external_feedback_items",
        "reproducible_feedback_items",
        "Please do not post raw customer data",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in html]
    if missing:
        raise AssertionError(f"reviewer landing page missing required fragments: {missing}")
    return {
        "reviewer_landing_page_verified": True,
        "required_fragment_count": len(required_fragments),
        "public_review_issue": "https://github.com/sunnnn2005/data-quality-agent/issues/17",
        "demo_feedback_template": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md",
    }


def main() -> None:
    print(json.dumps(verify_reviewer_landing_page(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
