import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTCOME_METRICS_PATH = ROOT / "docs" / "resume-outcome-metrics.json"
UPGRADE_PLAYBOOK_PATH = ROOT / "docs" / "outcome-upgrade-playbook.json"
OUTREACH_STATUS_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
EVIDENCE_GATE_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-outcome-action-checklist.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-outcome-action-checklist.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _next_action(
    *,
    action_id: str,
    title: str,
    target_metric: str,
    current_count: int,
    threshold: int,
    evidence_path: str,
    owner_action: str,
    completion_check: str,
    resulting_resume_line: str,
) -> dict[str, Any]:
    remaining = max(0, threshold - current_count)
    return {
        "id": action_id,
        "title": title,
        "target_metric": target_metric,
        "current_count": current_count,
        "threshold": threshold,
        "remaining_to_claim": remaining,
        "status": "claimable" if remaining == 0 else "next_action_needed",
        "evidence_path": evidence_path,
        "owner_action": owner_action,
        "completion_check": completion_check,
        "resulting_resume_line": resulting_resume_line if remaining == 0 else None,
    }


def build_resume_outcome_action_checklist() -> dict[str, Any]:
    metrics = load_json(OUTCOME_METRICS_PATH)
    playbook = load_json(UPGRADE_PLAYBOOK_PATH)
    outreach = load_json(OUTREACH_STATUS_PATH)
    gate = load_json(EVIDENCE_GATE_PATH)
    counts = {item["metric"]: item["current_count"] for item in metrics["tracked_outcomes"]}
    thresholds = {rule["metric"]: rule["threshold"] for rule in playbook["upgrade_rules"]}

    actions = [
        _next_action(
            action_id="capture_first_real_model_run",
            title="Capture one accepted real-model agent run",
            target_metric="accepted_real_model_runs",
            current_count=counts["accepted_real_model_runs"],
            threshold=1,
            evidence_path="docs/real-model-run-request-pack.md",
            owner_action=(
                "Run the real-model preflight, execute scripts/capture_real_model_run.py with an OpenAI-compatible "
                "model key, verify the final structured report, then submit only redacted telemetry through the "
                "real_model_run_review issue template."
            ),
            completion_check=(
                "One accepted real-model run issue includes provider, model, prompt version, trace id, tool calls, "
                "tokens, estimated cost, latency, verification status, and permission to count."
            ),
            resulting_resume_line=(
                "Captured 1 accepted OpenAI-compatible LLM agent run with redacted tool-call, token, cost, latency, "
                "and verification evidence."
            ),
        ),
        _next_action(
            action_id="send_first_reviewer_request",
            title="Send one prepared reviewer request",
            target_metric="external_feedback_items",
            current_count=counts["external_feedback_items"],
            threshold=1,
            evidence_path="docs/reviewer-outreach-status-board.md",
            owner_action=(
                "Send one message from the reviewer outreach execution pack to a real non-owner reviewer, "
                "then update the status board from not_sent to sent."
            ),
            completion_check="One outreach slot has status sent and no resume outcome is claimed yet.",
            resulting_resume_line="Collected first public reviewer feedback item through a gated GitHub evidence workflow.",
        ),
        _next_action(
            action_id="collect_first_public_run_issue",
            title="Collect one accepted public reviewer run issue",
            target_metric="confirmed_external_users",
            current_count=counts["confirmed_external_users"],
            threshold=thresholds["confirmed_external_users"],
            evidence_path="docs/external-reviewer-evidence-gate.md",
            owner_action=(
                "Ask the reviewer to submit a public issue with path tried, command or URL evidence, observed result, "
                "main feedback, no-private-data checkbox, and permission to count."
            ),
            completion_check="External reviewer evidence gate accepts one non-owner issue.",
            resulting_resume_line="Collected 1 confirmed external reviewer run through a public evidence gate.",
        ),
        _next_action(
            action_id="collect_ai_engineer_review",
            title="Collect one AI Engineer review",
            target_metric="ai_engineer_review_items",
            current_count=counts["ai_engineer_review_items"],
            threshold=1,
            evidence_path="docs/ai-engineer-review-intake.md",
            owner_action=(
                "Ask an AI/ML systems reviewer to inspect the tool-calling loop, PostgreSQL adapter, guardrails, "
                "trace evidence, and AI Engineer readiness document."
            ),
            completion_check="One public ai-engineer-review issue passes the evidence gate.",
            resulting_resume_line="Collected 1 public AI Engineer review with inspected-path evidence.",
        ),
        _next_action(
            action_id="collect_business_case",
            title="Collect one anonymized business-case validation",
            target_metric="business_case_feedback_items",
            current_count=counts["business_case_feedback_items"],
            threshold=thresholds["business_case_feedback_items"],
            evidence_path="docs/business-case-intake.md",
            owner_action=(
                "Ask a data/ops reviewer for an anonymized data-quality scenario and map it to the agent findings, "
                "business impact, fields involved, and useful next action."
            ),
            completion_check="One business-case public issue passes the evidence gate without sensitive data.",
            resulting_resume_line="Validated the agent against 1 anonymized real-world data-quality scenario.",
        ),
        _next_action(
            action_id="earn_first_star",
            title="Earn the first organic GitHub star",
            target_metric="github_stars",
            current_count=counts["github_stars"],
            threshold=1,
            evidence_path="docs/star-growth-kit.md",
            owner_action=(
                "Share the public demo, review page, and README with relevant student builders or data engineers; "
                "do not buy, trade, or request fake stars."
            ),
            completion_check="docs/adoption-metrics.json and the public GitHub stargazers page show at least 1 star.",
            resulting_resume_line="Earned the first organic GitHub star for a public LLM data-quality agent.",
        ),
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_resume_outcome_action_checklist.py",
        "purpose": "Turn blocked resume outcome claims into the shortest honest next actions with public evidence checks.",
        "tracked_action_count": len(actions),
        "next_action_needed_count": sum(1 for action in actions if action["status"] == "next_action_needed"),
        "claimable_action_count": sum(1 for action in actions if action["status"] == "claimable"),
        "evaluated_public_issue_count": gate["evaluated_issue_count"],
        "accepted_public_issue_count": gate["accepted_issue_count"],
        "outreach_slot_count": outreach["outreach_slot_count"],
        "not_sent_outreach_count": outreach["not_sent_count"],
        "actions": actions,
        "resume_safe_summary": (
            f"Published a CI-verified action checklist with {len(actions)} concrete next actions, "
            f"{gate['evaluated_issue_count']} evaluated public GitHub issues, "
            f"{gate['accepted_issue_count']} accepted public evidence items, and "
            f"{outreach['not_sent_count']} reviewer outreach slots still not sent."
        ),
        "not_claimed": [
            "The checklist does not claim users, feedback, business impact, or stars.",
            "A resume line becomes claimable only after the referenced public evidence check passes.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {id} | {target_metric} | {current_count} | {threshold} | {remaining_to_claim} | `{status}` | {evidence} |".format(
            id=action["id"],
            target_metric=action["target_metric"],
            current_count=action["current_count"],
            threshold=action["threshold"],
            remaining_to_claim=action["remaining_to_claim"],
            status=action["status"],
            evidence=f"[evidence]({action['evidence_path']})",
        )
        for action in payload["actions"]
    )
    action_items = "\n".join(
        f"### {action['title']}\n\n"
        f"- Owner action: {action['owner_action']}\n"
        f"- Completion check: {action['completion_check']}\n"
        f"- Resume line after proof: {action['resulting_resume_line'] or 'Not claimable yet'}\n"
        for action in payload["actions"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Resume Outcome Action Checklist

This generated checklist shows the shortest honest path from blocked outcome claims to resume-safe proof.

## Summary

| Metric | Value |
| --- | ---: |
| Tracked actions | {payload["tracked_action_count"]} |
| Next actions needed | {payload["next_action_needed_count"]} |
| Claimable actions | {payload["claimable_action_count"]} |
| Evaluated public issues | {payload["evaluated_public_issue_count"]} |
| Accepted public evidence | {payload["accepted_public_issue_count"]} |
| Outreach slots | {payload["outreach_slot_count"]} |
| Not-sent outreach slots | {payload["not_sent_outreach_count"]} |

## Action Table

| Action | Target Metric | Current | Threshold | Remaining | Status | Evidence |
| --- | --- | ---: | ---: | ---: | --- | --- |
{rows}

## Action Details

{action_items}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_resume_outcome_action_checklist(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["tracked_action_count"] != 6:
        raise AssertionError("resume outcome action checklist must track six next actions")
    if payload["claimable_action_count"] != 0:
        raise AssertionError("resume outcome action checklist must not mark zero-count actions as claimable")
    if payload["next_action_needed_count"] != 6:
        raise AssertionError("resume outcome action checklist must keep six next actions open")
    if payload["accepted_public_issue_count"] != 0:
        raise AssertionError("resume outcome action checklist must not claim accepted public evidence yet")
    if payload["outreach_slot_count"] != 9 or payload["not_sent_outreach_count"] != 9:
        raise AssertionError("resume outcome action checklist must preserve the not-sent outreach baseline")
    required = {
        "capture_first_real_model_run",
        "send_first_reviewer_request",
        "collect_first_public_run_issue",
        "collect_ai_engineer_review",
        "collect_business_case",
        "earn_first_star",
    }
    if {action["id"] for action in payload["actions"]} != required:
        raise AssertionError("resume outcome action checklist has the wrong action set")
    for action in payload["actions"]:
        if action["remaining_to_claim"] < 1:
            raise AssertionError(f"{action['id']} must still need proof")
        if not action["evidence_path"].startswith("docs/"):
            raise AssertionError(f"{action['id']} must point to a public evidence document")
    return {
        "resume_outcome_action_checklist_verified": True,
        "tracked_action_count": payload["tracked_action_count"],
        "next_action_needed_count": payload["next_action_needed_count"],
    }


def main() -> None:
    payload = build_resume_outcome_action_checklist()
    verify_resume_outcome_action_checklist(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
