import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTCOME_SUMMARY_PATH = ROOT / "docs" / "outcome-summary.json"
AGENT_READINESS_PATH = ROOT / "docs" / "agent-readiness.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "public-metrics-summary.json"
OUTPUT_MD_PATH = ROOT / "docs" / "public-metrics-summary.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_public_metrics_summary() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    outcome = load_json(OUTCOME_SUMMARY_PATH)
    readiness = load_json(AGENT_READINESS_PATH)
    verified_outcomes = outcome["verified_outcomes"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_public_metrics_summary.py",
        "repo": adoption["repo"],
        "public_demo": adoption["public_demo"],
        "release": adoption["release"]["tagName"],
        "container_image": adoption["container_image"]["image"],
        "public_metrics": {
            "stars": adoption["stars"],
            "forks": adoption["forks"],
            "watchers": adoption["watchers"],
            "issues_total": adoption["issues_total"],
            "test_count": adoption["test_count"],
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        },
        "verified_project_outcomes": {
            "support_ticket_issue_categories": verified_outcomes["issue_category_count"],
            "support_ticket_findings": verified_outcomes["finding_count"],
            "recommended_actions": verified_outcomes["recommended_action_count"],
            "implemented_agent_capabilities": len(readiness["implemented"]),
            "partial_agent_capabilities": len(readiness["partial"]),
        },
        "feedback_channels": feedback["feedback_channels"],
        "resume_policy": (
            "Use public demo, release, CI, container, support-ticket outcomes, and readiness metrics now. "
            "Do not claim external users, customer feedback, or production adoption until corresponding public metrics are greater than zero."
        ),
        "resume_safe_signals": [
            f"Public demo and {adoption['release']['tagName']} release",
            f"{adoption['test_count']} passing CI tests",
            f"{verified_outcomes['issue_category_count']} support-ticket issue categories",
            f"{verified_outcomes['recommended_action_count']} evidence-backed remediation actions",
            f"{len(readiness['implemented'])} implemented LLM agent-readiness capabilities",
            f"{adoption['forks']} public fork and {adoption['stars']} public stars as current honest adoption baseline",
        ],
        "not_claimed": [
            "external users",
            "customer feedback",
            "enterprise production usage",
            "GitHub stars beyond the current public count",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    metrics = payload["public_metrics"]
    outcomes = payload["verified_project_outcomes"]
    channels = "\n".join(f"- [{item['name']}]({item['url']}) -> `{item['counts_toward']}`" for item in payload["feedback_channels"])
    signals = "\n".join(f"- {item}" for item in payload["resume_safe_signals"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Public Metrics Summary

This page collects public adoption, feedback, release, CI, and outcome metrics into one resume-safe artifact.

## Public Footprint

| Metric | Current value |
| --- | ---: |
| Stars | {metrics["stars"]} |
| Forks | {metrics["forks"]} |
| Watchers | {metrics["watchers"]} |
| GitHub issues | {metrics["issues_total"]} |
| Passing CI tests | {metrics["test_count"]} |
| External feedback items | {metrics["external_feedback_items"]} |
| Confirmed external users | {metrics["confirmed_external_users"]} |
| Reproducible feedback items | {metrics["reproducible_feedback_items"]} |

## Verified Project Outcomes

| Outcome | Current value |
| --- | ---: |
| Support-ticket issue categories | {outcomes["support_ticket_issue_categories"]} |
| Support-ticket findings | {outcomes["support_ticket_findings"]} |
| Recommended remediation actions | {outcomes["recommended_actions"]} |
| Implemented LLM agent-readiness capabilities | {outcomes["implemented_agent_capabilities"]} |
| Partial agent-readiness capabilities documented | {outcomes["partial_agent_capabilities"]} |

## Feedback Channels

{channels}

## Resume-Safe Signals

{signals}

## Not Claimed

{not_claimed}
"""


def verify_public_metrics_summary(payload: dict[str, Any]) -> dict[str, Any]:
    metrics = payload["public_metrics"]
    outcomes = payload["verified_project_outcomes"]
    expected_metrics = {
        "stars": 0,
        "forks": 1,
        "test_count": 55,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
    }
    for key, expected in expected_metrics.items():
        if metrics.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {metrics.get(key)!r}")
    expected_outcomes = {
        "support_ticket_issue_categories": 4,
        "recommended_actions": 5,
        "implemented_agent_capabilities": 6,
    }
    for key, expected in expected_outcomes.items():
        if outcomes.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {outcomes.get(key)!r}")
    for required in ("external users", "customer feedback", "enterprise production usage"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"public metrics summary must not claim {required}")
    return {"public_metrics_summary_verified": True, **expected_metrics, **expected_outcomes}


def main() -> None:
    payload = build_public_metrics_summary()
    verify_public_metrics_summary(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
