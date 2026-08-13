# Runnable Release Packet

This generated artifact gives reviewers the shortest path to verify that the project is shipped as a runnable system.

## Runnable Surfaces

| Surface | Type | URL | Command |
| --- | --- | --- | --- |
| public_demo | hosted_static_demo | [https://sunnnn2005.github.io/data-quality-agent/](https://sunnnn2005.github.io/data-quality-agent/) | `-` |
| ghcr_container | container_image | [https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent](https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent) | `docker run --rm -p 8000:8000 ghcr.io/sunnnn2005/data-quality-agent:latest` |
| docker_compose_business_demo | local_postgres_plus_api | [https://github.com/sunnnn2005/data-quality-agent/blob/main/docker-compose.yml](https://github.com/sunnnn2005/data-quality-agent/blob/main/docker-compose.yml) | `docker compose up --build` |

## Acceptance Checks

| Check | Command | Expected |
| --- | --- | --- |
| Health check | `curl http://127.0.0.1:8000/health` | {"status":"ok","service":"data-quality-agent"} |
| Deterministic built-in report | `curl -X POST http://127.0.0.1:8000/datasets/orders_daily/quality-report` | QualityReport JSON with evidence-backed findings and verification metadata |
| Read-only PostgreSQL report | `curl -X POST http://127.0.0.1:8000/postgres/support-tickets/quality-report` | Report over 8 seeded support-ticket rows with duplicate, missing, negative, and outlier findings |
| LLM agent fallback route | `curl -X POST http://127.0.0.1:8000/postgres/support-tickets/agent-report` | Structured DISABLED fallback when OPENAI_API_KEY is not configured |

## OpenAPI Coverage

Published path count: 14

Required runnable paths:

- `/health`
- `/datasets/{dataset_id}/quality-report`
- `/datasets/{dataset_id}/agent-report`
- `/business-data/agent-report`
- `/postgres/support-tickets/agent-report`
- `/runs/{trace_id}`

## Resume-Safe Summary

Published a runnable release packet covering a public demo, GHCR container command, Docker Compose PostgreSQL demo, 4 acceptance checks, and a CI-verified OpenAPI surface.

## Not Claimed

- No package download count is claimed.
- No external installs are claimed.
- No production deployment is claimed.
- No customer usage is claimed.
