import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTREACH_STATUS_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
SEND_QUEUE_PATH = ROOT / "docs" / "reviewer-send-queue.json"
OUTCOME_LEDGER_PATH = ROOT / "docs" / "resume-outcome-evidence-ledger.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "pilot-reviewer-crm.json"
OUTPUT_MD_PATH = ROOT / "docs" / "pilot-reviewer-crm.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _priority_for_metric(metric: str) -> int:
    priority = {
        "ai_engineer_review_items": 1,
        "confirmed_external_users": 2,
        "reproducible_feedback_items": 3,
        "business_case_feedback_items": 4,
        "external_feedback_items": 5,
    }
    return priority.get(metric, 9)


def _weekly_goal(metric: str) -> str:
    goals = {
        "ai_engineer_review_items": "Get one technical reviewer to inspect the LLM agent loop and submit an AI Engineer review issue.",
        "confirmed_external_users": "Get one non-owner reviewer to open the demo or run the repo and confirm the path publicly.",
        "reproducible_feedback_items": "Get one reviewer to run the Docker/local path and paste command or URL evidence.",
        "business_case_feedback_items": "Get one data or operations reviewer to map the demo to a real anonymized workflow.",
        "external_feedback_items": "Collect concrete product feedback from a peer reviewer without counting private replies.",
    }
    return goals.get(metric, "Collect public reviewer evidence.")


