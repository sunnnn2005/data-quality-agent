from scripts.build_external_run_evidence_packet import (
    build_external_run_evidence_packet,
    render_markdown,
    verify_external_run_evidence_packet,
)


def test_external_run_evidence_packet_defines_public_reviewer_run_proof():
    payload = build_external_run_evidence_packet()
    verification = verify_external_run_evidence_packet(payload)
    markdown = render_markdown(payload)

    assert verification["external_run_evidence_packet_verified"] is True
    assert payload["review_path_count"] == 3
    assert payload["submission_field_count"] == 8
    assert payload["upgrade_rule_count"] == 3
    assert payload["runnable_surface_count"] == 3
    assert payload["acceptance_check_count"] == 4
    assert payload["public_collection_issue"]["number"] == 18
    assert payload["public_collection_issue"]["url"].endswith("/issues/18")
    assert payload["public_collection_issue"]["counting_status"] == "collection_open_not_counted_yet"
    assert payload["external_run_review_template"]["url"].endswith("template=external_run_review.md")
    assert payload["current_counts"] == {
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
    }
    assert {path["counts_toward_after_public_issue"] for path in payload["review_paths"]} == {
        "external_feedback_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
    }
    assert "docker run" in markdown
    assert "docker compose up --build" in markdown
    assert "issues/18" in markdown
    assert "external_run_review.md" in markdown
    assert "No external reviewer run is claimed yet." in markdown


def test_external_run_evidence_packet_requires_permission_and_privacy_boundaries():
    payload = build_external_run_evidence_packet()

    required_fields = {field["name"] for field in payload["submission_fields"] if field["required"]}
    assert "permission_to_count_publicly" in required_fields
    assert "observed_result" in required_fields
    assert "environment" in required_fields
    assert any("Do not ask reviewers to upload private business data." == item for item in payload["privacy_boundaries"])
    assert any("Count only public GitHub issues" in item for item in payload["privacy_boundaries"])
