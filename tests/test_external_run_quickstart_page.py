from scripts.build_external_run_quickstart_page import (
    build_external_run_quickstart_payload,
    render_html,
    verify_external_run_quickstart_payload,
)


def test_external_run_quickstart_routes_reviewers_to_countable_public_evidence():
    payload = build_external_run_quickstart_payload()
    verification = verify_external_run_quickstart_payload(payload)
    html = render_html(payload)

    assert verification["external_run_quickstart_verified"] is True
    assert payload["review_path_count"] == 3
    assert payload["submission_field_count"] == 8
    assert payload["upgrade_rule_count"] == 3
    assert payload["collection_issue"].endswith("/issues/18")
    assert payload["review_template"].endswith("template=external_run_review.md")
    assert payload["current_counts"]["confirmed_external_users"] == 0
    assert "External run quickstart" in html
    assert "docker compose up --build" in html
    assert "No private business data" in html
