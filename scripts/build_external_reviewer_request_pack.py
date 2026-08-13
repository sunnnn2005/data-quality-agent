import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_RUN_PACKET_PATH = ROOT / "docs" / "external-run-evidence-packet.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "external-reviewer-request-pack.json"
OUTPUT_MD_PATH = ROOT / "docs" / "external-reviewer-request-pack.md"
PUBLIC_COLLECTION_ISSUE_URL = "https://github.com/sunnnn2005/data-quality-agent/issues/18"
EXTERNAL_RUN_REVIEW_TEMPLATE_URL = (
    "https://github.com/sunnnn2005/data-quality-agent/issues/new?template=external_run_review.md"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_external_reviewer_request_pack_payload() -> dict[str, Any]:
    external_run = load_json(EXTERNAL_RUN_PACKET_PATH)
    feedback = load_json(FEEDBACK_METRICS_PATH)
    paths = {path["id"]: path for path in external_run["review_paths"]}
    entry_urls = {
        "public_demo_review": "https://sunnnn2005.github.io/data-quality-agent/",
        "container_smoke_run": "https://github.com/sunnnn2005/data-quality-agent/pkgs/container/data-quality-agent",
        "postgres_replay_run": "https://github.com/sunnnn2005/data-quality-agent/blob/main/docker-compose.yml",
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_external_reviewer_request_pack.py",
        "purpose": (
            "Provide copy-ready outreach messages that ask real reviewers to run one public path, "
            "then comment on issue #18 with enough evidence and permission to count the run later."
        ),
        "status": "outreach_ready_not_counted",
        "public_collection_issue": {
            "number": 18,
            "url": PUBLIC_COLLECTION_ISSUE_URL,
            "purpose": "Public collection point for external reviewer run evidence.",
        },
        "external_run_review_template": {
            "url": EXTERNAL_RUN_REVIEW_TEMPLATE_URL,
            "purpose": "Use this when a reviewer prefers opening a separate structured run issue.",
        },
        "current_counts": {
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        },
        "outreach_messages": [
            {
                "id": "classmate_public_demo",
                "audience": "UC Davis classmate or student developer",
                "minutes": 8,
                "run_path": "public_demo_review",
                "entry_url": entry_urls["public_demo_review"],
                "collection_url": PUBLIC_COLLECTION_ISSUE_URL,
                "template_url": EXTERNAL_RUN_REVIEW_TEMPLATE_URL,
                "message": (
                    "Could you spend 8 minutes trying my Data Quality Agent public demo, then leave a short comment "
                    "on issue #18, or open the External Run Review template, with what worked, what was confusing, "
                    "and whether I may count your review publicly? No private data needed."
                ),
            },
            {
                "id": "developer_container_smoke_run",
                "audience": "student developer comfortable with Docker",
                "minutes": 12,
                "run_path": "container_smoke_run",
                "entry_url": entry_urls["container_smoke_run"],
                "collection_url": PUBLIC_COLLECTION_ISSUE_URL,
                "template_url": EXTERNAL_RUN_REVIEW_TEMPLATE_URL,
                "message": (
                    "Could you run the GHCR container smoke test for my Data Quality Agent and comment on issue #18, "
                    "or open the External Run Review template, with your OS, commands, observed result, and permission "
                    "to count it publicly? The command is: docker run --rm -p 8000:8000 "
                    "ghcr.io/sunnnn2005/data-quality-agent:latest"
                ),
            },
            {
                "id": "mentor_postgres_replay",
                "audience": "mentor, data practitioner, or AI engineer",
                "minutes": 15,
                "run_path": "postgres_replay_run",
                "entry_url": entry_urls["postgres_replay_run"],
                "collection_url": PUBLIC_COLLECTION_ISSUE_URL,
                "template_url": EXTERNAL_RUN_REVIEW_TEMPLATE_URL,
                "message": (
                    "Could you try the Docker Compose PostgreSQL replay for my read-only Data Quality Agent and "
                    "comment on issue #18, or open the External Run Review template, with whether the seeded "
                    "business-data run is reproducible and credible? Please do not upload private data; a redacted "
                    "run summary is enough."
                ),
            },
        ],
        "required_comment_fields": external_run["submission_fields"],
        "counting_policy": [
            "Only public comments on issue #18 or linked public issues can be counted.",
            "The reviewer must state which path they tried and whether permission to count publicly is yes.",
            "Self-authored local tests and planning notes remain excluded from external evidence counts.",
            "Counts stay at zero until a qualifying reviewer comment exists.",
        ],
        "not_claimed": [
            "No outreach recipient has completed a run yet.",
            "No external reviewer run is claimed yet.",
            "No customer feedback is claimed yet.",
            "No enterprise deployment is claimed yet.",
        ],
        "resume_safe_summary": (
            "Published a copy-ready external reviewer request pack linked to issue #18 with 3 outreach messages, "
            "3 run paths, 8 required evidence fields, permission-based counting rules, and a zero-count baseline."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_counts"].items())
    messages = "\n\n".join(
        "\n".join(
            [
                f"### {item['id']} -> {item['audience']}",
                "",
                f"- Minutes: {item['minutes']}",
                f"- Run path: `{item['run_path']}`",
                f"- Entry: [{item['entry_url']}]({item['entry_url']})",
                f"- Collection issue: [{item['collection_url']}]({item['collection_url']})",
                f"- Separate issue template: [{item['template_url']}]({item['template_url']})",
                "",
                item["message"],
            ]
        )
        for item in payload["outreach_messages"]
    )
    fields = "\n".join(
        f"| {field['name']} | {field['required']} | {field['example']} |"
        for field in payload["required_comment_fields"]
    )
    policy = "\n".join(f"- {item}" for item in payload["counting_policy"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    issue = payload["public_collection_issue"]
    return f"""# External Reviewer Request Pack

This generated pack turns the public issue #18 evidence workflow into copy-ready outreach.

## Purpose

{payload["purpose"]}

## Status

`{payload["status"]}`

## Public Collection Issue

Issue #{issue["number"]}: [{issue["url"]}]({issue["url"]})

{issue["purpose"]}

Separate issue template: [{payload["external_run_review_template"]["url"]}]({payload["external_run_review_template"]["url"]})

## Current Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Copy-Ready Messages

{messages}

## Required Comment Fields

| Field | Required | Example |
| --- | --- | --- |
{fields}

## Counting Policy

{policy}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_external_reviewer_request_pack(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "message_count": 3,
        "run_path_count": 3,
        "required_field_count": 8,
        "issue_number": 18,
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
    }
    if payload["status"] != "outreach_ready_not_counted":
        raise AssertionError("external reviewer request pack must preserve not-counted status")
    if payload["public_collection_issue"]["number"] != expected["issue_number"]:
        raise AssertionError("external reviewer request pack must link issue #18")
    if not payload["public_collection_issue"]["url"].endswith("/issues/18"):
        raise AssertionError("external reviewer request pack must link the public collection issue")
    if not payload["external_run_review_template"]["url"].endswith("template=external_run_review.md"):
        raise AssertionError("external reviewer request pack must link the external run issue template")
    if len(payload["outreach_messages"]) != expected["message_count"]:
        raise AssertionError("external reviewer request pack must include three copy-ready messages")
    run_paths = {item["run_path"] for item in payload["outreach_messages"]}
    if run_paths != {"public_demo_review", "container_smoke_run", "postgres_replay_run"}:
        raise AssertionError("external reviewer request pack must cover all three external run paths")
    if len(payload["required_comment_fields"]) != expected["required_field_count"]:
        raise AssertionError("external reviewer request pack must preserve eight evidence fields")
    counts = payload["current_counts"]
    for key in ("external_feedback_items", "confirmed_external_users", "reproducible_feedback_items"):
        if counts[key] != expected[key]:
            raise AssertionError(f"{key} must remain zero until public reviewer evidence exists")
    for item in payload["outreach_messages"]:
        if item["collection_url"] != PUBLIC_COLLECTION_ISSUE_URL:
            raise AssertionError("each outreach message must route to issue #18")
        if item["template_url"] != EXTERNAL_RUN_REVIEW_TEMPLATE_URL:
            raise AssertionError("each outreach message must include the separate external run issue template")
        if "private data" not in item["message"].lower() and item["run_path"] != "container_smoke_run":
            raise AssertionError("reviewer messages must protect private data")
    if "No outreach recipient has completed a run yet." not in payload["not_claimed"]:
        raise AssertionError("request pack must avoid claiming completed external runs")
    return {"external_reviewer_request_pack_verified": True, **expected}


def main() -> None:
    payload = build_external_reviewer_request_pack_payload()
    verification = verify_external_reviewer_request_pack(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
