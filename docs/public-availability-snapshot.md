# Public Availability Snapshot

This generated artifact captures whether the public demo and evidence surfaces are reachable at snapshot time.

## Summary

| Metric | Value |
| --- | ---: |
| Available public endpoints | 4 / 4 |
| Successful main-branch workflows | 3 / 3 |
| Max observed endpoint latency | 3984 ms |

## Public Endpoints

| Endpoint | Surface | Status | Available | Latency ms |
| --- | --- | ---: | --- | ---: |
| public_demo | GitHub Pages | 200 | True | 3984 |
| reviewer_landing_page | GitHub Pages | 200 | True | 99 |
| openapi_contract | GitHub raw artifact | 200 | True | 89 |
| public_metrics | GitHub raw artifact | 200 | True | 194 |

## Workflow Health

| Check | Workflow | Status | Conclusion | Verified |
| --- | --- | --- | --- | --- |
| ci | test.yml | completed | success | True |
| public_evidence_health | public-evidence-health.yml | completed | success | True |
| container_publish | publish-image.yml | completed | success | True |

## Resume Policy

This snapshot proves public entrypoint reachability and recent workflow health only. Do not claim production uptime SLA, active users, customer adoption, or paid availability monitoring from this artifact.

## Resume-Safe Summary

Captured 4/4 reachable public project surfaces and 3/3 successful main-branch workflows in a generated availability snapshot.

## Not Claimed

- production uptime SLA
- active users
- customer adoption
- paid availability monitoring
