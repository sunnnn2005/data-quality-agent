import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
REVIEWER_SUBMISSION_HUB_PATH = ROOT / "docs" / "reviewer-submission-hub.json"
EVIDENCE_GAP_DIAGNOSTICS_PATH = ROOT / "docs" / "evidence-gap-diagnostics.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "outcome-witness-packet.json"
OUTPUT_MD_PATH = ROOT / "docs" / "outcome-witness-packet.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _submission_by_metric(hub: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {path["target_metric"]: path for path in hub["submission_paths"]}


def _build_witness_cards(
    hub: dict[str, Any],
    gaps: dict[str, Any],
) -> list[dict[str, Any]]:
    paths = _submission_by_metric(hub)
    unlock_by_metric = {item["target_metric"]: item for item in gaps["nearest_unlock_paths"]}
    priority_metrics = [
        "ai_engineer_review_items",
        "confirmed_external_users",
        "external_feedback_items",
        "business_case_feedback_items",
        "reproducible_feedback_items",
    ]
    reviewer_prompts = {
        "ai_engineer_review_items": (
            "Inspect the public AI Engineer evidence and tell me whether this looks like a real LLM agent project."
        ),
        "confirmed_external_users": (
            "Open the public demo or run path and submit what you actually observed."
        ),
        "external_feedback_items": (
            "Try one visible workflow and submit one useful improvement or confusing moment."
        ),
        "business_case_feedback_items": (
            "Share one anonymized data-quality workflow where a wrong result would affect a business decision."
        ),
        "reproducible_feedback_items": (
            "Run or replay one workflow and report the command, result, and what the agent caught or missed."
        ),
    }
    evidence_upgrade = {
        "ai_engineer_review_items": "AI Engineer review bullet can materialize after one accepted non-owner public issue.",
        "confirmed_external_users": "External-user validation bullet can materialize after one accepted public run issue.",
        "external_feedback_items": "Feedback bullet can materialize after one accepted non-owner public feedback issue.",
        "business_case_feedback_items": "Business-case bullet can materialize after one accepted anonymized business-case issue.",
        "reproducible_feedback_items": "Reproducible-run bullet can materialize after one accepted replay issue with trace evidence.",
    }
    cards = []
    for metric in priority_metrics:
        path = paths[metric]
        unlock = unlock_by_metric.get(metric)
        cards.append(
            {
                "id": f"witness_{metric}",
                "target_metric": metric,
                "reviewer_prompt": reviewer_prompts[metric],
                "minimum_minutes": path["minimum_minutes"],
                "review_path": path["review_path"],
                "submission_url": path["submission_url"],
                "permission_sentence": (
                    "I give permission for this public issue to be counted as project review evidence."
                ),
                "no_private_data_sentence": (
                    "I confirm this public issue contains no raw customer data, private business data, secrets, "
                    "tokens, private emails, addresses, or production rows."
                ),
                "required_evidence": path["required_evidence"],
                "first_unlock_requirement": unlock["first_unlock_requirement"] if unlock else path["counting_rule"],
                "resume_upgrade_after_acceptance": evidence_upgrade[metric],
                "counting_rule": path["counting_rule"],
            }
        )
    return cards


def build_outcome_witness_packet() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    hub = load_json(REVIEWER_SUBMISSION_HUB_PATH)
    gaps = load_json(EVIDENCE_GAP_DIAGNOSTICS_PATH)
    cards = _build_witness_cards(hub, gaps)
    current_counts = {
        "confirmed_external_users": feedback["confirmed_external_users"],
        "external_feedback_items": feedback["external_feedback_items"],
        "reproducible_feedback_items": feedback.get("reproducible_feedback_items", 0),
        "business_case_feedback_items": feedback.get("business_case_feedback_items", 0),
        "ai_engineer_review_items": feedback.get("ai_engineer_review_items", 0),
    }
    payload = {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_outcome_witness_packet.py",
        "purpose": (
            "Give one external reviewer a short, public, permissioned task card that can become resume-countable "
            "only after the evidence gate accepts the submitted GitHub issue."
        ),
        "witness_card_count": len(cards),
        "target_metric_count": len({card["target_metric"] for card in cards}),
        "total_required_evidence_fields": sum(len(card["required_evidence"]) for card in cards),
        "current_public_counts": current_counts,
        "witness_cards": cards,
        "resume_outcome_upgraded": False,
        "not_claimed": [
            "Witness cards are invitations, not users or feedback.",
            "No resume outcome is upgraded until a non-owner public GitHub issue passes the evidence gate.",
            "Private messages, private names, and private notes are not counted as public evidence.",
            "GitHub stars must come from public GitHub data and must never be bought, traded, or pressured.",
        ],
        "resume_safe_summary": (
            "Published an outcome witness packet with 5 reviewer task cards, "
            "5 target outcome metrics, 22 required evidence fields, and zero resume outcome upgrades."
        ),
    }
    verify_outcome_witness_packet(payload)
    return payload


