import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEND_QUEUE_PATH = ROOT / "docs" / "reviewer-send-queue.json"
STATUS_BOARD_PATH = ROOT / "docs" / "reviewer-outreach-status-board.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-outreach-console.json"
OUTPUT_HTML_PATH = ROOT / "docs" / "reviewer-outreach-console.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _status_slot_id(send_slot_id: str) -> str:
    mapping = {
        "slot_01_ds_peer_demo": "review_slot_01",
        "slot_03_local_replay": "review_slot_03",
        "slot_04_confirmed_use": "review_slot_04",
        "slot_05_data_analyst_case": "review_slot_05",
        "slot_07_ai_engineer_review": "review_slot_07",
    }
    return mapping[send_slot_id]


def build_reviewer_outreach_console() -> dict[str, Any]:
    queue = load_json(SEND_QUEUE_PATH)
    status_board = load_json(STATUS_BOARD_PATH)
    status_by_slot = {slot["slot_id"]: slot for slot in status_board["outreach_slots"]}

    sends = []
    for item in queue["next_sends"]:
        status_slot_id = _status_slot_id(item["slot_id"])
        status_slot = status_by_slot[status_slot_id]
        sends.append(
            {
                "rank": item["rank"],
                "queue_slot_id": item["slot_id"],
                "status_slot_id": status_slot_id,
                "target_metric": item["target_metric"],
                "reviewer_profile": item["reviewer_profile"],
                "recommended_channel": item["recommended_channel"],
                "who_to_choose": item["who_to_choose"],
                "current_status": status_slot["status"],
                "public_issue_url": item["public_issue_url"],
                "entry_url": item["entry_url"],
                "submission_url": item["submission_url"],
                "copy_ready_message": item["copy_ready_message"],
                "copy_ready_follow_up": item["copy_ready_follow_up"],
                "record_sent_command": (
                    f"python scripts/record_reviewer_outreach_event.py --slot-id {status_slot_id} "
                    f"--status sent --reviewer-contact \"<reviewer name or handle>\" "
                    f"--channel-used \"{item['recommended_channel']}\" "
                    f"--note \"Sent {item['target_metric']} reviewer request\""
                ),
                "counts_only_after": item["counts_only_after"],
            }
        )

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_outreach_console.py",
        "purpose": (
            "Put the highest-priority reviewer asks, copy-ready messages, submission links, and sent-event "
            "recording commands on one public page so real outreach can happen without inventing outcomes."
        ),
        "send_count": len(sends),
        "not_sent_count": sum(1 for item in sends if item["current_status"] == "not_sent"),
        "sent_count": sum(1 for item in sends if item["current_status"] == "sent"),
        "accepted_evidence_count": status_board["accepted_evidence_count"],
        "resume_upgrade_count": status_board["resume_upgrade_count"],
        "current_outcome_counts": status_board["current_outcome_counts"],
        "sends": sends,
        "counting_boundaries": [
            "Recording a sent message proves distribution execution only.",
            "Private replies do not count as public evidence.",
            "A resume outcome is upgraded only after a non-owner public GitHub issue passes the evidence gate.",
            "Do not include raw business rows, secrets, customer names, private emails, addresses, or tokens.",
            "Do not buy, trade, or pressure for GitHub stars.",
        ],
        "resume_safe_summary": (
            f"Published a reviewer outreach console with {len(sends)} prioritized asks, "
            f"{sum(1 for item in sends if item['current_status'] == 'not_sent')} not-sent messages, "
            "copy-ready evidence links, and zero upgraded resume outcomes."
        ),
    }


