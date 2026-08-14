import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs" / "public-evidence-health.json"
TIMEOUT_SECONDS = 15
RAW_GITHUB_HOST = "https://raw.githubusercontent.com/"


PUBLIC_CHECKS = [
    {
        "id": "public-demo",
        "url": "https://sunnnn2005.github.io/data-quality-agent/",
        "expected_text": "Data Quality Agent",
        "evidence_type": "html",
    },
    {
        "id": "demo-feedback-entrypoints",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/index.html",
        "expected_text": "Try It & Leave Feedback",
        "expected_texts": [
            "feedback-metrics.json",
            "bug_report.md",
            "feature_request.md",
            "review.html",
            "reviewer-outreach-console.html",
            "one-click-evidence-links.html",
            "reviewer-feedback-packet.md",
            "reviewer-funnel-board.md",
            "reviewer-invitation-kit.md",
            "external-reviewer-request-pack.md",
            "outcome-proof-page.html",
            "automated tests passing locally and in CI",
        ],
        "evidence_type": "source",
    },
    {
        "id": "readme-real-reviewer-tasks",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/README.md",
        "expected_text": "5 Real Reviewer Tasks",
        "expected_texts": [
            "AI Engineer review",
            "Confirmed external run",
            "Reproducible local replay",
            "Business-case validation",
            "Product feedback",
            "ai_engineer_review.md",
            "business_case_review.md",
            "review_slot_07",
            "A sent message is distribution evidence, not a resume outcome.",
        ],
        "evidence_type": "source",
    },
    {
        "id": "business-impact-artifact",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-impact.json",
        "expected_json": {"issue_category_count": 4, "affected_column_count": 4, "recommended_action_count": 5},
        "evidence_type": "json",
    },
    {
        "id": "outcome-evidence-manifest",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-evidence.json",
        "expected_text": "business-impact-artifact",
        "expected_texts": [
            "external-run-evidence-packet",
            "231 passing CI tests",
            "accepted-evidence-rollup",
            "real-model-evidence-capture",
            "reviewer-action-queue",
            "reviewer-outreach-execution-pack",
            "reviewer-outreach-status-board",
            "resume-outcome-evidence-ledger",
            "pilot-reviewer-crm",
            "resume-claim-materializer",
            "evidence-gap-diagnostics",
            "one-click-evidence-links",
            "resume-outcome-metrics",
            "real-reviewer-outreach-playbook",
        ],
        "evidence_type": "json",
    },
    {
        "id": "real-reviewer-outreach-playbook",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/real-reviewer-outreach-playbook.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "contact_pool_count": 5,
            "outreach_step_count": 5,
            "current_baseline": {
                "accepted_public_evidence": 0,
                "ai_engineer_review_items": 0,
                "confirmed_external_users": 0,
                "external_feedback_items": 0,
                "github_stars_claimable": 0,
            },
        },
        "expected_texts": [
            "review_slot_07",
            "non-owner public GitHub issue",
            "no private data",
            "evidence gate",
            "message sent",
        ],
        "evidence_type": "json",
    },
    {
        "id": "first-ai-reviewer-ask-page",
        "url": "https://sunnnn2005.github.io/data-quality-agent/first-ai-reviewer-ask.html",
        "expected_text": "Review the LLM agent design in 8-15 minutes",
        "expected_texts": [
            "Submit AI review",
            "app/agent.py",
            "docs/agent-safety-boundaries.md",
            "docs/llm-value-comparison.md",
            "adaptive strategy selection",
            "Required public evidence",
            "page view does not count",
        ],
        "evidence_type": "html",
    },
    {
        "id": "first-ai-reviewer-ask",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/first-ai-reviewer-ask.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "target_metric": "ai_engineer_review_items",
            "status_board_slot_id": "review_slot_07",
            "inspection_target_count": 5,
            "review_question_count": 4,
            "current_claimable_ai_reviews": 0,
        },
        "expected_texts": [
            "first-ai-reviewer-ask.html",
            "permission to count",
            "page view does not count",
            "docs/llm-value-comparison.md",
            "adaptive strategy selection",
            "ready_to_send_not_reviewed",
        ],
        "evidence_type": "json",
    },
    {
        "id": "resume-claim-materializer",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/resume-claim-materializer.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "safe_current_bullet_count": 4,
            "future_template_count": 5,
            "materialized_claim_count": 0,
            "accepted_public_evidence_count": 0,
        },
        "expected_text": "exact resume bullets",
        "expected_texts": [
            "confirmed_external_users",
            "ai_engineer_review_items",
            "No enterprise deployment is claimed",
        ],
        "evidence_type": "json",
    },
    {
        "id": "evidence-gap-diagnostics",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/evidence-gap-diagnostics.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "accepted_issue_count": 0,
            "accepted_counts": {
                "ai_engineer_review_items": 0,
                "business_case_feedback_items": 0,
                "confirmed_external_users": 0,
                "external_feedback_items": 0,
                "reproducible_feedback_items": 0,
            },
        },
        "expected_text": "Self-authored planning issues remain excluded from outcome metrics",
        "expected_texts": [
            "ai_engineer_review_items",
            "confirmed_external_users",
            "business_case_feedback_items",
            "nearest_unlock_paths",
        ],
        "evidence_type": "json",
    },
    {
        "id": "adoption-metrics",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/adoption-metrics.json",
        "expected_json": {"stars": 0, "forks": 1, "test_count": 231},
        "evidence_type": "json",
    },
    {
        "id": "outcome-collection-page",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-collection.html",
        "expected_text": "Turn reviews into resume-safe evidence",
        "expected_texts": [
            "Submit Evidence",
            "No external users are claimed",
            "Do not post raw customer data",
            "Start 8-minute review",
            "Action checklist",
        ],
        "evidence_type": "html",
    },
    {
        "id": "outcome-proof-page",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-proof-page.html",
        "expected_text": "Outcome Proof Page",
        "expected_texts": [
            "Verified Now",
            "Blocked Until Evidence",
            "Help Unlock Real Outcomes",
            "Open evidence path",
            "Traffic, self-authored planning issues, and outreach attempts do not count",
        ],
        "evidence_type": "html",
    },
    {
        "id": "outcome-proof-page-artifact",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-proof-page.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "claimable_card_count": 6,
            "blocked_card_count": 6,
            "reviewer_action_count": 5,
        },
        "expected_text": "verified resume-safe proof cards",
        "expected_texts": [
            "public, non-owner",
            "outreach attempts do not count",
            "confirmed_external_users",
            "github_stars",
            "ethical_star_or_fork",
        ],
        "evidence_type": "json",
    },
    {
        "id": "first-external-review-card-page",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/first-external-review-card.html",
        "expected_text": "Review Data Quality Agent in 5-12 minutes",
        "expected_texts": [
            "Submit public evidence",
            "Counting rule",
            "non-owner GitHub issue",
            "external_feedback_items",
            "confirmed_external_users",
            "ai_engineer_review_items",
        ],
        "evidence_type": "html",
    },
    {
        "id": "two-minute-review-card-page",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/two-minute-review-card.html",
        "expected_text": "Review Data Quality Agent in 2 minutes",
        "expected_texts": [
            "Required evidence",
            "external_feedback_items",
            "non-owner GitHub issue",
        ],
        "evidence_type": "html",
    },
    {
        "id": "two-minute-review-card",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/two-minute-review-card.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "time_budget_minutes": 2,
            "micro_step_count": 3,
            "required_evidence_count": 5,
        },
        "expected_text": "zero outcome upgrades",
        "expected_texts": [
            "external feedback",
            "confirmed external user",
            "production adoption",
            "https://sunnnn2005.github.io/data-quality-agent/two-minute-review-card.html",
        ],
        "evidence_type": "json",
    },
    {
        "id": "business-pilot-offer-page",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-pilot-offer.html",
        "expected_text": "Business Data Pilot Offer",
        "expected_texts": [
            "Pilot-ready, not pilot-validated yet",
            "Eligible data sources",
            "Evidence gates",
            "Current public counts",
        ],
        "evidence_type": "html",
    },
    {
        "id": "business-pilot-offer",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-pilot-offer.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "pilot_scope_count": 4,
            "eligible_data_source_count": 4,
            "evidence_gate_count": 6,
            "pilot_status": "ready_to_invite_not_validated",
            "public_issue_status": "open_self_authored_entrypoint_not_outcome_evidence",
        },
        "expected_text": "zero current external pilot claims",
        "expected_texts": [
            "completed pilot",
            "real enterprise customer",
            "production deployment",
            "business_data_replay",
            "business_case_review",
            "https://github.com/sunnnn2005/data-quality-agent/issues/31",
        ],
        "evidence_type": "json",
    },
    {
        "id": "business-pilot-evidence-checklist",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-pilot-evidence-checklist.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "outcome_track_count": 4,
            "template_check_count": 5,
            "passed_template_check_count": 5,
            "claimable_now": [],
        },
        "expected_text": "zero current business-pilot outcome claims",
        "expected_texts": [
            "confirmed_external_users",
            "business_case_feedback_items",
            "reproducible_feedback_items",
            "external_feedback_items",
            "selected tools or agent trace summary",
            "measured company impact",
        ],
        "evidence_type": "json",
    },
    {
        "id": "resume-live-proof-snapshot",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/resume-live-proof-snapshot.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "purpose": "Give recruiters a concise, resume-safe snapshot of public proof without inflating adoption.",
        },
        "expected_text": "resume_safe_bullets",
        "expected_texts": [
            "public evidence checks passing",
            "business_pilot_issue",
            "blocked_until_external_evidence",
            "confirmed external users",
            "Self-authored issues",
        ],
        "evidence_type": "json",
    },
    {
        "id": "business-pilot-offer-issue",
        "url": "https://github.com/sunnnn2005/data-quality-agent/issues/31",
        "expected_text": "Business pilot offer: collect redacted data-quality replay evidence",
        "expected_texts": [
            "Public pilot page",
            "safe, redacted business-shaped workflow",
            "does not claim completed pilots",
            "confirmation that no private data was posted",
        ],
        "evidence_type": "html",
    },
    {
        "id": "first-external-review-card",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/first-external-review-card.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "blocked_outcome_count": 6,
            "fastest_path_minutes": 5,
            "ai_engineer_path_minutes": 12,
        },
        "expected_text": "zero user, feedback, AI-review, and star claims",
        "expected_texts": [
            "accepted external review",
            "confirmed external user",
            "external feedback",
            "production adoption",
            "https://sunnnn2005.github.io/data-quality-agent/first-external-review-card.html",
        ],
        "evidence_type": "json",
    },
    {
        "id": "first-feedback-conversion-runbook",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/first-feedback-conversion-runbook.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "sprint_step_count": 5,
        },
        "expected_text": "zero resume upgrades",
        "expected_texts": [
            "ai_engineer_review_items",
            "confirmed_external_users",
            "external_feedback_items",
            "record_reviewer_outreach_event.py",
            "non-owner issue passes the gate",
        ],
        "evidence_type": "json",
    },
    {
        "id": "llm-agent-checklist-verdict",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/llm-agent-checklist-verdict.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "status_counts": {
                "yes": 10,
                "partial": 4,
                "not_yet": 2,
            },
        },
        "expected_text": "LLM-powered data quality agent",
        "expected_texts": [
            "real LLM-agent foundation",
            "not a production enterprise AI agent",
            "Business Data Quality Copilot",
            "accepted_real_model_runs",
        ],
        "evidence_type": "json",
    },
    {
        "id": "openapi-contract",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/openapi.json",
        "expected_text": "/business-data/agent-report",
        "expected_texts": ["/datasets/{dataset_id}/memory", "/postgres/support-tickets/agent-report"],
        "evidence_type": "json",
    },
    {
        "id": "eval-summary",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/eval-summary.json",
        "expected_json": {"scenario_count": 14},
        "evidence_type": "json",
    },
    {
        "id": "llm-value-comparison",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/llm-value-comparison.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "scenario_count": 14,
            "fixed_generic_average_recall": 0.417,
            "adaptive_strategy_average_recall": 1.0,
            "absolute_recall_lift": 0.583,
            "improved_scenario_count": 9,
        },
        "expected_texts": [
            "select_quality_strategy",
            "relative_recall_lift_percent",
            "without claiming paid-model benchmark results or external adoption",
            "enterprise customer impact",
        ],
        "evidence_type": "json",
    },
    {
        "id": "llm-value-comparison-page",
        "url": "https://sunnnn2005.github.io/data-quality-agent/llm-value-comparison.html",
        "expected_text": "LLM Value Comparison",
        "expected_texts": [
            "fixed average recall",
            "adaptive average recall",
            "139.8%",
            "external adoption",
        ],
        "evidence_type": "html",
    },
    {
        "id": "hypothesis-feedback",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/hypothesis-feedback.json",
        "expected_json": {"label_count": 3, "accepted_count": 2, "needs_review_count": 1},
        "evidence_type": "json",
    },
    {
        "id": "incident-pattern-memory",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/incident-pattern-memory.json",
        "expected_json": {"trace_count": 2, "incident_pattern_count": 3},
        "expected_text": "external production incidents",
        "evidence_type": "json",
    },
    {
        "id": "agent-observability",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-observability.json",
        "expected_json": {"observed_trace_count": 2, "fallback_event_count": 2},
        "expected_text": "production monitoring dashboard",
        "evidence_type": "json",
    },
    {
        "id": "agent-safety-boundaries",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-safety-boundaries.json",
        "expected_json": {"tool_allowlist_count": 9, "postgres_rejected_write_query_count": 3},
        "expected_text": "formal security audit",
        "evidence_type": "json",
    },
    {
        "id": "agent-capability-matrix",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-capability-matrix.json",
        "expected_json": {"tool_count": 9, "implemented_count": 13, "partial_count": 4},
        "expected_text": "enterprise production deployment",
        "expected_texts": ["llm-decision-making", "tool-feedback-loop", "production-adoption"],
        "evidence_type": "json",
    },
    {
        "id": "agent-maturity-audit",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/agent-maturity-audit.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "audit_row_count": 20,
            "maturity_level": "real_llm_agent_foundation",
        },
        "expected_text": "20-point LLM agent maturity checklist",
        "expected_texts": [
            "LLM decision-making",
            "Controlled tools",
            "Agent loop",
            "accepted real-model benchmark run",
        ],
        "evidence_type": "json",
    },
    {
        "id": "real-model-evidence-capture",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/real-model-evidence-capture.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "capture_required_field_count": 17,
            "accepted_real_model_run_count": 0,
            "blocked_outcome_claim_count": 4,
        },
        "expected_text": "real OpenAI model run completed",
        "expected_texts": ["raw_prompt_logged", "estimated_cost_usd", "tool_call_count"],
        "evidence_type": "json",
    },
    {
        "id": "real-model-preflight",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/real-model-preflight.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "real_model_execution_status": "not_ready",
            "real_model_run_executed_by_preflight": False,
            "total_check_count": 5,
            "blocked_check_count": 2,
        },
        "expected_text": "OPENAI_API_KEY is not configured",
        "expected_texts": ["raw prompt contents", "raw business rows", "production model traffic"],
        "evidence_type": "json",
    },
    {
        "id": "local-reviewer-demo",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/local-reviewer-demo.json",
        "expected_json": {"project": "Data Quality Agent", "reviewer_command": "docker compose up --build"},
        "expected_text": "readonly_agent",
        "expected_texts": ["support_tickets", "external reviewer completion"],
        "evidence_type": "json",
    },
    {
        "id": "runnable-release-packet",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/runnable-release-packet.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "ghcr_container",
        "expected_texts": [
            "docker run",
            "docker compose up --build",
            "No external installs are claimed.",
            "/postgres/support-tickets/agent-report",
        ],
        "evidence_type": "json",
    },
    {
        "id": "external-run-evidence-packet",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/external-run-evidence-packet.json",
        "expected_json": {"project": "Data Quality Agent", "review_path_count": 3},
        "expected_text": "permission_to_count_publicly",
        "expected_texts": [
            "docker run",
            "docker compose up --build",
            "issues/18",
            "external_run_review.md",
            "No external reviewer run is claimed yet.",
            "Do not ask reviewers to upload private business data.",
        ],
        "evidence_type": "json",
    },
    {
        "id": "external-run-collection-issue",
        "url": "https://github.com/sunnnn2005/data-quality-agent/issues/18",
        "expected_text": "External run evidence",
        "expected_texts": [
            "Path A: Public demo review",
            "Path B: Container smoke run",
            "Path C: Docker Compose PostgreSQL replay",
            "Permission to count this publicly",
        ],
        "evidence_type": "html",
    },
    {
        "id": "external-reviewer-request-pack",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/external-reviewer-request-pack.json",
        "expected_json": {"project": "Data Quality Agent", "status": "outreach_ready_not_counted"},
        "expected_text": "No outreach recipient has completed a run yet.",
        "expected_texts": [
            "issues/18",
            "external_run_review.md",
            "public_demo_review",
            "container_smoke_run",
            "postgres_replay_run",
            "permission_to_count_publicly",
        ],
        "evidence_type": "json",
    },
    {
        "id": "external-run-review-template",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/.github/ISSUE_TEMPLATE/external_run_review.md",
        "expected_text": "External run review",
        "expected_texts": [
            "GHCR container smoke run",
            "Docker Compose PostgreSQL replay",
            "Permission to count publicly",
            "This can be counted as public external run evidence.",
            "private business data, secrets, customer names, emails, addresses, or raw production rows",
        ],
        "evidence_type": "source",
    },
    {
        "id": "ai-engineer-review-template",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/.github/ISSUE_TEMPLATE/ai_engineer_review.md",
        "expected_text": "AI Engineer review",
        "expected_texts": [
            "LLM value comparison: `docs/llm-value-comparison.md`",
            "LLM tool calling",
            "Multi-step tool feedback loop",
            "You may count this public issue as external AI Engineer project feedback.",
            "Do not count this issue publicly.",
        ],
        "evidence_type": "source",
    },
    {
        "id": "external-run-quickstart-page",
        "url": "https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html",
        "expected_text": "External run quickstart",
        "expected_texts": [
            "Open External Run Review",
            "Comment on Issue #18",
            "docker run --rm -p 8000:8000 ghcr.io/sunnnn2005/data-quality-agent:latest",
            "docker compose up --build",
            "permission_to_count_publicly",
            "No private business data",
            "No external reviewer run is claimed yet.",
        ],
        "evidence_type": "html",
    },
    {
        "id": "external-reviewer-outreach-tracker",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/external-reviewer-outreach-tracker.json",
        "expected_json": {"queue_count": 3, "source_message_count": 3, "linked_pilot_review_slots": 3},
        "expected_text": "external reviewer outreach tracker",
        "expected_texts": [
            "A sent message does not count as feedback.",
            "No outreach message has been sent yet.",
            "No contacted reviewer is claimed yet.",
            "counts_toward_resume",
        ],
        "evidence_type": "json",
    },
    {
        "id": "external-reviewer-evidence-gate",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/external-reviewer-evidence-gate.json",
        "expected_json": {"linked_outreach_queue_count": 3, "accepted_issue_count": 0},
        "minimum_json": {"evaluated_issue_count": 0, "rejected_issue_count": 0},
        "expected_text": "external reviewer evidence gate",
        "expected_texts": [
            "Self-authored issues do not count as external evidence.",
            "Reviewer must grant explicit permission before a run or feedback is counted.",
            "Issues containing sensitive-data risk terms are rejected until redacted.",
            "The default artifact collects tracked public GitHub issues before applying the evidence gate.",
            "No accepted external reviewer issue exists yet.",
        ],
        "evidence_type": "json",
    },
    {
        "id": "accepted-evidence-rollup",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/accepted-evidence-rollup.json",
        "expected_json": {
            "accepted_issue_count": 0,
            "claimable_metric_count": 5,
            "blocked_outcome_claim_count": 5,
        },
        "expected_text": "accepted evidence rollup",
        "expected_texts": [
            "No accepted external reviewer issue exists yet.",
            "confirmed_external_users",
            "external_feedback_items",
            "No private business data is used as outcome evidence.",
        ],
        "evidence_type": "json",
    },
    {
        "id": "business-impact-ledger",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-impact-ledger.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "accepted_business_impact_signal_count": 0,
        },
        "expected_text": "business-impact ledger",
        "expected_texts": [
            "validated business impact",
            "raw production data",
            "not_claimable_yet",
        ],
        "evidence_type": "json",
    },
    {
        "id": "resume-traction-proof",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/resume-traction-proof.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "claimable_now_count": 6,
            "future_claim_count": 4,
            "blocked_claim_count": 5,
        },
        "expected_text": "baseline_claimable_growth_not_yet_claimable",
        "expected_texts": [
            "Do not claim active users",
            "Do not claim customer feedback",
            "Do not claim enterprise or production adoption",
            "Do not convert GitHub traffic views into user counts",
        ],
        "evidence_type": "json",
    },
    {
        "id": "resume-outcome-conversion-plan",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/resume-outcome-conversion-plan.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "claimable_now_count": 6,
            "blocked_outcome_count": 6,
            "conversion_row_count": 6,
        },
        "expected_text": "blocked_until_public_evidence",
        "expected_texts": [
            "one-click-evidence-links.html",
            "ai_engineer_review_items",
            "github_stars",
            "Outreach attempts alone do not count",
            "zero upgraded outcome claims",
        ],
        "evidence_type": "json",
    },
    {
        "id": "api-smoke-report",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/api-smoke-report.json",
        "expected_json": {"project": "Data Quality Agent", "check_count": 6, "passed_count": 6},
        "expected_text": "production uptime SLA",
        "expected_texts": ["/datasets/orders_daily/quality-report", "/datasets/orders_daily/agent-report"],
        "evidence_type": "json",
    },
    {
        "id": "performance-baseline",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/performance-baseline.json",
        "expected_json": {"project": "Data Quality Agent", "benchmark_count": 2, "passed_count": 2},
        "expected_text": "production latency SLA",
        "expected_texts": ["/datasets/orders_daily/quality-report", "/datasets/orders_daily/profile"],
        "evidence_type": "json",
    },
    {
        "id": "demo-usage-baseline",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/demo-usage-baseline.json",
        "expected_json": {"project": "Data Quality Agent", "release": "v0.3.0"},
        "expected_text": "visitor analytics",
        "expected_texts": ["tracked_usage_funnel", "confirmed_external_users", "star_repository"],
        "evidence_type": "json",
    },
    {
        "id": "community-growth-baseline",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/community-growth-baseline.json",
        "expected_json": {"project": "Data Quality Agent", "issue_template_count": 8, "label_count": 10},
        "expected_text": "external contributors",
        "expected_texts": [
            "public_growth_channels",
            "good%20first%20issue",
            "business_data_replay.md",
            "external_run_review.md",
            "Code of Conduct",
        ],
        "evidence_type": "json",
    },
    {
        "id": "code-of-conduct",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/CODE_OF_CONDUCT.md",
        "expected_text": "Outcome Evidence Boundary",
        "expected_texts": [
            "fake stars",
            "fake feedback",
            "unverifiable endorsements",
            "Do not post private data",
        ],
        "evidence_type": "markdown",
    },
    {
        "id": "contributor-conversion-kit",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/contributor-conversion-kit.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "conversion_path_count": 5,
            "evidence_gate_count": 5,
            "contributor_claimable_count": 0,
        },
        "expected_text": "0 contributor-claimable outcomes",
        "expected_texts": [
            "demo_feedback.md",
            "business_data_replay.md",
            "ai_engineer_review.md",
            "business_case_review.md",
            "ethical_star_or_fork",
            "public non-owner issue",
            "organic GitHub stars",
        ],
        "evidence_type": "json",
    },
    {
        "id": "impact-review-packet",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/impact-review-packet.json",
        "expected_json": {"project": "Data Quality Agent", "business_metric_count": 12, "evidence_link_count": 8},
        "expected_text": "support-operations data-quality case study",
        "expected_texts": ["production financial impact avoided", "company adoption"],
        "evidence_type": "json",
    },
    {
        "id": "business-problem-casebook",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-problem-casebook.json",
        "expected_json": {"project": "Data Quality Agent", "business_case_count": 1, "detected_risk_count": 4},
        "expected_text": "verified data-quality casebook",
        "expected_texts": ["real customer dataset", "production financial impact avoided"],
        "evidence_type": "json",
    },
    {
        "id": "business-resolution-brief",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-resolution-brief.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "business_problem",
        "expected_texts": [
            "resume_safe_result",
            "owner_handoffs",
            "high_priority_actions",
            "no customer production deployment is claimed",
        ],
        "evidence_type": "json",
    },
    {
        "id": "business-resolution-review-request",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-resolution-review-request.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "business_resolution_review_request.py",
        "expected_texts": [
            "issues/30",
            "self_authored_issue_counts_as_feedback",
            "current_external_feedback_items",
            "current_confirmed_external_users",
            "explicit permission",
            "no private company data",
        ],
        "evidence_type": "json",
    },
    {
        "id": "business-resolution-review-issue",
        "url": "https://github.com/sunnnn2005/data-quality-agent/issues/30",
        "expected_text": "Business resolution review",
        "expected_texts": [
            "Does this support-operations data-quality scenario look realistic?",
            "Are the 5 findings mapped to the right business risks?",
            "Are the 3 high-priority actions useful and specific enough?",
            "Are the 4 owner handoffs believable for a real data/ops team?",
            "A self-authored issue does not count as external feedback",
        ],
        "evidence_type": "html",
    },
    {
        "id": "public-traction-dashboard",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/public-traction-dashboard.json",
        "expected_json": {"project": "Data Quality Agent", "traction_surface_count": 4, "growth_channel_count": 20},
        "expected_text": "not_claimable_yet",
        "expected_texts": ["public_demo", "feedback_issue_template", "GitHub star growth beyond the current public count"],
        "evidence_type": "json",
    },
    {
        "id": "github-traffic-snapshot",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/github-traffic-snapshot.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "GitHub traffic API rolling 14-day window",
        "expected_texts": [
            "traffic_available",
            "unique_cloners",
            "resume_policy",
            "confirmed users from traffic alone",
        ],
        "evidence_type": "json",
    },
    {
        "id": "public-metrics-refresh-workflow",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/.github/workflows/refresh-public-metrics.yml",
        "expected_text": "Refresh Public Metrics",
        "expected_texts": [
            "schedule:",
            "workflow_dispatch:",
            "contents: write",
            "scripts/update_feedback_metrics.py",
            "scripts/update_adoption_metrics.py",
            "scripts/build_github_traffic_snapshot.py",
            "scripts/build_star_growth_kit.py",
            "scripts/build_reviewer_action_queue.py",
            "scripts/build_reviewer_outreach_execution_pack.py",
            "scripts/build_resume_outcome_metrics.py",
            "scripts/build_reviewer_submission_hub.py",
            "scripts/build_public_reviewer_call.py",
            "scripts/build_reviewer_share_kit.py",
            "scripts/build_reviewer_outreach_status_board.py",
            "scripts/build_public_metrics_summary.py",
            "git-auto-commit-action",
        ],
        "evidence_type": "workflow",
    },
    {
        "id": "reviewer-outreach-status-board",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/reviewer-outreach-status-board.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "outreach_slot_count": 8,
            "status_stage_count": 5,
            "accepted_evidence_count": 0,
        },
        "expected_text": "tracking_ready_not_claimable",
        "expected_texts": [
            "not_sent",
            "replied_private",
            "non-owner public GitHub issue",
            "evidence gate",
        ],
        "evidence_type": "json",
    },
    {
        "id": "public-availability-snapshot",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/public-availability-snapshot.json",
        "expected_json": {"project": "Data Quality Agent", "endpoint_count": 4, "workflow_count": 3},
        "expected_text": "public demo availability and workflow health snapshot",
        "expected_texts": [
            "available_endpoint_count",
            "successful_workflow_count",
            "production uptime SLA",
            "active users",
        ],
        "evidence_type": "json",
    },
    {
        "id": "star-growth-kit",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/star-growth-kit.json",
        "expected_json": {"project": "Data Quality Agent", "generated_by": "scripts/build_star_growth_kit.py"},
        "expected_text": "fake or incentivized stars",
        "expected_texts": [
            "topic_readiness",
            "ethical_growth_actions",
            "resume_upgrade_rules",
            "traffic_snapshot",
            "repository interest",
            "confirmed users from traffic alone",
        ],
        "evidence_type": "json",
    },
    {
        "id": "pilot-evidence-quicklink",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-evidence-quicklink.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "action_count": 4,
            "total_evidence_fields": 17,
            "target_metric_count": 4,
        },
        "expected_text": "CI-verified pilot evidence quicklink",
        "expected_texts": [
            "zero-count baselines",
            "external users",
            "customer feedback",
            "submitted external business cases",
        ],
        "evidence_type": "json",
    },
    {
        "id": "pilot-launch-control-room",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-launch-control-room.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "public_issue_thread_count": 4,
            "launch_gate_count": 5,
            "target_outcome_count": 4,
            "reviewer_send_plan_count": 3,
            "current_claimable_external_outcomes": 0,
        },
        "expected_text": "CI-verified pilot launch control room",
        "expected_texts": [
            "external users",
            "customer feedback",
            "business validation",
            "public issue threads",
            "target outcome metrics",
        ],
        "evidence_type": "json",
    },
    {
        "id": "resume-outcome-adjudication",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/resume-outcome-adjudication.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "claim_category_count": 5,
            "claimable_category_count": 0,
            "blocked_category_count": 5,
            "accepted_issue_count": 0,
        },
        "expected_text": "CI-verified resume outcome adjudication",
        "expected_texts": [
            "external users",
            "customer feedback",
            "business validation",
            "unlock_condition",
            "exact public evidence required",
        ],
        "evidence_type": "json",
    },
    {
        "id": "first-10-reviewer-sprint",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/first-10-reviewer-sprint.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "sprint_name": "first_10_external_reviewer_sprint",
            "slot_count": 10,
            "issue_launch_count": 10,
            "not_sent_count": 10,
            "completed_count": 0,
            "target_metric_count": 6,
        },
        "expected_text": "CI-verified first-10 reviewer sprint",
        "expected_texts": [
            "slot_07_ai_engineer_review",
            "slot_09_public_star_if_useful",
            "github_stars",
            "public_issue_created_not_sent",
            "first-10-issue-drafts",
            "zero sent outreach",
            "zero upgraded outcome claims",
        ],
        "evidence_type": "json",
    },
    {
        "id": "feedback-intake-quality",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/feedback-intake-quality.json",
        "expected_json": {"project": "Data Quality Agent", "required_section_count": 7, "captured_field_count": 7},
        "expected_text": "CI-verified feedback intake system",
        "expected_texts": ["external users", "survey responses"],
        "evidence_type": "json",
    },
    {
        "id": "business-case-intake",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-case-intake.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "required_section_count": 8,
            "required_outcome_count": 8,
            "captured_field_count": 8,
        },
        "expected_text": "business-case",
        "expected_texts": [
            "submitted external business cases",
            "permission_boundary",
            "resume_outcome_fields",
            "manual investigation time",
            "pilot readiness with anonymized data",
        ],
        "evidence_type": "json",
    },
    {
        "id": "business-data-replay-packet",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-data-replay-packet.json",
        "expected_json": {"project": "Data Quality Agent", "replay_path_count": 3, "evidence_field_count": 8},
        "expected_text": "replay_ready_not_claimable",
        "expected_texts": [
            "sanitized_csv_upload",
            "readonly_postgres_table",
            "business_data_replay.md",
            "real company data analyzed",
        ],
        "evidence_type": "json",
    },
    {
        "id": "business-replay-demo",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/business-replay-demo.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "Support Tickets Replay",
        "expected_texts": [
            "examples/support_tickets.csv",
            "\"finding_count\": 5",
            "real company data",
            "external user replay",
        ],
        "evidence_type": "json",
    },
    {
        "id": "real-model-runbook",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/real-model-runbook.json",
        "expected_json": {"project": "Data Quality Agent", "current_real_model_runs": 0, "evidence_field_count": 15},
        "expected_text": "real_model_run_ready_not_claimable",
        "expected_texts": [
            "OPENAI_API_KEY",
            "paid model benchmark results",
            "/business-data/agent-report",
        ],
        "evidence_type": "json",
    },
    {
        "id": "live-project-scorecard",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/live-project-scorecard.json",
        "expected_json": {"release": "v0.3.0"},
        "expected_text": "verified_resume_claims",
        "expected_texts": ["confirmed_external_users", "GitHub stars beyond the current public count"],
        "evidence_type": "json",
    },
    {
        "id": "resume-outcome-action-checklist",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/resume-outcome-action-checklist.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "tracked_action_count": 5,
            "next_action_needed_count": 5,
            "claimable_action_count": 0,
            "accepted_public_issue_count": 0,
        },
        "expected_text": "send_first_reviewer_request",
        "expected_texts": [
            "collect_first_public_run_issue",
            "collect_ai_engineer_review",
            "collect_business_case",
            "earn_first_star",
            "The checklist does not claim users, feedback, business impact, or stars.",
        ],
        "evidence_type": "json",
    },
    {
        "id": "recruiter-pitch",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/recruiter-pitch.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "AI Engineer Intern",
        "expected_texts": ["honest_baseline", "external users"],
        "evidence_type": "json",
    },
    {
        "id": "application-evidence-pack",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/application-evidence-pack.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "one_line_project_proof",
        "expected_texts": ["application_links", "honest_baseline", "external users"],
        "evidence_type": "json",
    },
    {
        "id": "reviewer-funnel-board",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/reviewer-funnel-board.json",
        "expected_json": {"project": "Data Quality Agent", "funnel_stage_count": 4, "total_remaining_evidence_items": 7},
        "expected_text": "evidence_collection_ready",
        "expected_texts": ["confirmed_external_users", "business_case_feedback_items", "needs_public_evidence"],
        "evidence_type": "json",
    },
    {
        "id": "reviewer-invitation-kit",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/reviewer-invitation-kit.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "invitation_count": 6,
            "distinct_funnel_stage_count": 5,
            "public_evidence_path_count": 5,
        },
        "expected_text": "copy-ready invitations",
        "expected_texts": [
            "classmate_quick_demo",
            "technical_friend_local_replay",
            "mentor_ai_engineer_review",
            "short_share_card",
            "Review Data Quality Agent in 8-12 minutes",
            "record_reviewer_outreach_event.py",
            "--status sent",
            "no public evidence yet",
            "https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html",
            "Opening a one-click issue link is not evidence by itself.",
            "\"accepted_issue_count\": 0",
            "\"claimable_resume_metric_count\": 0",
            "ai_engineer_review_items",
            "business_case_feedback_items",
            "explicit zero-feedback baselines",
        ],
        "evidence_type": "json",
    },
    {
        "id": "reviewer-action-queue",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/reviewer-action-queue.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "queue_count": 8,
            "not_contacted_count": 8,
            "evidence_goal_count": 5,
        },
        "expected_text": "outreach_queue_ready_not_claimable",
        "expected_texts": [
            "permission_to_count",
            "raw customer data",
            "ai_engineer_review_items",
            "zero contacted or completed reviewers",
        ],
        "evidence_type": "json",
    },
    {
        "id": "reviewer-send-queue",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/reviewer-send-queue.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "queue_count": 5,
            "not_sent_count": 5,
            "sent_count": 0,
            "accepted_evidence_count": 0,
        },
        "expected_text": "send_ready_not_claimable",
        "expected_texts": [
            "ai_engineer_review_items",
            "https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html",
            "non-owner public GitHub issue passes the evidence gate",
            "zero upgraded resume outcome claims",
        ],
        "evidence_type": "json",
    },
    {
        "id": "reviewer-outreach-execution-pack",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/reviewer-outreach-execution-pack.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "outreach_item_count": 8,
            "ready_message_count": 8,
            "follow_up_rule_count": 8,
            "evidence_goal_count": 5,
        },
        "expected_text": "ready_to_send_not_claimable",
        "expected_texts": [
            "not_sent",
            "permission",
            "raw customer data",
            "zero sent or completed outreach claimed",
        ],
        "evidence_type": "json",
    },
    {
        "id": "resume-outcome-metrics",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/resume-outcome-metrics.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "tracked_outcome_count": 6,
            "claimable_outcome_count": 0,
            "blocked_outcome_count": 6,
        },
        "expected_text": "not_claimable_yet",
        "expected_texts": [
            "confirmed_external_users",
            "external_feedback_items",
            "business_case_feedback_items",
            "github_stars",
            "GitHub traffic is treated as repository interest, not as users.",
        ],
        "evidence_type": "json",
    },
    {
        "id": "reviewer-submission-hub",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/reviewer-submission-hub.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "submission_path_count": 6,
            "target_metric_count": 6,
            "total_required_evidence_fields": 24,
        },
        "expected_text": "collection_ready_not_claimable",
        "expected_texts": [
            "confirmed_external_users",
            "ai_engineer_review_items",
            "github_stars",
            "never asks for fake engagement",
        ],
        "evidence_type": "json",
    },
    {
        "id": "public-reviewer-call",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/public-reviewer-call.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "reviewer_segment_count": 3,
            "linked_submission_paths": 6,
            "required_public_evidence_fields": 24,
        },
        "expected_text": "public_call_open_not_claimable",
        "expected_texts": [
            "issues/19",
            "technical_reviewer",
            "business_data_reviewer",
            "quick_demo_reviewer",
            "fake GitHub engagement",
        ],
        "evidence_type": "json",
    },
    {
        "id": "reviewer-share-kit",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/reviewer-share-kit.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "share_channel_count": 5,
            "ready_message_count": 5,
            "linked_submission_paths": 6,
        },
        "expected_text": "share_ready_not_claimable",
        "expected_texts": [
            "issues/19",
            "linkedin_dm",
            "permission",
            "fake GitHub engagement",
            "not_sent",
        ],
        "evidence_type": "json",
    },
    {
        "id": "public-reviewer-call-issue",
        "url": "https://github.com/sunnnn2005/data-quality-agent/issues/19",
        "expected_text": "Public reviewer call",
        "expected_texts": [
            "collecting real external review and pilot evidence",
            "confirmed external users: 0",
            "Counting rules",
            "does not contain private business data",
        ],
        "evidence_type": "html",
    },
    {
        "id": "reviewer-landing-page",
        "url": "https://sunnnn2005.github.io/data-quality-agent/review.html",
        "expected_text": "8-minute public review",
        "expected_texts": [
            "Open Demo",
            "Submit Feedback",
            "issues/17",
            "External feedback starts at zero",
            "tests",
        ],
        "evidence_type": "html",
    },
    {
        "id": "reviewer-outreach-console",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/reviewer-outreach-console.html",
        "expected_text": "Reviewer outreach console",
        "expected_texts": [
            "Open submission form",
            "Record after real send",
            "--slot-id review_slot_07",
            "accepted evidence",
            "Do not buy, trade, or pressure",
        ],
        "evidence_type": "html",
    },
    {
        "id": "resume-outcome-evidence-ledger",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/resume-outcome-evidence-ledger.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "claimable_now_count": 4,
            "blocked_until_evidence_count": 5,
            "accepted_public_evidence_count": 0,
            "resume_upgrade_count": 0,
        },
        "expected_text": "claimable engineering signals",
        "expected_texts": [
            "record_reviewer_outreach_event.py",
            "confirmed_external_users",
            "ai_engineer_review_items",
            "No enterprise production deployment is claimed",
        ],
        "evidence_type": "json",
    },
    {
        "id": "pilot-reviewer-crm",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-reviewer-crm.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "lead_count": 8,
            "priority_metric_count": 5,
            "week_count": 3,
            "accepted_public_evidence_count": 0,
        },
        "expected_text": "executable reviewer CRM",
        "expected_texts": [
            "ai_engineer_review_items",
            "record_reviewer_outreach_event.py",
            "Do not buy, trade, or pressure",
            "No enterprise deployment is claimed",
        ],
        "evidence_type": "json",
    },
    {
        "id": "private-reviewer-lead-workflow",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/private-reviewer-lead-workflow.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "private_paths_gitignored": True,
            "required_column_count": 11,
            "allowed_status_count": 6,
            "target_metric_count": 6,
        },
        "expected_text": "Private lead rows are not public evidence",
        "expected_texts": [
            "private_contact_label",
            "record_reviewer_outreach_event.py",
            "raw customer data",
            "gitignored private lead paths",
        ],
        "evidence_type": "json",
    },
    {
        "id": "private-reviewer-lead-summary",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/private-reviewer-lead-summary.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "private_source_path": "private/reviewer-leads.csv",
            "resume_outcome_upgraded": False,
            "public_evidence_url_count": 0,
            "accepted_ready_count": 0,
        },
        "expected_text": "Private lead rows are not public evidence",
        "expected_texts": [
            "Private reviewer names",
            "sensitive_columns_excluded",
            "validation_error_count",
            "zero resume outcome upgrades",
        ],
        "evidence_type": "json",
    },
    {
        "id": "outcome-witness-packet",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-witness-packet.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "witness_card_count": 5,
            "target_metric_count": 5,
            "total_required_evidence_fields": 22,
            "resume_outcome_upgraded": False,
        },
        "expected_text": "Witness cards are invitations, not users or feedback",
        "expected_texts": [
            "I give permission for this public issue to be counted as project review evidence.",
            "I confirm this public issue contains no raw customer data",
            "non-owner public GitHub issue passes the evidence gate",
        ],
        "evidence_type": "json",
    },
    {
        "id": "outcome-sprint-plan",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-sprint-plan.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "sprint_day_count": 5,
            "target_metric_count": 5,
            "claimable_resume_metric_count": 0,
            "accepted_issue_count": 0,
        },
        "expected_text": "five-day outcome sprint plan",
        "expected_texts": [
            "real non-owner action",
            "resume claim materializer",
            "Do not add user",
            "zero resume upgrades",
        ],
        "evidence_type": "json",
    },
    {
        "id": "one-click-evidence-links",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/one-click-evidence-links.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "link_count": 4,
            "target_metric_count": 4,
            "claimable_resume_metric_count": 0,
            "accepted_issue_count": 0,
        },
        "expected_text": "Opening a one-click issue link is not evidence by itself.",
        "expected_texts": [
            "I give permission for this public issue to be counted as project review evidence.",
            "I confirm this public issue contains no raw customer data",
            "zero resume upgrades",
        ],
        "evidence_type": "json",
    },
    {
        "id": "pilot-outreach-kit",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-outreach-kit.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "outreach_messages",
        "expected_texts": ["success_metrics", "tracking_rules", "external users"],
        "evidence_type": "json",
    },
    {
        "id": "pilot-program-plan",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-program-plan.json",
        "expected_json": {"project": "Data Quality Agent"},
        "expected_text": "participant_segments",
        "expected_texts": ["success_thresholds", "resume_upgrade_rules", "minimum_feedback_items_before_resume_claim"],
        "evidence_type": "json",
    },
    {
        "id": "pilot-review-tracker",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-review-tracker.json",
        "expected_json": {"project": "Data Quality Agent", "planned_review_count": 3},
        "expected_text": "not_contacted",
        "expected_texts": ["counts_toward_resume", "business_case_feedback_items", "not_claimable_yet"],
        "evidence_type": "json",
    },
    {
        "id": "pilot-conversion-board",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/pilot-conversion-board.json",
        "expected_json": {"project": "Data Quality Agent", "stage_count": 6, "claimable_stage_count": 2},
        "expected_text": "confirmed_external_users",
        "expected_texts": ["validated business impact", "production adoption", "resume_claim_allowed"],
        "evidence_type": "json",
    },
    {
        "id": "resume-outcome-readiness",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/resume-outcome-readiness.json",
        "expected_json": {"project": "Data Quality Agent", "stage_count": 6, "claimable_stage_count": 2},
        "expected_text": "missing_evidence",
        "expected_texts": ["remaining_needed", "confirmed_external_users", "blocked_until_public_evidence"],
        "evidence_type": "json",
    },
    {
        "id": "external-review-evidence-ledger",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/external-review-evidence-ledger.json",
        "expected_json": {
            "project": "Data Quality Agent",
            "entry_count": 0,
            "evidence_requirement_count": 5,
            "self_authored_planning_excluded": True,
        },
        "expected_text": "not_claimable_yet",
        "expected_texts": [
            "demo_feedback",
            "confirmed_run",
            "business_case_review",
            "reproducible_bug",
            "evidence_counts",
            "ignored_planning_labels",
        ],
        "evidence_type": "json",
    },
    {
        "id": "outcome-upgrade-playbook",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/outcome-upgrade-playbook.json",
        "expected_json": {"project": "Data Quality Agent", "upgrade_rule_count": 5, "blocked_upgrade_rule_count": 5},
        "expected_text": "baseline_only",
        "expected_texts": ["github_interest_signal", "business_case_signal", "not_claimable_yet"],
        "evidence_type": "json",
    },
    {
        "id": "reviewer-feedback-packet",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/reviewer-feedback-packet.json",
        "expected_json": {"project": "Data Quality Agent", "reviewer_task_count": 4, "conversion_path_count": 5},
        "expected_text": "collection_ready_not_claimable",
        "expected_texts": ["quick_demo_review", "business_case_review", "confirmed_external_users"],
        "evidence_type": "json",
    },
    {
        "id": "feedback-metrics",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/docs/feedback-metrics.json",
        "expected_json": {"external_feedback_items": 0, "confirmed_external_users": 0, "reproducible_feedback_items": 0},
        "evidence_type": "json",
    },
    {
        "id": "postgres-agent-route",
        "url": "https://raw.githubusercontent.com/sunnnn2005/data-quality-agent/main/app/main.py",
        "expected_text": "/postgres/support-tickets/agent-report",
        "evidence_type": "source",
    },
    {
        "id": "github-release",
        "url": "https://github.com/sunnnn2005/data-quality-agent/releases/tag/v0.3.0",
        "expected_text": "v0.3.0",
        "evidence_type": "release_page",
    },
]


