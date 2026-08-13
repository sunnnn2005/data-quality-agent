from scripts.build_public_reviewer_call import (
    build_public_reviewer_call,
    render_markdown,
    verify_public_reviewer_call,
)


def test_public_reviewer_call_opens_real_evidence_collection_without_claiming_outcomes():
    payload = build_public_reviewer_call()
    verification = verify_public_reviewer_call(payload)
    markdown = render_markdown(payload)

    assert verification["public_reviewer_call_verified"] is True
    assert payload["reviewer_segment_count"] == 3
    assert payload["linked_submission_paths"] == 6
    assert payload["linked_outreach_tasks"] == 8
    assert payload["required_public_evidence_fields"] == 23
    assert payload["resume_status"] == "public_call_open_not_claimable"
    assert payload["public_call_issue"].endswith("/issues/19")
    assert {segment["id"] for segment in payload["reviewer_segments"]} == {
        "technical_reviewer",
        "business_data_reviewer",
        "quick_demo_reviewer",
    }
    assert all(value == 0 for value in payload["current_counts"].values())
    assert "Public Reviewer Call" in markdown
    assert "Does not count private DMs" in markdown
