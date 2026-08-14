from scripts.build_outcome_collection_page import (
    build_outcome_collection_payload,
    render_html,
    verify_outcome_collection_payload,
)


def test_outcome_collection_page_routes_reviewers_to_countable_evidence():
    payload = build_outcome_collection_payload()
    verification = verify_outcome_collection_payload(payload)
    html = render_html(payload)

    assert verification["outcome_collection_page_verified"] is True
    assert payload["tracked_action_count"] == 5
    assert payload["submission_path_count"] == 6
    assert payload["required_evidence_field_count"] == 23
    assert payload["current_counts"]["confirmed_external_users"] == 0
    assert payload["current_counts"]["external_feedback_items"] == 0
    assert payload["current_counts"]["github_stars"] == 0
    assert "Turn reviews into resume-safe evidence" in html
    assert "Start 8-minute review" in html
    assert "Submit Evidence" in html
    assert "No external users are claimed" in html
    assert "Do not post raw customer data" in html
