# AI Engineer Reviewer Card

This generated card gives one external AI/ML reviewer the shortest path to inspect the project and leave countable public feedback.

## Purpose

Give one external AI/ML reviewer a single low-friction card for inspecting the agent and submitting public evidence.

## Current Status

| Metric | Value |
| --- | --- |
| Target metric | `ai_engineer_review_items` |
| Current accepted reviews | 0 |
| Expected review time | 12 minutes |
| Resume status | `review_card_ready_not_claimable` |

## Inspect These First

| Area | Path | Why It Matters |
| --- | --- | --- |
| Agent loop | `app/tool_agent.py` | shows LLM-driven tool choice, loop state, and tool-result feedback |
| LLM boundary | `app/llm.py` | shows structured model calls, fallback handling, and output validation boundaries |
| Tool contracts | `app/models.py` | shows structured request and response schemas used by the API and agent |
| Business data adapter | `app/postgres_adapter.py` | shows read-only PostgreSQL access for realistic tabular business data |
| Evidence verifier | `app/verifier.py` | shows deterministic checks that keep LLM conclusions tied to evidence |
| Evaluation scenarios | `evals/scenarios.jsonl` | shows the project is evaluated against repeatable agent behavior cases |

## Optional Run Commands

| Step | Command | Expected Result |
| --- | --- | --- |
| Run tests | `.venv/bin/python -m pytest` | 210 passing tests before this card is regenerated |
| Run evidence verifier | `.venv/bin/python scripts/verify_outcome_evidence.py` | all resume outcome gates pass without upgrading zero-count claims |
| Run local demo | `docker compose up --build` | FastAPI, dashboard, and seeded PostgreSQL replay are available locally |

## Review Prompts

1. Does the model choose tools from evidence, or does the code force a fixed workflow?
2. Are tool outputs fed back into the agent before the final report is produced?
3. Are findings, hypotheses, recommendations, evidence, confidence, and limitations separated?
4. Where would prompt injection, sensitive data, or unsupported claims be blocked?
5. What one change would make this more credible for an AI Engineer Intern resume?

## Submit Public Review

- Public slot: [https://github.com/sunnnn2005/data-quality-agent/issues/26](https://github.com/sunnnn2005/data-quality-agent/issues/26)
- Submit review: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)

## Outcome Badge Snapshot

| Signal | Current Value |
| --- | --- |
| Ci Tests | 210 passing |
| Ai Review | 0 accepted |
| Confirmed Users | 0 accepted |
| External Feedback | 0 accepted |

## Acceptance Gate

Counts only after a non-owner public GitHub issue lists inspected paths, includes permission to count, contains no private data, and passes the external reviewer evidence gate.

## Resume-Safe Summary

Published a one-page AI Engineer reviewer card with 6 inspection targets, 3 run commands, 5 review prompts, public submission links, and a zero-review baseline.

## Not Claimed

- No external AI Engineer review has been accepted yet.
- No confirmed external users are claimed.
- No production deployment or business adoption is claimed.
