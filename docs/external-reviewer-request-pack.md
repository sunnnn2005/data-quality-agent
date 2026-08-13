# External Reviewer Request Pack

This generated pack turns the public issue #18 evidence workflow into copy-ready outreach.

## Purpose

Provide copy-ready outreach messages that ask real reviewers to run one public path, then comment on issue #18 with enough evidence and permission to count the run later.

## Status

`outreach_ready_not_counted`

## Public Collection Issue

Issue #18: [https://github.com/sunnnn2005/data-quality-agent/issues/18](https://github.com/sunnnn2005/data-quality-agent/issues/18)

Public collection point for external reviewer run evidence.

## Current Counts

| Metric | Current value |
| --- | ---: |
| External Feedback Items | 0 |
| Confirmed External Users | 0 |
| Reproducible Feedback Items | 0 |

## Copy-Ready Messages

### classmate_public_demo -> UC Davis classmate or student developer

- Minutes: 8
- Run path: `public_demo_review`
- Entry: [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/)
- Collection issue: [https://github.com/sunnnn2005/data-quality-agent/issues/18](https://github.com/sunnnn2005/data-quality-agent/issues/18)

Could you spend 8 minutes trying my Data Quality Agent public demo, then leave a short comment on issue #18 with what worked, what was confusing, and whether I may count your review publicly? No private data needed.

### developer_container_smoke_run -> student developer comfortable with Docker

- Minutes: 12
- Run path: `container_smoke_run`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent)
- Collection issue: [https://github.com/sunnnn2005/data-quality-agent/issues/18](https://github.com/sunnnn2005/data-quality-agent/issues/18)

Could you run the GHCR container smoke test for my Data Quality Agent and comment on issue #18 with your OS, commands, observed result, and permission to count it publicly? The command is: docker run --rm -p 8000:8000 ghcr.io/sunnnn2005/data-quality-agent:latest

### mentor_postgres_replay -> mentor, data practitioner, or AI engineer

- Minutes: 15
- Run path: `postgres_replay_run`
- Entry: [https://github.com/sunnnn2005/data-quality-agent/blob/main/docker-compose.yml](https://github.com/sunnnn2005/data-quality-agent/blob/main/docker-compose.yml)
- Collection issue: [https://github.com/sunnnn2005/data-quality-agent/issues/18](https://github.com/sunnnn2005/data-quality-agent/issues/18)

Could you try the Docker Compose PostgreSQL replay for my read-only Data Quality Agent and comment on issue #18 with whether the seeded business-data run is reproducible and credible? Please do not upload private data; a redacted run summary is enough.

## Required Comment Fields

| Field | Required | Example |
| --- | --- | --- |
| reviewer_role | True | student developer, data analyst, recruiter, mentor |
| path_tried | True | public_demo_review or container_smoke_run |
| environment | True | macOS 15, Docker Desktop 4.x, Chrome |
| commands_or_urls_used | True | docker compose up --build |
| observed_result | True | health returned ok and support-ticket report loaded |
| usefulness_score_1_to_5 | True | 4 |
| main_feedback | True | setup was clear, but report explanation could be shorter |
| permission_to_count_publicly | True | yes |

## Counting Policy

- Only public comments on issue #18 or linked public issues can be counted.
- The reviewer must state which path they tried and whether permission to count publicly is yes.
- Self-authored local tests and planning notes remain excluded from external evidence counts.
- Counts stay at zero until a qualifying reviewer comment exists.

## Resume-Safe Summary

Published a copy-ready external reviewer request pack linked to issue #18 with 3 outreach messages, 3 run paths, 8 required evidence fields, permission-based counting rules, and a zero-count baseline.

## Not Claimed

- No outreach recipient has completed a run yet.
- No external reviewer run is claimed yet.
- No customer feedback is claimed yet.
- No enterprise deployment is claimed yet.
