import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
BUSINESS_PILOT_OFFER_PATH = ROOT / "docs" / "business-pilot-offer.json"
BUSINESS_CASE_TEMPLATE_PATH = ROOT / ".github" / "ISSUE_TEMPLATE" / "business_case_review.md"
BUSINESS_DATA_REPLAY_TEMPLATE_PATH = ROOT / ".github" / "ISSUE_TEMPLATE" / "business_data_replay.md"
OUTPUT_JSON_PATH = ROOT / "docs" / "business-pilot-evidence-checklist.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-pilot-evidence-checklist.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_business_pilot_evidence_checklist() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    offer = load_json(BUSINESS_PILOT_OFFER_PATH)
    business_case_template = BUSINESS_CASE_TEMPLATE_PATH.read_text()
    replay_template = BUSINESS_DATA_REPLAY_TEMPLATE_PATH.read_text()
    outcome_tracks = [
        {
            "metric": "confirmed_external_users",
            "current_value": feedback["confirmed_external_users"],
            "minimum_before_claim": 1,
            "accepted_source": "business_data_replay.md issue",
            "required_public_evidence": [
                "non-owner reviewer",
                "replay path tried",
                "dataset shape",
                "agent run summary",
                "usefulness rating",
                "permission to count confirmed anonymized replay",
                "no private data confirmation",
            ],
            "future_resume_line": (
                "Validated the agent with an external reviewer on an anonymized business-shaped dataset."
            ),
        },
        {
            "metric": "business_case_feedback_items",
            "current_value": feedback["business_case_feedback_items"],
            "minimum_before_claim": 1,
            "accepted_source": "business_case_review.md issue",
            "required_public_evidence": [
                "business context",
                "data-quality problem",
                "business impact",
                "fields involved",
                "project evidence mapping",
                "business-case counting permission",
                "business-impact counting permission",
            ],
            "future_resume_line": (
                "Collected public business-case feedback mapping agent findings to a real workflow risk."
            ),
        },
        {
            "metric": "reproducible_feedback_items",
            "current_value": feedback["reproducible_feedback_items"],
            "minimum_before_claim": 1,
            "accepted_source": "business_data_replay.md issue with reproducible run evidence",
            "required_public_evidence": [
                "command or endpoint used",
                "observed report status",
                "finding count",
                "selected tools or agent trace summary",
                "catch-or-miss feedback",
                "redacted output summary",
            ],
            "future_resume_line": "Converted external replay feedback into a reproducible quality-rule improvement.",
        },
        {
            "metric": "external_feedback_items",
            "current_value": feedback["external_feedback_items"],
            "minimum_before_claim": 1,
            "accepted_source": "demo_feedback.md or business_data_replay.md issue",
            "required_public_evidence": [
                "specific path tried",
                "observed result",
                "main feedback",
                "permission to count external feedback",
                "no private data confirmation",
            ],
            "future_resume_line": "Incorporated external reviewer feedback into the agent evidence workflow.",
        },
    ]
    template_checks = {
        "business_case_collects_impact": all(
            phrase in business_case_template
            for phrase in (
                "Business impact",
                "Approximate time spent investigating manually:",
                "This can be counted as an anonymized business-impact signal.",
            )
        ),
        "business_case_maps_project_evidence": "Evidence from this project" in business_case_template,
        "replay_collects_agent_trace": "Selected tools shown in the agent trace:" in replay_template,
        "replay_collects_usefulness_rating": "Usefulness rating" in replay_template,
        "replay_blocks_private_data": "customer names, emails, addresses, tokens, secrets" in replay_template,
    }
    current_counts = {
        metric: feedback[metric]
        for metric in (
            "confirmed_external_users",
            "business_case_feedback_items",
            "reproducible_feedback_items",
            "external_feedback_items",
        )
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_pilot_evidence_checklist.py",
        "purpose": (
            "Define the exact public evidence needed before business pilot usage, external users, feedback, "
            "or business-impact claims can be added to a resume."
        ),
        "public_offer_url": offer["public_url"],
        "public_pilot_issue": offer["public_pilot_issue"],
        "outcome_track_count": len(outcome_tracks),
        "outcome_tracks": outcome_tracks,
        "template_checks": template_checks,
        "template_check_count": len(template_checks),
        "passed_template_check_count": sum(1 for value in template_checks.values() if value),
        "current_public_counts": current_counts,
        "claimable_now": [
            track["metric"]
            for track in outcome_tracks
            if track["current_value"] >= track["minimum_before_claim"]
        ],
        "blocked_until_public_evidence": [
            track["metric"]
            for track in outcome_tracks
            if track["current_value"] < track["minimum_before_claim"]
        ],
        "resume_safe_summary": (
            "Published a business pilot evidence checklist with 4 outcome tracks, explicit public evidence "
            "requirements, template coverage checks, and zero current business-pilot outcome claims."
        ),
        "not_claimed": [
            "completed business pilot",
            "confirmed external user",
            "real enterprise customer",
            "measured company impact",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    tracks = "\n".join(
        "| {metric} | {current_value} | {minimum_before_claim} | {accepted_source} | {future_resume_line} |".format(
            **track
        )
        for track in payload["outcome_tracks"]
    )
    requirements = "\n\n".join(
        "### `{metric}`\n\n{items}".format(
            metric=track["metric"],
            items="\n".join(f"- {item}" for item in track["required_public_evidence"]),
        )
        for track in payload["outcome_tracks"]
    )
    checks = "\n".join(
        f"| {name.replace('_', ' ')} | {value} |"
        for name, value in payload["template_checks"].items()
    )
    counts = "\n".join(
        f"| `{metric}` | {count} |" for metric, count in payload["current_public_counts"].items()
    )
    blocked = "\n".join(f"- `{metric}`" for metric in payload["blocked_until_public_evidence"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Business Pilot Evidence Checklist

{payload["purpose"]}

Public pilot offer: [{payload["public_offer_url"]}]({payload["public_offer_url"]})

Public pilot issue: [{payload["public_pilot_issue"]}]({payload["public_pilot_issue"]})

## Outcome Tracks

| Metric | Current value | Minimum before claim | Accepted source | Future resume line |
| --- | ---: | ---: | --- | --- |
{tracks}

## Required Public Evidence

{requirements}

## Template Coverage Checks

| Check | Passed |
| --- | --- |
{checks}

## Current Public Counts

| Metric | Count |
| --- | ---: |
{counts}

## Blocked Until Public Evidence

{blocked}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_business_pilot_evidence_checklist(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["outcome_track_count"] != 4:
        raise AssertionError("business pilot evidence checklist must define 4 outcome tracks")
    if payload["template_check_count"] != 5:
        raise AssertionError("business pilot evidence checklist must define 5 template checks")
    if payload["passed_template_check_count"] != payload["template_check_count"]:
        raise AssertionError("all business pilot template checks must pass")
    if payload["claimable_now"]:
        raise AssertionError("business pilot outcome metrics must not be claimable before public evidence")
    expected_blocked = {
        "confirmed_external_users",
        "business_case_feedback_items",
        "reproducible_feedback_items",
        "external_feedback_items",
    }
    if set(payload["blocked_until_public_evidence"]) != expected_blocked:
        raise AssertionError("business pilot checklist must block all outcome tracks from the zero baseline")
    for track in payload["outcome_tracks"]:
        if len(track["required_public_evidence"]) < 5:
            raise AssertionError(f"{track['metric']} must require at least 5 evidence fields")
        if track["minimum_before_claim"] != 1:
            raise AssertionError(f"{track['metric']} must require at least one accepted public evidence item")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("permission", "no private data", "business impact", "agent trace"):
        if required not in joined:
            raise AssertionError(f"business pilot checklist missing {required!r}")
    for forbidden in ("completed business pilot", "real enterprise customer", "measured company impact"):
        if forbidden not in payload["not_claimed"]:
            raise AssertionError(f"business pilot checklist must not claim {forbidden}")
    return {"business_pilot_evidence_checklist_verified": True}


def write_outputs(payload: dict[str, Any]) -> None:
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))


def main() -> None:
    payload = build_business_pilot_evidence_checklist()
    verify_business_pilot_evidence_checklist(payload)
    write_outputs(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
