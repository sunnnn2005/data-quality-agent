import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
REPLAY_PACKET_PATH = ROOT / "docs" / "business-data-replay-packet.json"
BUSINESS_CASE_PATH = ROOT / "docs" / "business-case-intake.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "business-pilot-offer.json"
OUTPUT_MD_PATH = ROOT / "docs" / "business-pilot-offer.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "business-pilot-offer.html"
PILOT_ISSUE_URL = "https://github.com/sunnnn2005/data-quality-agent/issues/31"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_business_pilot_offer() -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    replay = load_json(REPLAY_PACKET_PATH)
    business_case = load_json(BUSINESS_CASE_PATH)
    current_counts = {
        "confirmed_external_users": feedback["confirmed_external_users"],
        "external_feedback_items": feedback["external_feedback_items"],
        "business_case_feedback_items": feedback["business_case_feedback_items"],
        "reproducible_feedback_items": feedback["reproducible_feedback_items"],
    }
    pilot_scope = [
        {
            "step": 1,
            "name": "Scope a safe dataset",
            "owner": "reviewer_or_pilot_contact",
            "output": "Dataset shape, non-sensitive field names, business rule candidates, and permission boundary.",
        },
        {
            "step": 2,
            "name": "Run a bounded replay",
            "owner": "project_owner_or_reviewer",
            "output": "CSV upload or read-only PostgreSQL run with row/column limits and no stored raw data.",
        },
        {
            "step": 3,
            "name": "Review evidence-backed findings",
            "owner": "reviewer_or_domain_contact",
            "output": "Useful finding, missed rule, confusing recommendation, or accepted root-cause hypothesis.",
        },
        {
            "step": 4,
            "name": "Publish redacted evidence",
            "owner": "reviewer",
            "output": "GitHub issue with permission to count, no private data, and a concrete observed result.",
        },
    ]
    eligible_data = [
        "anonymized order, ticket, transaction, inventory, or signup CSV",
        "read-only PostgreSQL table with non-sensitive columns",
        "synthetic-but-business-shaped export that mirrors a real workflow",
        "written business case when data cannot be shared",
    ]
    not_allowed = [
        "customer names, emails, addresses, phone numbers, tokens, secrets, or raw production rows",
        "write access to production databases",
        "unbounded warehouse queries",
        "private evidence that cannot be audited publicly",
    ]
    evidence_gates = [
        "non-owner reviewer or pilot contact",
        "public GitHub issue or public review link",
        "explicit permission to count the redacted result",
        "dataset shape and path tried",
        "one concrete useful, confusing, missing, or reproducible finding",
        "confirmation that no private data was posted",
    ]
    resume_upgrade_rules = [
        {
            "future_metric": "confirmed_external_users",
            "current_value": current_counts["confirmed_external_users"],
            "minimum_before_claim": 1,
            "future_resume_line": "Validated the agent with an external reviewer on an anonymized business-shaped dataset.",
        },
        {
            "future_metric": "business_case_feedback_items",
            "current_value": current_counts["business_case_feedback_items"],
            "minimum_before_claim": 1,
            "future_resume_line": "Collected public business-case feedback mapping agent findings to a real workflow risk.",
        },
        {
            "future_metric": "reproducible_feedback_items",
            "current_value": current_counts["reproducible_feedback_items"],
            "minimum_before_claim": 1,
            "future_resume_line": "Converted external replay feedback into a reproducible quality-rule improvement.",
        },
    ]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_business_pilot_offer.py",
        "public_url": "https://sunnnn2005.github.io/data-quality-agent/business-pilot-offer.html",
        "public_pilot_issue": PILOT_ISSUE_URL,
        "evidence_checklist_url": (
            "https://github.com/sunnnn2005/data-quality-agent/blob/main/docs/business-pilot-evidence-checklist.md"
        ),
        "purpose": (
            "Turn the project from a portfolio demo into a safe pilot-ready offer for people who can bring "
            "anonymized business-shaped data or a real data-quality workflow problem."
        ),
        "pilot_scope_count": len(pilot_scope),
        "pilot_scope": pilot_scope,
        "eligible_data_source_count": len(eligible_data),
        "eligible_data_sources": eligible_data,
        "not_allowed_count": len(not_allowed),
        "not_allowed": not_allowed,
        "evidence_gate_count": len(evidence_gates),
        "evidence_gates": evidence_gates,
        "current_public_counts": current_counts,
        "submission_paths": {
            "business_data_replay": replay["submission_urls"]["business_data_replay"],
            "business_case_review": business_case["business_case_issue_template"],
            "demo_feedback": feedback["feedback_issue_template"],
        },
        "resume_upgrade_rules": resume_upgrade_rules,
        "pilot_status": "ready_to_invite_not_validated",
        "public_issue_status": "open_self_authored_entrypoint_not_outcome_evidence",
        "resume_safe_summary": (
            "Published a pilot-ready business data offer with 4 pilot steps, 4 eligible data-source types, "
            "6 evidence gates, a public pilot issue, and zero current external pilot claims."
        ),
        "not_claimed": [
            "completed pilot",
            "real enterprise customer",
            "production deployment",
            "external business-data replay",
            "measured company impact",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    scope = "\n".join(
        f"| {item['step']} | {item['name']} | {item['owner']} | {item['output']} |"
        for item in payload["pilot_scope"]
    )
    eligible = "\n".join(f"- {item}" for item in payload["eligible_data_sources"])
    not_allowed = "\n".join(f"- {item}" for item in payload["not_allowed"])
    gates = "\n".join(f"- {item}" for item in payload["evidence_gates"])
    counts = "\n".join(
        f"| `{metric}` | {count} |" for metric, count in payload["current_public_counts"].items()
    )
    submissions = "\n".join(f"- `{name}`: {url}" for name, url in payload["submission_paths"].items())
    rules = "\n".join(
        "| {future_metric} | {current_value} | {minimum_before_claim} | {future_resume_line} |".format(**rule)
        for rule in payload["resume_upgrade_rules"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Business Pilot Offer

{payload["purpose"]}

Public page: [{payload["public_url"]}]({payload["public_url"]})

Public pilot issue: [{payload["public_pilot_issue"]}]({payload["public_pilot_issue"]})

Evidence checklist: [{payload["evidence_checklist_url"]}]({payload["evidence_checklist_url"]})

## Pilot Scope

| Step | Name | Owner | Output |
| ---: | --- | --- | --- |
{scope}

## Eligible Data Sources

{eligible}

## Not Allowed

{not_allowed}

## Evidence Gates

{gates}

## Current Public Counts

| Metric | Count |
| --- | ---: |
{counts}

## Submission Paths

{submissions}

## Resume Upgrade Rules

| Future metric | Current value | Minimum before claim | Future resume line |
| --- | ---: | ---: | --- |
{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def render_html(payload: dict[str, Any]) -> str:
    scope = "".join(
        f"<article><span>Step {item['step']}</span><h2>{html.escape(item['name'])}</h2>"
        f"<p>{html.escape(item['output'])}</p></article>"
        for item in payload["pilot_scope"]
    )
    gates = "".join(f"<li>{html.escape(item)}</li>" for item in payload["evidence_gates"])
    eligible = "".join(f"<li>{html.escape(item)}</li>" for item in payload["eligible_data_sources"])
    counts = "".join(
        f"<li><span>{html.escape(metric)}</span><strong>{count}</strong></li>"
        for metric, count in payload["current_public_counts"].items()
    )
    submissions = "".join(
        f"<a href='{html.escape(url)}'>{html.escape(name.replace('_', ' '))}</a>"
        for name, url in payload["submission_paths"].items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Business Pilot Offer</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #07111d;
      --panel: #111b2a;
      --line: #26364c;
      --text: #f8fafc;
      --muted: #aab8cb;
      --accent: #67e8f9;
      --accent2: #f472b6;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(135deg, #07111d 0%, #161827 58%, #0f172a 100%);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{ width: min(1120px, calc(100% - 36px)); margin: 0 auto; padding: 54px 0; }}
    .eyebrow {{ color: var(--accent); font-size: 13px; font-weight: 850; text-transform: uppercase; }}
    h1 {{ font-size: clamp(44px, 8vw, 86px); line-height: .95; letter-spacing: 0; margin: 10px 0 18px; max-width: 900px; }}
    .lede {{ color: var(--muted); font-size: 21px; max-width: 820px; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin: 34px 0; }}
    article, section {{
      background: rgba(17, 27, 42, .86);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
    }}
    article span {{ color: var(--accent2); font-weight: 850; font-size: 13px; }}
    h2 {{ margin: 6px 0 8px; font-size: 21px; letter-spacing: 0; }}
    p, li {{ color: var(--muted); }}
    .columns {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
    .counts {{ list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }}
    .counts li {{ border: 1px solid var(--line); border-radius: 8px; padding: 14px; }}
    .counts span {{ display: block; font-size: 12px; }}
    .counts strong {{ display: block; color: var(--text); font-size: 30px; margin-top: 4px; }}
    .links {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }}
    a {{ color: #07111d; background: var(--accent); border-radius: 8px; padding: 10px 14px; font-weight: 850; text-decoration: none; }}
    @media (max-width: 860px) {{ .grid, .columns, .counts {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main>
    <div class="eyebrow">Pilot-ready, not pilot-validated yet</div>
    <h1>Business Data Pilot Offer</h1>
    <p class="lede">{html.escape(payload["purpose"])}</p>
    <div class="grid">{scope}</div>
    <div class="columns">
      <section><h2>Eligible data sources</h2><ul>{eligible}</ul></section>
      <section><h2>Evidence gates</h2><ul>{gates}</ul></section>
    </div>
    <section>
      <h2>Current public counts</h2>
      <ul class="counts">{counts}</ul>
    </section>
    <section>
      <h2>Submission paths</h2>
      <p>{html.escape(payload["resume_safe_summary"])}</p>
      <div class="links">{submissions}</div>
      <div class="links"><a href="{html.escape(payload["public_pilot_issue"])}">Open public pilot issue</a></div>
      <div class="links"><a href="{html.escape(payload["evidence_checklist_url"])}">Open evidence checklist</a></div>
    </section>
  </main>
</body>
</html>
"""


def verify_business_pilot_offer(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "pilot_scope_count": 4,
        "eligible_data_source_count": 4,
        "not_allowed_count": 4,
        "evidence_gate_count": 6,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value}, got {payload.get(key)}")
    if payload["pilot_status"] != "ready_to_invite_not_validated":
        raise AssertionError("business pilot offer must not claim validation")
    if payload["public_issue_status"] != "open_self_authored_entrypoint_not_outcome_evidence":
        raise AssertionError("business pilot issue must stay classified as an entrypoint, not outcome evidence")
    if not payload["public_pilot_issue"].endswith("/issues/31"):
        raise AssertionError("business pilot offer must point to the public pilot issue")
    if not payload["evidence_checklist_url"].endswith("/docs/business-pilot-evidence-checklist.md"):
        raise AssertionError("business pilot offer must link to the evidence checklist")
    if any(count != 0 for count in payload["current_public_counts"].values()):
        raise AssertionError("business pilot offer must preserve zero external pilot counts")
    joined = json.dumps(payload, sort_keys=True).lower()
    for required in ("permission to count", "no private data", "business_data_replay", "business_case_review"):
        if required not in joined:
            raise AssertionError(f"business pilot offer missing {required!r}")
    for forbidden in ("completed pilot", "real enterprise customer", "production deployment", "measured company impact"):
        if forbidden not in payload["not_claimed"]:
            raise AssertionError(f"business pilot offer must explicitly not claim {forbidden}")
    return {"business_pilot_offer_verified": True}


def write_outputs(payload: dict[str, Any]) -> None:
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))


def main() -> None:
    payload = build_business_pilot_offer()
    verify_business_pilot_offer(payload)
    write_outputs(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
