# Reviewer Outreach Execution Pack

This generated pack turns the reviewer action queue into messages that can be sent manually.

## Purpose

Convert the reviewer action queue into ready-to-send outreach messages, follow-up rules, and evidence checklists while preserving the zero-sent and zero-completed baseline.

## Source Queue

| Field | Value |
| --- | ---: |
| Queue Count | 9 |
| Evidence Goal Count | 6 |
| Not Contacted Count | 9 |
| Resume Status | outreach_queue_ready_not_claimable |

## Evidence Goals

- `accepted_real_model_runs`
- `ai_engineer_review_items`
- `business_case_feedback_items`
- `confirmed_external_users`
- `external_feedback_items`
- `reproducible_feedback_items`

## Outreach Items

### outreach_01_review_uc_davis_ds_peer_demo

- Segment: UC Davis data science peer
- Channel: LinkedIn, class Discord, club Slack, or direct message
- Status: `not_sent`
- Counts toward: `external_feedback_items`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Subject: Could you review my Data Quality Agent project? (UC Davis data science peer)

Message:

Hi {name}, I am trying to make my Data Quality Agent project credible for AI Engineer and SWE internship applications. Could you spend 8 minutes trying my public Data Quality Agent demo and leave one GitHub issue with anything confusing, useful, or broken? The shortest route is the one-click evidence page: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. I am tracking feedback publicly instead of claiming users without proof. If you are comfortable with it, please submit the review here: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md and include the sentence 'I give permission for this public issue to be counted as project review evidence.' Please do not include raw customer data, secrets, private emails, addresses, API keys, or production rows. Thank you.

Personalization checklist:
- Name the reviewer segment: UC Davis data science peer.
- Mention that the project is public and starts from a zero-feedback baseline.
- Ask them to use this entry path: https://sunnnn2005.github.io/data-quality-agent/.
- Ask them not to share private data and to submit only public, redacted evidence.

Evidence acceptance checklist:
- Public GitHub issue with demo path tried
- One concrete confusing, useful, or broken behavior
- Permission to count the issue as external feedback

Follow-up after 4 days:

Quick follow-up on my Data Quality Agent review request. No pressure, but if you have 8-15 minutes, the entry point is https://sunnnn2005.github.io/data-quality-agent/ and the public evidence form is https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. A short redacted comment is enough.

Status update rule: Move from not_sent to sent only after the message is actually sent. Move to completed only after a public GitHub issue passes the evidence gate.

### outreach_02_review_student_swe_peer_demo

- Segment: student software engineer peer
- Channel: LinkedIn, class Discord, club Slack, or direct message
- Status: `not_sent`
- Counts toward: `external_feedback_items`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Subject: Could you review my Data Quality Agent project? (student software engineer peer)

Message:

Hi {name}, I am trying to make my Data Quality Agent project credible for AI Engineer and SWE internship applications. I am collecting public review evidence for a data-quality LLM agent project. If anyone can try the demo, please leave one GitHub issue with what worked, what broke, or what would make it more useful for real data workflows. Fastest path: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. If you are comfortable with it, please submit the review here: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md and include the sentence 'I give permission for this public issue to be counted as project review evidence.' Please do not include raw customer data, secrets, private emails, addresses, API keys, or production rows. Thank you.

Personalization checklist:
- Name the reviewer segment: student software engineer peer.
- Mention that the project is public and starts from a zero-feedback baseline.
- Ask them to use this entry path: https://sunnnn2005.github.io/data-quality-agent/.
- Ask them not to share private data and to submit only public, redacted evidence.

Evidence acceptance checklist:
- Public GitHub issue with reviewed URL
- Specific product or engineering feedback
- Permission to count the issue as external feedback

Follow-up after 4 days:

Quick follow-up on my Data Quality Agent review request. No pressure, but if you have 8-15 minutes, the entry point is https://sunnnn2005.github.io/data-quality-agent/ and the public evidence form is https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. A short redacted comment is enough.

Status update rule: Move from not_sent to sent only after the message is actually sent. Move to completed only after a public GitHub issue passes the evidence gate.

### outreach_03_review_local_replay_engineer

