from scripts.verify_public_evidence_health import PUBLIC_CHECKS, _cache_busted_url, verify_public_evidence_health


def test_public_evidence_health_requires_core_public_signals():
    check_ids = {check["id"] for check in PUBLIC_CHECKS}

    assert {
        "public-demo",
        "demo-feedback-entrypoints",
        "business-impact-artifact",
        "outcome-evidence-manifest",
        "adoption-metrics",
        "outcome-collection-page",
        "incident-pattern-memory",
        "agent-observability",
        "agent-safety-boundaries",
        "agent-capability-matrix",
        "local-reviewer-demo",
        "runnable-release-packet",
        "external-run-evidence-packet",
        "external-run-collection-issue",
        "external-reviewer-request-pack",
        "external-run-review-template",
        "external-run-quickstart-page",
        "external-reviewer-outreach-tracker",
        "external-reviewer-evidence-gate",
        "api-smoke-report",
        "performance-baseline",
        "demo-usage-baseline",
        "impact-review-packet",
        "business-problem-casebook",
        "business-resolution-brief",
        "business-resolution-review-request",
        "business-resolution-review-issue",
        "github-traffic-snapshot",
        "public-metrics-refresh-workflow",
        "public-availability-snapshot",
        "pilot-evidence-quicklink",
        "pilot-launch-control-room",
        "resume-outcome-adjudication",
        "first-10-reviewer-sprint",
        "feedback-intake-quality",
        "business-data-replay-packet",
        "business-replay-demo",
        "real-model-runbook",
        "live-project-scorecard",
        "resume-outcome-action-checklist",
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
    resolution = next(check for check in PUBLIC_CHECKS if check["id"] == "business-resolution-brief")
    assert resolution["url"].endswith("/business-resolution-brief.json")
    assert "owner_handoffs" in resolution["expected_texts"]
    assert "no customer production deployment is claimed" in resolution["expected_texts"]
    resolution_review = next(check for check in PUBLIC_CHECKS if check["id"] == "business-resolution-review-request")
    assert resolution_review["url"].endswith("/business-resolution-review-request.json")
    assert "issues/30" in resolution_review["expected_texts"]
    assert "explicit permission" in resolution_review["expected_texts"]
    resolution_issue = next(check for check in PUBLIC_CHECKS if check["id"] == "business-resolution-review-issue")
    assert resolution_issue["url"].endswith("/issues/30")
    assert "A self-authored issue does not count as external feedback" in resolution_issue["expected_texts"]
    traffic = next(check for check in PUBLIC_CHECKS if check["id"] == "github-traffic-snapshot")
    assert "confirmed users from traffic alone" in traffic["expected_texts"]
    refresh = next(check for check in PUBLIC_CHECKS if check["id"] == "public-metrics-refresh-workflow")
    assert "scripts/update_adoption_metrics.py" in refresh["expected_texts"]
    assert "git-auto-commit-action" in refresh["expected_texts"]
    availability = next(check for check in PUBLIC_CHECKS if check["id"] == "public-availability-snapshot")
    assert availability["expected_json"]["endpoint_count"] == 4
    assert "production uptime SLA" in availability["expected_texts"]
    runnable = next(check for check in PUBLIC_CHECKS if check["id"] == "runnable-release-packet")
    assert "docker run" in runnable["expected_texts"]
    assert "No external installs are claimed." in runnable["expected_texts"]
    external_run = next(check for check in PUBLIC_CHECKS if check["id"] == "external-run-evidence-packet")
    assert external_run["expected_json"]["review_path_count"] == 3
    assert "permission_to_count_publicly" == external_run["expected_text"]
    assert "issues/18" in external_run["expected_texts"]
    assert "external_run_review.md" in external_run["expected_texts"]
    assert "No external reviewer run is claimed yet." in external_run["expected_texts"]
    external_issue = next(check for check in PUBLIC_CHECKS if check["id"] == "external-run-collection-issue")
    assert external_issue["url"].endswith("/issues/18")
    assert "Permission to count this publicly" in external_issue["expected_texts"]
    external_request = next(check for check in PUBLIC_CHECKS if check["id"] == "external-reviewer-request-pack")
    assert external_request["expected_json"]["status"] == "outreach_ready_not_counted"
    assert "issues/18" in external_request["expected_texts"]
    assert "external_run_review.md" in external_request["expected_texts"]
    assert "permission_to_count_publicly" in external_request["expected_texts"]
    template = next(check for check in PUBLIC_CHECKS if check["id"] == "external-run-review-template")
    assert "Permission to count publicly" in template["expected_texts"]
    assert "This can be counted as public external run evidence." in template["expected_texts"]
    quickstart = next(check for check in PUBLIC_CHECKS if check["id"] == "external-run-quickstart-page")
    assert quickstart["url"].endswith("/external-run-quickstart.html")
    assert "Comment on Issue #18" in quickstart["expected_texts"]
    assert "No external reviewer run is claimed yet." in quickstart["expected_texts"]
    quicklink = next(check for check in PUBLIC_CHECKS if check["id"] == "pilot-evidence-quicklink")
    assert quicklink["url"].endswith("/pilot-evidence-quicklink.json")
    assert quicklink["expected_json"]["action_count"] == 4
    assert quicklink["expected_json"]["total_evidence_fields"] == 17
    assert quicklink["expected_json"]["target_metric_count"] == 4
    assert "zero-count baselines" in quicklink["expected_texts"]
    control_room = next(check for check in PUBLIC_CHECKS if check["id"] == "pilot-launch-control-room")
    assert control_room["url"].endswith("/pilot-launch-control-room.json")
    assert control_room["expected_json"]["public_issue_thread_count"] == 4
    assert control_room["expected_json"]["launch_gate_count"] == 5
    assert control_room["expected_json"]["target_outcome_count"] == 4
    assert control_room["expected_json"]["current_claimable_external_outcomes"] == 0
    assert "business validation" in control_room["expected_texts"]
    adjudication = next(check for check in PUBLIC_CHECKS if check["id"] == "resume-outcome-adjudication")
    assert adjudication["url"].endswith("/resume-outcome-adjudication.json")
    assert adjudication["expected_json"]["claim_category_count"] == 5
    assert adjudication["expected_json"]["claimable_category_count"] == 0
    assert adjudication["expected_json"]["blocked_category_count"] == 5
    assert "exact public evidence required" in adjudication["expected_texts"]
    sprint = next(check for check in PUBLIC_CHECKS if check["id"] == "first-10-reviewer-sprint")
    assert sprint["url"].endswith("/first-10-reviewer-sprint.json")
    assert sprint["expected_json"]["slot_count"] == 10
    assert sprint["expected_json"]["issue_launch_count"] == 10
    assert sprint["expected_json"]["target_metric_count"] == 6
    assert sprint["expected_json"]["completed_count"] == 0
    assert "github_stars" in sprint["expected_texts"]
    assert "public_issue_created_not_sent" in sprint["expected_texts"]
    assert "first-10-issue-drafts" in sprint["expected_texts"]
    outreach = next(check for check in PUBLIC_CHECKS if check["id"] == "external-reviewer-outreach-tracker")
    assert outreach["url"].endswith("/external-reviewer-outreach-tracker.json")
    assert outreach["expected_json"]["queue_count"] == 3
    assert "No outreach message has been sent yet." in outreach["expected_texts"]
    assert "counts_toward_resume" in outreach["expected_texts"]
    gate = next(check for check in PUBLIC_CHECKS if check["id"] == "external-reviewer-evidence-gate")
    assert gate["url"].endswith("/external-reviewer-evidence-gate.json")
    assert gate["expected_json"]["accepted_issue_count"] == 0
    assert gate["minimum_json"]["rejected_issue_count"] == 0
    assert "The default artifact collects tracked public GitHub issues before applying the evidence gate." in gate["expected_texts"]
    assert "Reviewer must grant explicit permission before a run or feedback is counted." in gate["expected_texts"]
    action_checklist = next(check for check in PUBLIC_CHECKS if check["id"] == "resume-outcome-action-checklist")
    assert action_checklist["url"].endswith("/resume-outcome-action-checklist.json")
    assert action_checklist["expected_json"]["tracked_action_count"] == 5
    assert action_checklist["expected_json"]["claimable_action_count"] == 0
    assert "earn_first_star" in action_checklist["expected_texts"]
    assert "The checklist does not claim users, feedback, business impact, or stars." in action_checklist["expected_texts"]
    outcome_collection = next(check for check in PUBLIC_CHECKS if check["id"] == "outcome-collection-page")
    assert outcome_collection["url"].endswith("/docs/outcome-collection.html")
    assert outcome_collection["expected_text"] == "Turn reviews into resume-safe evidence"
    assert "Submit Evidence" in outcome_collection["expected_texts"]
    assert "Do not post raw customer data" in outcome_collection["expected_texts"]


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

    assert _cache_busted_url(raw_url, "abc123") == (
        "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/abc123/docs/adoption-metrics.json"
    )
    assert _cache_busted_url(page_url, "abc123") == page_url
