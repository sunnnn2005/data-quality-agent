import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
ACCEPTED_EVIDENCE_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
REVIEWER_OUTREACH_EXECUTION_PACK_PATH = ROOT / "docs" / "reviewer-outreach-execution-pack.json"
GITHUB_TRAFFIC_SNAPSHOT_PATH = ROOT / "docs" / "github-traffic-snapshot.json"
REAL_MODEL_RUN_REQUEST_PACK_PATH = ROOT / "docs" / "real-model-run-request-pack.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-outcome-metrics.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-outcome-metrics.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _resume_status(count: int) -> str:
    return "claimable" if count > 0 else "not_claimable_yet"


def _outcome_metric(
    *,
    metric: str,
    current_count: int,
    evidence_url: str,
    resume_wording_when_claimable: str,
    blocked_reason: str,
) -> dict[str, Any]:
    status = _resume_status(current_count)
    return {
        "metric": metric,
        "current_count": current_count,
        "resume_status": status,
        "evidence_url": evidence_url,
        "resume_wording": resume_wording_when_claimable if status == "claimable" else None,
        "blocked_reason": None if status == "claimable" else blocked_reason,
    }


def build_resume_outcome_metrics() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    accepted = load_json(ACCEPTED_EVIDENCE_ROLLUP_PATH)
    outreach = load_json(REVIEWER_OUTREACH_EXECUTION_PACK_PATH)
    traffic = load_json(GITHUB_TRAFFIC_SNAPSHOT_PATH)
    real_model_pack = load_json(REAL_MODEL_RUN_REQUEST_PACK_PATH)

    accepted_counts = accepted["accepted_counts"]
    tracked_metrics = [
        _outcome_metric(
            metric="confirmed_external_users",
            current_count=accepted_counts["confirmed_external_users"],
            evidence_url="https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/accepted-evidence-rollup.md",
            resume_wording_when_claimable=(
                f"Collected {accepted_counts['confirmed_external_users']} confirmed external reviewer runs through a gated public evidence workflow."
            ),
            blocked_reason="Needs a non-owner public reviewer issue that passes the external evidence gate.",
        ),
        _outcome_metric(
            metric="external_feedback_items",
            current_count=accepted_counts["external_feedback_items"],
            evidence_url="https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/accepted-evidence-rollup.md",
            resume_wording_when_claimable=(
                f"Collected {accepted_counts['external_feedback_items']} public feedback items through GitHub issue templates."
            ),
            blocked_reason="Needs accepted public feedback with permission to count and non-placeholder comments.",
        ),
        _outcome_metric(
            metric="reproducible_feedback_items",
            current_count=accepted_counts["reproducible_feedback_items"],
            evidence_url="https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/accepted-evidence-rollup.md",
            resume_wording_when_claimable=(
                f"Verified {accepted_counts['reproducible_feedback_items']} reproducible external runs with command or URL evidence."
            ),
            blocked_reason="Needs reviewer-submitted command, URL, and observed-result evidence.",
        ),
        _outcome_metric(
            metric="business_case_feedback_items",
            current_count=accepted_counts["business_case_feedback_items"],
            evidence_url="https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/accepted-evidence-rollup.md",
            resume_wording_when_claimable=(
                f"Collected {accepted_counts['business_case_feedback_items']} anonymized business-case validations for data-quality workflows."
            ),
            blocked_reason="Needs anonymized business-case issue evidence with explicit permission to count.",
        ),
        _outcome_metric(
            metric="ai_engineer_review_items",
            current_count=accepted_counts["ai_engineer_review_items"],
            evidence_url="https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/accepted-evidence-rollup.md",
            resume_wording_when_claimable=(
                f"Collected {accepted_counts['ai_engineer_review_items']} public AI Engineer project reviews with inspected-path evidence."
            ),
            blocked_reason="Needs a non-owner AI Engineer review issue with inspected paths and permission to count.",
        ),
        _outcome_metric(
            metric="github_stars",
            current_count=adoption["stars"],
            evidence_url="https://github.com/sunnnn2005/data-quality-agent/stargazers",
            resume_wording_when_claimable=f"Earned {adoption['stars']} GitHub stars for a public LLM data-quality agent.",
            blocked_reason="Needs public GitHub stars above zero; never buy, trade, or fake stars.",
        ),
        _outcome_metric(
            metric="accepted_real_model_runs",
            current_count=real_model_pack["current_real_model_runs"],
            evidence_url="https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/real-model-run-request-pack.md",
            resume_wording_when_claimable=(
                f"Captured {real_model_pack['current_real_model_runs']} accepted OpenAI-compatible LLM agent run with redacted public telemetry."
            ),
            blocked_reason="Needs one accepted redacted real-model run issue with tool calls, tokens, latency, cost, and verification evidence.",
        ),
    ]

    claimable_metrics = [item for item in tracked_metrics if item["resume_status"] == "claimable"]
    blocked_metrics = [item for item in tracked_metrics if item["resume_status"] != "claimable"]
    public_interest_signals = {
        "github_stars": adoption["stars"],
        "github_forks": adoption["forks"],
        "github_views_14_day": traffic["views"]["count"],
        "github_unique_visitors_14_day": traffic["views"]["uniques"],
        "github_clones_14_day": traffic["clones"]["count"],
        "github_unique_cloners_14_day": traffic["clones"]["uniques"],
        "issue_count": adoption["issues_total"],
            "feature_feedback_items": feedback["feature_feedback_items"],
            "accepted_real_model_runs": real_model_pack["current_real_model_runs"],
        }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_resume_outcome_metrics.py",
        "purpose": (
            "Convert public metrics, accepted evidence, and outreach readiness into resume-safe outcome wording "
            "without claiming users, feedback, business impact, or GitHub stars before evidence exists."
        ),
        "tracked_outcome_count": len(tracked_metrics),
        "claimable_outcome_count": len(claimable_metrics),
        "blocked_outcome_count": len(blocked_metrics),
        "tracked_outcomes": tracked_metrics,
        "public_interest_signals": public_interest_signals,
        "outreach_readiness": {
            "ready_message_count": outreach["ready_message_count"],
            "follow_up_rule_count": outreach["follow_up_rule_count"],
            "evidence_goal_count": outreach["evidence_goal_count"],
            "not_sent_count": outreach["send_status_counts"]["not_sent"],
            "resume_status": outreach["resume_status"],
        },
        "claimable_resume_lines": [item["resume_wording"] for item in claimable_metrics],
        "blocked_resume_lines": [
            {
                "metric": item["metric"],
                "blocked_reason": item["blocked_reason"],
            }
            for item in blocked_metrics
        ],
        "resume_safe_summary": (
            f"Published a CI-verified resume outcome metrics board tracking {len(tracked_metrics)} outcome metrics, "
            f"{len(claimable_metrics)} currently claimable outcome lines, {len(blocked_metrics)} blocked outcome lines, "
            f"{outreach['ready_message_count']} ready reviewer messages, and honest public-interest baselines."
        ),
        "not_claimed": [
            "No external users are claimed while confirmed_external_users is zero.",
            "No customer feedback is claimed while external_feedback_items is zero.",
            "No real business impact is claimed while business_case_feedback_items is zero.",
            "No GitHub star growth is claimed while github_stars is zero.",
            "No accepted real-model LLM run is claimed while accepted_real_model_runs is zero.",
            "GitHub traffic is treated as repository interest, not as users.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    outcome_rows = "\n".join(
        "| {metric} | {count} | `{status}` | {wording} | {blocked} | {url} |".format(
            metric=item["metric"],
            count=item["current_count"],
            status=item["resume_status"],
            wording=item["resume_wording"] or "-",
            blocked=item["blocked_reason"] or "-",
            url=f"[evidence]({item['evidence_url']})",
        )
        for item in payload["tracked_outcomes"]
    )
    interest_rows = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["public_interest_signals"].items()
    )
    outreach_rows = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["outreach_readiness"].items()
    )
    claimable_lines = "\n".join(f"- {item}" for item in payload["claimable_resume_lines"]) or "- None yet"
    blocked_lines = "\n".join(
        f"- `{item['metric']}`: {item['blocked_reason']}" for item in payload["blocked_resume_lines"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Resume Outcome Metrics

This generated board keeps real outcome claims separate from readiness signals.

## Summary

| Metric | Value |
| --- | ---: |
| Tracked outcomes | {payload["tracked_outcome_count"]} |
| Claimable outcome lines | {payload["claimable_outcome_count"]} |
| Blocked outcome lines | {payload["blocked_outcome_count"]} |

## Tracked Outcomes

| Metric | Count | Resume Status | Resume Wording | Blocked Reason | Evidence |
| --- | ---: | --- | --- | --- | --- |
{outcome_rows}

## Public Interest Signals

| Metric | Value |
| --- | ---: |
{interest_rows}

## Outreach Readiness

| Metric | Value |
| --- | ---: |
{outreach_rows}

## Claimable Resume Lines

{claimable_lines}

## Blocked Resume Lines

{blocked_lines}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_resume_outcome_metrics(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["tracked_outcome_count"] != 7:
        raise AssertionError("resume outcome metrics must track seven outcome metrics")
    if payload["claimable_outcome_count"] != 0:
        raise AssertionError("resume outcome metrics must not mark zero-count outcomes as claimable")
    if payload["blocked_outcome_count"] != 7:
        raise AssertionError("resume outcome metrics must block all seven zero-count outcome claims")
    outcomes = {item["metric"]: item for item in payload["tracked_outcomes"]}
    required = {
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "github_stars",
        "accepted_real_model_runs",
    }
    if set(outcomes) != required:
        raise AssertionError("resume outcome metrics must cover user, feedback, replay, business, AI review, star, and real-model metrics")
    for metric in required:
        if outcomes[metric]["current_count"] != 0:
            raise AssertionError(f"{metric} must stay at zero until public evidence exists")
        if outcomes[metric]["resume_status"] != "not_claimable_yet":
            raise AssertionError(f"{metric} must not be claimable at zero")
        if not outcomes[metric]["blocked_reason"]:
            raise AssertionError(f"{metric} must explain why it is blocked")
    if payload["outreach_readiness"]["ready_message_count"] != 9:
        raise AssertionError("resume outcome metrics must link the 9-message outreach execution pack")
    if payload["outreach_readiness"]["not_sent_count"] != 9:
        raise AssertionError("resume outcome metrics must preserve the not-sent baseline")
    for required_phrase in (
        "No external users are claimed",
        "No customer feedback is claimed",
        "No real business impact is claimed",
        "No GitHub star growth is claimed",
        "No accepted real-model LLM run is claimed",
        "GitHub traffic is treated as repository interest, not as users.",
    ):
        if not any(required_phrase in item for item in payload["not_claimed"]):
            raise AssertionError(f"resume outcome metrics must preserve not-claimed phrase: {required_phrase}")
    return {
        "resume_outcome_metrics_verified": True,
        "tracked_outcome_count": payload["tracked_outcome_count"],
        "claimable_outcome_count": payload["claimable_outcome_count"],
        "blocked_outcome_count": payload["blocked_outcome_count"],
    }


def main() -> None:
    payload = build_resume_outcome_metrics()
    verify_resume_outcome_metrics(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
