import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_reviewer_send_queue import build_reviewer_send_queue
from scripts.build_reviewer_outreach_status_board import build_reviewer_outreach_status_board


OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-outcome-sprint-calendar.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-outcome-sprint-calendar.md"


DAY_BY_METRIC = {
    "ai_engineer_review_items": {
        "day": 1,
        "sprint_action": "Ask one AI/ML systems reviewer to inspect the agent loop, guardrails, traces, and AI Engineer readiness evidence.",
        "resume_unlock": "first public AI Engineer review of tool calling, structured output, guardrails, and evidence quality",
    },
    "confirmed_external_users": {
        "day": 2,
        "sprint_action": "Ask one peer to open the public demo or local quickstart and submit observed-result evidence.",
        "resume_unlock": "first confirmed non-owner external run of the public demo or repo",
    },
    "reproducible_feedback_items": {
        "day": 3,
        "sprint_action": "Ask one developer to run the Docker/local replay path and report whether the result is reproducible.",
        "resume_unlock": "first reproducible local replay from a non-owner reviewer",
    },
    "business_case_feedback_items": {
        "day": 4,
        "sprint_action": "Ask one data/ops reviewer for an anonymized real data-quality scenario and business impact mapping.",
        "resume_unlock": "first anonymized business-case validation tied to a real workflow",
    },
    "external_feedback_items": {
        "day": 5,
        "sprint_action": "Ask one peer to leave product or README feedback after trying the demo.",
        "resume_unlock": "first specific external product feedback item",
    },
}


def _completion_criteria(item: dict[str, Any]) -> list[str]:
    return [
        f"Message sent through {item['recommended_channel']}.",
        "Reviewer submits their own public GitHub issue or response URL.",
        "Issue contains no private data, secrets, raw production rows, or customer identifiers.",
        "Issue includes explicit permission to count the evidence publicly.",
        "External reviewer evidence gate marks the issue accepted before any resume metric changes.",
    ]


