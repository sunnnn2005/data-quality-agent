from scripts.build_first_accepted_evidence_examples import (
    build_first_accepted_evidence_examples,
    render_markdown,
    verify_first_accepted_evidence_examples,
)


def test_first_accepted_evidence_examples_are_gate_tested_without_upgrading_claims():
    payload = build_first_accepted_evidence_examples()
    verification = verify_first_accepted_evidence_examples(payload)
    markdown = render_markdown(payload)

    assert verification["first_accepted_evidence_examples_verified"] is True
    assert payload["example_count"] == 4
    assert payload["accepted_example_count"] == 2
    assert payload["rejected_example_count"] == 2
    assert payload["real_public_issue_required"] is True
    assert payload["resume_claim_allowed_now"] is False
    assert "accepted_business_case" in markdown
    assert "accepted_real_model_run" in markdown
    assert "rejected_self_authored_business_case" in markdown
    assert "Synthetic examples are not counted as users" in payload["not_claimed"][0]


def test_first_accepted_evidence_examples_show_resume_unlock_paths_and_rejections():
    payload = build_first_accepted_evidence_examples()
    examples = {example["id"]: example for example in payload["examples"]}

    assert examples["accepted_business_case"]["accepted"] is True
    assert examples["accepted_business_case"]["counts_toward"] == ["business_case_feedback_items"]
    assert examples["accepted_real_model_run"]["accepted"] is True
    assert examples["accepted_real_model_run"]["counts_toward"] == ["accepted_real_model_runs"]
    assert examples["rejected_self_authored_business_case"]["accepted"] is False
    assert "self-authored issue" in examples["rejected_self_authored_business_case"]["failure_reasons"]
    assert examples["rejected_docs_only_replay"]["accepted"] is False
    assert "docs-only review is not a confirmed business-data replay" in examples["rejected_docs_only_replay"]["failure_reasons"]
