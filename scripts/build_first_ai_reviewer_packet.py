import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "docs" / "first-reviewer-handoff.json"
READINESS_PATH = ROOT / "docs" / "ai-engineer-readiness.json"
MATURITY_PATH = ROOT / "docs" / "agent-maturity-audit.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "first-ai-reviewer-packet.json"
OUTPUT_MD_PATH = ROOT / "docs" / "first-ai-reviewer-packet.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_first_ai_reviewer_packet() -> dict[str, Any]:
    handoff = load_json(HANDOFF_PATH)
    readiness = load_json(READINESS_PATH)
    maturity = load_json(MATURITY_PATH)
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_first_ai_reviewer_packet.py",
        "purpose": (
            "Give one external AI/ML systems reviewer a short, concrete review path that can produce the first "
            "public AI Engineer review signal without inflating resume outcomes."
        ),
        "target_metric": handoff["target_metric"],
        "current_count": handoff["current_count"],
        "required_count": handoff["required_count"],
        "submission_url": handoff["submission_url"],
        "public_slot_url": handoff["public_issue_url"],
        "review_time_minutes": "8-15",
        "reviewer_profile": handoff["reviewer_profile"],
        "inspection_targets": [
            {
                "label": "LLM tool loop and planning trace",
                "path": "app/tool_agent.py",
                "question": "Does the model choose tools based on tool feedback, and are planning steps recorded clearly?",
            },
            {
                "label": "Structured API contract",
                "path": "app/models.py",
                "question": "Are final outputs, tool calls, and planning steps machine-verifiable enough for downstream use?",
            },
            {
                "label": "Agent maturity audit",
                "path": "docs/agent-maturity-audit.md",
                "question": "Which implemented agent signals are credible, and which gaps should stay off the resume?",
            },
            {
                "label": "AI Engineer readiness",
                "path": "docs/ai-engineer-readiness.md",
                "question": "Does the project show enough LLM API, tool-calling, guardrail, and evaluation work for an AI Engineer intern signal?",
            },
            {
                "label": "Outcome evidence policy",
                "path": "docs/resume-outcome-action-checklist.md",
                "question": "Does the project avoid claiming users, feedback, or stars without public proof?",
            },
        ],
        "optional_local_checks": [
            ".venv/bin/python -m pytest tests/test_agent.py tests/test_agent_maturity_audit.py -q",
            ".venv/bin/python scripts/verify_outcome_evidence.py",
            ".venv/bin/python scripts/verify_public_evidence_health.py",
        ],
        "review_questions": [
            "What is the strongest AI Engineer signal in this repo?",
            "What is the least credible or most incomplete AI-agent claim?",
            "Would you describe this as a real LLM agent, a workflow, or something in between?",
            "Which one change would most improve interview credibility?",
            "Can this review be counted publicly without exposing private data?",
        ],
        "evidence_required_to_count": handoff["required_public_fields"],
        "acceptance_gate": handoff["evidence_gate"],
        "current_ai_engineer_signal_count": readiness["implemented_signal_count"],
        "current_agent_maturity_implemented": maturity["status_counts"]["implemented"],
        "current_agent_maturity_partial": maturity["status_counts"]["partial"],
        "future_resume_line": handoff["future_resume_line"],
        "resume_status": "ready_to_send_not_claimable",
        "not_claimed": [
            "sent outreach",
            "accepted AI Engineer review",
            "external user",
            "customer feedback",
            "production deployment",
        ],
        "resume_safe_summary": (
            f"Prepared a first AI Engineer reviewer packet with {readiness['implemented_signal_count']} implemented "
            f"AI Engineer signals, {maturity['status_counts']['implemented']} implemented maturity areas, "
            "5 inspection targets, and a public submission gate while preserving zero accepted AI reviews."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    targets = "\n".join(
        (
            f"### {item['label']}\n\n"
            f"- Path: `{item['path']}`\n"
            f"- Reviewer question: {item['question']}\n"
        )
        for item in payload["inspection_targets"]
    )
    checks = "\n".join(f"- `{command}`" for command in payload["optional_local_checks"])
    questions = "\n".join(f"- {question}" for question in payload["review_questions"])
    evidence = "\n".join(f"- {field}" for field in payload["evidence_required_to_count"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# First AI Reviewer Packet

This generated packet is the shortest external review path for the first AI Engineer credibility signal.

## Current Status

| Metric | Value |
| --- | --- |
| Target metric | `{payload["target_metric"]}` |
| Current accepted count | {payload["current_count"]} |
| Required count | {payload["required_count"]} |
| Resume status | `{payload["resume_status"]}` |
| Review time | {payload["review_time_minutes"]} minutes |
| Implemented AI Engineer signals | {payload["current_ai_engineer_signal_count"]} |
| Implemented maturity areas | {payload["current_agent_maturity_implemented"]} |
| Partial maturity areas | {payload["current_agent_maturity_partial"]} |

## Reviewer Links

- Public slot: [{payload["public_slot_url"]}]({payload["public_slot_url"]})
- Submission form: [{payload["submission_url"]}]({payload["submission_url"]})

## Inspection Targets

{targets}
## Optional Local Checks

{checks}

## Review Questions

{questions}

## Evidence Required To Count

{evidence}

## Acceptance Gate

{payload["acceptance_gate"]}

## Future Resume Line

Locked until a non-owner public review issue passes the evidence gate:

```text
{payload["future_resume_line"]}
```

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_first_ai_reviewer_packet(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["target_metric"] != "ai_engineer_review_items":
        raise AssertionError("first AI reviewer packet must target AI Engineer review evidence")
    if payload["current_count"] != 0:
        raise AssertionError("first AI reviewer packet must preserve zero accepted reviews")
    if payload["required_count"] != 1:
        raise AssertionError("first AI reviewer packet must require one accepted review")
    if len(payload["inspection_targets"]) != 5:
        raise AssertionError("first AI reviewer packet must have five inspection targets")
    if len(payload["review_questions"]) != 5:
        raise AssertionError("first AI reviewer packet must have five review questions")
    if payload["current_agent_maturity_implemented"] < 15:
        raise AssertionError("first AI reviewer packet must reflect the current implemented maturity count")
    if not payload["submission_url"].endswith("template=ai_engineer_review.md"):
        raise AssertionError("first AI reviewer packet must point to the AI Engineer review template")
    joined = json.dumps(payload, sort_keys=True).lower()
    for phrase in ("public", "permission", "zero accepted ai reviews", "not_claimed"):
        if phrase not in joined:
            raise AssertionError(f"first AI reviewer packet missing safety phrase: {phrase}")
    return {
        "first_ai_reviewer_packet_verified": True,
        "inspection_target_count": len(payload["inspection_targets"]),
        "review_question_count": len(payload["review_questions"]),
        "current_count": payload["current_count"],
    }


def main() -> None:
    payload = build_first_ai_reviewer_packet()
    verify_first_ai_reviewer_packet(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps({"status": "ok", "output": str(OUTPUT_JSON_PATH)}))


if __name__ == "__main__":
    main()
