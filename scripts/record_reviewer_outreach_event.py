import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.build_reviewer_outreach_status_board import (
    OUTREACH_EVENTS_PATH,
    OUTPUT_JSON_PATH as OUTREACH_STATUS_JSON_PATH,
    OUTPUT_MD_PATH as OUTREACH_STATUS_MD_PATH,
    build_reviewer_outreach_status_board,
    render_markdown as render_outreach_status_markdown,
    verify_reviewer_outreach_status_board,
)
from scripts.build_outcome_pipeline_board import (
    OUTPUT_JSON_PATH as OUTCOME_PIPELINE_JSON_PATH,
    OUTPUT_MD_PATH as OUTCOME_PIPELINE_MD_PATH,
    build_outcome_pipeline_board,
    render_markdown as render_outcome_pipeline_markdown,
    verify_outcome_pipeline_board,
)
from scripts.build_first_reviewer_send_kit import (
    OUTPUT_JSON_PATH as FIRST_REVIEWER_SEND_JSON_PATH,
    OUTPUT_MD_PATH as FIRST_REVIEWER_SEND_MD_PATH,
    build_first_reviewer_send_kit,
    render_markdown as render_first_reviewer_send_markdown,
    verify_first_reviewer_send_kit,
)


ALLOWED_STATUSES = {"sent", "replied_private", "public_issue_submitted"}


def load_events(path: Path = OUTREACH_EVENTS_PATH) -> dict[str, Any]:
    if not path.exists():
        return {
            "purpose": (
                "Append only real reviewer outreach events after a message is actually sent, "
                "a private reply is received, or a public redacted GitHub issue is submitted."
            ),
            "events": [],
        }
    return json.loads(path.read_text())


def append_event(payload: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    status = event.get("status")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"status must be one of {sorted(ALLOWED_STATUSES)}")
    if not event.get("slot_id"):
        raise ValueError("slot_id is required")
    if not event.get("reviewer_contact"):
        raise ValueError("reviewer_contact is required")
    if status == "public_issue_submitted" and not event.get("public_evidence_url"):
        raise ValueError("public_issue_submitted requires public_evidence_url")

    existing_events = payload.setdefault("events", [])
    duplicate = [
        item
        for item in existing_events
        if item.get("slot_id") == event["slot_id"]
        and item.get("status") == event["status"]
        and item.get("public_evidence_url") == event.get("public_evidence_url")
    ]
    if duplicate:
        raise ValueError("duplicate outreach event")

    existing_events.append(event)
    return payload


def build_event(args: argparse.Namespace) -> dict[str, Any]:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return {
        "slot_id": args.slot_id,
        "status": args.status,
        "reviewer_contact": args.reviewer_contact,
        "channel_used": args.channel_used,
        "sent_at": args.sent_at or now,
        "event_at": args.event_at or now,
        "public_evidence_url": args.public_evidence_url,
        "permission_to_count": bool(args.permission_to_count),
        "no_private_data_confirmed": bool(args.no_private_data_confirmed),
        "note": args.note,
    }


def refresh_downstream_artifacts() -> dict[str, Any]:
    status_board = build_reviewer_outreach_status_board()
    verify_reviewer_outreach_status_board(status_board)
    OUTREACH_STATUS_JSON_PATH.write_text(json.dumps(status_board, indent=2, sort_keys=True) + "\n")
    OUTREACH_STATUS_MD_PATH.write_text(render_outreach_status_markdown(status_board))

    pipeline = build_outcome_pipeline_board()
    verify_outcome_pipeline_board(pipeline)
    OUTCOME_PIPELINE_JSON_PATH.write_text(json.dumps(pipeline, indent=2, sort_keys=True) + "\n")
    OUTCOME_PIPELINE_MD_PATH.write_text(render_outcome_pipeline_markdown(pipeline))

    first_send = build_first_reviewer_send_kit()
    verify_first_reviewer_send_kit(first_send)
    FIRST_REVIEWER_SEND_JSON_PATH.write_text(json.dumps(first_send, indent=2, sort_keys=True) + "\n")
    FIRST_REVIEWER_SEND_MD_PATH.write_text(render_first_reviewer_send_markdown(first_send))

    return {
        "refreshed": True,
        "status_board_sent_count": status_board["sent_count"],
        "pipeline_sent_reviewer_messages": pipeline["current_baseline"]["sent_reviewer_messages"],
        "claimable_resume_metric_count": pipeline["claimable_resume_metric_count"],
        "first_send_status": first_send["source_outreach_status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Record a real reviewer outreach event without upgrading resume outcomes.")
    parser.add_argument("--slot-id", required=True, help="Reviewer slot id, for example review_slot_07")
    parser.add_argument("--status", required=True, choices=sorted(ALLOWED_STATUSES))
    parser.add_argument("--reviewer-contact", required=True, help="Reviewer name, public handle, or private contact label")
    parser.add_argument("--channel-used", required=True, help="LinkedIn, email, Discord, Slack, GitHub, etc.")
    parser.add_argument("--sent-at", help="ISO-8601 send timestamp; defaults to now")
    parser.add_argument("--event-at", help="ISO-8601 event timestamp; defaults to now")
    parser.add_argument("--public-evidence-url")
    parser.add_argument("--permission-to-count", action="store_true")
    parser.add_argument("--no-private-data-confirmed", action="store_true")
    parser.add_argument("--note")
    args = parser.parse_args()

    payload = append_event(load_events(), build_event(args))
    OUTREACH_EVENTS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    refresh_summary = refresh_downstream_artifacts()
    print(
        json.dumps(
            {
                "recorded": True,
                "slot_id": args.slot_id,
                "status": args.status,
                "event_count": len(payload["events"]),
                "status_board_sent_count": refresh_summary["status_board_sent_count"],
                "pipeline_sent_reviewer_messages": refresh_summary["pipeline_sent_reviewer_messages"],
                "resume_outcome_upgraded": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
