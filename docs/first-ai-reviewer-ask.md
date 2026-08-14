# First AI Reviewer Ask

Give the first AI/ML systems reviewer one focused public page for inspecting the agent design and submitting countable review evidence without exposing private data.

Public page: [https://sunnnn2005.github.io/data-quality-agent/first-ai-reviewer-ask.html](https://sunnnn2005.github.io/data-quality-agent/first-ai-reviewer-ask.html)

## Send This

```text
Could you review my Data Quality Agent as an AI Engineer project? The short path now includes the LLM value comparison that shows adaptive strategy selection beating a fixed checklist across 14 scenarios. Public review form: https://sunnnn2005.github.io/data-quality-agent/first-ai-reviewer-ask.html
```

## Reviewer Task

- Target metric: `ai_engineer_review_items`
- Slot: `review_slot_07`
- Current status: `not_sent`
- Submission form: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)

## Inspection Targets

- `app/agent.py` - Agent loop and tool routing: Does the LLM choose tools based on evidence instead of following a fixed script?
- `docs/agent-safety-boundaries.md` - Safety boundaries: Are read-only data access, query limits, and redaction rules clear enough?
- `docs/llm-agent-checklist-verdict.md` - Evidence-backed reporting: Are facts, inferences, limitations, and resume-safe claims separated?
- `docs/llm-value-comparison.md` - Adaptive strategy value: Does the 14-scenario comparison make the agentic strategy selection more credible than a fixed workflow?
- `docs/real-model-evidence-capture.md` - Real model evidence gate: Would the telemetry be enough to verify a real OpenAI-compatible run later?

## Review Questions

- What is the strongest AI Engineer signal in this project?
- What is the least credible or most missing part of the agent design?
- Which file or behavior should be improved before this is resume-strong?
- Would you count this as an LLM agent project, and why?

## Required Public Evidence

- reviewer is not the repository owner
- at least one inspected file, page, command, or behavior is named
- one concrete AI-agent strength or gap is described
- I give permission for this public issue to be counted as project review evidence.
- no private data, secrets, customer records, private emails, addresses, API keys, or production rows

## Record After Sending

```bash
python scripts/record_reviewer_outreach_event.py --slot-id review_slot_07 --status sent --reviewer-contact "<reviewer name or handle>" --channel-used "LinkedIn DM or mentor email" --note "Sent first AI Engineer reviewer request"
```

## Counting Boundary

This page can support the first AI Engineer review only after a real non-owner reviewer submits a public, redacted GitHub issue with permission to count. A sent message or page view does not count.

## Resume-Safe Summary

Published a focused first AI reviewer ask page with 5 inspection targets, 4 review questions, LLM value-comparison evidence, permission language, and recording guidance while keeping accepted AI reviews at zero.
