# Local Reviewer Demo

This generated artifact documents the reproducible local demo path for reviewers. It is verified from `docker-compose.yml` and `examples/postgres/init.sql`.

## One-Command Start

```bash
docker compose up --build
```

## Services

| Service Detail | Value |
| --- | --- |
| PostgreSQL image | `postgres:16-alpine` |
| API build context | `.` |
| PostgreSQL host port | `5433` |
| API host port | `8000` |

## Read-Only Database

| Field | Value |
| --- | --- |
| Database | `quality_demo` |
| Owner user | `quality_owner` |
| Read-only user | `readonly_agent` |

## Seeded Business Table

`support_tickets` has 8 seeded rows with known quality cases:

- duplicate ticket_id
- missing team
- missing priority
- negative amount
- amount outlier

## Reviewer Routes

| Route | Method | Path | Command |
| --- | --- | --- | --- |
| Deterministic PostgreSQL quality report | `POST` | `/postgres/support-tickets/quality-report` | `curl -X POST http://127.0.0.1:8000/postgres/support-tickets/quality-report` |
| LLM agent route with safe disabled fallback | `POST` | `/postgres/support-tickets/agent-report` | `curl -X POST http://127.0.0.1:8000/postgres/support-tickets/agent-report` |
| Interactive FastAPI docs | `GET` | `/docs` | `open http://127.0.0.1:8000/docs` |

## Resume-Safe Summary

Published a Docker Compose reviewer demo with a seeded PostgreSQL table, read-only database user, and 3 local review paths for reproducing quality and agent reports.

## Not Claimed

- No hosted production database is claimed.
- No external reviewer completion is claimed.
- No customer deployment is claimed.
