import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACCEPTED_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
OUTCOME_LEDGER_PATH = ROOT / "docs" / "resume-outcome-evidence-ledger.json"
PILOT_CRM_PATH = ROOT / "docs" / "pilot-reviewer-crm.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-claim-materializer.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-claim-materializer.md"


FUTURE_BULLET_TEMPLATES = {
    "confirmed_external_users": (
        "Validated the data-quality LLM agent with {count} external reviewer(s) who inspected "
        "the public demo, local run path, or repository evidence."
    ),
    "external_feedback_items": (
        "Incorporated {count} accepted external feedback item(s) into the data-quality agent "
        "roadmap and evidence gate."
    ),
    "reproducible_feedback_items": (
        "Collected {count} reproducible external run report(s) covering the FastAPI, Docker, "
        "CSV, or read-only PostgreSQL data-quality workflow."
    ),
    "business_case_feedback_items": (
        "Reviewed {count} anonymized business-data quality case(s) and converted feedback into "
        "evidence-backed remediation guidance."
    ),
    "ai_engineer_review_items": (
        "Collected {count} AI Engineer review item(s) covering tool calling, structured outputs, "
        "guardrails, traceability, and model fallback behavior."
    ),
    "accepted_real_model_runs": (
        "Captured {count} accepted real-model LLM agent run(s) with redacted tool calls, "
        "latency, token, cost, retry, and evidence-verification telemetry."
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_resume_claim_materializer() -> dict[str, Any]:
    accepted = load_json(ACCEPTED_ROLLUP_PATH)
    ledger = load_json(OUTCOME_LEDGER_PATH)
    crm = load_json(PILOT_CRM_PATH)
    accepted_counts = accepted.get("accepted_counts", {})

    safe_current_bullets = [
        {
            "status": "claimable_now",
            "source_signal": item["signal"],
            "proof_type": item["proof_type"],
            "evidence_url": item["evidence_url"],
            "bullet": item["resume_safe_line"],
        }
        for item in ledger.get("claimable_now", [])
    ]

    future_templates = []
    materialized_outcome_bullets = []
    for blocked in ledger.get("blocked_until_evidence", []):
        metric = blocked["metric"]
        current_count = int(accepted_counts.get(metric, 0))
        template = FUTURE_BULLET_TEMPLATES[metric]
        materialized = current_count > 0
        rendered = template.format(count=current_count) if materialized else None
        if rendered:
            materialized_outcome_bullets.append(
                {
                    "metric": metric,
                    "status": "materialized_from_accepted_public_evidence",
                    "accepted_count": current_count,
                    "bullet": rendered,
                    "evidence_requirement": blocked["required_public_evidence"],
                }
            )

        future_templates.append(
            {
                "metric": metric,
                "status": "blocked_until_accepted_public_evidence" if not materialized else "materialized",
                "current_count": current_count,
                "materialized": materialized,
                "template": template,
                "rendered_bullet": rendered,
                "blocked_reason": blocked["blocked_reason"] if not materialized else None,
                "required_public_evidence": blocked["required_public_evidence"],
            }
        )

    payload = {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_resume_claim_materializer.py",
        "purpose": (
            "Convert accepted public outcome evidence into exact resume bullets while keeping "
            "unverified users, feedback, business impact, AI review, real-model, and GitHub-star claims blocked."
        ),
        "safe_current_bullets": safe_current_bullets,
        "safe_current_bullet_count": len(safe_current_bullets),
        "materialized_outcome_bullets": materialized_outcome_bullets,
        "materialized_claim_count": len(materialized_outcome_bullets),
        "future_bullet_templates": future_templates,
        "future_template_count": len(future_templates),
        "blocked_claim_count": sum(1 for item in future_templates if not item["materialized"]),
        "accepted_public_evidence_count": int(ledger.get("accepted_public_evidence_count", 0)),
        "recorded_outreach_event_count": int(crm.get("recorded_outreach_event_count", 0)),
        "resume_upgrade_count": int(ledger.get("resume_upgrade_count", 0)),
        "reviewer_lead_count": int(crm.get("lead_count", 0)),
        "target_metric_count": int(crm.get("priority_metric_count", 0)),
        "not_claimed": [
            "No external users are claimed.",
            "No customer feedback is claimed.",
            "No enterprise deployment is claimed.",
            "No GitHub-star growth is claimed.",
            "No accepted real-model benchmark result is claimed.",
        ],
        "resume_safe_summary": (
            "Published a resume claim materializer with "
            f"{len(safe_current_bullets)} current claimable engineering bullets, "
            f"{len(materialized_outcome_bullets)} materialized external outcome bullets, "
            f"{len(future_templates)} blocked future outcome templates, and "
            f"{int(ledger.get('accepted_public_evidence_count', 0))} accepted public evidence items."
        ),
    }
    verify_resume_claim_materializer(payload)
    return payload


def verify_resume_claim_materializer(payload: dict[str, Any]) -> None:
    if payload["safe_current_bullet_count"] != 4:
        raise AssertionError("expected 4 current claimable engineering bullets")
    if payload["future_template_count"] != 6:
        raise AssertionError("expected 6 blocked future outcome templates")
    if payload["materialized_claim_count"] != 0:
        raise AssertionError("must not materialize external outcome bullets without accepted evidence")
    if payload["accepted_public_evidence_count"] != 0:
        raise AssertionError("accepted public evidence baseline must remain zero")
    if payload["resume_upgrade_count"] != 0:
        raise AssertionError("resume upgrade baseline must remain zero")

    metrics = {item["metric"] for item in payload["future_bullet_templates"]}
    required_metrics = set(FUTURE_BULLET_TEMPLATES)
    if metrics != required_metrics:
        raise AssertionError(f"future template metric mismatch: {sorted(metrics)}")
    for item in payload["future_bullet_templates"]:
        if item["current_count"] == 0 and item["materialized"]:
            raise AssertionError(f"zero-count metric must remain blocked: {item['metric']}")
        if item["current_count"] == 0 and item["rendered_bullet"] is not None:
            raise AssertionError(f"zero-count metric must not render a resume bullet: {item['metric']}")

    joined = json.dumps(payload, sort_keys=True)
    required_text = [
        "exact resume bullets",
        "confirmed_external_users",
        "ai_engineer_review_items",
        "accepted_real_model_runs",
        "No enterprise deployment is claimed.",
    ]
    for text in required_text:
        if text not in joined:
            raise AssertionError(f"missing required materializer text: {text}")


def write_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Resume Claim Materializer",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Current claimable engineering bullets | {payload['safe_current_bullet_count']} |",
        f"| Materialized Outcome Bullets | {payload['materialized_claim_count']} |",
        f"| Blocked Future Templates | {payload['future_template_count']} |",
        f"| Accepted public evidence | {payload['accepted_public_evidence_count']} |",
        f"| Reviewer leads queued | {payload['reviewer_lead_count']} |",
        "",
        "## Current Claimable Bullets",
        "",
    ]
    for item in payload["safe_current_bullets"]:
        lines.append(f"- {item['bullet']} ([evidence]({item['evidence_url']}))")

    lines.extend(["", "## Materialized Outcome Bullets", ""])
    if payload["materialized_outcome_bullets"]:
        for item in payload["materialized_outcome_bullets"]:
            lines.append(f"- {item['bullet']}")
    else:
        lines.append("- None yet. Accepted public evidence count is 0.")

    lines.extend(["", "## Blocked Future Templates", ""])
    for item in payload["future_bullet_templates"]:
        lines.append(f"- `{item['metric']}`: {item['template']}")
        lines.append(f"  - Status: {item['status']}")
        lines.append(f"  - Required evidence: {item['required_public_evidence']}")

    lines.extend(["", "## Not Claimed", ""])
    for item in payload["not_claimed"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Resume-Safe Summary", "", payload["resume_safe_summary"], ""])
    return "\n".join(lines)


def main() -> None:
    payload = build_resume_claim_materializer()
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(write_markdown(payload))


if __name__ == "__main__":
    main()
