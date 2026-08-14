# Reviewer Action Queue

This generated queue turns reviewer outreach into public, countable evidence tasks.

## Purpose

Turn the zero-user, zero-feedback baseline into a concrete public reviewer action queue without claiming any reviewer has been contacted or completed.

## Baseline

| Metric | Current value |
| --- | ---: |
| External Feedback Items | 0 |
| Confirmed External Users | 0 |
| Reproducible Feedback Items | 0 |
| Business Case Feedback Items | 0 |
| Ai Engineer Review Items | 0 |
| Stars | 0 |
| Accepted Real Model Runs | 0 |

## Evidence Goals

- `accepted_real_model_runs`
- `ai_engineer_review_items`
- `business_case_feedback_items`
- `confirmed_external_users`
- `external_feedback_items`
- `reproducible_feedback_items`

## Tasks

### review_uc_davis_ds_peer_demo

- Reviewer segment: UC Davis data science peer
- Status: `not_contacted`
- Counts toward: `external_feedback_items`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Claimable when: Counts only after a public GitHub issue is accepted by the evidence gate.

Could you spend 8 minutes trying my public Data Quality Agent demo and leave one GitHub issue with anything confusing, useful, or broken? The shortest route is the one-click evidence page: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. I am tracking feedback publicly instead of claiming users without proof.

Required public evidence:
- Public GitHub issue with demo path tried
- One concrete confusing, useful, or broken behavior
- Permission to count the issue as external feedback

Privacy boundary: Do not share raw customer data, secrets, private emails, addresses, API keys, or production rows. Use redacted screenshots, public demo links, synthetic CSVs, or short summaries only.

Permission rule: Reviewer must give explicit permission for the public GitHub issue to be counted as project feedback or usage evidence.

### review_student_swe_peer_demo

- Reviewer segment: student software engineer peer
- Status: `not_contacted`
- Counts toward: `external_feedback_items`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Claimable when: Counts toward feedback only after the issue names a reviewed project surface.

I am collecting public review evidence for a data-quality LLM agent project. If anyone can try the demo, please leave one GitHub issue with what worked, what broke, or what would make it more useful for real data workflows. Fastest path: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.

Required public evidence:
- Public GitHub issue with reviewed URL
- Specific product or engineering feedback
- Permission to count the issue as external feedback

Privacy boundary: Do not share raw customer data, secrets, private emails, addresses, API keys, or production rows. Use redacted screenshots, public demo links, synthetic CSVs, or short summaries only.

Permission rule: Reviewer must give explicit permission for the public GitHub issue to be counted as project feedback or usage evidence.

### review_local_replay_engineer

- Reviewer segment: engineer comfortable with Docker or local setup
- Status: `not_contacted`
- Counts toward: `reproducible_feedback_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md)
- Claimable when: Counts as reproducible feedback only after the reviewer confirms a local or container replay.

Could you clone my Data Quality Agent repo, run the local replay path, and submit whether the result was reproducible? Please avoid raw private data; a short redacted run summary is enough.

Required public evidence:
- Command or run path used
- Redacted result summary
- Whether the run was reproducible

Privacy boundary: Do not share raw customer data, secrets, private emails, addresses, API keys, or production rows. Use redacted screenshots, public demo links, synthetic CSVs, or short summaries only.

Permission rule: Reviewer must give explicit permission for the public GitHub issue to be counted as project feedback or usage evidence.

### review_confirmed_external_use

- Reviewer segment: reviewer who tried demo or local repo
- Status: `not_contacted`
- Counts toward: `confirmed_external_users`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-feedback-packet.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Claimable when: Counts as external use only after public confirmation names the path used.

If you already tried the Data Quality Agent demo or ran the repo locally, could you leave a short public note saying what path you used and whether the result was understandable? The one-click evidence page has the confirmed-use form: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html. I only count confirmed external use when it is public and specific.

Required public evidence:
- Public confirmation of demo or repo usage
- Path used
- Permission to count as confirmed external use

Privacy boundary: Do not share raw customer data, secrets, private emails, addresses, API keys, or production rows. Use redacted screenshots, public demo links, synthetic CSVs, or short summaries only.

Permission rule: Reviewer must give explicit permission for the public GitHub issue to be counted as project feedback or usage evidence.

### review_data_analyst_business_case

- Reviewer segment: data analyst or analytics student
- Status: `not_contacted`
- Counts toward: `business_case_feedback_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)
- Claimable when: Counts as a business case only after it includes an anonymized problem and impact description.

Do you have an anonymized data-quality problem this project should handle, such as duplicate IDs, stale exports, missing routing fields, or suspicious numeric values? A public business-case issue with no raw data would help me test real usefulness. The one-click evidence page is here: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.