def render_markdown(payload: dict[str, Any]) -> str:
    count_rows = "\n".join(
        f"| `{metric}` | {count} |" for metric, count in payload["current_public_counts"].items()
    )
    card_sections = []
    for card in payload["witness_cards"]:
        evidence = "\n".join(f"- {item}" for item in card["required_evidence"])
        card_sections.append(
            f"""### {card["target_metric"]}

Prompt: {card["reviewer_prompt"]}

- Time: {card["minimum_minutes"]} minutes
- Review: [{card["review_path"]}]({card["review_path"]})
- Submit: [{card["submission_url"]}]({card["submission_url"]})
- Permission sentence: `{card["permission_sentence"]}`
- No-private-data sentence: `{card["no_private_data_sentence"]}`
- First unlock requirement: {card["first_unlock_requirement"]}
- Resume upgrade after acceptance: {card["resume_upgrade_after_acceptance"]}

Required evidence:

{evidence}
"""
        )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Outcome Witness Packet

This generated packet turns outreach into short, public reviewer tasks with explicit evidence gates.

## Purpose

{payload["purpose"]}

## Current Public Counts

| Metric | Count |
| --- | ---: |
{count_rows}

## Witness Cards

{"\n".join(card_sections)}

## Not Claimed

{not_claimed}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def verify_outcome_witness_packet(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["witness_card_count"] != 5:
        raise AssertionError("outcome witness packet must define five reviewer task cards")
    if payload["target_metric_count"] != 5:
        raise AssertionError("outcome witness packet must target five outcome metrics")
    if payload["total_required_evidence_fields"] != 22:
        raise AssertionError("outcome witness packet must track 22 required evidence fields")
    if payload["resume_outcome_upgraded"] is not False:
        raise AssertionError("witness packet must not upgrade resume outcomes by itself")
    required_metrics = {
        "ai_engineer_review_items",
        "confirmed_external_users",
        "external_feedback_items",
        "business_case_feedback_items",
        "reproducible_feedback_items",
    }
    actual_metrics = {card["target_metric"] for card in payload["witness_cards"]}
    if actual_metrics != required_metrics:
        raise AssertionError(f"witness metric mismatch: {sorted(actual_metrics)}")
    if any(value != 0 for value in payload["current_public_counts"].values()):
        raise AssertionError("default witness packet must preserve zero external outcome counts")
    joined = json.dumps(payload, sort_keys=True)
    for required in (
        "I give permission for this public issue to be counted as project review evidence.",
        "I confirm this public issue contains no raw customer data",
        "non-owner public GitHub issue passes the evidence gate",
        "GitHub stars must come from public GitHub data",
    ):
        if required not in joined:
            raise AssertionError(f"missing witness packet boundary: {required}")
    for card in payload["witness_cards"]:
        if not card["review_path"].startswith("https://"):
            raise AssertionError("witness review paths must be public URLs")
        if not card["submission_url"].startswith("https://github.com/"):
            raise AssertionError("witness submissions must use GitHub public issue surfaces")
        if "Counts only" not in card["counting_rule"]:
            raise AssertionError("witness cards must keep conservative counting rules")
    return {"outcome_witness_packet_verified": True}


def main() -> None:
    payload = build_outcome_witness_packet()
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
