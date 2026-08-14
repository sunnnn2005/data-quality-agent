import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REVIEWER_LEDGER_PATH = ROOT / "docs" / "reviewer-outcome-ledger.json"
RESUME_SNAPSHOT_PATH = ROOT / "docs" / "resume-live-proof-snapshot.json"
ACCEPTED_ROLLUP_PATH = ROOT / "docs" / "accepted-evidence-rollup.json"
ADOPTION_METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
PUBLIC_HEALTH_PATH = ROOT / "docs" / "public-evidence-health.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "public-outcome-intake-dashboard.json"
OUTPUT_MD_PATH = ROOT / "docs" / "public-outcome-intake-dashboard.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "public-outcome-intake-dashboard.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _claimable_public_signals(resume_snapshot: dict[str, Any], adoption: dict[str, Any]) -> list[dict[str, Any]]:
    verified = resume_snapshot["verified_now"]
    return [
        {
            "signal": "Public release",
            "value": verified["public_release"],
            "resume_use": "Can describe the project as publicly released.",
            "evidence_url": resume_snapshot["evidence_links"]["github_repo"],
        },
        {
            "signal": "Containerized runnable artifact",
            "value": "published" if verified["container_image_published"] else "not published",
            "resume_use": "Can mention GHCR image and reproducible container setup.",
            "evidence_url": resume_snapshot["evidence_links"]["container_image"],
        },
        {
            "signal": "CI and public evidence health",
            "value": verified["public_evidence_health"],
            "resume_use": "Can mention CI-verified public proof system.",
            "evidence_url": resume_snapshot["evidence_links"]["public_evidence_health"],
        },
        {
            "signal": "GitHub repository interest",
            "value": f'{adoption["stars"]} stars, {adoption["forks"]} forks',
            "resume_use": "Can mention forks only as a public repo signal; stars remain zero.",
            "evidence_url": resume_snapshot["evidence_links"]["public_github_stats"],
        },
    ]


def _blocked_intake_paths(reviewer_ledger: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "metric": row["metric"],
            "label": row["label"],
            "current": row["accepted_evidence_count"],
            "required": row["required_count"],
            "remaining": row["remaining_to_resume_claim"],
            "best_reviewer": row["reviewer_profile"],
            "submission_url": row["submission_url"],
            "evidence_gate": row["evidence_gate"],
            "future_resume_wording": row["allowed_resume_wording_after_threshold"],
            "next_action": row["next_action"],
        }
        for row in reviewer_ledger["outcome_rows"]
    ]