def _current_commit() -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "unknown"
    return completed.stdout.strip() or "unknown"


def _cache_busted_url(url: str, commit: str) -> str:
    if not url.startswith(RAW_GITHUB_HOST):
        return url
    if commit == "unknown":
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}cache_bust={commit}"
    return url.replace("/data-quality-agent/main/", f"/data-quality-agent/{commit}/", 1)


def _fetch(url: str, commit: str | None = None) -> tuple[int, str]:
    request_url = _cache_busted_url(url, commit or _current_commit())
    request = urllib.request.Request(request_url, headers={"User-Agent": "data-quality-agent-public-health/1.0"})
    last_status = 0
    last_body = ""
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                body = response.read().decode("utf-8", errors="replace")
                return int(response.status), body
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            status = int(exc.code)
            last_status = status
            last_body = body
            if status not in {429, 500, 502, 503, 504} or attempt == 2:
                return status, body
        except urllib.error.URLError as exc:
            last_status = 0
            last_body = str(exc)
            if attempt == 2:
                return last_status, last_body
        time.sleep(1 + attempt)
    return last_status, last_body


def _verify_check(check: dict[str, Any]) -> dict[str, Any]:
    status_code, body = _fetch(check["url"])
    result = {
        "id": check["id"],
        "url": check["url"],
        "evidence_type": check["evidence_type"],
        "status_code": status_code,
        "passed": status_code == 200,
    }

    if status_code != 200:
        result["error"] = f"expected 200, got {status_code}"
        return result

    expected_text = check.get("expected_text")
    if expected_text and expected_text not in body:
        result["passed"] = False
        result["error"] = f"missing expected text: {expected_text}"
        return result

    expected_texts = check.get("expected_texts", [])
    for item in expected_texts:
        if item not in body:
            result["passed"] = False
            result["error"] = f"missing expected text: {item}"
            return result

    expected_json = check.get("expected_json")
    if expected_json:
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            result["passed"] = False
            result["error"] = f"invalid json: {exc}"
            return result
        for key, expected_value in expected_json.items():
            actual_value = payload.get(key)
            if actual_value != expected_value:
                result["passed"] = False
                result["error"] = f"{key} expected {expected_value!r}, got {actual_value!r}"
                return result
        minimum_json = check.get("minimum_json", {})
        for key, minimum_value in minimum_json.items():
            actual_value = payload.get(key)
            if not isinstance(actual_value, int | float) or actual_value < minimum_value:
                result["passed"] = False
                result["error"] = f"{key} expected at least {minimum_value!r}, got {actual_value!r}"
                return result
        result["verified_fields"] = sorted(set(expected_json) | set(minimum_json))

    return result


def build_public_evidence_health_payload() -> dict[str, Any]:
    checks = [_verify_check(check) for check in PUBLIC_CHECKS]
    passed_count = sum(1 for check in checks if check["passed"])
    return {
        "generated_by": "scripts/verify_public_evidence_health.py",
        "check_count": len(checks),
        "passed_count": passed_count,
        "failed_count": len(checks) - passed_count,
        "status": "PASS" if passed_count == len(checks) else "FAIL",
        "checks": checks,
    }


def verify_public_evidence_health(payload: dict[str, Any]) -> None:
    if payload["status"] != "PASS":
        failures = [check for check in payload["checks"] if not check["passed"]]
        raise AssertionError(f"public evidence health failed: {failures}")
    if payload["check_count"] < 6:
        raise AssertionError("public evidence health should check demo, artifacts, metrics, and release")


def main() -> None:
    payload = build_public_evidence_health_payload()
    verify_public_evidence_health(payload)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"public evidence health check failed: {exc}", file=sys.stderr)
        raise
