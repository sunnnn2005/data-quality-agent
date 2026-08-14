import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEND_QUEUE_PATH = ROOT / "docs" / "reviewer-send-queue.json"
ACCEPTANCE_CHECKLIST_PATH = ROOT / "docs" / "evidence-acceptance-checklist.json"
FIRST_REVIEWER_SEND_KIT_PATH = ROOT / "docs" / "first-reviewer-send-kit.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "first-reviewer-handoff.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-reviewer-handoff.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_first_reviewer_handoff() -> dict[str, Any]:
    send_queue = load_json(SEND_QUEUE_PATH)
    checklist = load_json(ACCEPTANCE_CHECKLIST_PATH)
    first_send_kit = load_json(FIRST_REVIEWER_SEND_KIT_PATH)
    first_send = send_queue["next_sends"][0]
    acceptance_by_metric = {item["metric"]: item for item in checklist["acceptance_items"]}
    acceptance = acceptance_by_metric[first_send["target_metric"]]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_reviewer_handoff.py",
        "purpose": (
            "Give the maintainer one concrete next outreach action that can unlock the first real, "
            "public, resume-countable AI Engineer review signal."
        ),
        "target_metric": first_send["target_metric"],
        "current_count": acceptance["current_count"],
        "required_count": acceptance["required_count"],
        "status": first_send["status"],
        "reviewer_profile": first_send["reviewer_profile"],
        "recommended_channel": first_send["recommended_channel"],
        "who_to_choose": first_send["who_to_choose"],
        "public_issue_url": first_send["public_issue_url"],
        "entry_url": first_send["entry_url"],
        "submission_url": first_send["submission_url"],
        "copy_ready_message": first_send["copy_ready_message"],
        "copy_ready_follow_up": first_send["copy_ready_follow_up"],
        "required_public_fields": acceptance["required_fields"],
        "completion_fields": first_send["completion_fields"],
        "record_sent_command": first_send_kit["record_sent_command"],
        "after_send_expected_pipeline_change": first_send_kit["after_send_expected_pipeline_change"],
        "counting_boundary": first_send_kit["counting_boundary"],
        "evidence_gate": acceptance["evidence_gate"],
        "future_resume_line": acceptance["future_resume_line"],
        "manual_acceptance_rule": checklist["manual_counting_rule"],
        "resume_status": "not_claimable_until_public_issue_is_accepted",
        "not_claimed": [
            "message sent",
            "reviewer replied",
            "accepted AI Engineer review",
            "external user",
            "resume outcome upgrade",
        ],
        "resume_safe_summary": (
            "Prepared a first-reviewer handoff for the highest-priority AI Engineer review path, including "
            "copy-ready outreach, required public evidence fields, acceptance gate, and future resume wording "
            "while preserving zero sent outreach and zero accepted reviews."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    required_fields = "\n".join(f"- {field}" for field in payload["required_public_fields"])
    completion_fields = "\n".join(f"- `{field}`" for field in payload["completion_fields"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    pipeline_change = payload["after_send_expected_pipeline_change"]
    return f"""# First Reviewer Handoff

This generated handoff picks the single next reviewer ask most likely to unlock an honest AI Engineer resume signal.

## Current Status

| Metric | Value |
| --- | --- |
| Target metric | `{payload["target_metric"]}` |
| Current count | {payload["current_count"]} |
| Required count | {payload["required_count"]} |
| Status | `{payload["status"]}` |
| Resume status | `{payload["resume_status"]}` |

## Who To Ask

- Reviewer profile: {payload["reviewer_profile"]}
- Recommended channel: {payload["recommended_channel"]}
- Who to choose: {payload["who_to_choose"]}

## Links

- Public slot: [{payload["public_issue_url"]}]({payload["public_issue_url"]})
- Reviewer entry page: [{payload["entry_url"]}]({payload["entry_url"]})
- Submission form: [{payload["submission_url"]}]({payload["submission_url"]})

## Copy-Ready Message

```text
{payload["copy_ready_message"]}
```

## Follow-Up

```text
{payload["copy_ready_follow_up"]}
```

## Required Public Evidence

{required_fields}

## Completion Fields

{completion_fields}

## After You Send

Run this only after the message is sent to a real reviewer:

```bash
{payload["record_sent_command"]}
```

Expected pipeline change after recording one real send:

| Metric | Before | After recording one real send |
| --- | ---: | ---: |
| Sent reviewer messages | {pipeline_change["sent_reviewer_messages"]["before"]} | {pipeline_change["sent_reviewer_messages"]["after_recording_one_real_send"]} |
| Claimable resume metrics | {pipeline_change["claimable_resume_metric_count"]["before"]} | {pipeline_change["claimable_resume_metric_count"]["after_recording_one_real_send"]} |

{payload["counting_boundary"]}

## Acceptance Gate

{payload["evidence_gate"]}

Manual rule: {payload["manual_acceptance_rule"]}

## Future Resume Line

This line is locked until the public evidence gate passes:

```text
{payload["future_resume_line"]}
```

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_first_reviewer_handoff(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["target_metric"] != "ai_engineer_review_items":
        raise AssertionError("first reviewer handoff must prioritize AI Engineer review")
    if payload["current_count"] != 0:
        raise AssertionError("first reviewer handoff must preserve zero accepted reviews")
    if payload["required_count"] != 1:
        raise AssertionError("first reviewer handoff must target one accepted review")
    if payload["status"] != "not_sent":
        raise AssertionError("first reviewer handoff must not claim outreach was sent")
    if "AI/ML engineer" not in payload["who_to_choose"]:
        raise AssertionError("first reviewer handoff must explain who to choose")
    if "{name}" not in payload["copy_ready_message"]:
        raise AssertionError("first reviewer message must keep recipient placeholder")
    if payload["public_issue_url"] not in payload["copy_ready_message"]:
        raise AssertionError("first reviewer message must include the public issue URL")
    if "--slot-id review_slot_07" not in payload["record_sent_command"]:
        raise AssertionError("first reviewer handoff must include the real send recorder command")
    if payload["after_send_expected_pipeline_change"]["sent_reviewer_messages"]["after_recording_one_real_send"] != 1:
        raise AssertionError("first reviewer handoff must show that a real send changes the outreach pipeline")
    if payload["after_send_expected_pipeline_change"]["claimable_resume_metric_count"]["after_recording_one_real_send"] != 0:
        raise AssertionError("first reviewer handoff must not turn sent outreach into a resume claim")
    if len(payload["required_public_fields"]) < 4:
        raise AssertionError("first reviewer handoff must require enough public evidence fields")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in (
        "public",
        "permission",
        "zero sent outreach",
        "zero accepted reviews",
        "not_claimable_until_public_issue_is_accepted",
    ):
        if phrase not in joined:
            raise AssertionError(f"first reviewer handoff missing safety phrase: {phrase}")
    return {
        "first_reviewer_handoff_verified": True,
        "target_metric": payload["target_metric"],
        "current_count": payload["current_count"],
        "required_count": payload["required_count"],
    }


def main() -> None:
    payload = build_first_reviewer_handoff()
    verify_first_reviewer_handoff(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
