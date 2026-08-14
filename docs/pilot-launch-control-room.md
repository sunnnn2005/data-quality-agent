# Pilot Launch Control Room

Centralize the public launch, pilot evidence links, issue threads, target metrics, and blocked resume claims so future outcome numbers can be earned from external evidence instead of self-authored notes.

Quicklink: [https://sunnnn2005.github.io/data-quality-agent/pilot-evidence-quicklink.html](https://sunnnn2005.github.io/data-quality-agent/pilot-evidence-quicklink.html)

## Public Issue Threads

| Thread | Purpose | Link |
| --- | --- | --- |
| `pilot_feedback_tracker` | track pilot outreach and evidence status | [Open](https://github.com/sunnnn2005/data-quality-agent/issues/16) |
| `first_public_feedback_request` | collect first external feedback | [Open](https://github.com/sunnnn2005/data-quality-agent/issues/17) |
| `external_run_evidence` | collect reviewer run evidence | [Open](https://github.com/sunnnn2005/data-quality-agent/issues/18) |
| `public_reviewer_call` | route external reviewers into countable evidence paths | [Open](https://github.com/sunnnn2005/data-quality-agent/issues/19) |

## Launch Gates

| Gate | Status | Evidence |
| --- | --- | --- |
| `public_demo_available` | `ready` | https://sunnnn2005.github.io/data-quality-agent/ |
| `container_available` | `ready` | {'image': 'ghcr.io/sunnnn2005/data-quality-agent:latest', 'package_url': 'https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent'} |
| `feedback_intake_available` | `ready` | https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md |
| `external_feedback_received` | `blocked` | 0 accepted non-owner public feedback issues |
| `business_case_received` | `blocked` | 0 accepted anonymized business-case issues |

## Target Outcomes

| Metric | Current | Target | Resume Upgrade Rule |
| --- | ---: | ---: | --- |
| `external_feedback_items` | 0 | 3 | Can claim external product feedback only after 3 accepted public issues. |
| `confirmed_external_users` | 0 | 1 | Can claim an external run only after one non-owner reviewer submits reproducible evidence. |
| `business_case_feedback_items` | 0 | 1 | Can claim business-problem validation only after one anonymized public case is accepted. |
| `github_stars` | 0 | 5 | Can claim early GitHub traction only after the public star count reaches 5. |

## Reviewer Send Plan

| Reviewer Slot | Action | Proof Required |
| --- | --- | --- |
| `classmate_or_student_developer` | send the pilot evidence quicklink and ask for one useful/confusing/broken observation | public issue with permission to count |
| `data_or_operations_reviewer` | ask for one anonymized data-quality problem the agent should handle | business-case issue with no raw private data |
| `ai_engineer_or_ml_reviewer` | ask whether the tool-calling loop, evidence trail, and guardrails look interview-credible | AI Engineer review issue with implementation path inspected |

## Resume-Safe Summary

Published a CI-verified pilot launch control room with 4 public issue threads, 5 launch gates, 4 target outcome metrics, and 3 reviewer-send paths while keeping external usage and feedback claims blocked at zero until public evidence arrives.

## Not Claimed

- external users
- customer feedback
- business validation
- GitHub traction beyond the current public count
