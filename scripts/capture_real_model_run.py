import argparse
import json
import mimetypes
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import quote
import urllib.request
from uuid import uuid4

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

    def post_multipart(self, url: str, fields: dict[str, str], files: dict[str, Path], timeout: int):
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

    def post_multipart(self, url: str, fields: dict[str, str], files: dict[str, Path], timeout: int) -> UrllibResponse:
        boundary = f"----data-quality-agent-{uuid4().hex}"
        body = _encode_multipart(fields, files, boundary)
        request = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return UrllibResponse(response.read(), response.status)

    def get(self, url: str, timeout: int) -> UrllibResponse:
        request = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return UrllibResponse(response.read(), response.status)


def _encode_multipart(fields: dict[str, str], files: dict[str, Path], boundary: str) -> bytes:
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                str(value).encode("utf-8"),
                b"\r\n",
            ]
        )
    for name, path in files.items():
        filename = path.name
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                (
                    f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
                    f"Content-Type: {content_type}\r\n\r\n"
                ).encode("utf-8"),
                path.read_bytes(),
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks)


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
    csv_path: Path | None = None,
    dataset_name: str = "Business Replay Dataset",
    owner: str = "reviewer",
    primary_key: str = "id",
    expected_columns: str | None = None,
    description: str | None = None,
    timeout: int = 60,
    transport: Transport | None = None,
) -> dict[str, Any]:
    active_transport = transport or UrllibTransport()
    normalized_base = base_url.rstrip("/")
    if csv_path is None:
        encoded_dataset = quote(dataset_id, safe="")
        report_response = active_transport.post(
            f"{normalized_base}/datasets/{encoded_dataset}/agent-report",
            timeout=timeout,
        )
    else:
        fields = {
            "dataset_name": dataset_name,
            "owner": owner,
            "primary_key": primary_key,
        }
        if expected_columns:
            fields["expected_columns"] = expected_columns
        if description:
            fields["description"] = description
        report_response = active_transport.post_multipart(
            f"{normalized_base}/business-data/agent-report",
            fields=fields,
            files={"file": csv_path},
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
    parser.add_argument("--csv-path", type=Path, help="Optional anonymized business CSV to send to /business-data/agent-report")
    parser.add_argument("--dataset-name", default="Business Replay Dataset")
    parser.add_argument("--owner", default="reviewer")
    parser.add_argument("--primary-key", default="id")
    parser.add_argument("--expected-columns")
    parser.add_argument("--description")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--write", action="store_true", help="Write docs/real-model-evidence-capture.json and .md")
    args = parser.parse_args()

    payload = capture_real_model_run(
        base_url=args.base_url,
        dataset_id=args.dataset_id,
        csv_path=args.csv_path,
        dataset_name=args.dataset_name,
        owner=args.owner,
        primary_key=args.primary_key,
        expected_columns=args.expected_columns,
        description=args.description,
        timeout=args.timeout,
    )
    if args.write:
        OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
