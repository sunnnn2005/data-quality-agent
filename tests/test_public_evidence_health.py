from scripts.verify_public_evidence_health import PUBLIC_CHECKS, _cache_busted_url, verify_public_evidence_health


def test_public_evidence_health_requires_core_public_signals():
    check_ids = {check["id"] for check in PUBLIC_CHECKS}

    assert {
        "public-demo",
        "readme-real-reviewer-tasks",
        "demo-feedback-entrypoints",
        "business-impact-artifact",
        "outcome-evidence-manifest",
        "adoption-metrics",
        "first-ai-reviewer-ask-page",
        "first-ai-reviewer-ask",
        "llm-value-comparison",
        "llm-value-comparison-page",
        "outcome-collection-page",
        "outcome-proof-page",
        "outcome-proof-page-artifact",
        "two-minute-review-card-page",
        "two-minute-review-card",
        "business-pilot-offer-page",
        "business-pilot-offer",
        "resume-live-proof-snapshot",
        "business-pilot-offer-issue",
        "first-external-review-card-page",
        "first-external-review-card",
        "first-feedback-conversion-runbook",
        "llm-agent-checklist-verdict",
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
        "resume-outcome-conversion-plan",
        "api-smoke-report",
        "performance-baseline",
        "demo-usage-baseline",
        "code-of-conduct",
        "contributor-conversion-kit",
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
        "reviewer-send-queue",
        "reviewer-landing-page",
        "reviewer-outreach-console",
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
        "reviewer-outreach-console.html",
        "one-click-evidence-links.html",
        "reviewer-feedback-packet.md",
        "reviewer-funnel-board.md",
        "reviewer-invitation-kit.md",
        "outcome-proof-page.html",
        "automated tests passing locally and in CI",
    } <= set(feedback_entrypoints["expected_texts"])
    readme_reviewer_tasks = next(check for check in PUBLIC_CHECKS if check["id"] == "readme-real-reviewer-tasks")
    assert readme_reviewer_tasks["url"].endswith("/README.md")
    assert readme_reviewer_tasks["expected_text"] == "5 Real Reviewer Tasks"
    assert {
        "AI Engineer review",
        "Confirmed external run",
        "Reproducible local replay",
        "Business-case validation",
        "Product feedback",
        "ai_engineer_review.md",
        "business_case_review.md",
        "review_slot_07",
        "A sent message is distribution evidence, not a resume outcome.",
    } <= set(readme_reviewer_tasks["expected_texts"])
    first_ai_reviewer_page = next(check for check in PUBLIC_CHECKS if check["id"] == "first-ai-reviewer-ask-page")
    assert first_ai_reviewer_page["url"].endswith("/first-ai-reviewer-ask.html")
    assert first_ai_reviewer_page["expected_text"] == "Review the LLM agent design in 8-15 minutes"
    assert {
        "Submit AI review",
        "app/agent.py",
        "docs/agent-safety-boundaries.md",
        "Required public evidence",
        "page view does not count",
    } <= set(first_ai_reviewer_page["expected_texts"])
    first_ai_reviewer = next(check for check in PUBLIC_CHECKS if check["id"] == "first-ai-reviewer-ask")
    assert first_ai_reviewer["url"].endswith("/first-ai-reviewer-ask.json")
    assert first_ai_reviewer["expected_json"]["target_metric"] == "ai_engineer_review_items"
    assert first_ai_reviewer["expected_json"]["status_board_slot_id"] == "review_slot_07"
    assert first_ai_reviewer["expected_json"]["current_claimable_ai_reviews"] == 0
    assert "ready_to_send_not_reviewed" in first_ai_reviewer["expected_texts"]
    llm_value = next(check for check in PUBLIC_CHECKS if check["id"] == "llm-value-comparison")
    assert llm_value["url"].endswith("/llm-value-comparison.json")
    assert llm_value["expected_json"]["scenario_count"] == 14
    assert llm_value["expected_json"]["fixed_generic_average_recall"] == 0.417
    assert llm_value["expected_json"]["adaptive_strategy_average_recall"] == 1.0
    assert llm_value["expected_json"]["absolute_recall_lift"] == 0.583
    assert "select_quality_strategy" in llm_value["expected_texts"]
    llm_value_page = next(check for check in PUBLIC_CHECKS if check["id"] == "llm-value-comparison-page")
    assert llm_value_page["url"].endswith("/llm-value-comparison.html")
    assert "139.8%" in llm_value_page["expected_texts"]
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
    proof_page = next(check for check in PUBLIC_CHECKS if check["id"] == "outcome-proof-page")
    assert proof_page["url"].endswith("/docs/outcome-proof-page.html")
    assert proof_page["expected_text"] == "Outcome Proof Page"
    assert "Help Unlock Real Outcomes" in proof_page["expected_texts"]
    proof_artifact = next(check for check in PUBLIC_CHECKS if check["id"] == "outcome-proof-page-artifact")
    assert proof_artifact["url"].endswith("/outcome-proof-page.json")
    assert proof_artifact["expected_json"]["claimable_card_count"] == 6
    assert proof_artifact["expected_json"]["blocked_card_count"] == 6
    assert proof_artifact["expected_json"]["reviewer_action_count"] == 5
    assert "ethical_star_or_fork" in proof_artifact["expected_texts"]
    review_card_page = next(check for check in PUBLIC_CHECKS if check["id"] == "first-external-review-card-page")
    assert review_card_page["url"].endswith("/first-external-review-card.html")
    assert review_card_page["expected_text"] == "Review Data Quality Agent in 5-12 minutes"
    assert "Submit public evidence" in review_card_page["expected_texts"]
    micro_card_page = next(check for check in PUBLIC_CHECKS if check["id"] == "two-minute-review-card-page")
    assert micro_card_page["url"].endswith("/two-minute-review-card.html")
    assert micro_card_page["expected_text"] == "Review Data Quality Agent in 2 minutes"
    assert "Required evidence" in micro_card_page["expected_texts"]
    micro_card = next(check for check in PUBLIC_CHECKS if check["id"] == "two-minute-review-card")
    assert micro_card["url"].endswith("/two-minute-review-card.json")
    assert micro_card["expected_json"]["time_budget_minutes"] == 2
    assert micro_card["expected_json"]["micro_step_count"] == 3
    assert micro_card["expected_json"]["required_evidence_count"] == 5
    assert "production adoption" in micro_card["expected_texts"]
    pilot_offer_page = next(check for check in PUBLIC_CHECKS if check["id"] == "business-pilot-offer-page")
    assert pilot_offer_page["url"].endswith("/business-pilot-offer.html")
    assert pilot_offer_page["expected_text"] == "Business Data Pilot Offer"
    assert "Evidence gates" in pilot_offer_page["expected_texts"]
    pilot_offer = next(check for check in PUBLIC_CHECKS if check["id"] == "business-pilot-offer")
    assert pilot_offer["url"].endswith("/business-pilot-offer.json")
    assert pilot_offer["expected_json"]["pilot_scope_count"] == 4
    assert pilot_offer["expected_json"]["evidence_gate_count"] == 6
    assert pilot_offer["expected_json"]["pilot_status"] == "ready_to_invite_not_validated"
    assert pilot_offer["expected_json"]["public_issue_status"] == "open_self_authored_entrypoint_not_outcome_evidence"
    assert "production deployment" in pilot_offer["expected_texts"]
    assert "https://github.com/sunnnn2005/data-quality-agent/issues/31" in pilot_offer["expected_texts"]
    resume_live_proof = next(check for check in PUBLIC_CHECKS if check["id"] == "resume-live-proof-snapshot")
    assert resume_live_proof["url"].endswith("/resume-live-proof-snapshot.json")
    assert resume_live_proof["expected_text"] == "resume_safe_bullets"
    assert "business_pilot_issue" in resume_live_proof["expected_texts"]
    assert "Self-authored issues" in resume_live_proof["expected_texts"]
    pilot_offer_issue = next(check for check in PUBLIC_CHECKS if check["id"] == "business-pilot-offer-issue")
    assert pilot_offer_issue["url"].endswith("/issues/31")
    assert pilot_offer_issue["expected_text"] == "Business pilot offer: collect redacted data-quality replay evidence"
    assert "does not claim completed pilots" in pilot_offer_issue["expected_texts"]
    review_card = next(check for check in PUBLIC_CHECKS if check["id"] == "first-external-review-card")
    assert review_card["url"].endswith("/first-external-review-card.json")
    assert review_card["expected_json"]["blocked_outcome_count"] == 6
    assert "production adoption" in review_card["expected_texts"]
    conversion_runbook = next(check for check in PUBLIC_CHECKS if check["id"] == "first-feedback-conversion-runbook")
    assert conversion_runbook["url"].endswith("/first-feedback-conversion-runbook.json")
    assert conversion_runbook["expected_json"]["sprint_step_count"] == 5
    assert "record_reviewer_outreach_event.py" in conversion_runbook["expected_texts"]
    agent_verdict = next(check for check in PUBLIC_CHECKS if check["id"] == "llm-agent-checklist-verdict")
    assert agent_verdict["url"].endswith("/llm-agent-checklist-verdict.json")
    assert agent_verdict["expected_json"]["status_counts"] == {"yes": 10, "partial": 4, "not_yet": 2}
    assert "not a production enterprise AI agent" in agent_verdict["expected_texts"]
    assert "Business Data Quality Copilot" in agent_verdict["expected_texts"]
    invitation = next(check for check in PUBLIC_CHECKS if check["id"] == "reviewer-invitation-kit")
    assert invitation["expected_json"]["invitation_count"] == 6
    assert invitation["expected_json"]["public_evidence_path_count"] == 5
    assert "short_share_card" in invitation["expected_texts"]
    assert "Review Data Quality Agent in 8-12 minutes" in invitation["expected_texts"]
    assert "record_reviewer_outreach_event.py" in invitation["expected_texts"]
    assert "--status sent" in invitation["expected_texts"]
    assert "no public evidence yet" in invitation["expected_texts"]
    assert "https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html" in invitation["expected_texts"]
    assert "\"accepted_issue_count\": 0" in invitation["expected_texts"]
    assert "\"claimable_resume_metric_count\": 0" in invitation["expected_texts"]
    send_queue = next(check for check in PUBLIC_CHECKS if check["id"] == "reviewer-send-queue")
    assert send_queue["expected_json"]["queue_count"] == 5
    assert send_queue["expected_json"]["sent_count"] == 0
    assert "https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html" in send_queue["expected_texts"]
    assert "zero upgraded resume outcome claims" in send_queue["expected_texts"]
    conversion = next(check for check in PUBLIC_CHECKS if check["id"] == "resume-outcome-conversion-plan")
    assert conversion["expected_json"]["conversion_row_count"] == 6
    assert conversion["expected_json"]["blocked_outcome_count"] == 6
    assert "one-click-evidence-links.html" in conversion["expected_texts"]
    assert "Outreach attempts alone do not count" in conversion["expected_texts"]
    contributor = next(check for check in PUBLIC_CHECKS if check["id"] == "contributor-conversion-kit")
    assert contributor["url"].endswith("/contributor-conversion-kit.json")
    assert contributor["expected_json"]["conversion_path_count"] == 5
    assert contributor["expected_json"]["contributor_claimable_count"] == 0
    assert "business_data_replay.md" in contributor["expected_texts"]
    assert "ai_engineer_review.md" in contributor["expected_texts"]
    assert "organic GitHub stars" in contributor["expected_texts"]
    community = next(check for check in PUBLIC_CHECKS if check["id"] == "community-growth-baseline")
    assert "Code of Conduct" in community["expected_texts"]
    conduct = next(check for check in PUBLIC_CHECKS if check["id"] == "code-of-conduct")
    assert conduct["url"].endswith("/CODE_OF_CONDUCT.md")
    assert conduct["expected_text"] == "Outcome Evidence Boundary"
    assert "fake stars" in conduct["expected_texts"]
    assert "fake feedback" in conduct["expected_texts"]
    assert "Do not post private data" in conduct["expected_texts"]


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