- Segment: engineer comfortable with Docker or local setup
- Channel: LinkedIn, email, or mentor message
- Status: `not_sent`
- Counts toward: `reproducible_feedback_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)
- Subject: Could you review my Data Quality Agent project? (engineer comfortable with Docker or local setup)

Message:

Hi {name}, I am trying to make my Data Quality Agent project credible for AI Engineer and SWE internship applications. Could you clone my Data Quality Agent repo, run the local replay path, and submit whether the result was reproducible? Please avoid raw private data; a short redacted run summary is enough. If you are comfortable with it, please submit the review here: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md and include the sentence 'I give permission for this public issue to be counted as project review evidence.' Please do not include raw customer data, secrets, private emails, addresses, API keys, or production rows. Thank you.

Personalization checklist:
- Name the reviewer segment: engineer comfortable with Docker or local setup.
- Mention that the project is public and starts from a zero-feedback baseline.
- Ask them to use this entry path: https://github.com/sunnnn2005/data-quality-agent.
- Ask them not to share private data and to submit only public, redacted evidence.

Evidence acceptance checklist:
- Command or run path used
- Redacted result summary
- Whether the run was reproducible

Follow-up after 4 days:

Quick follow-up on my Data Quality Agent review request. No pressure, but if you have 8-15 minutes, the entry point is https://github.com/sunnnn2005/data-quality-agent and the public evidence form is https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md. A short redacted comment is enough.

Status update rule: Move from not_sent to sent only after the message is actually sent. Move to completed only after a public GitHub issue passes the evidence gate.

### outreach_04_review_confirmed_external_use

- Segment: reviewer who tried demo or local repo
- Channel: LinkedIn, email, or mentor message
- Status: `not_sent`
- Counts toward: `confirmed_external_users`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Subject: Could you review my Data Quality Agent project? (reviewer who tried demo or local repo)

Message:

Hi {name}, I am trying to make my Data Quality Agent project credible for AI Engineer and SWE internship applications. If you already tried the Data Quality Agent demo or ran the repo locally, could you leave a short public note saying what path you used and whether the result was understandable? The one-click evidence page has the confirmed-use form: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. I only count confirmed external use when it is public and specific. If you are comfortable with it, please submit the review here: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md and include the sentence 'I give permission for this public issue to be counted as project review evidence.' Please do not include raw customer data, secrets, private emails, addresses, API keys, or production rows. Thank you.

Personalization checklist:
- Name the reviewer segment: reviewer who tried demo or local repo.
- Mention that the project is public and starts from a zero-feedback baseline.
- Ask them to use this entry path: https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md.
- Ask them not to share private data and to submit only public, redacted evidence.

Evidence acceptance checklist:
- Public confirmation of demo or repo usage
- Path used
- Permission to count as confirmed external use

Follow-up after 4 days:

Quick follow-up on my Data Quality Agent review request. No pressure, but if you have 8-15 minutes, the entry point is https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md and the public evidence form is https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. A short redacted comment is enough.

Status update rule: Move from not_sent to sent only after the message is actually sent. Move to completed only after a public GitHub issue passes the evidence gate.

### outreach_05_review_data_analyst_business_case

- Segment: data analyst or analytics student
- Channel: LinkedIn, class Discord, club Slack, or direct message
- Status: `not_sent`
- Counts toward: `business_case_feedback_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)
- Subject: Could you review my Data Quality Agent project? (data analyst or analytics student)

Message:

Hi {name}, I am trying to make my Data Quality Agent project credible for AI Engineer and SWE internship applications. Do you have an anonymized data-quality problem this project should handle, such as duplicate IDs, stale exports, missing routing fields, or suspicious numeric values? A public business-case issue with no raw data would help me test real usefulness. The one-click evidence page is here: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. If you are comfortable with it, please submit the review here: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md and include the sentence 'I give permission for this public issue to be counted as project review evidence.' Please do not include raw customer data, secrets, private emails, addresses, API keys, or production rows. Thank you.

Personalization checklist:
- Name the reviewer segment: data analyst or analytics student.
- Mention that the project is public and starts from a zero-feedback baseline.
- Ask them to use this entry path: https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md.
- Ask them not to share private data and to submit only public, redacted evidence.

