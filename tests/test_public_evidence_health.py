from scripts.verify_public_evidence_health import PUBLIC_CHECKS, verify_public_evidence_health


def test_public_evidence_health_requires_core_public_signals():
    check_ids = {check["id"] for check in PUBLIC_CHECKS}

    assert {
        "public-demo",
        "demo-feedback-entrypoints",
        "business-impact-artifact",
        "outcome-evidence-manifest",
        "adoption-metrics",
        "incident-pattern-memory",
        "agent-observability",
        "agent-safety-boundaries",
        "local-reviewer-demo",
        "api-smoke-report",
        "performance-baseline",
        "demo-usage-baseline",
        "live-project-scorecard",
        "recruiter-pitch",
        "application-evidence-pack",
        "pilot-outreach-kit",
        "pilot-program-plan",
        "feedback-metrics",
        "postgres-agent-route",
        "github-release",
    } <= check_ids
    feedback_entrypoints = next(check for check in PUBLIC_CHECKS if check["id"] == "demo-feedback-entrypoints")
    assert feedback_entrypoints["expected_text"] == "Try It & Leave Feedback"
    assert {"feedback-metrics.json", "bug_report.md", "feature_request.md"} <= set(
        feedback_entrypoints["expected_texts"]
    )


def test_public_evidence_health_verifier_rejects_failed_checks():
    payload = {
        "status": "FAIL",
        "check_count": 6,
        "passed_count": 5,
        "failed_count": 1,
        "checks": [{"id": "public-demo", "url": "https://example.test", "passed": False}],
    }

    try:
        verify_public_evidence_health(payload)
    except AssertionError as exc:
        assert "public evidence health failed" in str(exc)
    else:
        raise AssertionError("expected failed public evidence health payload to raise")
