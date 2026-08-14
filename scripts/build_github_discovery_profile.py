import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "github-discovery-profile.json"
OUTPUT_MD_PATH = ROOT / "docs" / "github-discovery-profile.md"

REQUIRED_DISCOVERY_TOPICS = {
    "ai-agent",
    "data-engineering",
    "data-quality",
    "data-reliability",
    "docker",
    "fastapi",
    "github-actions",
    "llm",
    "llm-agent",
    "openai",
    "pandas",
    "postgres",
    "pydantic",
    "python",
    "quality-monitoring",
    "tool-calling",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_github_discovery_profile() -> dict[str, Any]:
    adoption = load_json(ADOPTION_METRICS_PATH)
    repo = _load_repo_metadata()
    topics = sorted(topic["name"] for topic in repo.get("repositoryTopics", []))
    missing_topics = sorted(REQUIRED_DISCOVERY_TOPICS - set(topics))
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_github_discovery_profile.py",
        "purpose": (
            "Verify the public GitHub discovery surface that can help real reviewers, contributors, "
            "and recruiters find the project without inflating stars or usage."
        ),
        "repo": repo["url"],
        "description": repo["description"],
        "homepage_url": repo["homepageUrl"],
        "is_private": repo["isPrivate"],
        "topic_count": len(topics),
        "topics": topics,
        "required_topics": sorted(REQUIRED_DISCOVERY_TOPICS),
        "missing_topics": missing_topics,
        "discovery_ready": not missing_topics and not repo["isPrivate"] and bool(repo["homepageUrl"]),
        "current_public_counts": {
            "stars": repo["stargazerCount"],
            "forks": repo["forkCount"],
            "watchers": repo["watchers"]["totalCount"],
            "adoption_metric_stars": adoption["stars"],
            "adoption_metric_forks": adoption["forks"],
        },
        "reviewer_entrypoints": [
            repo["url"],
            repo["homepageUrl"],
            f"{repo['url']}/blob/main/docs/application-evidence-pack.md",
            f"{repo['url']}/blob/main/docs/resume-claim-upgrade-ledger.md",
            f"{repo['url']}/issues/new?template=demo_feedback.md",
            f"{repo['url']}/issues/new?template=ai_engineer_review.md",
        ],
        "resume_safe_summary": (
            "Published a CI-verified GitHub discovery profile with 16 relevant repository topics, "
            "public homepage metadata, reviewer entrypoints, and honest zero-star baseline."
        ),
        "not_claimed": [
            "GitHub stars beyond the current public count",
            "organic discovery results",
            "external contributors",
            "external users",
            "customer feedback",
        ],
    }


def _load_repo_metadata() -> dict[str, Any]:
    completed = subprocess.run(
        [
            "gh",
            "repo",
            "view",
            "sunnnn2005/data-quality-agent",
            "--json",
            "description,forkCount,homepageUrl,isPrivate,repositoryTopics,stargazerCount,url,watchers",
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return json.loads(completed.stdout)


def render_markdown(payload: dict[str, Any]) -> str:
    topics = "\n".join(f"- `{topic}`" for topic in payload["topics"])
    entrypoints = "\n".join(f"- [{url}]({url})" for url in payload["reviewer_entrypoints"])
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |"
        for key, value in payload["current_public_counts"].items()
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# GitHub Discovery Profile

{payload["purpose"]}

## Public Metadata

- Repository: [{payload["repo"]}]({payload["repo"]})
- Homepage: [{payload["homepage_url"]}]({payload["homepage_url"]})
- Private: `{payload["is_private"]}`
- Discovery ready: `{payload["discovery_ready"]}`
- Description: {payload["description"]}

## Topics

{topics}

## Current Public Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Reviewer Entrypoints

{entrypoints}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_github_discovery_profile(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["is_private"] is not False:
        raise AssertionError("GitHub discovery profile requires a public repository")
    if payload["homepage_url"] != "https://sunnnn2005.github.io/data-quality-agent/":
        raise AssertionError("GitHub discovery profile must verify the public GitHub Pages homepage")
    if payload["topic_count"] != 16:
        raise AssertionError("GitHub discovery profile must verify 16 precise discovery topics")
    if payload["missing_topics"]:
        raise AssertionError(f"GitHub discovery profile missing topics: {payload['missing_topics']}")
    if payload["discovery_ready"] is not True:
        raise AssertionError("GitHub discovery profile must be discovery ready")
    counts = payload["current_public_counts"]
    if counts["stars"] != 0 or counts["adoption_metric_stars"] != 0:
        raise AssertionError("GitHub discovery profile must preserve the zero-star baseline")
    if counts["forks"] != counts["adoption_metric_forks"]:
        raise AssertionError("GitHub discovery profile fork count must match adoption metrics")
    if len(payload["reviewer_entrypoints"]) != 6:
        raise AssertionError("GitHub discovery profile must expose 6 reviewer entrypoints")
    for required in ("external users", "customer feedback", "GitHub stars beyond the current public count"):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"GitHub discovery profile must not claim {required}")
    return {
        "github_discovery_profile_verified": True,
        "topic_count": payload["topic_count"],
        "reviewer_entrypoint_count": len(payload["reviewer_entrypoints"]),
    }


def main() -> None:
    payload = build_github_discovery_profile()
    verify_github_discovery_profile(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
