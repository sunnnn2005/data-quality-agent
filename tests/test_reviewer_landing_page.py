from scripts.verify_reviewer_landing_page import verify_reviewer_landing_page


def test_reviewer_landing_page_routes_reviewers_to_public_feedback():
    verification = verify_reviewer_landing_page()

    assert verification["reviewer_landing_page_verified"] is True
    assert verification["required_fragment_count"] == 26
    assert verification["index_conversion_paths"] == 9
    assert verification["public_review_issue"].endswith("/issues/17")
    assert verification["demo_feedback_template"].endswith("template=demo_feedback.md")
