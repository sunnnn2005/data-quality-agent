from scripts.verify_public_evidence_health import PUBLIC_CHECKS, _cache_busted_url, verify_public_evidence_health


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
        "agent-capability-matrix",
        "local-reviewer-demo",
        "runnable-release-packet",
        "external-run-evidence-packet",
        "api-smoke-report",
        "performance-baseline",
        "demo-usage-baseline",
        "impact-review-packet",
        "business-problem-casebook",
        "github-traffic-snapshot",
        "public-availability-snapshot",
        "feedback-intake-quality",
        "business-data-replay-packet",
        "business-replay-demo",
        "real-model-runbook",
        "live-project-scorecard",
        "recruiter-pitch",
        "application-evidence-pack",
        "reviewer-funnel-board",
        "reviewer-invitation-kit",
        "reviewer-landing-page",
        "pilot-outreach-kit",
        "pilot-program-plan",
        "pilot-conversion-board",
        "resume-outcome-readiness",
        "external-review-evidence-ledger",
        "feedback-metrics",
        "postgres-agent-route",
        "github-release",
    } <= check_ids
    replay_packet = next(check for check in PUBLIC_CHECKS if check["id"] == "business-data-replay-packet")
    assert "business_data_replay.md" in replay_packet["expected_texts"]
    feedback_entrypoints = next(check for check in PUBLIC_CHECKS if check["id"] == "demo-feedback-entrypoints")
    assert feedback_entrypoints["expected_text"] == "Try It & Leave Feedback"
    assert {
        "feedback-metrics.json",
        "bug_report.md",
        "feature_request.md",
        "review.html",
        "reviewer-feedback-packet.md",
        "reviewer-funnel-board.md",
        "reviewer-invitation-kit.md",
        "automated tests passing locally and in CI",
    } <= set(feedback_entrypoints["expected_texts"])
    external_ledger = next(check for check in PUBLIC_CHECKS if check["id"] == "external-review-evidence-ledger")
    assert external_ledger["expected_json"]["self_authored_planning_excluded"] is True
    assert "evidence_counts" in external_ledger["expected_texts"]
    traffic = next(check for check in PUBLIC_CHECKS if check["id"] == "github-traffic-snapshot")
    assert "confirmed users from traffic alone" in traffic["expected_texts"]
    availability = next(check for check in PUBLIC_CHECKS if check["id"] == "public-availability-snapshot")
    assert availability["expected_json"]["endpoint_count"] == 4
    assert "production uptime SLA" in availability["expected_texts"]
    runnable = next(check for check in PUBLIC_CHECKS if check["id"] == "runnable-release-packet")
    assert "docker run" in runnable["expected_texts"]
    assert "No external installs are claimed." in runnable["expected_texts"]
    external_run = next(check for check in PUBLIC_CHECKS if check["id"] == "external-run-evidence-packet")
    assert external_run["expected_json"]["review_path_count"] == 3
    assert "permission_to_count_publicly" == external_run["expected_text"]
    assert "No external reviewer run is claimed yet." in external_run["expected_texts"]


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


def test_public_evidence_health_cache_busts_raw_github_urls_only():
    raw_url = "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/adoption-metrics.json"
    page_url = "https://sunnnn2005.github.io/data-quality-agent/review.html"

    assert _cache_busted_url(raw_url, "abc123").endswith("?cache_bust=abc123")
    assert _cache_busted_url(page_url, "abc123") == page_url