def build_pilot_reviewer_crm() -> dict[str, Any]:
    outreach_status = load_json(OUTREACH_STATUS_PATH)
    send_queue = load_json(SEND_QUEUE_PATH)
    outcome_ledger = load_json(OUTCOME_LEDGER_PATH)
    queue_by_metric = {item["target_metric"]: item for item in send_queue["next_sends"]}

    leads = []
    for slot in outreach_status["outreach_slots"]:
        metric = slot["counts_toward"]
        queued = queue_by_metric.get(metric, {})
        priority = _priority_for_metric(metric)
        leads.append(
            {
                "lead_id": f"pilot_{slot['slot_id']}",
                "slot_id": slot["slot_id"],
                "reviewer_segment": slot["reviewer_segment"],
                "target_metric": metric,
                "priority": priority,
                "status": slot["status"],
                "resume_countable_now": False,
                "recommended_channel": queued.get("recommended_channel", slot["channel"]),
                "weekly_goal": _weekly_goal(metric),
                "submission_url": queued.get("submission_url"),
                "review_context_url": queued.get("entry_url"),
                "tracking_issue_url": queued.get("public_issue_url"),
                "next_action": slot["next_action"],
                "record_sent_command": queued.get("record_sent_command")
                or (
                    "python scripts/record_reviewer_outreach_event.py "
                    f"--slot-id {slot['slot_id']} --status sent "
                    "--reviewer-contact \"<real reviewer>\" "
                    f"--channel-used {slot['channel']}"
                ),
                "upgrade_gate": (
                    "Only upgrade after a non-owner public GitHub issue includes permission to count, "
                    "no private data, and enough evidence for the external reviewer gate."
                ),
            }
        )

    leads.sort(key=lambda item: (item["priority"], item["slot_id"]))
    target_counts: dict[str, int] = {}
    for lead in leads:
        target_counts[lead["target_metric"]] = target_counts.get(lead["target_metric"], 0) + 1

    sprint_plan = [
        {
            "week": 1,
            "goal": "Send the top AI Engineer review ask and one confirmed-user ask.",
            "lead_ids": [lead["lead_id"] for lead in leads[:2]],
            "success_metric": "2 real sends recorded, 0 resume outcomes upgraded until public evidence exists.",
        },
        {
            "week": 2,
            "goal": "Follow up on week 1 and send reproducible-run plus business-case asks.",
            "lead_ids": [lead["lead_id"] for lead in leads[2:5]],
            "success_metric": "At least 1 public issue submitted or clear rejection reason recorded.",
        },
        {
            "week": 3,
            "goal": "Collect remaining peer feedback and route public submissions through the evidence gate.",
            "lead_ids": [lead["lead_id"] for lead in leads[5:]],
            "success_metric": "Accepted evidence rollup remains the source of truth for any resume upgrade.",
        },
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_pilot_reviewer_crm.py",
        "purpose": (
            "Turn outcome evidence collection into an executable reviewer CRM without fabricating reviewer names, "
            "private replies, users, feedback, or GitHub stars."
        ),
        "lead_count": len(leads),
        "priority_metric_count": len(target_counts),
        "week_count": len(sprint_plan),
        "recorded_outreach_event_count": outreach_status["recorded_event_count"],
        "accepted_public_evidence_count": outcome_ledger["accepted_public_evidence_count"],
        "resume_upgrade_count": outcome_ledger["resume_upgrade_count"],
        "target_counts": target_counts,
        "leads": leads,
        "sprint_plan": sprint_plan,
        "operating_rules": [
            "Do not enter private names into public files unless the reviewer explicitly wants public credit.",
            "Do not count sent messages, private replies, or self-authored issues as outcome evidence.",
            "Do not buy, trade, or pressure for GitHub stars.",
            "Every upgraded resume claim must point to accepted public evidence.",
            "Keep raw business rows, customer names, emails, phone numbers, tokens, and addresses out of public issues.",
        ],
        "not_claimed": [
            "No reviewer has been contacted until a real event is recorded.",
            "No external user, feedback, business validation, AI review, or star-growth outcome is claimed.",
            "No enterprise deployment is claimed.",
        ],
        "resume_safe_summary": (
            f"Published a pilot reviewer CRM with {len(leads)} reviewer leads, {len(target_counts)} target outcome metrics, "
            f"a {len(sprint_plan)}-week evidence collection plan, {outreach_status['recorded_event_count']} recorded sends, "
            f"and {outcome_ledger['accepted_public_evidence_count']} accepted public evidence items."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lead_rows = "\n".join(
        f"| {lead['lead_id']} | {lead['reviewer_segment']} | `{lead['target_metric']}` | {lead['priority']} | `{lead['status']}` | {lead['weekly_goal']} |"
        for lead in payload["leads"]
    )
    sprint_rows = "\n".join(
        f"| Week {item['week']} | {item['goal']} | {', '.join(item['lead_ids'])} | {item['success_metric']} |"
        for item in payload["sprint_plan"]
    )
    target_rows = "\n".join(
        f"| {metric} | {count} |" for metric, count in sorted(payload["target_counts"].items())
    )
    rules = "\n".join(f"- {rule}" for rule in payload["operating_rules"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    commands = "\n".join(
        f"- `{lead['record_sent_command']}`" for lead in payload["leads"][:3]
    )
    return f"""# Pilot Reviewer CRM

This generated CRM turns the outcome-evidence goal into concrete reviewer leads and weekly execution.

## Purpose

{payload["purpose"]}

## Target Counts

| Metric | Lead Count |
| --- | ---: |
{target_rows}

## Reviewer Leads

| Lead | Reviewer Segment | Target Metric | Priority | Status | Weekly Goal |
| --- | --- | --- | ---: | --- | --- |
{lead_rows}

## Three-Week Sprint

| Week | Goal | Lead IDs | Success Metric |
| --- | --- | --- | --- |
{sprint_rows}

## First Commands To Record Real Sends

{commands}

## Operating Rules

{rules}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_pilot_reviewer_crm(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["lead_count"] != 9:
        raise AssertionError("pilot reviewer CRM must expose nine reviewer leads")
    if payload["priority_metric_count"] != 6:
        raise AssertionError("pilot reviewer CRM must cover six target outcome metrics")
    if payload["week_count"] != 3:
        raise AssertionError("pilot reviewer CRM must include a three-week sprint")
    if payload["recorded_outreach_event_count"] != 0:
        raise AssertionError("pilot reviewer CRM must not fabricate sent outreach")
    if payload["accepted_public_evidence_count"] != 0:
        raise AssertionError("pilot reviewer CRM must not fabricate accepted public evidence")
    if payload["resume_upgrade_count"] != 0:
        raise AssertionError("pilot reviewer CRM must not upgrade resume outcomes")
    if payload["leads"][0]["target_metric"] != "ai_engineer_review_items":
        raise AssertionError("AI Engineer review lead should be the first priority")
    for required in (
        "ai_engineer_review_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "external_feedback_items",
    ):
        if required not in payload["target_counts"]:
            raise AssertionError(f"pilot reviewer CRM missing target metric {required}")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("do not buy", "private", "accepted public evidence", "enterprise deployment"):
        if required not in joined:
            raise AssertionError(f"pilot reviewer CRM missing boundary {required}")
    return {
        "pilot_reviewer_crm_verified": True,
        "lead_count": payload["lead_count"],
        "priority_metric_count": payload["priority_metric_count"],
        "accepted_public_evidence_count": payload["accepted_public_evidence_count"],
    }


def main() -> None:
    payload = build_pilot_reviewer_crm()
    verify_pilot_reviewer_crm(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
