from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class Severity(str, Enum):
    low = "LOW"
    medium = "MEDIUM"
    high = "HIGH"
    critical = "CRITICAL"


class DatasetSummary(BaseModel):
    id: str
    name: str
    owner: str
    primary_key: str
    expected_columns: list[str]
    description: str
    last_loaded_at: datetime


class ColumnProfile(BaseModel):
    column: str
    dtype: str
    missing_count: int
    missing_rate: float
    unique_count: int
    sample_values: list[str]


class DatasetProfile(BaseModel):
    dataset: DatasetSummary
    row_count: int
    column_count: int
    columns: list[ColumnProfile]


class QualityFinding(BaseModel):
    check_name: str
    severity: Severity
    column: str | None = None
    message: str
    evidence: dict[str, Any]
    recommendation: str


class QualityReport(BaseModel):
    dataset: DatasetSummary
    generated_at: datetime
    quality_score: int = Field(ge=0, le=100)
    status: Literal["PASS", "WARN", "FAIL"]
    row_count: int
    findings: list[QualityFinding]
    likely_causes: list[str]
    recommended_next_steps: list[str]
    agent_trace: list[str]
