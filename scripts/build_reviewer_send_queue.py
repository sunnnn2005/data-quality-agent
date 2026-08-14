import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTREACH_LOG_PATH = ROOT / "docs" / "first-10-outreach-execution-log.json"
SCOREBOARD_PATH = ROOT / "docs" / "resume-outcome-scoreboard.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-send-queue.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-send-queue.md"


CHANNEL_BY_METRIC = {
    "ai_engineer_review_items": "LinkedIn DM or mentor email",
    "business_case_feedback_items": "email or in-person ask to someone who has handled messy operational data",
    "confirmed_external_users": "class Discord, friend DM, or club Slack",
    "external_feedback_items": "LinkedIn DM, class Discord, or project channel",
    "reproducible_feedback_items": "GitHub issue comment, Discord, or DM to a developer comfortable with Docker",
    "github_stars": "GitHub repo link only; never trade, buy, or pressure for stars",
}


PRIORITY_BY_METRIC = {
    "ai_engineer_review_items": 1,
    "confirmed_external_users": 2,
    "reproducible_feedback_items": 3,
    "business_case_feedback_items": 4,
    "external_feedback_items": 5,
    "github_stars": 6,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _contact_prompt(entry: dict[str, Any]) -> str:
    metric = entry["target_metric"]
    if metric == "ai_engineer_review_items":
        return "Choose one AI/ML engineer, professor, mentor, or advanced student who can inspect agent architecture."
    if metric == "confirmed_external_users":
        return "Choose one person who can simply open the demo and confirm what they tried."
    if metric == "reproducible_feedback_items":
        return "Choose one developer who can run a command or inspect the local replay instructions."
    if metric == "business_case_feedback_items":
        return "Choose one person who has seen messy spreadsheets, support tickets, sales data, or operations data."
    if metric == "external_feedback_items":
        return "Choose one peer who can leave specific product or README feedback."
    return "Share only with someone who may genuinely find the repo useful; do not ask for fake engagement."


def _completion_fields(entry: dict[str, Any]) -> list[str]:
    return [
        "reviewer_contact",
        "sent_at",
        "channel_used",
        "public_issue_or_response_url",
        "permission_sentence_present",
        "no_private_data_confirmed",
    ]


def build_reviewer_send_queue() -> dict[str, Any]:
    outreach = load_json(OUTREACH_LOG_PATH)
    scoreboard = load_json(SCOREBOARD_PATH)
    entries = sorted(
        outreach["entries"],
        key=lambda item: (PRIORITY_BY_METRIC[item["target_metric"]], item["sequence"]),
    )
    selected_entries = []
    seen_metrics = set()
    for entry in entries:
        if entry["target_metric"] in seen_metrics:
            continue
        if entry["target_metric"] == "github_stars":
            continue
        selected_entries.append(entry)
        seen_metrics.add(entry["target_metric"])
        if len(selected_entries) == 5:
            break

    next_sends = []
    for rank, entry in enumerate(selected_entries, start=1):
        next_sends.append(
            {
                "rank": rank,
                "slot_id": entry["slot_id"],
                "target_metric": entry["target_metric"],
                "reviewer_profile": entry["reviewer_profile"],
                "recommended_channel": CHANNEL_BY_METRIC[entry["target_metric"]],
                "who_to_choose": _contact_prompt(entry),
                "status": entry["status"],
                "public_issue_url": entry["public_issue_url"],
                "entry_url": entry["entry_url"],
                "submission_url": entry["submission_url"],
                "copy_ready_message": entry["copy_ready_message"],
                "copy_ready_follow_up": entry["copy_ready_follow_up"],
                "completion_fields": _completion_fields(entry),
                "counts_only_after": entry["counts_only_after"],
            }
        )

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_send_queue.py",
        "purpose": (
            "Convert the reviewer outreach backlog into the next five concrete sends needed to unlock real, "
            "public, resume-countable evidence without claiming sent outreach or external outcomes prematurely."
        ),
        "source": "docs/first-10-outreach-execution-log.json",
        "queue_count": len(next_sends),
        "not_sent_count": sum(1 for item in next_sends if item["status"] == "not_sent"),
        "sent_count": 0,
        "accepted_evidence_count": 0,
        "target_metrics": sorted({item["target_metric"] for item in next_sends}),
        "next_sends": next_sends,
        "scoreboard_remaining_evidence_items": scoreboard["reviewer_funnel"]["remaining_evidence_items"],
        "resume_status": "send_ready_not_claimable",
        "manual_execution_rule": (
            "Only change an item from not_sent to sent after the maintainer sends it to a real person; only count an "
            "outcome after a non-owner public GitHub issue passes the evidence gate."
        ),
        "resume_safe_summary": (
            f"Published a reviewer send queue with {len(next_sends)} prioritized next sends across "
            f"{len({item['target_metric'] for item in next_sends})} target metrics while preserving zero sent outreach, "
            "zero accepted evidence, and zero upgraded resume outcome claims."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    target_metrics = "\n".join(f"- `{metric}`" for metric in payload["target_metrics"])
    entries = []
    for item in payload["next_sends"]:
        fields = "\n".join(f"- {field}" for field in item["completion_fields"])
        entries.append(
            f"""### {item["rank"]}. {item["slot_id"]}

- Target metric: `{item["target_metric"]}`
- Reviewer profile: {item["reviewer_profile"]}
- Recommended channel: {item["recommended_channel"]}
- Who to choose: {item["who_to_choose"]}
- Status: `{item["status"]}`
- Public issue: [{item["public_issue_url"]}]({item["public_issue_url"]})
- Entry URL: [{item["entry_url"]}]({item["entry_url"]})
- Submission URL: [{item["submission_url"]}]({item["submission_url"]})

Copy-ready message:

```text
{item["copy_ready_message"]}
```

Follow-up:

```text
{item["copy_ready_follow_up"]}
```

Completion fields:
{fields}

Counting rule: {item["counts_only_after"]}
"""
        )
    return f"""# Reviewer Send Queue

This generated queue turns planned outreach into the next concrete sends.

## Purpose

{payload["purpose"]}

## Status

| Metric | Count |
| --- | ---: |
| Prioritized sends | {payload["queue_count"]} |
| Not sent | {payload["not_sent_count"]} |
| Sent | {payload["sent_count"]} |
| Accepted evidence | {payload["accepted_evidence_count"]} |
| Scoreboard remaining evidence items | {payload["scoreboard_remaining_evidence_items"]} |

## Target Metrics

{target_metrics}

## Manual Execution Rule

{payload["manual_execution_rule"]}

## Next Sends

{chr(10).join(entries)}
## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_reviewer_send_queue(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["queue_count"] != 5:
        raise AssertionError("reviewer send queue must prioritize five next sends")
    if payload["not_sent_count"] != 5 or payload["sent_count"] != 0:
        raise AssertionError("reviewer send queue must preserve a zero-sent baseline")
    if payload["accepted_evidence_count"] != 0:
        raise AssertionError("reviewer send queue must not fabricate accepted evidence")
    if payload["scoreboard_remaining_evidence_items"] != 7:
        raise AssertionError("reviewer send queue must preserve the seven-item evidence gap")
    required_metrics = {
        "ai_engineer_review_items",
        "business_case_feedback_items",
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
    }
    if set(payload["target_metrics"]) != required_metrics:
        raise AssertionError("reviewer send queue must cover the five most useful non-star outcome metrics")
    ranks = [item["rank"] for item in payload["next_sends"]]
    if ranks != [1, 2, 3, 4, 5]:
        raise AssertionError("reviewer send queue ranks must be stable and ordered")
    first_metric = payload["next_sends"][0]["target_metric"]
    if first_metric != "ai_engineer_review_items":
        raise AssertionError("AI Engineer review should be the first send for the user's target role")
    for item in payload["next_sends"]:
        if item["status"] != "not_sent":
            raise AssertionError("send queue must not mark any item sent")
        if "{name}" not in item["copy_ready_message"]:
            raise AssertionError("send queue messages must keep the recipient placeholder")
        if item["public_issue_url"] not in item["copy_ready_message"]:
            raise AssertionError("send queue message must include the public issue URL")
        if len(item["completion_fields"]) != 6:
            raise AssertionError("send queue must define six completion fields")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in ("non-owner public github issue", "evidence gate", "zero upgraded resume outcome claims"):
        if phrase not in joined:
            raise AssertionError(f"send queue missing safety phrase: {phrase}")
    return {
        "reviewer_send_queue_verified": True,
        "queue_count": payload["queue_count"],
        "target_metric_count": len(payload["target_metrics"]),
        "not_sent_count": payload["not_sent_count"],
    }


def main() -> None:
    payload = build_reviewer_send_queue()
    verify_reviewer_send_queue(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps({"status": "ok", "output": str(OUTPUT_JSON_PATH), "queue_count": payload["queue_count"]}))


if __name__ == "__main__":
    main()
