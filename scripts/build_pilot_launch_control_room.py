import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
PILOT_EVIDENCE_QUICKLINK_PATH = ROOT / "docs" / "pilot-evidence-quicklink.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "pilot-launch-control-room.json"
OUTPUT_MD_PATH = ROOT / "docs" / "pilot-launch-control-room.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_pilot_launch_control_room() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    quicklink = load_json(PILOT_EVIDENCE_QUICKLINK_PATH)
    repo = adoption["repo"]

    public_issue_threads = [
        {
            "id": "pilot_feedback_tracker",
            "purpose": "track pilot outreach and evidence status",
            "url": f"{repo}/issues/16",
        },
        {
            "id": "first_public_feedback_request",
            "purpose": "collect first external feedback",
            "url": f"{repo}/issues/17",
        },
        {
            "id": "external_run_evidence",
            "purpose": "collect reviewer run evidence",
            "url": f"{repo}/issues/18",
        },
        {
            "id": "public_reviewer_call",
            "purpose": "route external reviewers into countable evidence paths",
            "url": f"{repo}/issues/19",
        },
    ]
    launch_gates = [
        {
            "id": "public_demo_available",
            "status": "ready",
            "evidence": adoption["public_demo"],
        },
        {
            "id": "container_available",
            "status": "ready",
            "evidence": adoption["container_image"],
        },
        {
            "id": "feedback_intake_available",
            "status": "ready",
            "evidence": f"{repo}/issues/new?template=demo_feedback.md",
        },
        {
            "id": "external_feedback_received",
            "status": "blocked",
            "evidence": "0 accepted non-owner public feedback issues",
        },
        {
            "id": "business_case_received",
            "status": "blocked",
            "evidence": "0 accepted anonymized business-case issues",
        },
    ]
    target_outcomes = [
        {
            "metric": "external_feedback_items",
            "current": feedback["external_feedback_items"],
            "target": 3,
            "resume_upgrade": "Can claim external product feedback only after 3 accepted public issues.",
        },
        {
            "metric": "confirmed_external_users",
            "current": feedback["confirmed_external_users"],
            "target": 1,
            "resume_upgrade": "Can claim an external run only after one non-owner reviewer submits reproducible evidence.",
        },
        {
            "metric": "business_case_feedback_items",
            "current": feedback["business_case_feedback_items"],
            "target": 1,
            "resume_upgrade": "Can claim business-problem validation only after one anonymized public case is accepted.",
        },
        {
            "metric": "github_stars",
            "current": adoption["stars"],
            "target": 5,
            "resume_upgrade": "Can claim early GitHub traction only after the public star count reaches 5.",
        },
    ]
    reviewer_send_plan = [
        {
            "slot": "classmate_or_student_developer",
            "action": "send the pilot evidence quicklink and ask for one useful/confusing/broken observation",
            "proof_required": "public issue with permission to count",
        },
        {
            "slot": "data_or_operations_reviewer",
            "action": "ask for one anonymized data-quality problem the agent should handle",
            "proof_required": "business-case issue with no raw private data",
        },
        {
            "slot": "ai_engineer_or_ml_reviewer",
            "action": "ask whether the tool-calling loop, evidence trail, and guardrails look interview-credible",
            "proof_required": "AI Engineer review issue with implementation path inspected",
        },
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_pilot_launch_control_room.py",
        "purpose": (
            "Centralize the public launch, pilot evidence links, issue threads, target metrics, and blocked resume "
            "claims so future outcome numbers can be earned from external evidence instead of self-authored notes."
        ),
        "quicklink_public_url": quicklink["public_url"],
        "quicklink_action_count": quicklink["action_count"],
        "public_issue_thread_count": len(public_issue_threads),
        "public_issue_threads": public_issue_threads,
        "launch_gate_count": len(launch_gates),
        "launch_gates": launch_gates,
        "ready_gate_count": sum(gate["status"] == "ready" for gate in launch_gates),
        "blocked_gate_count": sum(gate["status"] == "blocked" for gate in launch_gates),
        "target_outcome_count": len(target_outcomes),
        "target_outcomes": target_outcomes,
        "reviewer_send_plan_count": len(reviewer_send_plan),
        "reviewer_send_plan": reviewer_send_plan,
        "current_claimable_external_outcomes": 0,
        "resume_safe_summary": (
            "Published a CI-verified pilot launch control room with 4 public issue threads, 5 launch gates, "
            "4 target outcome metrics, and 3 reviewer-send paths while keeping external usage and feedback "
            "claims blocked at zero until public evidence arrives."
        ),
        "not_claimed": [
            "external users",
            "customer feedback",
            "business validation",
            "GitHub traction beyond the current public count",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    issue_rows = "\n".join(
        f"| `{thread['id']}` | {thread['purpose']} | [Open]({thread['url']}) |"
        for thread in payload["public_issue_threads"]
    )
    gate_rows = "\n".join(
        f"| `{gate['id']}` | `{gate['status']}` | {gate['evidence']} |"
        for gate in payload["launch_gates"]
    )
    outcome_rows = "\n".join(
        f"| `{outcome['metric']}` | {outcome['current']} | {outcome['target']} | {outcome['resume_upgrade']} |"
        for outcome in payload["target_outcomes"]
    )
    send_rows = "\n".join(
        f"| `{plan['slot']}` | {plan['action']} | {plan['proof_required']} |"
        for plan in payload["reviewer_send_plan"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Pilot Launch Control Room

{payload["purpose"]}

Quicklink: [{payload["quicklink_public_url"]}]({payload["quicklink_public_url"]})

## Public Issue Threads

| Thread | Purpose | Link |
| --- | --- | --- |
{issue_rows}

## Launch Gates

| Gate | Status | Evidence |
| --- | --- | --- |
{gate_rows}

## Target Outcomes

| Metric | Current | Target | Resume Upgrade Rule |
| --- | ---: | ---: | --- |
{outcome_rows}

## Reviewer Send Plan

| Reviewer Slot | Action | Proof Required |
| --- | --- | --- |
{send_rows}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_pilot_launch_control_room(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["quicklink_action_count"] != 4:
        raise AssertionError("pilot launch control room must link to the 4-action quicklink")
    if payload["public_issue_thread_count"] != 4:
        raise AssertionError("pilot launch control room must track 4 public issue threads")
    if payload["launch_gate_count"] != 5:
        raise AssertionError("pilot launch control room must track 5 launch gates")
    if payload["ready_gate_count"] != 3:
        raise AssertionError("pilot launch control room must keep exactly 3 ready gates")
    if payload["blocked_gate_count"] != 2:
        raise AssertionError("pilot launch control room must keep outcome gates blocked until evidence exists")
    if payload["target_outcome_count"] != 4:
        raise AssertionError("pilot launch control room must track 4 target outcome metrics")
    if payload["reviewer_send_plan_count"] != 3:
        raise AssertionError("pilot launch control room must include 3 reviewer-send paths")
    if payload["current_claimable_external_outcomes"] != 0:
        raise AssertionError("pilot launch control room must not claim external outcomes yet")
    for metric in ("external_feedback_items", "confirmed_external_users", "business_case_feedback_items", "github_stars"):
        if metric not in {outcome["metric"] for outcome in payload["target_outcomes"]}:
            raise AssertionError(f"pilot launch control room missing target metric: {metric}")
    for required in ("external users", "customer feedback", "business validation"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"pilot launch control room must not claim {required}")
    markdown = render_markdown(payload)
    for fragment in ("Pilot Launch Control Room", "Public Issue Threads", "Launch Gates", "Target Outcomes"):
        if fragment not in markdown:
            raise AssertionError(f"pilot launch control room missing markdown fragment: {fragment}")
    return {
        "pilot_launch_control_room_verified": True,
        "public_issue_thread_count": payload["public_issue_thread_count"],
        "target_outcome_count": payload["target_outcome_count"],
    }


def main() -> None:
    payload = build_pilot_launch_control_room()
    verify_pilot_launch_control_room(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
