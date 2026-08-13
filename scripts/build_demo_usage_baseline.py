import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
INDEX_PATH = ROOT / "docs" / "index.html"
OUTPUT_JSON_PATH = ROOT / "docs" / "demo-usage-baseline.json"
OUTPUT_MD_PATH = ROOT / "docs" / "demo-usage-baseline.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_demo_usage_baseline_payload() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    index_html = INDEX_PATH.read_text()
    demo_links = {
        "public_demo": adoption["public_demo"],
        "feedback_issue": feedback["feedback_issue_template"],
        "feedback_metrics": f"{adoption['public_demo']}feedback-metrics.json",
        "adoption_metrics": f"{adoption['public_demo']}adoption-metrics.json",
        "resume_evidence": f"{adoption['public_demo']}resume-evidence.md",
        "reviewer_feedback_packet": f"{adoption['public_demo']}reviewer-feedback-packet.md",
        "reviewer_funnel_board": f"{adoption['public_demo']}reviewer-funnel-board.md",
    }
    funnel = [
        {
            "step": "view_public_demo",
            "tracking_source": "GitHub Pages public URL",
            "current_count": None,
            "status": "not_measured",
        },
        {
            "step": "submit_feedback_issue",
            "tracking_source": "GitHub issues with feedback label",
            "current_count": feedback["external_feedback_items"],
            "status": "tracked",
        },
        {
            "step": "confirmed_external_user",
            "tracking_source": "GitHub issues with confirmed-user label",
            "current_count": feedback["confirmed_external_users"],
            "status": "tracked",
        },
        {
            "step": "star_repository",
            "tracking_source": "GitHub repository stars",
            "current_count": adoption["stars"],
            "status": "tracked",
        },
        {
            "step": "fork_repository",
            "tracking_source": "GitHub repository forks",
            "current_count": adoption["forks"],
            "status": "tracked",
        },
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_demo_usage_baseline.py",
        "public_demo": adoption["public_demo"],
        "repo": adoption["repo"],
        "release": adoption["release"]["tagName"],
        "demo_links": demo_links,
        "demo_entrypoints_verified": {
            "try_feedback_button": "Try It & Leave Feedback" in index_html,
            "feedback_metrics_link": "feedback-metrics.json" in index_html,
            "adoption_metrics_link": "adoption-metrics.json" in index_html,
            "resume_evidence_link": "resume-evidence.md" in index_html,
            "reviewer_feedback_packet_link": "reviewer-feedback-packet.md" in index_html,
            "reviewer_funnel_board_link": "reviewer-funnel-board.md" in index_html,
        },
        "tracked_usage_funnel": funnel,
        "tracked_counts": {
            "stars": adoption["stars"],
            "forks": adoption["forks"],
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        },
        "resume_safe_summary": (
            "Published a public demo usage baseline that verifies demo entrypoints and tracks stars, forks, "
            "feedback issues, and reproducible feedback from an honest zero-adoption baseline."
        ),
        "not_claimed": [
            "No visitor analytics are claimed because GitHub Pages traffic logs are not available in this project.",
            "No external users are claimed.",
            "No customer feedback is claimed.",
            "No production adoption is claimed.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["tracked_counts"].items())
    entrypoints = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["demo_entrypoints_verified"].items()
    )
    funnel = "\n".join(
        f"| {item['step']} | {item['tracking_source']} | {item['current_count']} | `{item['status']}` |"
        for item in payload["tracked_usage_funnel"]
    )
    links = "\n".join(f"- {key.replace('_', ' ').title()}: [{url}]({url})" for key, url in payload["demo_links"].items())
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Demo Usage Baseline

This generated artifact documents what the public demo can honestly prove today. It separates visible demo entrypoints from metrics that are actually tracked through GitHub.

## Demo Links

{links}

## Demo Entrypoints Verified

| Entrypoint | Present |
| --- | --- |
{entrypoints}

## Tracked Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Usage Funnel

| Step | Tracking source | Current count | Status |
| --- | --- | ---: | --- |
{funnel}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_demo_usage_baseline(payload: dict[str, Any]) -> dict[str, Any]:
    entrypoints = payload["demo_entrypoints_verified"]
    if not all(entrypoints.values()):
        raise AssertionError("demo usage baseline must verify all public demo entrypoints")
    counts = payload["tracked_counts"]
    expected = {
        "stars": 0,
        "forks": 1,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
    }
    for key, value in expected.items():
        if counts.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {counts.get(key)!r}")
    funnel_steps = {item["step"] for item in payload["tracked_usage_funnel"]}
    required_steps = {
        "view_public_demo",
        "submit_feedback_issue",
        "confirmed_external_user",
        "star_repository",
        "fork_repository",
    }
    if funnel_steps != required_steps:
        raise AssertionError("demo usage baseline must cover the complete tracked funnel")
    not_claimed = " ".join(payload["not_claimed"]).lower()
    for required in ("visitor analytics", "external users", "customer feedback", "production adoption"):
        if required not in not_claimed:
            raise AssertionError(f"demo usage baseline must not claim {required}")
    return {"demo_usage_baseline_verified": True, "tracked_funnel_steps": 5, **expected}


def main() -> None:
    payload = build_demo_usage_baseline_payload()
    verify_demo_usage_baseline(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
