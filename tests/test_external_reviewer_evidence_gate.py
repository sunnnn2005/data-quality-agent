from scripts.build_external_reviewer_evidence_gate import (
    build_external_reviewer_evidence_gate,
    evaluate_issue,
    render_markdown,
    verify_external_reviewer_evidence_gate,
)


VALID_EXTERNAL_RUN_BODY = """## Reviewer role

- Role or background: student developer
- Relationship to the project owner, if any: none

## Path tried

- [x] Public demo review
- [ ] GHCR container smoke run
- [ ] Docker Compose PostgreSQL replay
- [ ] I reviewed the docs but did not run it

## Environment

- OS: macOS
- Browser: Chrome
- Docker version, if used:
- Python version, if used:

## Commands or URLs used

```bash
https://sunnnn2005.github.io/data-quality-agent/
```

## Observed result

- Health endpoint result: ok
- Report or page opened: support-ticket case study
- Agent/report status: FAIL
- Finding or output inspected: duplicate ticket IDs

## Usefulness score

- [x] 4 - useful with small changes

## Main feedback

The support-ticket example makes the data-quality workflow clear.

## Permission to count publicly

- [x] This issue contains no private business data, secrets, customer names, emails, addresses, or raw production rows.
- [x] This can be counted as public external run evidence.
- [x] This can be counted as external feedback.
- [x] This can be counted as a reproducible local replay, if I ran the container or Docker Compose path.
- [ ] Do not quote my name, organization, or private context.
"""


def issue(body: str, author: str = "external-reviewer", labels: list[str] | None = None):
    return {
        "number": 31,
        "title": "External run: public demo",
        "url": "https://github.com/sunnnn2005/data-quality-agent/issues/31",
        "author": {"login": author},
        "labels": [{"name": name} for name in (labels or ["feedback", "pilot", "reproducible"])],
        "body": body,
    }


def test_external_reviewer_evidence_gate_starts_from_zero_without_fake_claims():
    payload = build_external_reviewer_evidence_gate()
    verification = verify_external_reviewer_evidence_gate(payload)
    markdown = render_markdown(payload)

    assert verification["external_reviewer_evidence_gate_verified"] is True
    assert payload["evaluated_issue_count"] == 0
    assert payload["accepted_issue_count"] == 0
    assert payload["accepted_counts"]["external_feedback_items"] == 0
    assert payload["accepted_counts"]["confirmed_external_users"] == 0
    assert payload["linked_outreach_queue_count"] == 3
    assert "No accepted external reviewer issue exists yet." in payload["not_claimed"]
    assert "External Reviewer Evidence Gate" in markdown


def test_external_reviewer_evidence_gate_accepts_complete_public_run_issue():
    payload = build_external_reviewer_evidence_gate(issues=[issue(VALID_EXTERNAL_RUN_BODY)])
    evaluation = payload["evaluations"][0]

    assert evaluation["accepted"] is True
    assert evaluation["failure_reasons"] == []
    assert evaluation["counts_toward"] == [
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
    ]
    assert payload["accepted_issue_count"] == 1
    assert payload["accepted_counts"]["confirmed_external_users"] == 1
    assert payload["accepted_counts"]["external_feedback_items"] == 1
    assert payload["accepted_counts"]["reproducible_feedback_items"] == 1


def test_external_reviewer_evidence_gate_rejects_self_authored_missing_permission_or_sensitive_issue():
    missing_permission_body = VALID_EXTERNAL_RUN_BODY.replace(
        "- [x] This can be counted as public external run evidence.",
        "- [ ] This can be counted as public external run evidence.",
    )
    self_authored = evaluate_issue(issue(VALID_EXTERNAL_RUN_BODY, author="sunnnn2005"))
    missing_permission = evaluate_issue(issue(missing_permission_body))
    sensitive = evaluate_issue(issue(VALID_EXTERNAL_RUN_BODY + "\npassword: example"))

    assert self_authored["accepted"] is False
    assert "self-authored issue" in self_authored["failure_reasons"]
    assert missing_permission["accepted"] is False
    assert "missing public external run permission" in missing_permission["failure_reasons"]
    assert sensitive["accepted"] is False
    assert "contains sensitive-data risk terms" in sensitive["failure_reasons"]
