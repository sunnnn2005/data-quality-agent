import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
PUBLIC_TRACTION_DASHBOARD_PATH = ROOT / "docs" / "public-traction-dashboard.json"
PUBLIC_METRICS_SUMMARY_PATH = ROOT / "docs" / "public-metrics-summary.json"
PUBLIC_AVAILABILITY_SNAPSHOT_PATH = ROOT / "docs" / "public-availability-snapshot.json"
REVIEWER_EVIDENCE_KIT_PATH = ROOT / "docs" / "reviewer-evidence-kit.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-traction-proof.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-traction-proof.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _status(current: int, threshold: int) -> str:
    return "claimable" if current >= threshold else "not_claimable_yet"


def build_resume_traction_proof() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    traction = load_json(PUBLIC_TRACTION_DASHBOARD_PATH)
    metrics_summary = load_json(PUBLIC_METRICS_SUMMARY_PATH)
    availability = load_json(PUBLIC_AVAILABILITY_SNAPSHOT_PATH)
    reviewer_kit = load_json(REVIEWER_EVIDENCE_KIT_PATH)

    public_counts = {
        "stars": adoption["stars"],
        "forks": adoption["forks"],
        "watchers": adoption["watchers"],
        "issues_total": adoption["issues_total"],
        "confirmed_external_users": feedback["confirmed_external_users"],
        "external_feedback_items": feedback["external_feedback_items"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        "github_views": metrics_summary["public_metrics"]["github_view_count"],
        "github_unique_visitors": metrics_summary["public_metrics"]["github_unique_visitors"],
        "github_clones": metrics_summary["public_metrics"]["github_clone_count"],
        "github_unique_cloners": metrics_summary["public_metrics"]["github_unique_cloners"],
    }
    claimable_now = [
        {
            "signal": "public launch",
            "resume_phrase": "Launched a public GitHub Pages demo for a business-data quality agent.",
            "evidence": adoption["public_demo"],
            "status": "claimable",
        },
        {
            "signal": "public release",
            "resume_phrase": f"Published {adoption['release']['tagName']} release and runnable GHCR container image.",
            "evidence": adoption["release"]["url"],
            "status": "claimable",
        },
        {
            "signal": "verified engineering quality",
            "resume_phrase": f"Maintained {adoption['test_count']} passing CI tests across agent, API, evidence, and safety checks.",
            "evidence": "https://github.com/sunnnn2005/data-quality-agent/actions/workflows/test.yml",
            "status": "claimable",
        },
        {
            "signal": "evidence collection system",
            "resume_phrase": (
                f"Built a reviewer evidence system with {reviewer_kit['evidence_form_count']} public issue templates "
                f"and {reviewer_kit['reviewer_script_step_count']} privacy/permission steps."
            ),
            "evidence": "https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/reviewer-evidence-kit.md",
            "status": "claimable",
        },
        {
            "signal": "early repository interest",
            "resume_phrase": (
                f"Captured GitHub's rolling 14-day traffic snapshot with {public_counts['github_views']} views, "
                f"{public_counts['github_unique_visitors']} unique visitors, {public_counts['github_clones']} clones, "
                f"and {public_counts['github_unique_cloners']} unique cloners without counting traffic as users."
            ),
            "evidence": "https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/github-traffic-snapshot.md",
            "status": "claimable",
        },
        {
            "signal": "public availability evidence",
            "resume_phrase": (
                f"Verified {availability['available_endpoint_count']}/{availability['endpoint_count']} public project surfaces "
                f"and {availability['successful_workflow_count']}/{availability['workflow_count']} main-branch workflows "
                "in a generated availability snapshot."
            ),
            "evidence": "https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/public-availability-snapshot.md",
            "status": "claimable",
        },
    ]
    future_claims = [
        {
            "signal": "external users",
            "current_value": public_counts["confirmed_external_users"],
            "threshold": 3,
            "status": _status(public_counts["confirmed_external_users"], 3),
            "resume_phrase_after_threshold": "Validated the agent with 3+ external reviewers/users using public evidence issues.",
            "evidence_required": "accepted non-owner GitHub issues with confirmed-user label and permission to count",
        },
        {
            "signal": "user feedback",
            "current_value": public_counts["external_feedback_items"],
            "threshold": 3,
            "status": _status(public_counts["external_feedback_items"], 3),
            "resume_phrase_after_threshold": "Collected and triaged 3+ public feedback items from external reviewers.",
            "evidence_required": "accepted GitHub feedback issues with concrete tried path, result, and permission",
        },
        {
            "signal": "reproducible product feedback",
            "current_value": public_counts["reproducible_feedback_items"],
            "threshold": 1,
            "status": _status(public_counts["reproducible_feedback_items"], 1),
            "resume_phrase_after_threshold": "Used reproducible reviewer feedback to improve the public agent demo.",
            "evidence_required": "public issue with reproduction steps and linked fix or accepted triage result",
        },
        {
            "signal": "GitHub stars",
            "current_value": public_counts["stars"],
            "threshold": 5,
            "status": _status(public_counts["stars"], 5),
            "resume_phrase_after_threshold": "Earned 5+ GitHub stars for a public data-quality agent project.",
            "evidence_required": "public GitHub stargazer count",
        },
    ]
    blocked_claims = [
        "Do not claim active users until confirmed_external_users is greater than zero and publicly evidenced.",
        "Do not claim customer feedback until accepted feedback issues exist.",
        "Do not claim enterprise or production adoption without permissioned business-case evidence.",
        "Do not claim star growth beyond the current public GitHub count.",
        "Do not convert GitHub traffic views into user counts.",
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_resume_traction_proof.py",
        "public_counts": public_counts,
        "claimable_now_count": len(claimable_now),
        "claimable_now": claimable_now,
        "future_claim_count": len(future_claims),
        "future_claims": future_claims,
        "blocked_claim_count": len(blocked_claims),
        "blocked_claims": blocked_claims,
        "linked_public_traction_surfaces": traction["traction_surface_count"],
        "linked_growth_channels": traction["growth_channel_count"],
        "resume_status": "baseline_claimable_growth_not_yet_claimable",
        "resume_safe_summary": (
            f"Published a CI-verified resume traction proof with {len(claimable_now)} claimable launch/quality/traffic/availability signals, "
            f"{len(future_claims)} threshold-based future outcome claims, and {len(blocked_claims)} blocked claims "
            "to prevent overstating users, feedback, production adoption, or stars."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["public_counts"].items())
    claimable = "\n".join(
        f"| {item['signal']} | {item['resume_phrase']} | [{item['evidence']}]({item['evidence']}) | `{item['status']}` |"
        for item in payload["claimable_now"]
    )
    future = "\n".join(
        "| {signal} | {current_value} | {threshold} | {resume_phrase_after_threshold} | {evidence_required} | `{status}` |".format(
            **item
        )
        for item in payload["future_claims"]
    )
    blocked = "\n".join(f"- {item}" for item in payload["blocked_claims"])
    return f"""# Resume Traction Proof

This generated artifact turns public project evidence into resume-safe traction wording. It separates current claimable signals from future outcome claims that still need public evidence.

## Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Claimable Now

| Signal | Resume-safe phrase | Evidence | Status |
| --- | --- | --- | --- |
{claimable}

## Future Outcome Claims

| Signal | Current value | Threshold | Phrase after threshold | Evidence required | Status |
| --- | ---: | ---: | --- | --- | --- |
{future}

## Blocked Claims

{blocked}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_resume_traction_proof(payload: dict[str, Any]) -> dict[str, Any]:
    expected_counts = {
        "stars": 0,
        "forks": 1,
        "issues_total": 26,
        "confirmed_external_users": 0,
        "external_feedback_items": 0,
        "reproducible_feedback_items": 0,
    }
    for key, expected in expected_counts.items():
        if payload["public_counts"].get(key) != expected:
            raise AssertionError(f"resume traction proof {key} expected {expected!r}")
    if payload["claimable_now_count"] != 6:
        raise AssertionError("resume traction proof must include 6 claimable baseline signals")
    if payload["future_claim_count"] != 4:
        raise AssertionError("resume traction proof must include 4 future threshold claims")
    if payload["blocked_claim_count"] != 5:
        raise AssertionError("resume traction proof must include 5 blocked claims")
    if payload["linked_public_traction_surfaces"] != 4:
        raise AssertionError("resume traction proof must link public traction surfaces")
    if payload["linked_growth_channels"] != 21:
        raise AssertionError("resume traction proof must link growth channels")
    if not all(item["status"] == "claimable" for item in payload["claimable_now"]):
        raise AssertionError("current launch and quality signals must be claimable")
    if not all(item["status"] == "not_claimable_yet" for item in payload["future_claims"]):
        raise AssertionError("zero outcome metrics must not be claimable yet")
    blocked = " ".join(payload["blocked_claims"]).lower()
    for required in ("active users", "customer feedback", "production adoption", "github traffic views"):
        if required not in blocked:
            raise AssertionError(f"resume traction proof must block {required}")
    if payload["resume_status"] != "baseline_claimable_growth_not_yet_claimable":
        raise AssertionError("resume traction proof must separate baseline claims from growth claims")
    return {
        "resume_traction_proof_verified": True,
        "claimable_now_count": payload["claimable_now_count"],
        "future_claim_count": payload["future_claim_count"],
        "blocked_claim_count": payload["blocked_claim_count"],
    }


def main() -> None:
    payload = build_resume_traction_proof()
    verify_resume_traction_proof(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
