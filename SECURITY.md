# Security

Data Quality Agent is local-first and deterministic by default. It does not require secrets, production credentials, paid APIs, external databases, or private datasets.

## Supported Use

The default project is safe to run locally because it only reads bundled sample datasets.

## Reporting Issues

If you find a security issue, please open a GitHub issue with enough detail to reproduce it. Do not include secrets, private data, database credentials, or proprietary datasets in the report.

## Integration Guidelines

Future integrations should follow these rules:

- read-only by default
- no secrets committed to the repository
- no private data in examples, tests, or screenshots
- clear failure behavior when credentials or external services are unavailable
- tests that run without network access

## Out of Scope

Data Quality Agent is not a production warehouse governance system. It does not claim to safely operate on private datasets or production tables without additional integration work.
