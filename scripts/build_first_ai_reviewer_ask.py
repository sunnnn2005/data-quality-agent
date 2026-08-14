import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEND_KIT_PATH = ROOT / "docs" / "first-reviewer-send-kit.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "first-ai-reviewer-ask.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-ai-reviewer-ask.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "first-ai-reviewer-ask.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_first_ai_reviewer_ask() -> dict[str, Any]:
    send_kit = load_json(SEND_KIT_PATH)
    inspection_targets = [
        {
            "label": "Agent loop and tool routing",
            "path": "app/agent.py",
            "question": "Does the LLM choose tools based on evidence instead of following a fixed script?",
        },
        {
            "label": "Safety boundaries",
            "path": "docs/agent-safety-boundaries.md",
            "question": "Are read-only data access, query limits, and redaction rules clear enough?",
        },
        {
            "label": "Evidence-backed reporting",
            "path": "docs/llm-agent-checklist-verdict.md",
            "question": "Are facts, inferences, limitations, and resume-safe claims separated?",
        },
        {
            "label": "Real model evidence gate",
            "path": "docs/real-model-evidence-capture.md",
            "question": "Would the telemetry be enough to verify a real OpenAI-compatible run later?",
        },
    ]
    review_questions = [
        "What is the strongest AI Engineer signal in this project?",
        "What is the least credible or most missing part of the agent design?",
        "Which file or behavior should be improved before this is resume-strong?",
        "Would you count this as an LLM agent project, and why?",
    ]
    permission_sentence = "I give permission for this public issue to be counted as project review evidence."
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_ai_reviewer_ask.py",
        "public_url": "https://sunnnn2005.github.io/data-quality-agent/first-ai-reviewer-ask.html",
        "purpose": (
            "Give the first AI/ML systems reviewer one focused public page for inspecting the agent design and "
            "submitting countable review evidence without exposing private data."
        ),
        "target_metric": send_kit["selected_metric"],
        "status_board_slot_id": send_kit["status_board_slot_id"],
        "source_outreach_status": send_kit["source_outreach_status"],
        "recommended_reviewer": send_kit["selected_reviewer_profile"],
        "recommended_channel": send_kit["recommended_channel"],
        "public_issue_url": send_kit["public_issue_url"],
        "submission_url": send_kit["submission_url"],
        "copy_ready_message": (
            "Could you review my Data Quality Agent as an AI Engineer project? "
            "This page has the shortest inspection path and public review form: "
            "https://sunnnn2005.github.io/data-quality-agent/first-ai-reviewer-ask.html"
        ),
        "inspection_target_count": len(inspection_targets),
        "inspection_targets": inspection_targets,
        "review_question_count": len(review_questions),
        "review_questions": review_questions,
        "required_public_evidence": [
            "reviewer is not the repository owner",
            "at least one inspected file, page, command, or behavior is named",
            "one concrete AI-agent strength or gap is described",
            permission_sentence,
            "no private data, secrets, customer records, private emails, addresses, API keys, or production rows",
        ],
        "permission_sentence": permission_sentence,
        "record_sent_command": send_kit["record_sent_command"],
        "counting_boundary": (
            "This page can support the first AI Engineer review only after a real non-owner reviewer submits a "
            "public, redacted GitHub issue with permission to count. A sent message or page view does not count."
        ),
        "current_claimable_ai_reviews": 0,
        "resume_status": "ready_to_send_not_reviewed",
        "resume_safe_summary": (
            "Published a focused first AI reviewer ask page with 4 inspection targets, 4 review questions, "
            "permission language, and recording guidance while keeping accepted AI reviews at zero."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    targets = "\n".join(
        f"- `{target['path']}` - {target['label']}: {target['question']}"
        for target in payload["inspection_targets"]
    )
    questions = "\n".join(f"- {question}" for question in payload["review_questions"])
    evidence = "\n".join(f"- {item}" for item in payload["required_public_evidence"])
    return f"""# First AI Reviewer Ask

{payload["purpose"]}

Public page: [{payload["public_url"]}]({payload["public_url"]})

## Send This

```text
{payload["copy_ready_message"]}
```

## Reviewer Task

- Target metric: `{payload["target_metric"]}`
- Slot: `{payload["status_board_slot_id"]}`
- Current status: `{payload["source_outreach_status"]}`
- Submission form: [{payload["submission_url"]}]({payload["submission_url"]})

## Inspection Targets

{targets}

## Review Questions

{questions}

## Required Public Evidence

{evidence}

## Record After Sending

```bash
{payload["record_sent_command"]}
```

## Counting Boundary

{payload["counting_boundary"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def render_html(payload: dict[str, Any]) -> str:
    targets = "\n".join(
        f"""
        <article>
          <span>{html.escape(target['path'])}</span>
          <h2>{html.escape(target['label'])}</h2>
          <p>{html.escape(target['question'])}</p>
        </article>
        """
        for target in payload["inspection_targets"]
    )
    questions = "".join(f"<li>{html.escape(question)}</li>" for question in payload["review_questions"])
    evidence = "".join(f"<li>{html.escape(item)}</li>" for item in payload["required_public_evidence"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>First AI Reviewer Ask</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #07111f;
      --panel: #101826;
      --line: #2a3a52;
      --text: #f8fafc;
      --muted: #a8b3c5;
      --accent: #7dd3fc;
      --accent2: #f472b6;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(135deg, #07111f 0%, #121827 54%, #1b1530 100%);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{
      width: min(1080px, calc(100% - 36px));
      margin: 0 auto;
      padding: 54px 0;
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 13px;
      font-weight: 850;
      text-transform: uppercase;
    }}
    h1 {{
      max-width: 900px;
      margin: 10px 0 18px;
      font-size: clamp(42px, 7vw, 78px);
      line-height: .98;
      letter-spacing: 0;
    }}
    .lede {{
      max-width: 780px;
      color: var(--muted);
      font-size: 20px;
    }}
    .actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin: 30px 0;
    }}
    a.button {{
      display: inline-flex;
      min-height: 48px;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      padding: 0 18px;
      background: var(--accent);
      color: #07111f;
      font-weight: 850;
      text-decoration: none;
    }}
    a.secondary {{
      background: transparent;
      color: var(--text);
      border: 1px solid var(--line);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin: 34px 0;
    }}
    article, .panel {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(16, 24, 38, .88);
      padding: 20px;
    }}
    article span {{
      color: var(--accent2);
      font-size: 13px;
      font-weight: 800;
    }}
    h2 {{
      margin: 6px 0 8px;
      font-size: 21px;
    }}
    ul {{
      margin: 12px 0 0;
      padding-left: 20px;
      color: var(--muted);
    }}
    code {{
      color: var(--accent);
      overflow-wrap: anywhere;
    }}
    @media (max-width: 760px) {{
      .grid {{ grid-template-columns: 1fr; }}
      main {{ padding: 34px 0; }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="eyebrow">Data Quality Agent · First external AI review</div>
    <h1>Review the LLM agent design in 8-15 minutes</h1>
    <p class="lede">{html.escape(payload["purpose"])}</p>
    <div class="actions">
      <a class="button" href="{html.escape(payload["submission_url"])}">Submit AI review</a>
      <a class="button secondary" href="{html.escape(payload["public_issue_url"])}">Open tracking issue</a>
    </div>
    <section class="panel">
      <h2>Copy-ready ask</h2>
      <p>{html.escape(payload["copy_ready_message"])}</p>
      <p><strong>Slot:</strong> <code>{html.escape(payload["status_board_slot_id"])}</code> · <strong>Status:</strong> <code>{html.escape(payload["source_outreach_status"])}</code></p>
    </section>
    <section class="grid">{targets}</section>
    <section class="grid">
      <div class="panel">
        <h2>Review questions</h2>
        <ul>{questions}</ul>
      </div>
      <div class="panel">
        <h2>Required public evidence</h2>
        <ul>{evidence}</ul>
      </div>
    </section>
    <section class="panel">
      <h2>Counting boundary</h2>
      <p>{html.escape(payload["counting_boundary"])}</p>
      <p><code>{html.escape(payload["permission_sentence"])}</code></p>
    </section>
  </main>
</body>
</html>
"""


def verify_first_ai_reviewer_ask(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["target_metric"] != "ai_engineer_review_items":
        raise AssertionError("first AI reviewer ask must target ai_engineer_review_items")
    if payload["status_board_slot_id"] != "review_slot_07":
        raise AssertionError("first AI reviewer ask must use review_slot_07")
    if payload["inspection_target_count"] != 4:
        raise AssertionError("first AI reviewer ask must include four inspection targets")
    if payload["review_question_count"] != 4:
        raise AssertionError("first AI reviewer ask must include four review questions")
    if payload["current_claimable_ai_reviews"] != 0:
        raise AssertionError("first AI reviewer ask must not claim accepted reviews")
    joined = json.dumps(payload, sort_keys=True)
    for phrase in (
        "public, redacted GitHub issue",
        "permission to count",
        "page view does not count",
        "app/agent.py",
        "docs/agent-safety-boundaries.md",
    ):
        if phrase not in joined:
            raise AssertionError(f"first AI reviewer ask missing phrase: {phrase}")
    return {
        "first_ai_reviewer_ask_verified": True,
        "inspection_target_count": payload["inspection_target_count"],
        "review_question_count": payload["review_question_count"],
    }


def main() -> None:
    payload = build_first_ai_reviewer_ask()
    verification = verify_first_ai_reviewer_ask(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
