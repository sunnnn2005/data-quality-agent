# Public Availability Snapshot

This generated artifact captures whether the public demo and evidence surfaces are reachable at snapshot time.

## Summary

| Metric | Value |
| --- | ---: |
| Available public endpoints | 4 / 4 |
| Successful main-branch workflows | 3 / 3 |
| Max observed endpoint latency | 250 ms |

## Public Endpoints

| Endpoint | Surface | Status | Available | Latency ms |
| --- | --- | ---: | --- | ---: |
| public_demo | GitHub Pages | 200 | True | 250 |
| reviewer_landing_page | GitHub Pages | 200 | True | 230 |
| openapi_contract | GitHub raw artifact | 200 | True | 229 |
| public_metrics | GitHub raw artifact | 200 | True | 212 |

## Workflow Health

| Check | Workflow | Status | Conclusion | Verified |
| --- | --- | --- | --- | --- |
| ci | test.yml | completed | success | True |
| public_evidence_health | public-evidence-health.yml | completed | success | True |
| container_publish | publish-image.yml | completed | success | True |

## Deployment Evidence

| Evidence | Surface | Status | Detail | URL |
| --- | --- | --- | --- | --- |
| public_demo_live | Public GitHub Pages demo | available | HTTP 200, latency 250 ms | https://sunnnn2005.github.io/data-quality-agent/ |
| ci_verified | Main-branch CI | success | test.yml | https://github.com/sunnnn2005/data-quality-agent/actions/runs/31823361701 |
| public_health_verified | Public evidence health | success | public-evidence-health.yml | https://github.com/sunnnn2005/data-quality-agent/actions/runs/31823361802 |
| container_publish_verified | Container publish workflow | success | publish-image.yml | https://github.com/sunnnn2005/data-quality-agent/actions/runs/31823361691 |

## Resume Policy

This snapshot proves public entrypoint reachability and recent workflow health only. Do not claim production uptime SLA, active users, customer adoption, or paid availability monitoring from this artifact.

## Resume-Safe Deployment Line

Published a public GitHub Pages demo with reachable project surfaces and passing CI, public evidence health, and container publish workflows at snapshot time.

## Resume-Safe Summary

Captured 4/4 reachable public project surfaces and 3/3 successful main-branch workflows in a generated availability snapshot.

## Not Claimed

- production uptime SLA
- active users
- customer adoption
- paid availability monitoring