Evidence acceptance checklist:
- Anonymized business-data quality problem
- Expected business impact
- No private rows or sensitive fields

Follow-up after 4 days:

Quick follow-up on my Data Quality Agent review request. No pressure, but if you have 8-15 minutes, the entry point is https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md and the public evidence form is https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md. A short redacted comment is enough.

Status update rule: Move from not_sent to sent only after the message is actually sent. Move to completed only after a public GitHub issue passes the evidence gate.

### outreach_06_review_operator_business_case

- Segment: small-business operator or operations teammate
- Channel: LinkedIn or email to someone who has seen messy CSV, support, sales, or operations data
- Status: `not_sent`
- Counts toward: `business_case_feedback_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)
- Subject: Could you review my Data Quality Agent project? (small-business operator or operations teammate)

Message:

Hi {name}, I am trying to make my Data Quality Agent project credible for AI Engineer and SWE internship applications. Do you have an anonymized data-quality problem this project should handle, such as duplicate IDs, stale exports, missing routing fields, or suspicious numeric values? A public business-case issue with no raw data would help me test real usefulness. The one-click evidence page is here: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. If you are comfortable with it, please submit the review here: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md and include the sentence 'I give permission for this public issue to be counted as project review evidence.' Please do not include raw customer data, secrets, private emails, addresses, API keys, or production rows. Thank you.

Personalization checklist:
- Name the reviewer segment: small-business operator or operations teammate.
- Mention that the project is public and starts from a zero-feedback baseline.
- Ask them to use this entry path: https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md.
- Ask them not to share private data and to submit only public, redacted evidence.

Evidence acceptance checklist:
- Workflow affected by data-quality failure
- What decision would be wrong if the data is bad
- Permission to count the anonymized case as business feedback

Follow-up after 4 days:

Quick follow-up on my Data Quality Agent review request. No pressure, but if you have 8-15 minutes, the entry point is https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md and the public evidence form is https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md. A short redacted comment is enough.

Status update rule: Move from not_sent to sent only after the message is actually sent. Move to completed only after a public GitHub issue passes the evidence gate.

### outreach_07_review_ai_engineer_agent_readiness

- Segment: AI engineer, mentor, or ML systems reviewer
- Channel: LinkedIn, email, or mentor message
- Status: `not_sent`
- Counts toward: `ai_engineer_review_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)
- Subject: Could you review my Data Quality Agent project? (AI engineer, mentor, or ML systems reviewer)

Message:

Hi {name}, I am trying to make my Data Quality Agent project credible for AI Engineer and SWE internship applications. I am improving this project for AI Engineer internship applications. Could you review whether the LLM tool-calling loop, business-data connector, structured output, guardrails, and evidence trail look credible enough for an intern interview? If yes, please use the one-click evidence page or leave a public AI Engineer review issue with the path you inspected: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. If you are comfortable with it, please submit the review here: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md and include the sentence 'I give permission for this public issue to be counted as project review evidence.' Please do not include raw customer data, secrets, private emails, addresses, API keys, or production rows. Thank you.

Personalization checklist:
- Name the reviewer segment: AI engineer, mentor, or ML systems reviewer.
- Mention that the project is public and starts from a zero-feedback baseline.
- Ask them to use this entry path: https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md.
- Ask them not to share private data and to submit only public, redacted evidence.

Evidence acceptance checklist:
- Inspected LLM tool-calling or agent-readiness path
- Concrete AI Engineer credibility feedback
- Permission to count as AI Engineer review evidence

Follow-up after 4 days:

Quick follow-up on my Data Quality Agent review request. No pressure, but if you have 8-15 minutes, the entry point is https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md and the public evidence form is https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md. A short redacted comment is enough.

Status update rule: Move from not_sent to sent only after the message is actually sent. Move to completed only after a public GitHub issue passes the evidence gate.

### outreach_08_review_open_source_maintainer

