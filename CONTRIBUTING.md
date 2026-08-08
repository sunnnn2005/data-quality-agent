# Contributing

Thanks for your interest in Data Quality Agent.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
```

## Pull Requests

Please keep changes focused and include tests for new checks, API behavior, or dashboard behavior when relevant.

Good contribution areas:

- Add new quality checks
- Add new sample datasets
- Improve quality scoring
- Improve dashboard usability
- Expand tests and documentation