def build_public_outcome_intake_dashboard() -> dict[str, Any]:
    reviewer_ledger = load_json(REVIEWER_LEDGER_PATH)
    resume_snapshot = load_json(RESUME_SNAPSHOT_PATH)
    accepted_rollup = load_json(ACCEPTED_ROLLUP_PATH)
    adoption = load_json(ADOPTION_METRICS_PATH)
    public_health = load_json(PUBLIC_HEALTH_PATH)

    claimable_signals = _claimable_public_signals(resume_snapshot, adoption)
    blocked_paths = _blocked_intake_paths(reviewer_ledger)

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_public_outcome_intake_dashboard.py",
        "purpose": (
            "Give reviewers and recruiters one public intake dashboard that separates claimable public proof from "
            "blocked outcome metrics and routes each missing metric to a public evidence submission path."
        ),
        "dashboard_url": "https://sunnnn2005.github.io/data-quality-agent/public-outcome-intake-dashboard.html",
        "input_artifacts": [
            "docs/reviewer-outcome-ledger.json",
            "docs/resume-live-proof-snapshot.json",
            "docs/accepted-evidence-rollup.json",
            "docs/adoption-metrics.json",
            "docs/public-evidence-health.json",
        ],
        "claimable_signal_count": len(claimable_signals),
        "blocked_intake_path_count": len(blocked_paths),
        "accepted_external_evidence_count": accepted_rollup["accepted_issue_count"],
        "public_health_status": public_health["status"],
        "public_health_check_count": public_health["check_count"],
        "github_stars": adoption["stars"],
        "github_forks": adoption["forks"],
        "claimable_public_signals": claimable_signals,
        "blocked_intake_paths": blocked_paths,
        "resume_safe_bullets": resume_snapshot["resume_safe_bullets"],
        "next_resume_unlocks": resume_snapshot["next_resume_unlocks"],
        "counting_rule": (
            "Only public, non-owner, permissioned, redacted GitHub evidence can unlock external users, feedback, "
            "AI reviews, business validation, real-model runs, or GitHub-star resume claims. Page views, self-authored "
            "planning issues, private replies, and outreach attempts are not counted."
        ),
        "resume_safe_summary": (
            f"Published a public outcome intake dashboard with {len(claimable_signals)} claimable proof signals, "
            f"{len(blocked_paths)} blocked external-outcome intake paths, {accepted_rollup['accepted_issue_count']} "
            f"accepted external evidence items, {adoption['stars']} GitHub stars, and public evidence health at "
            f"{public_health['passed_count']}/{public_health['check_count']} PASS."
        ),
        "not_claimed": [
            "No confirmed external users are claimed.",
            "No external customer or business feedback is claimed.",
            "No enterprise deployment, production usage, or measured company impact is claimed.",
            "No GitHub stars beyond the live public count are claimed.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    claimable_rows = "\n".join(
        "| {signal} | {value} | {resume_use} | [evidence]({evidence_url}) |".format(**item)
        for item in payload["claimable_public_signals"]
    )
    intake_rows = "\n".join(
        "| {label} | `{metric}` | {current}/{required} | {best_reviewer} | [submit]({submission_url}) |".format(**item)
        for item in payload["blocked_intake_paths"]
    )
    bullets = "\n".join(f"- {item}" for item in payload["resume_safe_bullets"])
    unlocks = "\n".join(f"- {item}" for item in payload["next_resume_unlocks"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Public Outcome Intake Dashboard

{payload["purpose"]}

Public page: [{payload["dashboard_url"]}]({payload["dashboard_url"]})

## Summary

| Metric | Value |
| --- | ---: |
| Claimable public signals | {payload["claimable_signal_count"]} |
| Blocked intake paths | {payload["blocked_intake_path_count"]} |
| Accepted external evidence | {payload["accepted_external_evidence_count"]} |
| GitHub stars | {payload["github_stars"]} |
| GitHub forks | {payload["github_forks"]} |
| Public evidence health | {payload["public_health_status"]} |
| Public evidence checks | {payload["public_health_check_count"]} |

## Claimable Public Proof

| Signal | Current Value | Resume Use | Evidence |
| --- | --- | --- | --- |
{claimable_rows}

## Intake Paths For Real Outcomes

| Outcome | Metric | Accepted / Required | Best Reviewer | Submission |
| --- | --- | ---: | --- | --- |
{intake_rows}

## Resume-Safe Bullets Now

{bullets}

## Next Resume Unlocks

{unlocks}

## Counting Rule

{payload["counting_rule"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def render_html(payload: dict[str, Any]) -> str:
    proof_cards = "".join(
        f"""<article>
  <p class="eyebrow">Claimable now</p>
  <h2>{html.escape(item["signal"])}</h2>
  <strong>{html.escape(str(item["value"]))}</strong>
  <p>{html.escape(item["resume_use"])}</p>
  <a href="{html.escape(item["evidence_url"], quote=True)}">View evidence</a>
</article>"""
        for item in payload["claimable_public_signals"]
    )
    intake_cards = "".join(
        f"""<article>
  <p class="eyebrow blocked">{html.escape(item["metric"])}</p>
  <h2>{html.escape(item["label"])}</h2>
  <strong>{item["current"]}/{item["required"]} accepted</strong>
  <p>{html.escape(item["evidence_gate"])}</p>
  <p>{html.escape(item["future_resume_wording"])}</p>
  <a class="button" href="{html.escape(item["submission_url"], quote=True)}">Submit public evidence</a>
</article>"""
        for item in payload["blocked_intake_paths"]
    )
    bullets = "".join(f"<li>{html.escape(item)}</li>" for item in payload["resume_safe_bullets"])
    unlocks = "".join(f"<li>{html.escape(item)}</li>" for item in payload["next_resume_unlocks"])
    not_claimed = "".join(f"<li>{html.escape(item)}</li>" for item in payload["not_claimed"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Public Outcome Intake Dashboard</title>
  <style>
    :root {{ color-scheme: dark; --bg: #0b0f14; --panel: #151b23; --line: #2b3442; --text: #f7f9fc; --muted: #a8b3c4; --blue: #67d4ff; --green: #42d392; --pink: #ff2d6f; --amber: #ffd166; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 48px 20px 72px; }}
    h1 {{ margin: 0; font-size: 48px; letter-spacing: 0; }}
    h2 {{ margin: 0 0 10px; font-size: 20px; letter-spacing: 0; }}
    p, li {{ color: var(--muted); line-height: 1.55; }}
    .lede {{ max-width: 820px; font-size: 18px; }}
    .stats, .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; }}
    .stats {{ margin: 28px 0 34px; }}
    .stat, article, .panel {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
    .stat strong, article strong {{ display: block; color: var(--text); font-size: 28px; margin-bottom: 8px; }}
    .eyebrow {{ color: var(--green); font-weight: 800; margin: 0 0 8px; }}
    .blocked {{ color: var(--amber); }}
    a {{ color: var(--blue); font-weight: 800; }}
    .button {{ display: inline-block; margin-top: 8px; padding: 10px 14px; border-radius: 6px; color: white; background: var(--pink); text-decoration: none; }}
    section {{ margin-top: 34px; }}
    ul {{ padding-left: 20px; }}
  </style>
</head>
<body>
<main>
  <h1>Public Outcome Intake Dashboard</h1>
  <p class="lede">One public page for reviewers and recruiters to see what can be claimed now, what is blocked until external evidence exists, and exactly where to submit evidence that can unlock future resume outcomes.</p>
  <section class="stats">
    <div class="stat"><strong>{payload["claimable_signal_count"]}</strong><span>claimable proof signals</span></div>
    <div class="stat"><strong>{payload["blocked_intake_path_count"]}</strong><span>blocked intake paths</span></div>
    <div class="stat"><strong>{payload["accepted_external_evidence_count"]}</strong><span>accepted external evidence</span></div>
    <div class="stat"><strong>{payload["github_stars"]}</strong><span>GitHub stars</span></div>
    <div class="stat"><strong>{payload["public_health_check_count"]}</strong><span>public evidence checks</span></div>
  </section>
  <section>
    <h2>Claimable Public Proof</h2>
    <div class="grid">{proof_cards}</div>
  </section>
  <section>
    <h2>Submit Evidence For Real Outcomes</h2>
    <div class="grid">{intake_cards}</div>
  </section>
  <section class="panel">
    <h2>Resume-Safe Bullets Now</h2>
    <ul>{bullets}</ul>
  </section>
  <section class="panel">
    <h2>Next Resume Unlocks</h2>
    <ul>{unlocks}</ul>
  </section>
  <section class="panel">
    <h2>Counting Rule</h2>
    <p>{html.escape(payload["counting_rule"])}</p>
    <h2>Not Claimed</h2>
    <ul>{not_claimed}</ul>
  </section>
</main>
</body>
</html>
"""


def verify_public_outcome_intake_dashboard(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["claimable_signal_count"] != 4:
        raise AssertionError("dashboard must expose four claimable public proof signals")
    if payload["blocked_intake_path_count"] != 5:
        raise AssertionError("dashboard must expose five blocked external-outcome intake paths")
    if payload["accepted_external_evidence_count"] != 0:
        raise AssertionError("dashboard must preserve zero accepted external evidence")
    if payload["github_stars"] != 0:
        raise AssertionError("dashboard must preserve the live zero-star baseline")
    if payload["public_health_status"] != "PASS" or payload["public_health_check_count"] < 100:
        raise AssertionError("dashboard must be backed by passing public evidence health")
    for item in payload["blocked_intake_paths"]:
        if item["current"] != 0 or item["remaining"] < 1:
            raise AssertionError("blocked paths must stay locked until accepted public evidence exists")
        if not item["submission_url"].startswith("https://github.com/"):
            raise AssertionError("blocked paths must use public GitHub issue submission URLs")
        if "public" not in item["evidence_gate"].lower():
            raise AssertionError("blocked paths must document public evidence gates")
    for phrase in ("public, non-owner", "private replies", "outreach attempts"):
        if phrase not in payload["counting_rule"]:
            raise AssertionError(f"dashboard counting rule missing: {phrase}")
    for forbidden in ("confirmed external users", "measured company impact", "GitHub stars beyond"):
        if not any(forbidden in item for item in payload["not_claimed"]):
            raise AssertionError(f"dashboard must avoid overclaiming: {forbidden}")
    return {
        "public_outcome_intake_dashboard_verified": True,
        "claimable_signal_count": payload["claimable_signal_count"],
        "blocked_intake_path_count": payload["blocked_intake_path_count"],
        "accepted_external_evidence_count": payload["accepted_external_evidence_count"],
    }


def main() -> None:
    payload = build_public_outcome_intake_dashboard()
    verify_public_outcome_intake_dashboard(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(verify_public_outcome_intake_dashboard(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
