import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
RESUME_OUTCOME_METRICS_PATH = ROOT / "docs" / "resume-outcome-metrics.json"
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-submission-hub.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-submission-hub.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _channel_url(feedback: dict[str, Any], name: str) -> str:
    for channel in feedback["feedback_channels"]:
        if channel["name"] == name:
            return channel["url"]
    raise KeyError(name)


def build_reviewer_submission_hub() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    outcome_metrics = load_json(RESUME_OUTCOME_METRICS_PATH)
    adoption = load_json(ADOPTION_METRICS_PATH)
    repo = adoption["repo"]
    links = {
        "demo": adoption["public_demo"],
        "external_run_quickstart": "https://sunnnn2005.github.io/data-quality-agent/external-run-quickstart.html",
        "github_repo": repo,
        "business_case_intake": f"{repo}/blob/main/docs/business-case-intake.md",
        "ai_engineer_review_intake": f"{repo}/blob/main/docs/ai-engineer-review-intake.md",
        "real_model_run_request_pack": f"{repo}/blob/main/docs/real-model-run-request-pack.md",
    }
    external_run_url = f"{repo}/issues/new?template=external_run_review.md"
    business_data_replay_url = f"{repo}/issues/new?template=business_data_replay.md"
    real_model_run_url = f"{repo}/issues/new?template=real_model_run_review.md"
    submission_paths = [
        {
            "id": "try_public_demo",
            "target_metric": "external_feedback_items",
            "minimum_minutes": 5,
            "review_path": links["demo"],
            "submission_url": _channel_url(feedback, "Demo feedback"),
            "required_evidence": [
                "path tried",
                "what was useful",
                "what was confusing",
                "permission to count publicly",
            ],
            "counting_rule": "Counts only after a non-owner public issue grants permission and passes the evidence gate.",
        },
        {
            "id": "confirm_external_run",
            "target_metric": "confirmed_external_users",
            "minimum_minutes": 8,
            "review_path": links["external_run_quickstart"],
            "submission_url": external_run_url,
            "required_evidence": [
                "command or URL used",
                "observed result",
                "environment",
                "permission to count public run evidence",
            ],
            "counting_rule": "Counts only when the reviewer ran or opened a runnable path and submitted observed-result evidence.",
        },
        {
            "id": "submit_reproducible_issue",
            "target_metric": "reproducible_feedback_items",
            "minimum_minutes": 10,
            "review_path": links["github_repo"],
            "submission_url": business_data_replay_url,
            "required_evidence": [
                "command or endpoint used",
                "dataset shape",
                "report status and finding count",
                "selected tools shown in the agent trace",
                "what the agent caught or missed",
            ],
            "counting_rule": (
                "Counts only when a non-owner submits a sanitized business-data replay issue with run evidence, "
                "agent trace summary, and permission to count publicly."
            ),
        },
        {
            "id": "submit_business_case",
            "target_metric": "business_case_feedback_items",
            "minimum_minutes": 12,
            "review_path": links["business_case_intake"],
            "submission_url": _channel_url(feedback, "Business case review"),
            "required_evidence": [
                "anonymized workflow",
                "data-quality problem",
                "business impact",
                "project evidence mapping",
                "permission to count anonymized case",
            ],
            "counting_rule": "Counts only when the business case is anonymized, permissioned, and contains no raw production data.",
        },
        {
            "id": "submit_ai_engineer_review",
            "target_metric": "ai_engineer_review_items",
            "minimum_minutes": 12,
            "review_path": links["ai_engineer_review_intake"],
            "submission_url": _channel_url(feedback, "AI Engineer review"),
            "required_evidence": [
                "inspected implementation paths",
                "strongest AI-agent signal",
                "weakest AI-agent gap",
                "permission to count public AI Engineer feedback",
            ],
            "counting_rule": "Counts only when an external reviewer inspects implementation evidence and grants permission.",
        },
        {
            "id": "submit_real_model_run",
            "target_metric": "accepted_real_model_runs",
            "minimum_minutes": 15,
            "review_path": links["real_model_run_request_pack"],
            "submission_url": real_model_run_url,
            "required_evidence": [
                "model provider and model name",
                "trace id and prompt version",
                "selected tool names or tool-call count",
                "total tokens",
                "estimated cost",
                "latency",
                "verification status",
                "permission to count redacted run evidence",
            ],
            "counting_rule": (
                "Counts only when a redacted real-model issue includes provider, model, tool calls, token, cost, "
                "latency, verification evidence, and permission to count publicly."
            ),
        },
        {
            "id": "star_or_fork_if_useful",
            "target_metric": "github_stars",
            "minimum_minutes": 1,
            "review_path": repo,
            "submission_url": f"{repo}/stargazers",
            "required_evidence": [
                "public GitHub star count above zero",
                "no paid, traded, or fake engagement",
            ],
            "counting_rule": "Counts only from GitHub public star data; never asks for fake engagement.",
        },
    ]
    tracked_status = {
        item["metric"]: {
            "current_count": item["current_count"],
            "resume_status": item["resume_status"],
            "blocked_reason": item["blocked_reason"],
        }
        for item in outcome_metrics["tracked_outcomes"]
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_submission_hub.py",
        "purpose": (
            "Give reviewers one short public hub for submitting evidence that can turn zero-count resume outcomes "
            "into evidence-backed claims after the external evidence gate accepts them."
        ),
        "submission_path_count": len(submission_paths),
        "submission_paths": submission_paths,
        "target_metric_count": len({path["target_metric"] for path in submission_paths}),
        "total_required_evidence_fields": sum(len(path["required_evidence"]) for path in submission_paths),
        "tracked_outcome_status": tracked_status,
        "resume_status": "collection_ready_not_claimable",
        "not_claimed": outcome_metrics["not_claimed"],
        "resume_safe_summary": (
            "Published a CI-verified reviewer submission hub with 7 public submission paths, 7 tracked outcome metrics, "
            "32 required evidence fields, and zero current outcome claims upgraded."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    path_rows = "\n".join(
        "| {id} | `{target_metric}` | {minimum_minutes} | [Review]({review_path}) | [Submit]({submission_url}) | {counting_rule} |".format(
            **path
        )
        for path in payload["submission_paths"]
    )
    evidence_sections = "\n\n".join(
        "### {id}\n\n".format(**path)
        + "\n".join(f"- {field}" for field in path["required_evidence"])
        for path in payload["submission_paths"]
    )
    status_rows = "\n".join(
        "| {metric} | {current_count} | `{resume_status}` | {blocked_reason} |".format(metric=metric, **status)
        for metric, status in payload["tracked_outcome_status"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Reviewer Submission Hub

This generated hub gives external reviewers one short path to submit public evidence.

## Purpose

{payload["purpose"]}

## Submission Paths

| Path | Target Metric | Minutes | Review Path | Submit Evidence | Counting Rule |
| --- | --- | ---: | --- | --- | --- |
{path_rows}

## Required Evidence Fields

{evidence_sections}

## Current Outcome Status

| Metric | Current Count | Resume Status | Blocked Reason |
| --- | ---: | --- | --- |
{status_rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_reviewer_submission_hub(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["submission_path_count"] != 7:
        raise AssertionError("reviewer submission hub must define seven submission paths")
    if payload["target_metric_count"] != 7:
        raise AssertionError("reviewer submission hub must cover seven outcome metrics")
    if payload["total_required_evidence_fields"] != 32:
        raise AssertionError("reviewer submission hub must track 32 required evidence fields")
    if payload["resume_status"] != "collection_ready_not_claimable":
        raise AssertionError("reviewer submission hub must not upgrade resume outcomes by itself")
    required_metrics = {
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "accepted_real_model_runs",
        "github_stars",
    }
    actual_metrics = {path["target_metric"] for path in payload["submission_paths"]}
    if actual_metrics != required_metrics:
        raise AssertionError("reviewer submission hub must map every outcome metric to a public path")
    for path in payload["submission_paths"]:
        if not path["review_path"].startswith("https://"):
            raise AssertionError("reviewer submission paths must be public URLs")
        if not path["submission_url"].startswith("https://github.com/"):
            raise AssertionError("reviewer submission URLs must use public GitHub surfaces")
        if not path["required_evidence"]:
            raise AssertionError("reviewer submission paths must define required evidence")
        if "Counts only" not in path["counting_rule"]:
            raise AssertionError("reviewer submission paths must include conservative counting rules")
    for metric, status in payload["tracked_outcome_status"].items():
        if metric in required_metrics:
            if status["current_count"] != 0:
                raise AssertionError(f"{metric} must stay at zero until public evidence exists")
            if status["resume_status"] != "not_claimable_yet":
                raise AssertionError(f"{metric} must stay blocked at zero")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in (
        "business_data_replay.md",
        "selected tools shown in the agent trace",
        "permission",
        "evidence gate",
        "no raw production data",
        "never asks for fake engagement",
    ):
        if required not in joined:
            raise AssertionError(f"reviewer submission hub missing safety phrase: {required}")
    return {
        "reviewer_submission_hub_verified": True,
        "submission_path_count": payload["submission_path_count"],
        "target_metric_count": payload["target_metric_count"],
        "total_required_evidence_fields": payload["total_required_evidence_fields"],
    }


def main() -> None:
    payload = build_reviewer_submission_hub()
    verify_reviewer_submission_hub(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
