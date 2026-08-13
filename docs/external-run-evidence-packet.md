# External Run Evidence Packet

This generated packet defines how an outside reviewer can run the project and submit evidence that is safe to count later.

## Purpose

Turn external reviewer runs into public, resume-safe evidence by requiring commands, environment, observed results, and permission before any user or feedback claim is counted.

## Reviewer Run Paths

| Path | Surface | Minutes | Command | Counts Toward After Public Issue |
| --- | --- | ---: | --- | --- |
| public_demo_review | public_demo | 8 | `-` | `external_feedback_items` |
| container_smoke_run | ghcr_container | 12 | `docker run --rm -p 8000:8000 ghcr.io/sunnnn2005/data-quality-agent:latest` | `confirmed_external_users` |
| postgres_replay_run | docker_compose_business_demo | 15 | `docker compose up --build` | `reproducible_feedback_items` |

Submission URL: [https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md](https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md)

Public collection issue: [#18](https://github.com/sunnnn2005/data-quality-agent/issues/18)

Counting status: `collection_open_not_counted_yet`

## Required Submission Fields

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

## Resume Upgrade Rules

| Future Claim | Metric | Minimum Public Count | Required Label |
| --- | --- | ---: | --- |
| tried by an external reviewer | `confirmed_external_users` | 1 | `confirmed-user` |
| collected external feedback | `external_feedback_items` | 3 | `feedback` |
| validated through reproducible local replay | `reproducible_feedback_items` | 1 | `reproducible` |

## Current Counts

| Metric | Current value |
| --- | ---: |
| External Feedback Items | 0 |
| Confirmed External Users | 0 |
| Reproducible Feedback Items | 0 |

## Privacy Boundaries

- Do not ask reviewers to upload private business data.
- Do not store raw reviewer datasets in this repository.
- Ask for anonymized field names, command output summaries, and screenshots only when safe.
- Count only public GitHub issues where the reviewer gave permission to count the run.

## Resume-Safe Summary

Published an external-run evidence packet and public collection issue defining 3 reviewer run paths, 8 required submission fields, 3 resume-upgrade rules, and privacy boundaries for converting future reviewer runs into public evidence.

## Not Claimed

- No external reviewer run is claimed yet.
- No external users are claimed yet.
- No customer feedback is claimed yet.
- No enterprise deployment is claimed yet.
