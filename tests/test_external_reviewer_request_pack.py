from scripts.build_external_reviewer_request_pack import (
    build_external_reviewer_request_pack_payload,
    render_markdown,
    verify_external_reviewer_request_pack,
)


def test_external_reviewer_request_pack_routes_real_runs_to_issue_18():
    payload = build_external_reviewer_request_pack_payload()
    verification = verify_external_reviewer_request_pack(payload)
    markdown = render_markdown(payload)

    assert verification["external_reviewer_request_pack_verified"] is True
    assert payload["status"] == "outreach_ready_not_counted"
    assert payload["public_collection_issue"]["number"] == 18
    assert payload["public_collection_issue"]["url"].endswith("/issues/18")
    assert payload["external_run_review_template"]["url"].endswith("template=external_run_review.md")
    assert len(payload["outreach_messages"]) == 3
    assert {item["run_path"] for item in payload["outreach_messages"]} == {
        "public_demo_review",
        "container_smoke_run",
        "postgres_replay_run",
    }
    assert all(item["collection_url"].endswith("/issues/18") for item in payload["outreach_messages"])
    assert all(item["template_url"].endswith("template=external_run_review.md") for item in payload["outreach_messages"])
    assert len(payload["required_comment_fields"]) == 8
    assert {field["name"] for field in payload["required_comment_fields"]} >= {
        "reviewer_role",
        "path_tried",
        "observed_result",
        "permission_to_count_publicly",
    }
    assert payload["current_counts"]["external_feedback_items"] == 0
    assert payload["current_counts"]["confirmed_external_users"] == 0
    assert payload["current_counts"]["reproducible_feedback_items"] == 0
    assert "No outreach recipient has completed a run yet." in payload["not_claimed"]
    assert "External Reviewer Request Pack" in markdown
    assert "Copy-Ready Messages" in markdown


def test_external_reviewer_request_pack_preserves_resume_safe_claiming_rules():
    payload = build_external_reviewer_request_pack_payload()

    assert any("Only public comments on issue #18" in rule for rule in payload["counting_policy"])
    assert any("Self-authored local tests" in rule for rule in payload["counting_policy"])
    assert any("Counts stay at zero" in rule for rule in payload["counting_policy"])
    assert "zero-count baseline" in payload["resume_safe_summary"]
    assert "No customer feedback is claimed yet." in payload["not_claimed"]
