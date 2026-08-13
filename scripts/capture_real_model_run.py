import argparse
import json
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import quote
import urllib.request

from scripts.build_real_model_evidence_capture import (
    build_real_model_evidence_capture_payload,
    render_markdown,
    verify_real_model_evidence_capture,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON_PATH = ROOT / "docs" / "real-model-evidence-capture.json"
OUTPUT_MD_PATH = ROOT / "docs" / "real-model-evidence-capture.md"


class Transport(Protocol):
    def post(self, url: str, timeout: int):
        ...

    def get(self, url: str, timeout: int):
        ...


class UrllibResponse:
    def __init__(self, payload: bytes, status_code: int) -> None:
        self._payload = payload
        self.status_code = status_code

    def json(self) -> dict[str, Any]:
        return json.loads(self._payload.decode("utf-8"))

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class UrllibTransport:
    def post(self, url: str, timeout: int) -> UrllibResponse:
        request = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return UrllibResponse(response.read(), response.status)

    def get(self, url: str, timeout: int) -> UrllibResponse:
        request = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return UrllibResponse(response.read(), response.status)


def _verification_passed(report: dict[str, Any], trace: dict[str, Any]) -> bool:
    report_verification = (
        report.get("quality_report", {})
        .get("verification", {})
        .get("passed")
    )
    trace_summary_verification = trace.get("summary", {}).get("verification_passed")
    trace_eval_verification = trace.get("evaluation", {}).get("verification_passed")
    return any(value is True for value in (report_verification, trace_summary_verification, trace_eval_verification))


def build_capture_record(report: dict[str, Any], trace: dict[str, Any]) -> dict[str, Any]:
    evaluation = report.get("evaluation", {})
    return {
        "trace_id": report.get("trace_id") or trace.get("trace_id"),
        "provider": evaluation.get("provider"),
        "model": evaluation.get("model"),
        "prompt_version": evaluation.get("prompt_version"),
        "dataset_id": report.get("dataset", {}).get("id") or trace.get("dataset_id"),
        "model_call_count": evaluation.get("model_call_count"),
        "tool_call_count": evaluation.get("tool_call_count"),
        "distinct_tool_count": evaluation.get("distinct_tool_count"),
        "used_strategy_tool": evaluation.get("used_strategy_tool"),
        "used_required_report_tool": evaluation.get("used_required_report_tool"),
        "final_report_attached": evaluation.get("final_report_attached"),
        "total_tokens": evaluation.get("total_tokens"),
        "estimated_cost_usd": evaluation.get("estimated_cost_usd"),
        "latency_ms": evaluation.get("latency_ms"),
        "verification_passed": _verification_passed(report, trace),
        "redaction_status": "redacted",
        "raw_prompt_logged": False,
    }


def capture_real_model_run(
    *,
    base_url: str,
    dataset_id: str,
    timeout: int = 60,
    transport: Transport | None = None,
) -> dict[str, Any]:
    active_transport = transport or UrllibTransport()
    normalized_base = base_url.rstrip("/")
    encoded_dataset = quote(dataset_id, safe="")
    report_response = active_transport.post(
        f"{normalized_base}/datasets/{encoded_dataset}/agent-report",
        timeout=timeout,
    )
    report_response.raise_for_status()
    report = report_response.json()
    trace_id = report.get("trace_id")
    if not trace_id:
        raise RuntimeError("agent report did not include trace_id")

    trace_response = active_transport.get(f"{normalized_base}/runs/{quote(trace_id, safe='')}", timeout=timeout)
    trace_response.raise_for_status()
    trace = trace_response.json()
    record = build_capture_record(report, trace)
    payload = build_real_model_evidence_capture_payload(real_runs=[record])
    verify_real_model_evidence_capture(
        payload,
        expected_current_real_model_runs=payload["accepted_real_model_run_count"],
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture a redacted real LLM agent run from the local FastAPI API.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--dataset-id", default="orders_daily")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--write", action="store_true", help="Write docs/real-model-evidence-capture.json and .md")
    args = parser.parse_args()

    payload = capture_real_model_run(base_url=args.base_url, dataset_id=args.dataset_id, timeout=args.timeout)
    if args.write:
        OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
