import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_GATE_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
ACCEPTED_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
PILOT_CONTROL_ROOM_PATH = ROOT / "docs" / "pilot-launch-control-room.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-outcome-adjudication.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-outcome-adjudication.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_resume_outcome_adjudication() -> dict[str, Any]:
    gate = load_json(EVIDENCE_GATE_PATH)
    rollup = load_json(ACCEPTED_ROLLUP_PATH)
    control_room = load_json(PILOT_CONTROL_ROOM_PATH)
    categories = [
        {
            "claim_category": "external users",
            "metric": "confirmed_external_users",
            "current_count": rollup["accepted_counts"]["confirmed_external_users"],
            "claimable": False,
            "unlock_condition": "one accepted non-owner external-run issue with runnable-path evidence and permission to count",
            "safe_current_wording": "No verified external users yet; project is public and runnable.",
        },
        {
            "claim_category": "customer feedback",
            "metric": "external_feedback_items",
            "current_count": rollup["accepted_counts"]["external_feedback_items"],
            "claimable": False,
            "unlock_condition": "three accepted non-owner feedback issues with concrete observations and permission to count",
            "safe_current_wording": "Feedback intake is public; no accepted external feedback has arrived yet.",
        },
        {
            "claim_category": "reproducible external run",
            "metric": "reproducible_feedback_items",
            "current_count": rollup["accepted_counts"]["reproducible_feedback_items"],
            "claimable": False,
            "unlock_condition": "one accepted reviewer issue containing command or URL evidence and observed result",
            "safe_current_wording": "CI and local tests verify reproducibility; no non-owner external run is counted yet.",
        },
        {
            "claim_category": "business validation",
            "metric": "business_case_feedback_items",
            "current_count": rollup["accepted_counts"]["business_case_feedback_items"],
            "claimable": False,
            "unlock_condition": "one accepted anonymized business-case issue with workflow, impact, fields, and permission to count",
            "safe_current_wording": "Business-case intake is ready; no accepted external business case exists yet.",
        },
        {
            "claim_category": "AI Engineer review",
            "metric": "ai_engineer_review_items",
            "current_count": rollup["accepted_counts"]["ai_engineer_review_items"],
            "claimable": False,
            "unlock_condition": "one accepted AI Engineer review issue with inspected implementation paths and permission to count",
            "safe_current_wording": "AI Engineer review intake is public; no accepted external AI review is counted yet.",
        },
    ]
    rejected_summary = [
        {
            "issue_number": item["issue_number"],
            "reason_count": len(item["failure_reasons"]),
            "top_reasons": item["failure_reasons"][:3],
        }
        for item in rollup["rejected_issue_summaries"]
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_resume_outcome_adjudication.py",
        "purpose": (
            "Translate public reviewer evidence-gate results into clear resume decisions: what can be claimed now, "
            "what remains blocked, and what public evidence would unlock each stronger outcome claim."
        ),
        "evaluated_issue_count": gate["evaluated_issue_count"],
        "accepted_issue_count": rollup["accepted_issue_count"],
        "rejected_issue_count": rollup["rejected_issue_count"],
        "claim_category_count": len(categories),
        "claimable_category_count": sum(1 for item in categories if item["claimable"]),
        "blocked_category_count": sum(1 for item in categories if not item["claimable"]),
        "categories": categories,
        "rejected_issue_summary_count": len(rejected_summary),
        "rejected_issue_summary": rejected_summary,
        "launch_control_room": {
            "public_issue_thread_count": control_room["public_issue_thread_count"],
            "target_outcome_count": control_room["target_outcome_count"],
            "reviewer_send_plan_count": control_room["reviewer_send_plan_count"],
        },
        "resume_safe_summary": (
            "Published a CI-verified resume outcome adjudication report covering 5 outcome categories, "
            "0 claimable external outcome categories, 5 blocked categories, and the exact public evidence required "
            "to unlock user, feedback, reproducible-run, business-validation, and AI-review resume claims."
        ),
        "not_claimed": [
            "external users",
            "customer feedback",
            "reproducible external usage",
            "business validation",
            "external AI Engineer review feedback",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    category_rows = "\n".join(
        "| {claim_category} | `{metric}` | {current_count} | {claimable} | {unlock_condition} | {safe_current_wording} |".format(
            **item
        )
        for item in payload["categories"]
    )
    rejected_rows = "\n".join(
        f"| #{item['issue_number']} | {item['reason_count']} | {', '.join(item['top_reasons'])} |"
        for item in payload["rejected_issue_summary"]
    )
    if not rejected_rows:
        rejected_rows = "| - | - | - |"
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Resume Outcome Adjudication

{payload["purpose"]}

## Current Decision

| Metric | Value |
| --- | ---: |
| Evaluated public issues | {payload["evaluated_issue_count"]} |
| Accepted public issues | {payload["accepted_issue_count"]} |
| Rejected public issues | {payload["rejected_issue_count"]} |
| Outcome categories | {payload["claim_category_count"]} |
| Claimable external categories | {payload["claimable_category_count"]} |
| Blocked external categories | {payload["blocked_category_count"]} |

## Claim Categories

| Claim Category | Metric | Current Count | Claimable | Unlock Condition | Safe Current Wording |
| --- | --- | ---: | --- | --- | --- |
{category_rows}

## Rejected Public Issues

| Issue | Failure Reasons | Top Reasons |
| --- | ---: | --- |
{rejected_rows}

## Launch Control Room Linkage

| Signal | Count |
| --- | ---: |
| Public issue threads | {payload["launch_control_room"]["public_issue_thread_count"]} |
| Target outcome metrics | {payload["launch_control_room"]["target_outcome_count"]} |
| Reviewer-send paths | {payload["launch_control_room"]["reviewer_send_plan_count"]} |

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_resume_outcome_adjudication(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["claim_category_count"] != 5:
        raise AssertionError("resume outcome adjudication must cover 5 external outcome categories")
    if payload["claimable_category_count"] != 0:
        raise AssertionError("resume outcome adjudication must not mark external outcomes claimable yet")
    if payload["blocked_category_count"] != 5:
        raise AssertionError("resume outcome adjudication must keep 5 categories blocked")
    if payload["accepted_issue_count"] != 0:
        raise AssertionError("resume outcome adjudication must preserve zero accepted public issues")
    if payload["launch_control_room"]["public_issue_thread_count"] != 4:
        raise AssertionError("resume outcome adjudication must link the 4 public issue threads")
    metrics = {item["metric"] for item in payload["categories"]}
    for metric in (
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
    ):
        if metric not in metrics:
            raise AssertionError(f"resume outcome adjudication missing metric: {metric}")
    for required in ("external users", "customer feedback", "business validation"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"resume outcome adjudication must not claim {required}")
    markdown = render_markdown(payload)
    for fragment in ("Resume Outcome Adjudication", "Claim Categories", "Unlock Condition"):
        if fragment not in markdown:
            raise AssertionError(f"resume outcome adjudication missing markdown fragment: {fragment}")
    return {
        "resume_outcome_adjudication_verified": True,
        "claim_category_count": payload["claim_category_count"],
        "blocked_category_count": payload["blocked_category_count"],
    }


def main() -> None:
    payload = build_resume_outcome_adjudication()
    verify_resume_outcome_adjudication(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
