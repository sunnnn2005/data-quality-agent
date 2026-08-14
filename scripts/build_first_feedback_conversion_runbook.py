import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REVIEW_CARD_PATH = ROOT / "docs" / "first-external-review-card.json"
SEND_QUEUE_PATH = ROOT / "docs" / "reviewer-send-queue.json"
CHECKLIST_PATH = ROOT / "docs" / "evidence-acceptance-checklist.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "first-feedback-conversion-runbook.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-feedback-conversion-runbook.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_first_feedback_conversion_runbook() -> dict[str, Any]:
    review_card = load_json(REVIEW_CARD_PATH)
    send_queue = load_json(SEND_QUEUE_PATH)
    checklist = load_json(CHECKLIST_PATH)
    next_sends = send_queue["next_sends"][:5]
    acceptance_by_metric = {
        item["metric"]: item for item in checklist["acceptance_items"]
    }

    sprint_steps = [
        {
            "step": 1,
            "name": "Send the first AI Engineer review ask",
            "owner_action": next_sends[0]["copy_ready_message"],
            "evidence_record_command": (
                'python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent '
                '--reviewer-contact "<private-label>" --channel-used "<LinkedIn|email|Discord>" '
                '--note "Sent first external review card; no public evidence yet."'
            ),
            "counts_as_resume_outcome": False,
            "why": "Sending a message creates outreach trace only; it does not prove feedback, use, or review quality.",
        },
        {
            "step": 2,
            "name": "Ask the reviewer to choose one public path",
            "owner_action": review_card["public_url"],
            "evidence_record_command": None,
            "counts_as_resume_outcome": False,
            "why": "Opening the card is not enough; the reviewer must submit public, permissioned evidence.",
        },
        {
            "step": 3,
            "name": "Collect the first public GitHub issue",
            "owner_action": next_sends[0]["submission_url"],
            "evidence_record_command": None,
            "counts_as_resume_outcome": False,
            "why": "A submitted issue still needs to pass the evidence gate before it upgrades a metric.",
        },
        {
            "step": 4,
            "name": "Run the evidence gate and refresh outcome artifacts",
            "owner_action": (
                "python scripts/build_external_reviewer_evidence_gate.py && "
                "python scripts/build_accepted_evidence_rollup.py && "
                "python scripts/build_resume_outcome_metrics.py && "
                "python scripts/build_resume_claim_materializer.py"
            ),
            "evidence_record_command": None,
            "counts_as_resume_outcome": False,
            "why": "Deterministic scripts decide whether the public issue is countable; the owner does not manually inflate metrics.",
        },
        {
            "step": 5,
            "name": "Use only materialized resume wording",
            "owner_action": "docs/resume-claim-materializer.md",
            "evidence_record_command": None,
            "counts_as_resume_outcome": True,
            "why": "The final resume line is allowed only after the materializer sees accepted public evidence.",
        },
    ]

    first_metric = next_sends[0]["target_metric"]
    first_gate = acceptance_by_metric[first_metric]
    unlocks = [
        {
            "metric": first_metric,
            "current_count": review_card["current_counts"][first_metric],
            "required_count": first_gate["required_count"],
            "submission_url": next_sends[0]["submission_url"],
            "future_resume_line": first_gate["future_resume_line"],
            "evidence_gate": first_gate["evidence_gate"],
        },
        {
            "metric": "confirmed_external_users",
            "current_count": review_card["current_counts"]["confirmed_external_users"],
            "required_count": acceptance_by_metric["confirmed_external_users"]["required_count"],
            "submission_url": review_card["primary_routes"][1]["submission_url"],
            "future_resume_line": acceptance_by_metric["confirmed_external_users"]["future_resume_line"],
            "evidence_gate": acceptance_by_metric["confirmed_external_users"]["evidence_gate"],
        },
        {
            "metric": "external_feedback_items",
            "current_count": review_card["current_counts"]["external_feedback_items"],
            "required_count": acceptance_by_metric["external_feedback_items"]["required_count"],
            "submission_url": review_card["primary_routes"][2]["submission_url"],
            "future_resume_line": acceptance_by_metric["external_feedback_items"]["future_resume_line"],
            "evidence_gate": acceptance_by_metric["external_feedback_items"]["evidence_gate"],
        },
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_feedback_conversion_runbook.py",
        "purpose": (
            "Convert the first real reviewer contact into a public evidence item that can unlock stronger resume "
            "outcome wording only after the evidence gate accepts it."
        ),
        "review_card_url": review_card["public_url"],
        "sprint_step_count": len(sprint_steps),
        "sprint_steps": sprint_steps,
        "first_send": {
            "slot_id": next_sends[0]["slot_id"],
            "target_metric": next_sends[0]["target_metric"],
            "recommended_channel": next_sends[0]["recommended_channel"],
            "reviewer_profile": next_sends[0]["reviewer_profile"],
            "copy_ready_message": next_sends[0]["copy_ready_message"],
        },
        "first_unlock_options": unlocks,
        "current_counts": review_card["current_counts"],
        "resume_safe_summary": (
            "Published a first-feedback conversion runbook that turns one reviewer message into a 5-step evidence "
            "workflow, 3 possible public metric unlocks, and zero resume upgrades until a non-owner issue passes the gate."
        ),
        "not_claimed": [
            "message sent",
            "accepted review",
            "confirmed external user",
            "external feedback",
            "GitHub stars",
            "production adoption",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    steps = "\n\n".join(
        (
            f"### {item['step']}. {item['name']}\n\n"
            f"- Action: {item['owner_action']}\n"
            f"- Counts as resume outcome: `{item['counts_as_resume_outcome']}`\n"
            f"- Why: {item['why']}\n"
            + (
                f"- Record command: `{item['evidence_record_command']}`\n"
                if item["evidence_record_command"]
                else ""
            )
        )
        for item in payload["sprint_steps"]
    )
    unlock_rows = "\n".join(
        "| {metric} | {current_count} | {required_count} | [submit]({submission_url}) | {future_resume_line} |".format(
            **item
        )
        for item in payload["first_unlock_options"]
    )
    counts = "\n".join(
        f"| `{metric}` | {count} |" for metric, count in payload["current_counts"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# First Feedback Conversion Runbook

{payload["purpose"]}

## Shareable Review Card

[{payload["review_card_url"]}]({payload["review_card_url"]})

## First Send

- Slot: `{payload["first_send"]["slot_id"]}`
- Target metric: `{payload["first_send"]["target_metric"]}`
- Reviewer profile: {payload["first_send"]["reviewer_profile"]}
- Channel: {payload["first_send"]["recommended_channel"]}

```text
{payload["first_send"]["copy_ready_message"]}
```

## Five-Step Conversion Workflow

{steps}

## First Unlock Options

| Metric | Current | Required | Submission | Future Resume Line |
| --- | ---: | ---: | --- | --- |
{unlock_rows}

## Current Counts

| Metric | Current Count |
| --- | ---: |
{counts}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_first_feedback_conversion_runbook(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["sprint_step_count"] != 5:
        raise AssertionError("first feedback conversion runbook must define five execution steps")
    if payload["first_send"]["target_metric"] != "ai_engineer_review_items":
        raise AssertionError("first send should prioritize AI Engineer review evidence")
    if any(value != 0 for value in payload["current_counts"].values()):
        raise AssertionError("first feedback conversion runbook must preserve zero current outcome counts")
    if len(payload["first_unlock_options"]) != 3:
        raise AssertionError("first feedback conversion runbook must expose three fast unlock options")
    if payload["sprint_steps"][-1]["counts_as_resume_outcome"] is not True:
        raise AssertionError("only the final materialized wording step can count as a resume outcome")
    if any(step["counts_as_resume_outcome"] for step in payload["sprint_steps"][:-1]):
        raise AssertionError("pre-gate outreach and submitted issues must not count as resume outcomes")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in ("non-owner issue passes the gate", "record_reviewer_outreach_event.py", "zero resume upgrades"):
        if phrase not in joined:
            raise AssertionError(f"first feedback conversion runbook missing boundary phrase: {phrase}")
    return {
        "first_feedback_conversion_runbook_verified": True,
        "sprint_step_count": payload["sprint_step_count"],
        "unlock_option_count": len(payload["first_unlock_options"]),
    }


def main() -> None:
    payload = build_first_feedback_conversion_runbook()
    verify_first_feedback_conversion_runbook(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps({"status": "ok", "output": str(OUTPUT_JSON_PATH)}))


if __name__ == "__main__":
    main()
