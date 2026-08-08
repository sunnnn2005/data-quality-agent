from datetime import timedelta

import pandas as pd

from app.data import NOW
from app.models import DatasetSummary, QualityFinding, Severity


class QualityCheckRunner:
    name = "quality_check_runner"

    def run(self, dataset: DatasetSummary, frame: pd.DataFrame) -> list[QualityFinding]:
        findings: list[QualityFinding] = []
        findings.extend(self._schema_checks(dataset, frame))
        findings.extend(self._missing_value_checks(frame))
        findings.extend(self._duplicate_key_check(dataset, frame))
        findings.extend(self._freshness_check(dataset))
        findings.extend(self._numeric_outlier_checks(frame))
        findings.extend(self._domain_checks(frame))
        findings.extend(self._volume_check(frame))
        return findings

    def _schema_checks(self, dataset: DatasetSummary, frame: pd.DataFrame) -> list[QualityFinding]:
        expected = set(dataset.expected_columns)
        actual = set(frame.columns)
        findings = []

        missing = sorted(expected - actual)
        if missing:
            findings.append(
                QualityFinding(
                    check_name="schema_required_columns",
                    severity=Severity.critical,
                    message="Required columns are missing from the dataset.",
                    evidence={"missing_columns": missing},
                    recommendation="Block downstream jobs and restore the expected schema before publishing.",
                )
            )

        unexpected = sorted(actual - expected)
        if unexpected:
            findings.append(
                QualityFinding(
                    check_name="schema_drift",
                    severity=Severity.medium,
                    message="Unexpected columns were detected, which may indicate upstream schema drift.",
                    evidence={"unexpected_columns": unexpected},
                    recommendation="Confirm whether the producer intentionally shipped new fields and update contracts if needed.",
                )
            )
        return findings

    def _missing_value_checks(self, frame: pd.DataFrame) -> list[QualityFinding]:
        findings = []
        for column in frame.columns:
            missing_rate = float(frame[column].isna().mean())
            if missing_rate >= 0.1:
                findings.append(
                    QualityFinding(
                        check_name="missing_values",
                        severity=Severity.high if missing_rate >= 0.3 else Severity.medium,
                        column=column,
                        message=f"{column} has an elevated missing-value rate.",
                        evidence={"missing_rate": round(missing_rate, 3), "missing_count": int(frame[column].isna().sum())},
                        recommendation=f"Trace null generation for {column} in the upstream transform or source API.",
                    )
                )
        return findings

    def _duplicate_key_check(self, dataset: DatasetSummary, frame: pd.DataFrame) -> list[QualityFinding]:
        if dataset.primary_key not in frame.columns:
            return []
        duplicate_count = int(frame[dataset.primary_key].duplicated().sum())
        if duplicate_count == 0:
            return []
        return [
            QualityFinding(
                check_name="duplicate_primary_key",
                severity=Severity.critical,
                column=dataset.primary_key,
                message="Primary key contains duplicate records.",
                evidence={"duplicate_count": duplicate_count},
                recommendation="Deduplicate by the latest event timestamp, add idempotent merge logic, and enforce a uniqueness constraint in the pipeline.",
            )
        ]

    def _freshness_check(self, dataset: DatasetSummary) -> list[QualityFinding]:
        age_hours = (NOW - dataset.last_loaded_at).total_seconds() / 3600
        if age_hours <= 24:
            return []
        return [
            QualityFinding(
                check_name="freshness_sla",
                severity=Severity.high,
                message="Dataset missed the 24-hour freshness SLA.",
                evidence={"age_hours": round(age_hours, 2), "last_loaded_at": dataset.last_loaded_at.isoformat()},
                recommendation="Check scheduler failures, upstream extract jobs, and warehouse load history.",
            )
        ]

    def _numeric_outlier_checks(self, frame: pd.DataFrame) -> list[QualityFinding]:
        findings = []
        numeric_columns = frame.select_dtypes(include="number").columns
        for column in numeric_columns:
            series = frame[column].dropna()
            if len(series) < 4:
                continue
            q1 = float(series.quantile(0.25))
            q3 = float(series.quantile(0.75))
            iqr = q3 - q1
            if iqr == 0:
                continue
            upper = q3 + 1.5 * iqr
            lower = q1 - 1.5 * iqr
            count = int(((series > upper) | (series < lower)).sum())
            if count:
                findings.append(
                    QualityFinding(
                        check_name="numeric_outliers",
                        severity=Severity.medium,
                        column=column,
                        message=f"{column} contains values outside the expected IQR band.",
                        evidence={"outlier_count": count, "lower_bound": round(lower, 2), "upper_bound": round(upper, 2)},
                        recommendation=f"Inspect source records for {column} and decide whether to cap, filter, or correct them.",
                    )
                )
        return findings

    def _domain_checks(self, frame: pd.DataFrame) -> list[QualityFinding]:
        findings = []
        for column in ["amount", "order_total", "lifetime_value"]:
            if column in frame.columns and (frame[column].dropna() < 0).any():
                findings.append(
                    QualityFinding(
                        check_name="negative_amount",
                        severity=Severity.high,
                        column=column,
                        message=f"{column} contains negative values.",
                        evidence={"negative_count": int((frame[column].dropna() < 0).sum())},
                        recommendation="Validate refund handling and separate credit events from positive payment facts.",
                    )
                )
        return findings

    def _volume_check(self, frame: pd.DataFrame) -> list[QualityFinding]:
        expected_minimum = 6
        if len(frame) >= expected_minimum:
            return []
        return [
            QualityFinding(
                check_name="volume_anomaly",
                severity=Severity.medium,
                message="Dataset row count is below the expected demo baseline.",
                evidence={"row_count": len(frame), "expected_minimum": expected_minimum},
                recommendation="Verify ingestion completeness and compare source row counts against the warehouse table.",
            )
        ]
