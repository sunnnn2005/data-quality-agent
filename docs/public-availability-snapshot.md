# Public Availability Snapshot

This generated artifact captures whether the public demo and evidence surfaces are reachable at snapshot time.

## Summary

| Metric | Value |
| --- | ---: |
| Available public endpoints | 4 / 4 |
| Successful main-branch workflows | 2 / 3 |
| Max observed endpoint latency | 222 ms |

## Public Endpoints

| Endpoint | Surface | Status | Available | Latency ms |
| --- | --- | ---: | --- | ---: |
| public_demo | GitHub Pages | 200 | True | 202 |
| reviewer_landing_page | GitHub Pages | 200 | True | 215 |
| openapi_contract | GitHub raw artifact | 200 | True | 218 |
| public_metrics | GitHub raw artifact | 200 | True | 222 |

## Workflow Health

| Check | Workflow | Status | Conclusion | Verified |
| --- | --- | --- | --- | --- |
| ci | test.yml | completed | success | True |
| public_evidence_health | public-evidence-health.yml | completed | failure | False |
| container_publish | publish-image.yml | completed | success | True |

## Resume Policy

This snapshot proves public entrypoint reachability and recent workflow health only. Do not claim production uptime SLA, active users, customer adoption, or paid availability monitoring from this artifact.

## Resume-Safe Summary

Captured 4/4 reachable public project surfaces and 2/3 successful main-branch workflows in a generated availability snapshot.

## Not Claimed

- production uptime SLA
- active users
- customer adoption
- paid availability monitoring
