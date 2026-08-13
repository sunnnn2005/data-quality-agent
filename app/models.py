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


class BusinessRuleReference(BaseModel):
    rule_id: str
    source: str
    title: str
    text: str
    matched_checks: list[str] = Field(default_factory=list)


class RootCauseHypothesis(BaseModel):
    title: str
    confidence: float = Field(ge=0, le=1)
    supporting_checks: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    recommended_action: str


class LLMAssessment(BaseModel):
    enabled: bool = False
    provider: str = "disabled"
    model: str | None = None
    summary: str | None = None
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] | None = None
    evidence_used: list[str] = Field(default_factory=list)
    suggested_actions: list[str] = Field(default_factory=list)
    evaluation: dict[str, Any] = Field(default_factory=dict)
    cost_estimate_usd: float | None = None
    error: str | None = None


class AgentToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    result_preview: dict[str, Any] = Field(default_factory=dict)


class VerificationIssue(BaseModel):
    code: str
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    message: str


class ReportVerification(BaseModel):
    passed: bool
    issue_count: int
    evidence_support_rate: float
    checked_rules: list[str]
    issues: list[VerificationIssue] = Field(default_factory=list)


class AgentRunReport(BaseModel):
    trace_id: str | None = None
    dataset: DatasetSummary
    generated_at: datetime
    status: Literal["PASS", "WARN", "FAIL", "DISABLED", "ERROR"]
    final_answer: str
    tool_calls: list[AgentToolCall]
    quality_report: "QualityReport | None" = None
    evaluation: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class QualityReport(BaseModel):
    trace_id: str | None = None
    dataset: DatasetSummary
    generated_at: datetime
    quality_score: int = Field(ge=0, le=100)
    status: Literal["PASS", "WARN", "FAIL"]
    row_count: int
    findings: list[QualityFinding]
    business_rule_references: list[BusinessRuleReference] = Field(default_factory=list)
    likely_causes: list[str]
    root_cause_hypotheses: list[RootCauseHypothesis] = Field(default_factory=list)
    recommended_next_steps: list[str]
    llm_assessment: LLMAssessment = Field(default_factory=LLMAssessment)
    verification: ReportVerification | None = None
    agent_trace: list[str]


class StoredRunTrace(BaseModel):
    trace_id: str
    dataset_id: str
    dataset_name: str
    owner: str
    generated_at: datetime
    status: str
    report_type: Literal["quality_report", "agent_report"]
    summary: dict[str, Any] = Field(default_factory=dict)
    tool_calls: list[AgentToolCall] = Field(default_factory=list)
    evaluation: dict[str, Any] = Field(default_factory=dict)
    fallback_status: str | None = None
    error: str | None = None


class IncidentPatternMemory(BaseModel):
    pattern_id: str
    title: str
    recurrence_count: int
    supporting_checks: list[str] = Field(default_factory=list)
    evidence_trace_ids: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)


class DatasetMemorySummary(BaseModel):
    dataset_id: str
    trace_count: int
    latest_generated_at: datetime | None = None
    recurring_checks: list[str] = Field(default_factory=list)
    recurring_root_causes: list[str] = Field(default_factory=list)
    incident_patterns: list[IncidentPatternMemory] = Field(default_factory=list)
    recent_traces: list[StoredRunTrace] = Field(default_factory=list)
