# Roadmap

Data Quality Agent is intentionally small, but it should grow in directions that make the quality loop more realistic and easier to extend.

## Near Term

- Add more deterministic dataset scenarios.
- Add markdown export for quality reports.
- Add YAML or JSON dataset contracts.
- Add tests for empty datasets and missing primary keys.
- Document how to add a new quality check.

## Medium Term

- Add configurable severity rules per column.
- Add historical baselines for volume and distribution drift.
- Add CSV upload support for local files.
- Add dashboard filters by severity and check type.
- Add JSON export for data incident automation.

## Long Term

- Add read-only warehouse adapters.
- Support saved report history.
- Add plugin-style check registration.
- Add baseline comparison across multiple runs.

## Contribution Notes

Good roadmap issues should stay small enough to review in one pull request. If a feature touches multiple layers, split it into a model/check PR, agent PR, and dashboard PR.
