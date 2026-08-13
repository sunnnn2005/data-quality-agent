import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PILOT_OUTREACH_PATH = ROOT / "docs" / "pilot-outreach-kit.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "pilot-program-plan.json"
OUTPUT_MD_PATH = ROOT / "docs" / "pilot-program-plan.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_pilot_program_plan_payload() -> dict[str, Any]:
    outreach = load_json(PILOT_OUTREACH_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_pilot_program_plan.py",
        "objective": (
            "Run a small public pilot to turn the current zero-feedback baseline into verified public feedback, "
            "while keeping resume claims tied to GitHub issues and metrics artifacts."
        ),
        "pilot_window": "3 weeks",
        "participant_segments": [
            {
                "segment": "student_reviewers",
                "target_count": 5,
                "source": "UC Davis classmates or data/AI club members",
                "requested_action": "Try the public demo and leave one feedback issue.",
            },
            {
                "segment": "developer_reviewers",
                "target_count": 3,
                "source": "student developers or open-source reviewers",
                "requested_action": "Run the repo locally or inspect the API contract and leave a bug or feature issue.",
            },
            {
                "segment": "career_reviewers",
                "target_count": 2,
                "source": "recruiters, mentors, or hiring managers",
                "requested_action": "Review the evidence pack and comment on project clarity for AI Engineer Intern roles.",
            },
        ],
        "weekly_plan": [
            {
                "week": 1,
                "focus": "Send outreach and collect first impressions.",
                "deliverable": "At least one public feedback issue or a documented zero-response checkpoint.",
            },
            {
                "week": 2,
                "focus": "Ask reviewers to reproduce one demo path or local run path.",
                "deliverable": "Bug, feature, or reproducibility feedback labeled in GitHub issues.",
            },
            {
                "week": 3,
                "focus": "Triage feedback, implement one small improvement, and update metrics.",
                "deliverable": "A public changelog entry linking feedback to a resolved issue or documented decision.",
            },
        ],
        "feedback_evidence_rules": outreach["tracking_rules"],
        "success_thresholds": {
            "current_external_feedback_items": feedback["external_feedback_items"],
            "current_confirmed_external_users": feedback["confirmed_external_users"],
            "minimum_feedback_items_before_resume_claim": 3,
            "minimum_confirmed_users_before_user_claim": 1,
            "minimum_reproducible_items_before_case_study_claim": 1,
        },
        "issue_labels_to_count": feedback["tracking_labels"],
        "review_paths": outreach["review_paths"],
        "resume_upgrade_rules": [
            "If external_feedback_items reaches 3, resume may say the project collected public pilot feedback.",
            "If confirmed_external_users reaches 1, resume may say it was tried by an external reviewer.",
            "If reproducible_feedback_items reaches 1 and an improvement is merged, resume may say it used feedback to improve the product.",
            "Do not claim production usage, customers, or traction unless public evidence exists.",
        ],
        "not_claimed": outreach["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    segments = "\n".join(
        "| {segment} | {target_count} | {source} | {requested_action} |".format(**item)
        for item in payload["participant_segments"]
    )
    weeks = "\n".join(
        "| {week} | {focus} | {deliverable} |".format(**item)
        for item in payload["weekly_plan"]
    )
    rules = "\n".join(f"- {item}" for item in payload["feedback_evidence_rules"])
    thresholds = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["success_thresholds"].items())
    labels = "\n".join(f"| {key.replace('_', ' ').title()} | `{value}` |" for key, value in payload["issue_labels_to_count"].items())
    review_paths = "\n".join(f"- {key.replace('_', ' ').title()}: [{url}]({url})" for key, url in payload["review_paths"].items())
    upgrade_rules = "\n".join(f"- {item}" for item in payload["resume_upgrade_rules"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Pilot Program Plan

This generated plan defines how the project can collect real feedback before making adoption claims.

## Objective

{payload["objective"]}

## Pilot Window

{payload["pilot_window"]}

## Participant Segments

| Segment | Target Count | Source | Requested Action |
| --- | ---: | --- | --- |
{segments}

## Weekly Plan

| Week | Focus | Deliverable |
| ---: | --- | --- |
{weeks}

## Feedback Evidence Rules

{rules}

## Success Thresholds

| Metric | Current / Threshold |
| --- | ---: |
{thresholds}

## Issue Labels To Count

| Metric | GitHub Label |
| --- | --- |
{labels}

## Review Paths

{review_paths}

## Resume Upgrade Rules

{upgrade_rules}

## Not Claimed

{not_claimed}
"""


def verify_pilot_program_plan(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "participant_segment_count": 3,
        "pilot_week_count": 3,
        "feedback_rule_count": 4,
        "resume_upgrade_rule_count": 4,
        "current_external_feedback_items": 0,
        "current_confirmed_external_users": 0,
    }
    if len(payload["participant_segments"]) != expected["participant_segment_count"]:
        raise AssertionError("pilot plan must include three participant segments")
    if len(payload["weekly_plan"]) != expected["pilot_week_count"]:
        raise AssertionError("pilot plan must include a three-week plan")
    if len(payload["feedback_evidence_rules"]) != expected["feedback_rule_count"]:
        raise AssertionError("pilot plan must include four feedback evidence rules")
    if len(payload["resume_upgrade_rules"]) != expected["resume_upgrade_rule_count"]:
        raise AssertionError("pilot plan must include four resume upgrade rules")
    thresholds = payload["success_thresholds"]
    if thresholds["current_external_feedback_items"] != expected["current_external_feedback_items"]:
        raise AssertionError("pilot plan must preserve current feedback baseline")
    if thresholds["current_confirmed_external_users"] != expected["current_confirmed_external_users"]:
        raise AssertionError("pilot plan must preserve current user baseline")
    if thresholds["minimum_feedback_items_before_resume_claim"] != 3:
        raise AssertionError("pilot plan must require three feedback items before feedback claims")
    if thresholds["minimum_confirmed_users_before_user_claim"] != 1:
        raise AssertionError("pilot plan must require one confirmed user before user claims")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("existing users", "customer traction", "production customers"):
        if forbidden in joined:
            raise AssertionError(f"pilot plan must not claim {forbidden}")
    return {"pilot_program_plan_verified": True, **expected}


def main() -> None:
    payload = build_pilot_program_plan_payload()
    verify_pilot_program_plan(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