Required public evidence:
- Anonymized business-data quality problem
- Expected business impact
- No private rows or sensitive fields

Privacy boundary: Do not share raw customer data, secrets, private emails, addresses, API keys, or production rows. Use redacted screenshots, public demo links, synthetic CSVs, or short summaries only.

Permission rule: Reviewer must give explicit permission for the public GitHub issue to be counted as project feedback or usage evidence.

### review_operator_business_case

- Reviewer segment: small-business operator or operations teammate
- Status: `not_contacted`
- Counts toward: `business_case_feedback_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-problem-casebook.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md)
- Claimable when: Counts only when a real workflow impact is described without exposing private data.

Do you have an anonymized data-quality problem this project should handle, such as duplicate IDs, stale exports, missing routing fields, or suspicious numeric values? A public business-case issue with no raw data would help me test real usefulness. The one-click evidence page is here: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.

Required public evidence:
- Workflow affected by data-quality failure
- What decision would be wrong if the data is bad
- Permission to count the anonymized case as business feedback

Privacy boundary: Do not share raw customer data, secrets, private emails, addresses, API keys, or production rows. Use redacted screenshots, public demo links, synthetic CSVs, or short summaries only.

Permission rule: Reviewer must give explicit permission for the public GitHub issue to be counted as project feedback or usage evidence.

### review_ai_engineer_agent_readiness

- Reviewer segment: AI engineer, mentor, or ML systems reviewer
- Status: `not_contacted`
- Counts toward: `ai_engineer_review_items`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/ai-engineer-review-intake.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md)
- Claimable when: Counts as AI Engineer review evidence only after the reviewer names an inspected path.

I am improving this project for AI Engineer internship applications. Could you review whether the LLM tool-calling loop, business-data connector, structured output, guardrails, and evidence trail look credible enough for an intern interview? If yes, please use the one-click evidence page or leave a public AI Engineer review issue with the path you inspected: https://sunnnn2005.github.io/data-quality-agent/one-click-evidence-links.html.

Required public evidence:
- Inspected LLM tool-calling or agent-readiness path
- Concrete AI Engineer credibility feedback
- Permission to count as AI Engineer review evidence

Privacy boundary: Do not share raw customer data, secrets, private emails, addresses, API keys, or production rows. Use redacted screenshots, public demo links, synthetic CSVs, or short summaries only.

Permission rule: Reviewer must give explicit permission for the public GitHub issue to be counted as project feedback or usage evidence.

### review_open_source_maintainer

- Reviewer segment: open-source maintainer or GitHub contributor
- Status: `not_contacted`
- Counts toward: `external_feedback_items`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)
- Claimable when: Counts as feedback only after the issue gives contributor-facing evidence.

Could you review whether this repo is understandable for an outside contributor? I am especially looking for feedback on README clarity, issue templates, evidence artifacts, and whether a first-time contributor could run the project.

Required public evidence:
- Public issue with contributor-readiness feedback
- One suggested improvement for README, setup, tests, or issue templates
- Permission to count the issue as external feedback

Privacy boundary: Do not share raw customer data, secrets, private emails, addresses, API keys, or production rows. Use redacted screenshots, public demo links, synthetic CSVs, or short summaries only.

Permission rule: Reviewer must give explicit permission for the public GitHub issue to be counted as project feedback or usage evidence.

### review_real_model_run_evidence

- Reviewer segment: AI engineer or developer willing to inspect a redacted real-model trace
- Status: `not_contacted`
- Counts toward: `accepted_real_model_runs`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/real-model-run-request-pack.md](https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/real-model-run-request-pack.md)
- Submission: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=real_model_run_review.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=real_model_run_review.md)
- Claimable when: Counts only after the real-model run request pack reaches at least 1 accepted redacted run.

I added a privacy-safe evidence path for a real OpenAI-compatible LLM agent run. Could you review the runbook, capture gate, and issue template, then help verify one redacted trace after I run it locally with credentials that are never shared?

Required public evidence:
- Accepted redacted real-model run issue
- Trace id, model name, prompt version, tool calls, latency, tokens, and estimated cost
- Final structured report verification result
- Permission to count the public issue as real-model LLM agent evidence

Privacy boundary: Do not share raw customer data, secrets, private emails, addresses, API keys, or production rows. Use redacted screenshots, public demo links, synthetic CSVs, or short summaries only.

Permission rule: Reviewer must give explicit permission for the public GitHub issue to be counted as project feedback or usage evidence.

## Resume-Safe Summary

Published a CI-verified reviewer action queue with 9 concrete outreach tasks mapped to 6 evidence goals and zero contacted or completed reviewers.

## Blocked Resume Claims

- active users
- customer feedback
- enterprise production usage
- earned GitHub stars beyond the current public count
- completed external reviews
- accepted real-model LLM runs
