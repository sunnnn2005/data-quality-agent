import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from app.models import DatasetProfile, LLMAssessment, QualityFinding


SENSITIVE_KEYS = {"email", "phone", "name", "address", "ssn", "token", "api_key"}


@dataclass
class LLMSettings:
    api_key: str | None = os.getenv("OPENAI_API_KEY")
    base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    timeout_seconds: float = float(os.getenv("LLM_TIMEOUT_SECONDS", "8"))
    max_retries: int = int(os.getenv("LLM_MAX_RETRIES", "2"))


class LLMDataQualityAdvisor:
    name = "llm_data_quality_advisor"

    def __init__(self, settings: LLMSettings | None = None) -> None:
        self.settings = settings or LLMSettings()

    @property
    def enabled(self) -> bool:
        return bool(self.settings.api_key)

    def assess(self, profile: DatasetProfile, findings: list[QualityFinding]) -> LLMAssessment:
        if not self.enabled:
            return LLMAssessment(error="OPENAI_API_KEY is not configured")

        prompt_payload = self._build_prompt_payload(profile, findings)
        body = {
            "model": self.settings.model,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a data reliability reviewer. Use only the provided JSON evidence. "
                        "Do not infer private values, credentials, or facts that are not present. "
                        "Return strict JSON with keys: summary, risk_level, evidence_used, suggested_actions."
                    ),
                },
                {"role": "user", "content": json.dumps(prompt_payload, sort_keys=True)},
            ],
        }

        result, latency_ms = self._post_with_retries(body)
        try:
            content = result["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            assessment = LLMAssessment(
                enabled=True,
                provider="openai-compatible",
                model=self.settings.model,
                summary=parsed.get("summary"),
                risk_level=parsed.get("risk_level"),
                evidence_used=list(parsed.get("evidence_used", []))[:8],
                suggested_actions=list(parsed.get("suggested_actions", []))[:6],
                cost_estimate_usd=self._estimate_cost(result.get("usage", {})),
                evaluation={
                    "latency_ms": latency_ms,
                    "findings_referenced": self._count_referenced_findings(parsed, findings),
                    "unsupported_claims": self._unsupported_claims(parsed, findings),
                },
            )
            return assessment
        except (KeyError, TypeError, json.JSONDecodeError, ValidationError) as exc:
            return LLMAssessment(
                enabled=True,
                provider="openai-compatible",
                model=self.settings.model,
                error=f"invalid structured model output: {exc.__class__.__name__}",
            )

    def _post_with_retries(self, body: dict[str, Any]) -> tuple[dict[str, Any], int]:
        url = self.settings.base_url.rstrip("/") + "/chat/completions"
        payload = json.dumps(body).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.settings.api_key}",
            "Content-Type": "application/json",
        }
        last_error: Exception | None = None
        started = time.monotonic()
        for attempt in range(self.settings.max_retries + 1):
            request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(request, timeout=self.settings.timeout_seconds) as response:
                    elapsed_ms = int((time.monotonic() - started) * 1000)
                    return json.loads(response.read().decode("utf-8")), elapsed_ms
            except (TimeoutError, urllib.error.URLError, urllib.error.HTTPError) as exc:
                last_error = exc
                if attempt >= self.settings.max_retries:
                    break
                time.sleep(min(2**attempt, 4))
        raise RuntimeError(f"LLM request failed after retries: {last_error}")

    def _build_prompt_payload(self, profile: DatasetProfile, findings: list[QualityFinding]) -> dict[str, Any]:
        return {
            "dataset": {
                "id": profile.dataset.id,
                "owner": profile.dataset.owner,
                "row_count": profile.row_count,
                "column_count": profile.column_count,
                "description": profile.dataset.description,
            },
            "columns": [
                {
                    "column": column.column,
                    "dtype": column.dtype,
                    "missing_rate": round(column.missing_rate, 4),
                    "unique_count": column.unique_count,
                    "sample_values": [self._redact(value) for value in column.sample_values[:3]],
                }
                for column in profile.columns
            ],
            "findings": [
                {
                    "check_name": finding.check_name,
                    "severity": finding.severity.value,
                    "column": finding.column,
                    "message": finding.message,
                    "evidence": self._redact(finding.evidence),
                    "recommendation": finding.recommendation,
                }
                for finding in findings
            ],
        }

    def _redact(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: "[REDACTED]" if key.lower() in SENSITIVE_KEYS else self._redact(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [self._redact(item) for item in value]
        return value

    def _estimate_cost(self, usage: dict[str, Any]) -> float | None:
        prompt_tokens = usage.get("prompt_tokens")
        completion_tokens = usage.get("completion_tokens")
        if not isinstance(prompt_tokens, int) or not isinstance(completion_tokens, int):
            return None
        return round((prompt_tokens * 0.00000015) + (completion_tokens * 0.0000006), 6)

    def _count_referenced_findings(self, parsed: dict[str, Any], findings: list[QualityFinding]) -> int:
        evidence_text = " ".join(str(item).lower() for item in parsed.get("evidence_used", []))
        return sum(1 for finding in findings if finding.check_name.lower() in evidence_text)

    def _unsupported_claims(self, parsed: dict[str, Any], findings: list[QualityFinding]) -> list[str]:
        allowed_terms = {finding.check_name.lower() for finding in findings}
        allowed_terms.update({"schema", "missing", "duplicate", "freshness", "outlier", "volume", "negative"})
        claims = []
        for item in parsed.get("evidence_used", []):
            text = str(item).lower()
            if not any(term in text for term in allowed_terms):
                claims.append(str(item))
        return claims[:5]
