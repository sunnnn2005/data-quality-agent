import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCOREBOARD_PATH = ROOT / "docs" / "resume-outcome-scoreboard.json"
CONVERSION_KIT_PATH = ROOT / "docs" / "contributor-conversion-kit.json"
PUBLIC_HEALTH_PATH = ROOT / "docs" / "public-evidence-health.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "outcome-proof-page.json"
OUTPUT_MD_PATH = ROOT / "docs" / "outcome-proof-page.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "outcome-proof-page.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_outcome_proof_page() -> dict[str, Any]:
    scoreboard = load_json(SCOREBOARD_PATH)
    conversion = load_json(CONVERSION_KIT_PATH)
    public_health = load_json(PUBLIC_HEALTH_PATH)

    claimable_cards = [
        {
            "label": item["label"],
            "resume_line": item["resume_line"],
            "evidence_url": item["evidence_url"],
        }
        for item in scoreboard["claimable_now"]
    ]
    blocked_cards = [
        {
            "metric": item["metric"],
            "current_count": item["current_count"],
            "required_count": item["required_count"],
            "remaining_to_threshold": item["remaining_to_threshold"],
            "future_resume_line": item["future_resume_line"],
            "evidence_gate": item["evidence_gate"],
        }
        for item in scoreboard["blocked_outcomes"]
    ]
    reviewer_actions = [
        {
            "id": item["id"],
            "target_signal": item["target_signal"],
            "best_reviewer": item["best_reviewer"],
            "entrypoint_url": item["entrypoint_url"],
            "evidence_gate": item["evidence_gate"],
        }
        for item in conversion["conversion_paths"]
    ]

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_outcome_proof_page.py",
        "purpose": (
            "Give recruiters and external reviewers one public page that separates verified outcomes from blocked "
            "future claims and routes reviewers to the exact evidence actions that can unlock stronger resume metrics."
        ),
        "proof_page_url": "https://sunnnn2005.github.io/data-quality-agent/outcome-proof-page.html",
        "claimable_card_count": len(claimable_cards),
        "blocked_card_count": len(blocked_cards),
        "reviewer_action_count": len(reviewer_actions),
        "public_health_status": public_health["status"],
        "public_health_check_count": public_health["check_count"],
        "current_public_counts": scoreboard["current_public_counts"],
        "claimable_cards": claimable_cards,
        "blocked_cards": blocked_cards,
        "reviewer_actions": reviewer_actions,
        "counting_rule": (
            "A resume outcome is upgraded only after public, non-owner, permissioned, redacted evidence passes the "
            "evidence gate. Traffic, self-authored planning issues, and outreach attempts do not count as users, "
            "feedback, business validation, or stars."
        ),
        "resume_safe_summary": (
            f"Published an outcome proof page with {len(claimable_cards)} verified resume-safe proof cards, "
            f"{len(blocked_cards)} blocked future outcome cards, {len(reviewer_actions)} reviewer action paths, "
            f"and public evidence health at {public_health['passed_count']}/{public_health['check_count']} PASS."
        ),
        "not_claimed": scoreboard["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    verified = "\n".join(
        "| {label} | {resume_line} | [evidence]({evidence_url}) |".format(**item)
        for item in payload["claimable_cards"]
    )
    blocked = "\n".join(
        "| {metric} | {current_count} | {required_count} | {remaining_to_threshold} | {evidence_gate} |".format(**item)
        for item in payload["blocked_cards"]
    )
    actions = "\n".join(
        "| {id} | {target_signal} | {best_reviewer} | [open]({entrypoint_url}) |".format(**item)
        for item in payload["reviewer_actions"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Outcome Proof Page

{payload["purpose"]}

Public page: [{payload["proof_page_url"]}]({payload["proof_page_url"]})

## Summary

| Metric | Value |
| --- | ---: |
| Claimable proof cards | {payload["claimable_card_count"]} |
| Blocked future outcome cards | {payload["blocked_card_count"]} |
| Reviewer action paths | {payload["reviewer_action_count"]} |
| Public evidence health | {payload["public_health_status"]} |
| Public evidence checks | {payload["public_health_check_count"]} |

## Verified Now

| Signal | Resume-Safe Line | Evidence |
| --- | --- | --- |
{verified}

## Blocked Until Evidence

| Metric | Current | Required | Remaining | Evidence Gate |
| --- | ---: | ---: | ---: | --- |
{blocked}

## Reviewer Actions

| Path | Target Signal | Best Reviewer | Entrypoint |
| --- | --- | --- | --- |
{actions}

## Counting Rule

{payload["counting_rule"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def render_html(payload: dict[str, Any]) -> str:
    verified_cards = "".join(
        f"""<article>
  <p class="eyebrow">Verified now</p>
  <h2>{html.escape(item["label"])}</h2>
  <p>{html.escape(item["resume_line"])}</p>
  <a href="{html.escape(item["evidence_url"], quote=True)}">View evidence</a>
</article>"""
        for item in payload["claimable_cards"]
    )
    blocked_cards = "".join(
        f"""<article>
  <p class="eyebrow blocked">Blocked future claim</p>
  <h2>{html.escape(item["metric"])}</h2>
  <p><strong>{item["current_count"]}/{item["required_count"]}</strong> collected. Remaining: {item["remaining_to_threshold"]}.</p>
  <p>{html.escape(item["evidence_gate"])}</p>
</article>"""
        for item in payload["blocked_cards"]
    )
    actions = "".join(
        f"""<article>
  <p class="eyebrow action">Reviewer action</p>
  <h2>{html.escape(item["id"])}</h2>
  <p>{html.escape(item["best_reviewer"])}</p>
  <a class="button" href="{html.escape(item["entrypoint_url"], quote=True)}">Open evidence path</a>
</article>"""
        for item in payload["reviewer_actions"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Outcome Proof Page</title>
  <style>
    :root {{ color-scheme: dark; --bg: #0e1116; --panel: #161b22; --line: #303847; --text: #f5f7fb; --muted: #aeb7c8; --pink: #ff2d6f; --green: #42d392; --amber: #ffd166; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--text); }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 48px 20px 64px; }}
    h1 {{ font-size: 48px; margin: 0 0 12px; letter-spacing: 0; }}
    h2 {{ font-size: 20px; margin: 0 0 10px; letter-spacing: 0; }}
    p {{ color: var(--muted); line-height: 1.55; }}
    .lede {{ max-width: 780px; font-size: 18px; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 28px 0; }}
    .stat, article {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
    .stat strong {{ display: block; font-size: 30px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin: 18px 0 34px; }}
    .eyebrow {{ color: var(--green); font-weight: 800; margin: 0 0 8px; }}
    .blocked {{ color: var(--amber); }}
    .action {{ color: var(--pink); }}
    a {{ color: #7cc7ff; font-weight: 700; }}
    .button {{ display: inline-block; margin-top: 8px; background: var(--pink); color: white; text-decoration: none; padding: 10px 14px; border-radius: 6px; }}
    .rule {{ border-top: 1px solid var(--line); padding-top: 20px; margin-top: 20px; }}
  </style>
</head>
<body>
<main>
  <h1>Outcome Proof Page</h1>
  <p class="lede">A public, resume-safe proof page for Data Quality Agent. Verified signals are separated from blocked future outcome claims, and every reviewer action points to a public evidence path.</p>
  <section class="stats">
    <div class="stat"><strong>{payload["claimable_card_count"]}</strong><span>verified proof cards</span></div>
    <div class="stat"><strong>{payload["blocked_card_count"]}</strong><span>blocked future claims</span></div>
    <div class="stat"><strong>{payload["reviewer_action_count"]}</strong><span>reviewer action paths</span></div>
    <div class="stat"><strong>{payload["public_health_check_count"]}</strong><span>public health checks</span></div>
  </section>
  <h2>Verified Now</h2>
  <section class="grid">{verified_cards}</section>
  <h2>Blocked Until Evidence</h2>
  <section class="grid">{blocked_cards}</section>
  <h2>Help Unlock Real Outcomes</h2>
  <section class="grid">{actions}</section>
  <section class="rule">
    <h2>Counting Rule</h2>
    <p>{html.escape(payload["counting_rule"])}</p>
  </section>
</main>
</body>
</html>
"""


def verify_outcome_proof_page(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["claimable_card_count"] != 6:
        raise AssertionError("outcome proof page must preserve six currently claimable proof cards")
    if payload["blocked_card_count"] != 6:
        raise AssertionError("outcome proof page must preserve six blocked future outcomes")
    if payload["reviewer_action_count"] != 5:
        raise AssertionError("outcome proof page must expose five reviewer action paths")
    if payload["public_health_status"] != "PASS" or payload["public_health_check_count"] < 90:
        raise AssertionError("outcome proof page must be backed by passing public evidence health")
    counts = payload["current_public_counts"]
    for key in ("confirmed_external_users", "external_feedback_items", "github_stars"):
        if counts[key] != 0:
            raise AssertionError(f"{key} must not be claimed before public evidence exists")
    for phrase in ("public, non-owner", "outreach attempts do not count", "Traffic"):
        if phrase not in payload["counting_rule"]:
            raise AssertionError(f"counting rule missing: {phrase}")
    summary = payload["resume_safe_summary"]
    for phrase in ("verified resume-safe proof cards", "blocked future outcome cards", "reviewer action paths"):
        if phrase not in summary:
            raise AssertionError(f"summary missing: {phrase}")
    markdown = render_markdown(payload)
    html_page = render_html(payload)
    for section in ("Verified Now", "Blocked Until Evidence", "Reviewer Actions", "Not Claimed"):
        if section not in markdown:
            raise AssertionError(f"markdown missing section: {section}")
    for required in ("Outcome Proof Page", "Help Unlock Real Outcomes", "Open evidence path"):
        if required not in html_page:
            raise AssertionError(f"html missing: {required}")
    return {
        "outcome_proof_page_verified": True,
        "claimable_card_count": payload["claimable_card_count"],
        "blocked_card_count": payload["blocked_card_count"],
        "reviewer_action_count": payload["reviewer_action_count"],
    }


def main() -> None:
    payload = build_outcome_proof_page()
    verify_outcome_proof_page(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(verify_outcome_proof_page(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