def render_html(payload: dict[str, Any]) -> str:
    cards = "\n".join(
        f"""
        <article class="card">
          <div class="meta">#{item["rank"]} · {item["target_metric"]}</div>
          <h3>{item["reviewer_profile"]}</h3>
          <p>{item["who_to_choose"]}</p>
          <p><strong>Channel:</strong> {item["recommended_channel"]}</p>
          <p><strong>Status:</strong> <code>{item["current_status"]}</code></p>
          <div class="actions">
            <a class="button" href="{item["submission_url"]}">Open submission form</a>
            <a class="button secondary" href="{item["entry_url"]}">Review context</a>
            <a class="button secondary" href="{item["public_issue_url"]}">Tracking slot</a>
          </div>
          <label>Message</label>
          <textarea readonly>{item["copy_ready_message"]}</textarea>
          <label>Record after real send</label>
          <pre>{item["record_sent_command"]}</pre>
          <p class="boundary">{item["counts_only_after"]}</p>
        </article>
        """
        for item in payload["sends"]
    )
    boundaries = "\n".join(f"<li>{item}</li>" for item in payload["counting_boundaries"])
    counts = "\n".join(
        f"<div class=\"metric\"><strong>{value}</strong><span>{key.replace('_', ' ')}</span></div>"
        for key, value in payload["current_outcome_counts"].items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Reviewer Outreach Console</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0a0f15;
      --panel: #111924;
      --panel-2: #172232;
      --text: #f7fafc;
      --muted: #a7b3c7;
      --line: #2a3548;
      --accent: #5eead4;
      --accent-2: #8ab4ff;
      --warn: #ffd166;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at 12% 0%, rgba(94, 234, 212, .16), transparent 28rem),
        radial-gradient(circle at 88% 2%, rgba(138, 180, 255, .16), transparent 30rem),
        var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    a {{ color: inherit; }}
    .shell {{ width: min(1120px, calc(100% - 40px)); margin: 0 auto; padding: 46px 0; }}
    header {{ display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 28px; align-items: end; min-height: 48vh; }}
    .eyebrow, .meta {{ color: var(--accent); font-size: 13px; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; }}
    h1 {{ font-size: clamp(42px, 7vw, 82px); line-height: .95; letter-spacing: 0; margin: 12px 0 18px; }}
    .lede {{ color: var(--muted); font-size: clamp(18px, 2.2vw, 23px); margin: 0; max-width: 780px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .metric, .card, .guardrail {{ background: rgba(17, 25, 36, .9); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
    .metric strong {{ display: block; font-size: 32px; line-height: 1; margin-bottom: 6px; }}
    .metric span, .card p, .guardrail li {{ color: var(--muted); }}
    section {{ border-top: 1px solid var(--line); padding: 38px 0; }}
    h2 {{ font-size: clamp(28px, 4vw, 42px); line-height: 1; letter-spacing: 0; margin: 0 0 16px; }}
    .cards {{ display: grid; gap: 14px; }}
    .card h3 {{ font-size: 22px; margin: 8px 0; }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 14px 0; }}
    .button {{ align-items: center; background: var(--accent); border: 1px solid rgba(255,255,255,.12); border-radius: 8px; color: #06201b; display: inline-flex; font-weight: 850; min-height: 42px; padding: 0 14px; text-decoration: none; }}
    .button.secondary {{ background: rgba(255,255,255,.07); color: var(--text); }}
    label {{ color: var(--warn); display: block; font-size: 12px; font-weight: 900; margin: 16px 0 8px; text-transform: uppercase; }}
    textarea, pre {{
      background: #071016;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: #dbeafe;
      font: 13px/1.55 ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      margin: 0;
      overflow-x: auto;
      padding: 14px;
      width: 100%;
    }}
    textarea {{ min-height: 150px; resize: vertical; }}
    .boundary {{ border-top: 1px solid var(--line); margin-top: 16px; padding-top: 12px; }}
    .guardrail ul {{ margin: 0; padding-left: 18px; }}
    footer {{ border-top: 1px solid var(--line); color: var(--muted); padding-top: 24px; }}
    @media (max-width: 860px) {{
      header {{ grid-template-columns: 1fr; min-height: auto; }}
      .metrics {{ grid-template-columns: 1fr; }}
      .shell {{ width: min(100% - 28px, 1120px); padding: 28px 0; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <header>
      <div>
        <div class="eyebrow">Reviewer outreach console</div>
        <h1>Send real asks, then record only what happened.</h1>
        <p class="lede">{payload["purpose"]}</p>
      </div>
      <div class="metrics" aria-label="Current outcome counts">
        <div class="metric"><strong>{payload["send_count"]}</strong><span>prioritized asks</span></div>
        <div class="metric"><strong>{payload["not_sent_count"]}</strong><span>not sent</span></div>
        <div class="metric"><strong>{payload["accepted_evidence_count"]}</strong><span>accepted evidence</span></div>
        <div class="metric"><strong>{payload["resume_upgrade_count"]}</strong><span>resume upgrades</span></div>
      </div>
    </header>

    <section>
      <h2>Next Reviewer Asks</h2>
      <div class="cards">{cards}
      </div>
    </section>

    <section>
      <h2>Counting Boundaries</h2>
      <div class="guardrail">
        <ul>{boundaries}</ul>
      </div>
    </section>

    <footer>
      Generated by <code>{payload["generated_by"]}</code>. {payload["resume_safe_summary"]}
    </footer>
  </main>
</body>
</html>
"""


def verify_reviewer_outreach_console(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["send_count"] != 5:
        raise AssertionError("reviewer outreach console must expose five prioritized asks")
    if payload["not_sent_count"] != 5 or payload["sent_count"] != 0:
        raise AssertionError("reviewer outreach console must preserve the zero-sent baseline")
    if payload["accepted_evidence_count"] != 0 or payload["resume_upgrade_count"] != 0:
        raise AssertionError("reviewer outreach console must not claim accepted evidence or resume upgrades")
    required_metrics = {
        "ai_engineer_review_items",
        "business_case_feedback_items",
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
    }
    if {item["target_metric"] for item in payload["sends"]} != required_metrics:
        raise AssertionError("reviewer outreach console must cover the five non-star outcome metrics")
    if payload["sends"][0]["target_metric"] != "ai_engineer_review_items":
        raise AssertionError("reviewer outreach console must prioritize AI Engineer review first")
    for item in payload["sends"]:
        if item["current_status"] != "not_sent":
            raise AssertionError("reviewer outreach console must not mark messages sent")
        if item["submission_url"] not in item["copy_ready_message"]:
            raise AssertionError("copy-ready messages must include the submission URL")
        if item["public_issue_url"] not in item["copy_ready_message"]:
            raise AssertionError("copy-ready messages must include the tracking issue URL")
        if f"--slot-id {item['status_slot_id']}" not in item["record_sent_command"]:
            raise AssertionError("record command must match the status board slot")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in ("non-owner public github issue", "private replies do not count", "do not buy, trade, or pressure"):
        if phrase not in joined:
            raise AssertionError(f"reviewer outreach console missing boundary phrase: {phrase}")
    return {
        "reviewer_outreach_console_verified": True,
        "send_count": payload["send_count"],
        "not_sent_count": payload["not_sent_count"],
        "resume_upgrade_count": payload["resume_upgrade_count"],
    }


def main() -> None:
    payload = build_reviewer_outreach_console()
    verify_reviewer_outreach_console(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps({"status": "ok", "output": str(OUTPUT_JSON_PATH), "send_count": payload["send_count"]}))


if __name__ == "__main__":
    main()
