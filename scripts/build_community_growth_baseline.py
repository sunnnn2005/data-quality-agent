import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON_PATH = ROOT / "docs" / "community-growth-baseline.json"
OUTPUT_MD_PATH = ROOT / "docs" / "community-growth-baseline.md"


def load_json(path: Path) -> dict[str, Any] | list[dict[str, Any]]:
    return json.loads(path.read_text())


def build_community_growth_baseline() -> dict[str, Any]:
    labels = load_json(ROOT / ".github" / "labels.json")
    adoption = load_json(ROOT / "docs" / "adoption-metrics.json")
    feedback = load_json(ROOT / "docs" / "feedback-metrics.json")
    readme = (ROOT / "README.md").read_text()
    contributing = (ROOT / "CONTRIBUTING.md").read_text()
    code_of_conduct = (ROOT / "CODE_OF_CONDUCT.md").read_text()
    pr_template = (ROOT / ".github" / "pull_request_template.md").read_text()
    issue_template_dir = ROOT / ".github" / "ISSUE_TEMPLATE"
    issue_templates = sorted(path.name for path in issue_template_dir.glob("*.md"))
    label_names = {label["name"] for label in labels}

    required_issue_templates = {
        "bug_report.md",
        "business_data_replay.md",
        "business_case_review.md",
        "demo_feedback.md",
        "external_run_review.md",
        "feature_request.md",
        "good_first_issue.md",
        "ai_engineer_review.md",
    }
    required_labels = {
        "ai-engineer-review",
        "feedback",
        "confirmed-user",
        "reproducible",
        "bug",
        "business-case",
        "business-data-replay",
        "community",
        "enhancement",
        "first-10-reviewer",
    }
    contribution_paths = {
        "readme_contributing_section": "## Contributing" in readme,
        "contributing_setup": "## Local Setup" in contributing,
        "good_first_issue_guidance": "good first issue" in readme and "Good First Issues" in contributing,
        "feedback_guidance": "Demo Feedback" in contributing,
        "code_of_conduct": "CODE_OF_CONDUCT.md" in readme
        and "CODE_OF_CONDUCT.md" in contributing
        and "Outcome Evidence Boundary" in code_of_conduct,
        "pull_request_template": "## Test Plan" in pr_template and "## Checklist" in pr_template,
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_community_growth_baseline.py",
        "issue_template_count": len(issue_templates),
        "issue_templates": issue_templates,
        "required_issue_templates_present": required_issue_templates <= set(issue_templates),
        "required_issue_templates": sorted(required_issue_templates),
        "label_count": len(labels),
        "required_labels_present": required_labels <= label_names,
        "required_labels": sorted(required_labels),
        "contribution_paths": contribution_paths,
        "public_growth_channels": [
            {
                "name": "Good first issue label",
                "url": "https://github.com/sunnnn2005/data-quality-agent/labels/good%20first%20issue",
                "purpose": "beginner-friendly contribution entrypoint",
            },
            {
                "name": "Help wanted label",
                "url": "https://github.com/sunnnn2005/data-quality-agent/labels/help%20wanted",
                "purpose": "broader contribution discovery",
            },
            {
                "name": "Demo feedback issue",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=demo_feedback.md",
                "purpose": "external reproducibility and product feedback",
            },
            {
                "name": "Bug report issue",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=bug_report.md",
                "purpose": "public bug reports",
            },
            {
                "name": "Feature request issue",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=feature_request.md",
                "purpose": "public improvement requests",
            },
            {
                "name": "Business case review issue",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_case_review.md",
                "purpose": "anonymized real-world business workflow feedback",
            },
            {
                "name": "Business data replay issue",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=business_data_replay.md",
                "purpose": "confirmed anonymized replay evidence for CSV or read-only data runs",
            },
            {
                "name": "External run review issue",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md",
                "purpose": "structured public evidence when a reviewer runs the demo, container, or PostgreSQL replay",
            },
            {
                "name": "AI Engineer review issue",
                "url": "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=ai_engineer_review.md",
                "purpose": "permissioned external review of LLM tool calling, guardrails, structured output, and interview readiness",
            },
            {
                "name": "Code of Conduct",
                "url": "https://github.com/sunnnn2005/data-quality-agent/blob/main/CODE_OF_CONDUCT.md",
                "purpose": "community trust boundary for public reviews, issues, and contribution behavior",
            },
        ],
        "current_public_counts": {
            "stars": adoption["stars"],
            "forks": adoption["forks"],
            "issues_total": adoption["issues_total"],
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        },
        "resume_safe_signal": (
            "Published a CI-verified community growth baseline with 8 issue templates, 10 configured labels, "
            "10 public growth channels, contribution guidance, a code of conduct, and honest current public counts."
        ),
        "not_claimed": [
            "external contributors",
            "community adoption",
            "GitHub stars beyond the current public count",
            "external users",
            "customer feedback",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    templates = "\n".join(f"- `{item}`" for item in payload["issue_templates"])
    labels = "\n".join(f"- `{item}`" for item in payload["required_labels"])
    paths = "\n".join(f"| {key} | {value} |" for key, value in payload["contribution_paths"].items())
    channels = "\n".join(f"- [{item['name']}]({item['url']}) -> {item['purpose']}" for item in payload["public_growth_channels"])
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_public_counts"].items())
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Community Growth Baseline

This generated artifact verifies the public contribution and feedback paths that can turn the project into a more reviewable open-source project over time.

## Issue Templates

{templates}

## Required Labels

{labels}

## Contribution Paths

| Path | Verified |
| --- | --- |
{paths}

## Public Growth Channels

{channels}

## Current Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Resume-Safe Signal

{payload["resume_safe_signal"]}

## Not Claimed

{not_claimed}
"""


def verify_community_growth_baseline(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["issue_template_count"] != 8:
        raise AssertionError("community growth baseline must verify 8 issue templates")
    if payload["label_count"] != 10:
        raise AssertionError("community growth baseline must verify 10 labels")
    if payload["required_issue_templates_present"] is not True:
        raise AssertionError("community growth baseline must verify required issue templates")
    if payload["required_labels_present"] is not True:
        raise AssertionError("community growth baseline must verify required labels")
    if not all(payload["contribution_paths"].values()):
        raise AssertionError("community growth baseline must verify contribution paths")
    if len(payload["public_growth_channels"]) != 10:
        raise AssertionError("community growth baseline must expose 10 public growth channels")
    counts = payload["current_public_counts"]
    expected_counts = {
        "stars": 0,
        "forks": 1,
        "issues_total": 26,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
    }
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            raise AssertionError(f"{key} expected {expected!r}, got {counts.get(key)!r}")
    for required in ("external contributors", "community adoption", "external users", "customer feedback"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"community growth baseline must not claim {required}")
    return {
        "community_growth_baseline_verified": True,
        "issue_template_count": payload["issue_template_count"],
        "label_count": payload["label_count"],
        "public_growth_channels": len(payload["public_growth_channels"]),
    }


def main() -> None:
    payload = build_community_growth_baseline()
    verify_community_growth_baseline(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