def build_reviewer_outcome_sprint_calendar() -> dict[str, Any]:
    send_queue = build_reviewer_send_queue()
    status_board = build_reviewer_outreach_status_board()
    status_by_metric = {
        unlock["metric"]: unlock for unlock in status_board["next_resume_unlocks"]
    }

    day_cards = []
    for item in send_queue["next_sends"]:
        metric = item["target_metric"]
        config = DAY_BY_METRIC[metric]
        unlock = status_by_metric[metric]
        day_cards.append(
            {
                "day": config["day"],
                "slot_id": item["slot_id"],
                "target_metric": metric,
                "reviewer_profile": item["reviewer_profile"],
                "recommended_channel": item["recommended_channel"],
                "sprint_action": config["sprint_action"],
                "copy_ready_message": item["copy_ready_message"],
                "follow_up_message": item["copy_ready_follow_up"],
                "submission_url": item["submission_url"],
                "tracking_issue_url": item["public_issue_url"],
                "completion_criteria": _completion_criteria(item),
                "remaining_needed": unlock["remaining_needed"],
                "resume_unlock_after_accepted_evidence": config["resume_unlock"],
                "claimable_now": False,
            }
        )

    day_cards = sorted(day_cards, key=lambda card: card["day"])
    follow_up_cards = [
        {
            "day": 6,
            "action": "Follow up with any reviewer who was contacted but has not submitted a public issue.",
            "counts_as_resume_evidence": False,
            "success_condition": "At least one reviewer submits a public issue URL; still not claimable until the gate accepts it.",
        },
        {
            "day": 7,
            "action": "Run the external reviewer evidence gate and update resume outcome metrics only for accepted public issues.",
            "counts_as_resume_evidence": False,
            "success_condition": "Accepted evidence count is greater than zero; otherwise keep all user/feedback/business-impact claims blocked.",
        },
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_outcome_sprint_calendar.py",
        "purpose": (
            "Turn the reviewer send queue into a seven-day execution calendar that can produce real public evidence "
            "for resume outcomes without counting outreach attempts as users or feedback."
        ),
        "sprint_day_count": 7,
        "send_day_count": len(day_cards),
        "follow_up_day_count": len(follow_up_cards),
        "target_metric_count": len({card["target_metric"] for card in day_cards}),
        "public_submission_path_count": len({card["submission_url"] for card in day_cards}),
        "completion_criteria_count": sum(len(card["completion_criteria"]) for card in day_cards),
        "current_sent_count": status_board["sent_count"],
        "current_public_issue_submitted_count": status_board["public_issue_submitted_count"],
        "current_accepted_evidence_count": status_board["accepted_evidence_count"],
        "resume_claim_allowed_now": False,
        "day_cards": day_cards,
        "follow_up_cards": follow_up_cards,
        "execution_commands": [
            "python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact '<name-or-handle>' --channel-used '<LinkedIn|email|Discord>'",
            "python scripts/build_external_reviewer_evidence_gate.py",
            "python scripts/verify_outcome_evidence.py",
        ],
        "not_claimed": [
            "The calendar itself does not count as users, feedback, business impact, stars, or accepted model runs.",
            "Sent outreach and private replies are tracked but not resume-countable.",
            "Only non-owner public GitHub issues accepted by the evidence gate can unlock outcome wording.",
        ],
        "resume_safe_summary": (
            "Published a seven-day reviewer outcome sprint calendar with 5 prioritized sends, 5 target metrics, "
            "25 completion criteria, 0 sent messages, 0 accepted evidence, and no upgraded resume claims."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| Day {day} | `{target_metric}` | {reviewer_profile} | [{slot_id}]({tracking_issue_url}) | [Submit]({submission_url}) | {remaining_needed} |".format(
            **card
        )
        for card in payload["day_cards"]
    )
    detail_sections = []
    for card in payload["day_cards"]:
        criteria = "\n".join(f"- {item}" for item in card["completion_criteria"])
        detail_sections.append(
            f"""### Day {card["day"]}: {card["target_metric"]}

- Slot: `{card["slot_id"]}`
- Sprint action: {card["sprint_action"]}
- Resume unlock after accepted evidence: {card["resume_unlock_after_accepted_evidence"]}
- Recommended channel: {card["recommended_channel"]}

Copy-ready message:

```text
{card["copy_ready_message"]}
```

Completion criteria:
{criteria}
"""
        )
    follow_ups = "\n".join(
        f"- Day {item['day']}: {item['action']} Success condition: {item['success_condition']}"
        for item in payload["follow_up_cards"]
    )
    commands = "\n".join(f"- `{command}`" for command in payload["execution_commands"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Reviewer Outcome Sprint Calendar

This generated calendar converts planned outreach into a one-week push for real, public outcome evidence.

## Summary

| Metric | Value |
| --- | ---: |
| Sprint days | {payload["sprint_day_count"]} |
| Send days | {payload["send_day_count"]} |
| Follow-up days | {payload["follow_up_day_count"]} |
| Target metrics | {payload["target_metric_count"]} |
| Completion criteria | {payload["completion_criteria_count"]} |
| Current sent messages | {payload["current_sent_count"]} |
| Current accepted evidence | {payload["current_accepted_evidence_count"]} |
| Resume claim allowed now | {payload["resume_claim_allowed_now"]} |

## Send Calendar

| Day | Target Metric | Reviewer Profile | Tracking Slot | Submission | Remaining Needed |
| --- | --- | --- | --- | --- | ---: |
{rows}

## Daily Details

{chr(10).join(detail_sections)}

## Follow-Up Days

{follow_ups}

## Execution Commands

{commands}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_reviewer_outcome_sprint_calendar(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["sprint_day_count"] != 7:
        raise AssertionError("reviewer outcome sprint calendar must cover seven days")
    if payload["send_day_count"] != 5:
        raise AssertionError("reviewer outcome sprint calendar must include five prioritized sends")
    if payload["follow_up_day_count"] != 2:
        raise AssertionError("reviewer outcome sprint calendar must include two follow-up/gate days")
    if payload["target_metric_count"] != 5:
        raise AssertionError("reviewer outcome sprint calendar must cover five target metrics")
    if payload["completion_criteria_count"] != 25:
        raise AssertionError("each send day must include five completion criteria")
    if payload["resume_claim_allowed_now"] is not False:
        raise AssertionError("the calendar must not unlock resume claims by itself")
    if payload["current_sent_count"] != 0 or payload["current_accepted_evidence_count"] != 0:
        raise AssertionError("the sprint calendar must preserve current zero outcome baselines")
    expected_metric_order = [
        "ai_engineer_review_items",
        "confirmed_external_users",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "external_feedback_items",
    ]
    if [card["target_metric"] for card in payload["day_cards"]] != expected_metric_order:
        raise AssertionError("sprint calendar must prioritize AI Engineer evidence first")
    for card in payload["day_cards"]:
        if "{name}" not in card["copy_ready_message"]:
            raise AssertionError("copy-ready messages must keep a recipient placeholder")
        if "external reviewer evidence gate marks the issue accepted" not in " ".join(card["completion_criteria"]).lower():
            raise AssertionError("each send day must require evidence-gate acceptance")
        if not card["submission_url"].startswith("https://github.com/"):
            raise AssertionError("submission paths must use public GitHub URLs")
    return {"reviewer_outcome_sprint_calendar_verified": True}


def main() -> None:
    payload = build_reviewer_outcome_sprint_calendar()
    verify_reviewer_outcome_sprint_calendar(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
