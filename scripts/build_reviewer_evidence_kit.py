import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
RESUME_OUTCOME_READINESS_PATH = ROOT / "docs" / "resume-outcome-readiness.json"
BUSINESS_IMPACT_LEDGER_PATH = ROOT / "docs" / "business-impact-ledger.json"
APPLICATION_PACK_PATH = ROOT / "docs" / "application-evidence-pack.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "reviewer-evidence-kit.json"
OUTPUT_MD_PATH = ROOT / "docs" / "reviewer-evidence-kit.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_reviewer_evidence_kit() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    readiness = load_json(RESUME_OUTCOME_READINESS_PATH)
    ledger = load_json(BUSINESS_IMPACT_LEDGER_PATH)
    application_pack = load_json(APPLICATION_PACK_PATH)
    repo = application_pack["application_links"]["github_repo"]
    issue_base = f"{repo}/issues/new"
    evidence_forms = [
        {
            "id": "external_run",
            "metric": "confirmed_external_users",
            "template": "external_run_review.md",
            "url": f"{issue_base}?template=external_run_review.md",
            "minimum_required": 1,
            "copy_prompt": (
                "I ran the public demo/container/PostgreSQL replay, used this command or URL, observed this result, "
                "and I grant permission to count this as public external run evidence."
            ),
        },
        {
            "id": "demo_feedback",
            "metric": "external_feedback_items",
            "template": "demo_feedback.md",
            "url": f"{issue_base}?template=demo_feedback.md",
            "minimum_required": 3,
            "copy_prompt": (
                "I tried the demo or docs, this part was useful, this part was confusing, and this feedback can be "
                "counted publicly without private data."
            ),
        },
        {
            "id": "business_case",
            "metric": "business_case_feedback_items",
            "template": "business_case_review.md",
            "url": f"{issue_base}?template=business_case_review.md",
            "minimum_required": 1,
            "copy_prompt": (
                "Here is an anonymized workflow, data-quality problem, business impact, fields involved, and evidence "
                "mapping. I grant permission to count it as anonymized public business-case feedback."
            ),
        },
        {
            "id": "ai_engineer_review",
            "metric": "ai_engineer_review_items",
            "template": "ai_engineer_review.md",
            "url": f"{issue_base}?template=ai_engineer_review.md",
            "minimum_required": 1,
            "copy_prompt": (
                "I inspected the tool-calling, structured output, guardrails, trace, evaluation, and data connector "
                "evidence, and I grant permission to count this as AI Engineer project feedback."
            ),
        },
        {
            "id": "reproducible_bug",
            "metric": "reproducible_feedback_items",
            "template": "bug_report.md",
            "url": f"{issue_base}?template=bug_report.md",
            "minimum_required": 1,
            "copy_prompt": (
                "I found a reproducible issue, included expected result, actual result, environment, and reproduction "
                "steps, without private business data."
            ),
        },
    ]
    reviewer_script = [
        "Open the public demo or run the container/PostgreSQL replay.",
        "Copy the matching prompt into the linked GitHub issue template.",
        "Include only redacted schema, aggregate stats, command output, or screenshots with private data removed.",
        "Check the explicit permission box only if the issue can be counted publicly.",
        "Wait for the evidence gate to accept or reject the issue before any resume wording is upgraded.",
    ]
    current_counts = {
        "confirmed_external_users": feedback["confirmed_external_users"],
        "external_feedback_items": feedback["external_feedback_items"],
        "business_case_feedback_items": feedback["business_case_feedback_items"],
        "ai_engineer_review_items": feedback["ai_engineer_review_items"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
        "accepted_business_impact_signals": ledger["accepted_business_impact_signal_count"],
    }
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_reviewer_evidence_kit.py",
        "purpose": (
            "Give real reviewers a copy-ready, privacy-safe path for submitting public evidence that can upgrade "
            "resume outcome claims only after the evidence gate accepts it."
        ),
        "evidence_form_count": len(evidence_forms),
        "evidence_forms": evidence_forms,
        "reviewer_script_step_count": len(reviewer_script),
        "reviewer_script": reviewer_script,
        "current_counts": current_counts,
        "missing_evidence": readiness["missing_evidence"],
        "business_impact_resume_status": ledger["resume_upgrade_rule"]["resume_status"],
        "resume_status": "collection_ready_not_claimable",
        "not_claimed": [
            "external users",
            "customer feedback",
            "validated business impact",
            "production adoption",
            "GitHub stars beyond the current public count",
        ],
        "resume_safe_summary": (
            "Published a CI-verified reviewer evidence kit with 5 public issue templates, 5 copy-ready reviewer prompts, "
            "5 privacy/permission steps, and zero current external outcome counts."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    forms = "\n".join(
        "| {id} | `{metric}` | `{template}` | {minimum_required} | [Open]({url}) |".format(**form)
        for form in payload["evidence_forms"]
    )
    prompts = "\n\n".join(f"### {form['id']}\n\n{form['copy_prompt']}" for form in payload["evidence_forms"])
    script = "\n".join(f"{index}. {step}" for index, step in enumerate(payload["reviewer_script"], 1))
    counts = "\n".join(
        f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["current_counts"].items()
    )
    missing = "\n".join(
        "| {stage} | {current_value} | {minimum_to_claim} | {remaining_needed} |".format(**item)
        for item in payload["missing_evidence"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Reviewer Evidence Kit

This generated kit gives reviewers copy-ready instructions for producing public, countable evidence.

## Purpose

{payload["purpose"]}

## Public Evidence Forms

| Evidence Type | Metric | Template | Minimum Required | Link |
| --- | --- | --- | ---: | --- |
{forms}

## Copy-Ready Reviewer Prompts

{prompts}

## Reviewer Script

{script}

## Current Counts

| Metric | Current value |
| --- | ---: |
{counts}

## Missing Evidence

| Stage | Current | Minimum | Remaining |
| --- | ---: | ---: | ---: |
{missing}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_reviewer_evidence_kit(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["evidence_form_count"] != 5:
        raise AssertionError("reviewer evidence kit must define five public evidence forms")
    if payload["reviewer_script_step_count"] != 5:
        raise AssertionError("reviewer evidence kit must define five reviewer script steps")
    if payload["resume_status"] != "collection_ready_not_claimable":
        raise AssertionError("reviewer evidence kit must not claim external outcomes yet")
    expected_templates = {
        "external_run_review.md",
        "demo_feedback.md",
        "business_case_review.md",
        "ai_engineer_review.md",
        "bug_report.md",
    }
    templates = {form["template"] for form in payload["evidence_forms"]}
    if templates != expected_templates:
        raise AssertionError("reviewer evidence kit must link all required public issue templates")
    expected_counts = {
        "confirmed_external_users": 0,
        "external_feedback_items": 0,
        "business_case_feedback_items": 0,
        "ai_engineer_review_items": 0,
        "reproducible_feedback_items": 0,
        "accepted_business_impact_signals": 0,
    }
    if payload["current_counts"] != expected_counts:
        raise AssertionError("reviewer evidence kit must preserve zero current external outcome counts")
    if len(payload["missing_evidence"]) != 4:
        raise AssertionError("reviewer evidence kit must link four missing evidence stages")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("permission", "private data", "evidence gate", "github"):
        if required not in joined:
            raise AssertionError(f"reviewer evidence kit missing required safety or workflow signal: {required}")
    for required in payload["not_claimed"]:
        if required not in (
            "external users",
            "customer feedback",
            "validated business impact",
            "production adoption",
            "GitHub stars beyond the current public count",
        ):
            raise AssertionError(f"unexpected not-claimed item: {required}")
    return {
        "reviewer_evidence_kit_verified": True,
        "evidence_form_count": payload["evidence_form_count"],
        "reviewer_script_step_count": payload["reviewer_script_step_count"],
    }


def main() -> None:
    payload = build_reviewer_evidence_kit()
    verify_reviewer_evidence_kit(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
