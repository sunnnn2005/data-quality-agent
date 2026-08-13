import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "business-impact-ledger.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-impact-ledger.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _accepted_business_cases(evaluations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for item in evaluations:
        if not item.get("accepted") or item.get("evidence_type") != "business_case_review":
            continue
        impact = item.get("extracted_business_impact", {})
        if not impact:
            continue
        cases.append(
            {
                "issue_number": item.get("issue_number"),
                "title": item.get("title"),
                "url": item.get("url"),
                "author": item.get("author"),
                "business_context": impact.get("business_context", ""),
                "data_quality_problem": impact.get("data_quality_problem", ""),
                "business_impact": impact.get("business_impact", ""),
                "fields_involved": impact.get("fields_involved", ""),
                "project_evidence_mapping": impact.get("project_evidence_mapping", ""),
            }
        )
    return cases


def build_business_impact_ledger(gate_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    gate = load_json(GATE_PATH) if gate_payload is None else gate_payload
    cases = _accepted_business_cases(gate.get("evaluations", []))
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_impact_ledger.py",
        "purpose": (
            "Convert accepted anonymized business-case review issues into resume-safe business-impact evidence "
            "while keeping the zero-case baseline honest until public reviewer proof exists."
        ),
        "accepted_business_impact_signal_count": len(cases),
        "accepted_business_cases": cases,
        "source_gate": "docs/external-reviewer-evidence-gate.json",
        "source_gate_accepted_issue_count": gate.get("accepted_issue_count", 0),
        "resume_upgrade_rule": {
            "signal": "validated anonymized business-impact scenario",
            "current_value": len(cases),
            "minimum_before_claim": 1,
            "resume_status": "not_claimable_yet" if not cases else "claimable_with_linked_evidence",
            "evidence_required": (
                "accepted public business-case issue with non-owner author, impact permission, anonymized context, "
                "business-impact field, and project evidence mapping"
            ),
        },
        "resume_safe_summary": (
            "Published a CI-verified business-impact ledger that can turn accepted public business-case issues "
            "into resume-safe workflow, impact, and evidence-mapping claims; current accepted business-impact "
            f"signals: {len(cases)}."
        ),
        "not_claimed": [
            "validated business impact" if not cases else "business impact beyond accepted public issue evidence",
            "customer names",
            "raw production data",
            "revenue saved",
            "production adoption",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| #{issue_number} | [{title}]({url}) | {author} | {context} | {problem} | {impact} | {evidence} |".format(
            issue_number=item["issue_number"],
            title=item["title"],
            url=item["url"],
            author=item["author"],
            context=item["business_context"],
            problem=item["data_quality_problem"],
            impact=item["business_impact"],
            evidence=item["project_evidence_mapping"],
        )
        for item in payload["accepted_business_cases"]
    )
    if not rows:
        rows = "| - | - | - | - | - | - | - |"
    rule = payload["resume_upgrade_rule"]
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Business Impact Ledger

This generated ledger converts accepted public business-case review issues into resume-safe business-impact evidence.

## Summary

| Metric | Value |
| --- | ---: |
| Accepted business-impact signals | {payload["accepted_business_impact_signal_count"]} |
| Source gate accepted issues | {payload["source_gate_accepted_issue_count"]} |

## Accepted Business Cases

| Issue | Title | Author | Business Context | Data-Quality Problem | Business Impact | Project Evidence Mapping |
| --- | --- | --- | --- | --- | --- | --- |
{rows}

## Resume Upgrade Rule

| Signal | Current value | Minimum before claim | Evidence required | Status |
| --- | ---: | ---: | --- | --- |
| {rule["signal"]} | {rule["current_value"]} | {rule["minimum_before_claim"]} | {rule["evidence_required"]} | `{rule["resume_status"]}` |

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_business_impact_ledger(payload: dict[str, Any]) -> dict[str, Any]:
    count = payload["accepted_business_impact_signal_count"]
    if count != len(payload["accepted_business_cases"]):
        raise AssertionError("business impact ledger count must match accepted case list")
    if count == 0 and payload["resume_upgrade_rule"]["resume_status"] != "not_claimable_yet":
        raise AssertionError("business impact ledger must not be claimable before accepted public evidence")
    if count > 0 and payload["resume_upgrade_rule"]["resume_status"] != "claimable_with_linked_evidence":
        raise AssertionError("business impact ledger must become claimable when accepted business cases exist")
    for item in payload["accepted_business_cases"]:
        for field in (
            "business_context",
            "data_quality_problem",
            "business_impact",
            "fields_involved",
            "project_evidence_mapping",
        ):
            if not item.get(field):
                raise AssertionError(f"accepted business case missing {field}")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("customer email", "password", "api_key", "raw production rows"):
        if forbidden in joined:
            raise AssertionError(f"business impact ledger must not expose {forbidden}")
    return {
        "business_impact_ledger_verified": True,
        "accepted_business_impact_signal_count": count,
    }


def main() -> None:
    payload = build_business_impact_ledger()
    verify_business_impact_ledger(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
