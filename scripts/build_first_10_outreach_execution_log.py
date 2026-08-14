import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPRINT_PATH = ROOT / "docs" / "first-10-reviewer-sprint.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "first-10-outreach-execution-log.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-10-outreach-execution-log.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _message_for_slot(slot: dict[str, Any], issue_url: str) -> str:
    return (
        "Hi {name}, I am collecting public review evidence for my Data Quality Agent project so I can make "
        "resume claims only when they are backed by real, redacted GitHub evidence. Could you spend 8-15 minutes "
        f"on this reviewer slot: {issue_url}? The ask is: {slot['ask']} Please only share public, non-private "
        "details, and include the permission sentence in the issue if you are comfortable letting me count it."
    )


def _follow_up_for_slot(issue_url: str) -> str:
    return (
        "Quick follow-up on the Data Quality Agent review request. The public slot is still here: "
        f"{issue_url}. A short observed-result note is enough, and private data should not be included."
    )


def build_first_10_outreach_execution_log() -> dict[str, Any]:
    sprint = load_json(SPRINT_PATH)
    issues_by_slot = {item["slot_id"]: item for item in sprint["issue_launch_plan"]}
    entries = []
    for index, slot in enumerate(sprint["slots"], start=1):
        issue = issues_by_slot[slot["id"]]
        issue_url = issue["issue_url"]
        entries.append(
            {
                "sequence": index,
                "slot_id": slot["id"],
                "target_metric": slot["target_metric"],
                "reviewer_profile": slot["reviewer_profile"],
                "status": "not_sent",
                "public_issue_url": issue_url,
                "entry_url": slot["entry_url"],
                "submission_url": slot["submission_url"],
                "reviewer_contact": None,
                "channel": "manual_dm_or_email",
                "sent_at": None,
                "reply_status": "none",
                "accepted_evidence_url": None,
                "copy_ready_message": _message_for_slot(slot, issue_url),
                "follow_up_after_days": 4,
                "copy_ready_follow_up": _follow_up_for_slot(issue_url),
                "acceptance_evidence": slot["acceptance_evidence"],
                "counts_only_after": slot["counts_only_after"],
            }
        )

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_10_outreach_execution_log.py",
        "purpose": (
            "Turn the ten public reviewer issue entrypoints into a manual outreach execution log with copy-ready "
            "messages, follow-up timing, evidence fields, and conservative resume-counting boundaries."
        ),
        "source_sprint": "docs/first-10-reviewer-sprint.json",
        "entry_count": len(entries),
        "not_sent_count": len(entries),
        "sent_count": 0,
        "reply_count": 0,
        "accepted_evidence_count": 0,
        "public_issue_entrypoint_count": sprint["public_issue_entrypoint_count"],
        "target_metric_count": sprint["target_metric_count"],
        "target_counts": sprint["target_counts"],
        "current_counts": sprint["current_counts"],
        "entries": entries,
        "manual_update_rules": [
            "Fill reviewer_contact only after choosing a real person to contact.",
            "Move status to sent only after the message is actually sent.",
            "Private replies are notes, not resume-countable evidence.",
            "Move accepted_evidence_url only after a non-owner public GitHub issue passes the evidence gate.",
            "Do not count paid, traded, or requested-only GitHub stars as project traction.",
        ],
        "resume_status": "execution_ready_not_claimable",
        "resume_safe_summary": (
            f"Published a CI-verified first-10 outreach execution log with {len(entries)} copy-ready reviewer "
            "messages, 10 public issue entrypoints, zero sent outreach, and zero claimable external outcomes."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(f"| {key} | {value} |" for key, value in payload["current_counts"].items())
    targets = "\n".join(f"| {key} | {value} |" for key, value in payload["target_counts"].items())
    entries = []
    for entry in payload["entries"]:
        evidence = "\n".join(f"- {item}" for item in entry["acceptance_evidence"])
        entries.append(
            f"""### {entry["slot_id"]}

- Reviewer profile: {entry["reviewer_profile"]}
- Status: `{entry["status"]}`
- Target metric: `{entry["target_metric"]}`
- Public issue: [{entry["public_issue_url"]}]({entry["public_issue_url"]})
- Entry URL: [{entry["entry_url"]}]({entry["entry_url"]})
- Follow up after: {entry["follow_up_after_days"]} days

Copy-ready message:

```text
{entry["copy_ready_message"]}
```

Acceptance evidence:
{evidence}

Counting rule: {entry["counts_only_after"]}
"""
        )
    rules = "\n".join(f"- {rule}" for rule in payload["manual_update_rules"])
    return f"""# First 10 Outreach Execution Log

This generated log turns the public reviewer issues into concrete manual outreach steps.

## Purpose

{payload["purpose"]}

## Current Counts

| Metric | Current Count |
| --- | ---: |
{counts}

## Target Mix

| Metric | Target Slots |
| --- | ---: |
{targets}

## Execution Baseline

| Metric | Count |
| --- | ---: |
| Public issue entrypoints | {payload["public_issue_entrypoint_count"]} |
| Copy-ready outreach messages | {payload["entry_count"]} |
| Sent outreach | {payload["sent_count"]} |
| Replies | {payload["reply_count"]} |
| Accepted evidence | {payload["accepted_evidence_count"]} |

## Manual Update Rules

{rules}

## Entries

{chr(10).join(entries)}
## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_first_10_outreach_execution_log(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "entry_count": 10,
        "not_sent_count": 10,
        "sent_count": 0,
        "reply_count": 0,
        "accepted_evidence_count": 0,
        "public_issue_entrypoint_count": 10,
        "target_metric_count": 6,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    if payload.get("resume_status") != "execution_ready_not_claimable":
        raise AssertionError("execution log must not claim external outcomes")
    entries = payload.get("entries", [])
    if len(entries) != expected["entry_count"]:
        raise AssertionError("execution log must include ten outreach entries")
    issue_urls = {entry["public_issue_url"] for entry in entries}
    if len(issue_urls) != expected["public_issue_entrypoint_count"]:
        raise AssertionError("each outreach entry must map to a distinct public issue")
    for entry in entries:
        if entry["status"] != "not_sent":
            raise AssertionError("execution log must not fabricate sent outreach")
        if entry["reviewer_contact"] is not None or entry["sent_at"] is not None:
            raise AssertionError("execution log must not fabricate reviewer identities or sent timestamps")
        if entry["accepted_evidence_url"] is not None:
            raise AssertionError("execution log must not fabricate accepted evidence")
        if "{name}" not in entry["copy_ready_message"]:
            raise AssertionError("copy-ready message must keep reviewer name as a placeholder")
        if entry["public_issue_url"] not in entry["copy_ready_message"]:
            raise AssertionError("copy-ready message must point reviewers to the public issue")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in (
        "non-owner public github issue",
        "permission",
        "private data",
        "evidence gate",
        "zero claimable external outcomes",
    ):
        if required not in joined:
            raise AssertionError(f"execution log missing safety phrase: {required}")
    return {"first_10_outreach_execution_log_verified": True, **expected}


def main() -> None:
    payload = build_first_10_outreach_execution_log()
    verify_first_10_outreach_execution_log(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps({"status": "ok", "output": str(OUTPUT_JSON_PATH), "entry_count": payload["entry_count"]}))


if __name__ == "__main__":
    main()