- Segment: open-source maintainer or GitHub contributor
- Channel: GitHub discussion, maintainer DM, or project community channel
- Status: `not_sent`
- Counts toward: `external_feedback_items`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Subject: Could you review my Data Quality Agent project? (open-source maintainer or GitHub contributor)

Message:

Hi {name}, I am trying to make my Data Quality Agent project credible for AI Engineer and SWE internship applications. Could you review whether this repo is understandable for an outside contributor? I am especially looking for feedback on README clarity, issue templates, evidence artifacts, and whether a first-time contributor could run the project. If you are comfortable with it, please submit the review here: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md and include the sentence 'I give permission for this public issue to be counted as project review evidence.' Please do not include raw customer data, secrets, private emails, addresses, API keys, or production rows. Thank you.

Personalization checklist:
- Name the reviewer segment: open-source maintainer or GitHub contributor.
- Mention that the project is public and starts from a zero-feedback baseline.
- Ask them to use this entry path: https://sunnnn2005.github.io/data-quality-agent/.
- Ask them not to share private data and to submit only public, redacted evidence.

Evidence acceptance checklist:
- Public issue with contributor-readiness feedback
- One suggested improvement for README, setup, tests, or issue templates
- Permission to count the issue as external feedback

Follow-up after 4 days:

Quick follow-up on my Data Quality Agent review request. No pressure, but if you have 8-15 minutes, the entry point is https://sunnnn2005.github.io/data-quality-agent/ and the public evidence form is https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md. A short redacted comment is enough.

Status update rule: Move from not_sent to sent only after the message is actually sent. Move to completed only after a public GitHub issue passes the evidence gate.

### outreach_09_review_real_model_run_evidence

- Segment: AI engineer or developer willing to inspect a redacted real-model trace
- Channel: LinkedIn, email, or mentor message
- Status: `not_sent`
- Counts toward: `accepted_real_model_runs`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/real-model-run-request-pack.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/real-model-run-request-pack.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=real_model_run_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=real_model_run_review.md)
- Subject: Could you review my Data Quality Agent project? (AI engineer or developer willing to inspect a redacted real-model trace)

Message:

Hi {name}, I am trying to make my Data Quality Agent project credible for AI Engineer and SWE internship applications. I added a privacy-safe evidence path for a real OpenAI-compatible LLM agent run. Could you review the runbook, capture gate, and issue template, then help verify one redacted trace after I run it locally with credentials that are never shared? If you are comfortable with it, please submit the review here: https://github.com/sunnnn2005/data-quality-agent/issues/new?template=real_model_run_review.md and include the sentence 'I give permission for this public issue to be counted as project review evidence.' Please do not include raw customer data, secrets, private emails, addresses, API keys, or production rows. Thank you.

Personalization checklist:
- Name the reviewer segment: AI engineer or developer willing to inspect a redacted real-model trace.
- Mention that the project is public and starts from a zero-feedback baseline.
- Ask them to use this entry path: https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/real-model-run-request-pack.md.
- Ask them not to share private data and to submit only public, redacted evidence.

Evidence acceptance checklist:
- Accepted redacted real-model run issue
- Trace id, model name, prompt version, tool calls, latency, tokens, and estimated cost
- Final structured report verification result
- Permission to count the public issue as real-model LLM agent evidence

Follow-up after 4 days:

Quick follow-up on my Data Quality Agent review request. No pressure, but if you have 8-15 minutes, the entry point is https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/real-model-run-request-pack.md and the public evidence form is https://github.com/sunnnn2005/data-quality-agent/issues/new?template=real_model_run_review.md. A short redacted comment is enough.

Status update rule: Move from not_sent to sent only after the message is actually sent. Move to completed only after a public GitHub issue passes the evidence gate.

## Manual Execution Rules

- Do not mark a message as sent until it is actually sent to a real reviewer.
- Do not count private replies as public evidence.
- Do not count self-authored planning issues as external evidence.
- Do not ask reviewers to upload raw private business data.
- Do not write users, feedback, or business impact on a resume until a public issue passes the evidence gate.

## Resume-Safe Summary

Published a CI-verified outreach execution pack with 9 ready-to-send reviewer messages, 9 follow-up rules, 6 evidence goals, and zero sent or completed outreach claimed.
