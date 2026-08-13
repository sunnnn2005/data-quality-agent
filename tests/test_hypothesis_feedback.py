from scripts.build_hypothesis_feedback import (
    build_hypothesis_feedback_payload,
    render_markdown,
    verify_hypothesis_feedback,
)


def test_hypothesis_feedback_labels_root_cause_hypotheses_without_external_claims():
    payload = build_hypothesis_feedback_payload()
    verification = verify_hypothesis_feedback(payload)
    markdown = render_markdown(payload)

    assert verification["hypothesis_feedback_verified"] is True
    assert payload["label_count"] == 3
    assert payload["accepted_count"] == 2
    assert payload["needs_review_count"] == 1
    assert all(item["supporting_checks"] for item in payload["labels"])
    assert "external product feedback" in payload["not_claimed"]
    assert "Hypothesis Feedback" in markdown
    assert "`accepted`" in markdown
