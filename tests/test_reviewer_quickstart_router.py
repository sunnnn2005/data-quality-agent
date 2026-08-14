from pathlib import Path

from scripts.build_reviewer_quickstart_router import (
    build_reviewer_quickstart_router,
    render_markdown,
    verify_reviewer_quickstart_router,
)


ROOT = Path(__file__).resolve().parents[1]


def test_reviewer_quickstart_router_maps_reviewer_paths_to_zero_count_metrics():
    payload = build_reviewer_quickstart_router()
    result = verify_reviewer_quickstart_router(payload)

    assert result["reviewer_quickstart_router_verified"] is True
    assert payload["route_count"] == 5
    assert result["zero_metric_count"] == 5
    assert payload["prioritized_next_send"]["target_metric"] == "ai_engineer_review_items"
    assert set(payload["current_zero_counts"].values()) == {0}
    assert "non-owner public GitHub issue" in payload["manual_counting_rule"]


def test_reviewer_quickstart_router_markdown_exposes_short_paths_and_no_overclaiming():
    payload = build_reviewer_quickstart_router()
    markdown = render_markdown(payload)

    assert "# Reviewer Quickstart Router" in markdown
    assert "I only have 5 minutes" in markdown
    assert "I can review the agent architecture" in markdown
    assert "business_case_feedback_items" in markdown
    assert "Current Zero Counts" in markdown
    assert "preserving zero current claims" in markdown


def test_generated_reviewer_quickstart_router_artifacts_are_current():
    payload = build_reviewer_quickstart_router()
    verify_reviewer_quickstart_router(payload)

    generated_json = (ROOT / "docs" / "reviewer-quickstart-router.json").read_text()
    generated_md = (ROOT / "docs" / "reviewer-quickstart-router.md").read_text()

    assert '"route_count": 5' in generated_json
    assert '"target_metric": "ai_engineer_review_items"' in generated_json
    assert "# Reviewer Quickstart Router" in generated_md
