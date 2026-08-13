# Contributing

Thanks for your interest in Data Quality Agent.

Data Quality Agent is meant to stay small, deterministic, and easy to inspect. Contributions should make the dataset quality loop clearer, more realistic, or easier to test.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
```

## Development Workflow

1. Fork the repository.
2. Create a focused branch.
3. Make one small change.
4. Run `python -m pytest`.
5. Open a pull request with a short summary and test plan.

## Pull Requests

Please keep changes focused and include tests for new checks, API behavior, or dashboard behavior when relevant.

Good contribution areas:

- Add new quality checks
- Add new sample datasets
- Improve quality scoring
- Improve dashboard usability
- Expand tests and documentation

## Good First Issues

Beginner-friendly tasks are labeled `good first issue`. A good first PR should usually touch one of these areas:

- `app/data.py` for a new deterministic dataset
- `app/checks.py` for one small quality check
- `tests/` for one new behavior test
- `README.md` or `docs/` for documentation
- `app/dashboard.py` for a small UI improvement

## Demo Feedback

If you are not ready to contribute code, try the public demo or local API and open a `Demo feedback` issue. Useful feedback includes:

- whether the verified support-ticket result reproduced on your machine
- which part of the report was confusing
- what data-quality check would make the demo more realistic
- whether the Docker Compose PostgreSQL path worked
- screenshots, commands, or trace ids when something fails

The public adoption baseline lives in `docs/adoption-metrics.json`. Do not edit stars, forks, or feedback counts manually unless you are updating the file from a verified source such as the GitHub API.

## Design Constraints

- Keep default behavior local-only and deterministic.
- Do not add paid API requirements to the default path.
- Prefer typed Pydantic models over unstructured dictionaries for API contracts.
- Keep quality checks explicit and testable.
- Avoid large refactors unless they unlock a clear feature.

See [SECURITY.md](SECURITY.md) before adding integrations that touch external systems, credentials, or datasets.
