import html
import json
from pathlib import Path
from typing import Any
from urllib.parse import unquote_plus, urlencode


ROOT = Path(__file__).resolve().parents[1]
SPRINT_PATH = ROOT / "docs" / "outcome-sprint-plan.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "one-click-evidence-links.json"
OUTPUT_MD_PATH = ROOT / "docs" / "one-click-evidence-links.md"
OUTPUT_HTML_PATH = ROOT / "docs" / "one-click-evidence-links.html"
ISSUE_NEW_URL = "https://github.com/sunnnn2005/data-quality-agent/issues/new"


LABELS_BY_METRIC = {
    "ai_engineer_review_items": "ai-engineer-review,evidence-candidate",
    "business_case_feedback_items": "business-case,evidence-candidate",
    "confirmed_external_users": "confirmed-user,evidence-candidate",
    "external_feedback_items": "feedback,evidence-candidate",
    "reproducible_feedback_items": "reproducible-run,evidence-candidate",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _issue_body(day: dict[str, Any]) -> str:
    evidence = "\n".join(f"- [ ] {item}" for item in day["completion_evidence"])
    return f"""## Review Path

Target metric: `{day["target_metric"]}`
Execution artifact: `{day["execution_artifact"]}`
Reviewer profile: {day["reviewer_profile"]}

## What I Tried

- URL, command, or file inspected:
- What worked:
- What was confusing, broken, or useful:

## Completion Evidence

{evidence}

## Permission and Privacy

- [ ] I am not the repository owner.
- [ ] I give permission for this public issue to be counted as project review evidence.
- [ ] I confirm this public issue contains no raw customer data, private business data, secrets, tokens, private emails, addresses, or production rows.

## Resume Boundary

{day["resume_unlock_gate"]}
"""


def _link_for_day(day: dict[str, Any]) -> dict[str, Any]:
    title = f"Evidence candidate: {day['title']} ({day['target_metric']})"
    labels = LABELS_BY_METRIC.get(day["target_metric"], "evidence-candidate")
    body = _issue_body(day)
    query = urlencode({"title": title, "labels": labels, "body": body})
    return {
        "day": day["day"],
        "title": day["title"],
        "target_metric": day["target_metric"],
        "current_count": day["current_count"],
        "labels": labels.split(","),
        "issue_url": f"{ISSUE_NEW_URL}?{query}",
        "required_permission_sentence": "I give permission for this public issue to be counted as project review evidence.",
        "required_no_private_data_sentence": (
            "I confirm this public issue contains no raw customer data, private business data, secrets, tokens, "
            "private emails, addresses, or production rows."
        ),
        "resume_unlock_gate": day["resume_unlock_gate"],
    }


def build_one_click_evidence_links() -> dict[str, Any]:
    sprint = load_json(SPRINT_PATH)
    link_days = [
        day
        for day in sprint["sprint_days"]
        if day["target_metric"] in LABELS_BY_METRIC
    ]
    links = [_link_for_day(day) for day in link_days]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_one_click_evidence_links.py",
        "purpose": (
            "Reduce reviewer friction by publishing one-click GitHub issue links with prefilled public evidence "
            "fields, permission text, and privacy boundaries for the outcome sprint."
        ),
        "link_count": len(links),
        "target_metric_count": len({link["target_metric"] for link in links}),
        "current_public_counts": sprint["current_public_counts"],
        "claimable_resume_metric_count": sprint["claimable_resume_metric_count"],
        "accepted_issue_count": sprint["accepted_issue_count"],
        "links": links,
        "counting_rule": (
            "Opening a one-click issue link is not evidence by itself. A metric counts only after a non-owner "
            "submits the public issue, includes permission, includes no private data, and passes the evidence gate."
        ),
        "resume_safe_summary": (
            "Published 4 one-click public evidence links for external reviewers, each with prefilled permission "
            "and privacy language, while preserving zero accepted evidence and zero resume upgrades."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| Day {item['day']} | `{item['target_metric']}` | {item['current_count']} | [open issue]({item['issue_url']}) |"
        for item in payload["links"]
    )
    counts = "\n".join(
        f"| `{key}` | {value} |" for key, value in payload["current_public_counts"].items()
    )
    return f"""# One-Click Evidence Links

This generated artifact gives external reviewers prefilled GitHub issue links for submitting public, countable evidence.

## Current Public Counts

| Metric | Count |
| --- | ---: |
{counts}

## Links

| Sprint Day | Target Metric | Current Count | Link |
| --- | --- | ---: | --- |
{rows}

## Counting Rule

{payload["counting_rule"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}
"""


def render_html(payload: dict[str, Any]) -> str:
    cards = []
    for item in payload["links"]:
        labels = ", ".join(item["labels"])
        cards.append(
            f"""<article>
  <p class="eyebrow">Day {item["day"]} · {html.escape(item["target_metric"])}</p>
  <h2>{html.escape(item["title"])}</h2>
  <p>Current count: <strong>{item["current_count"]}</strong></p>
  <p>Labels: {html.escape(labels)}</p>
  <a class="button" href="{html.escape(item["issue_url"], quote=True)}">Open prefilled GitHub issue</a>
</article>"""
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>One-Click Evidence Links</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0e1116; color: #f5f7fb; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 48px 20px; }}
    h1 {{ font-size: 44px; margin: 0 0 12px; }}
    p {{ color: #aeb7c8; line-height: 1.55; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-top: 28px; }}
    article {{ background: #161b22; border: 1px solid #303847; border-radius: 8px; padding: 18px; }}
    .eyebrow {{ color: #ff2d6f; font-weight: 700; margin: 0 0 8px; }}
    h2 {{ font-size: 20px; margin: 0 0 12px; }}
    .button {{ display: inline-block; margin-top: 10px; color: white; background: #ff2d6f; text-decoration: none; padding: 10px 14px; border-radius: 6px; font-weight: 700; }}
    .rule {{ border-top: 1px solid #303847; margin-top: 32px; padding-top: 20px; }}
  </style>
</head>
<body>
<main>
  <h1>One-Click Evidence Links</h1>
  <p>Use these links to submit public, permissioned, redacted review evidence. Counts stay at zero until a non-owner issue passes the evidence gate.</p>
  <section class="grid">
    {''.join(cards)}
  </section>
  <section class="rule">
    <h2>Counting Rule</h2>
    <p>{html.escape(payload["counting_rule"])}</p>
  </section>
</main>
</body>
</html>
"""


def verify_one_click_evidence_links(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["link_count"] != 4:
        raise AssertionError("one-click evidence links must expose four public issue links")
    if payload["target_metric_count"] != 4:
        raise AssertionError("one-click evidence links must cover four reviewer-facing metrics")
    if payload["claimable_resume_metric_count"] != 0 or payload["accepted_issue_count"] != 0:
        raise AssertionError("one-click evidence links must not upgrade resume outcomes")
    if any(value != 0 for value in payload["current_public_counts"].values()):
        raise AssertionError("one-click evidence links must preserve zero public outcome counts")
    for item in payload["links"]:
        if not item["issue_url"].startswith(ISSUE_NEW_URL):
            raise AssertionError("one-click link must target the project GitHub issue form")
        decoded_url = unquote_plus(item["issue_url"])
        for required in (
            "I give permission for this public issue to be counted as project review evidence.",
            "I confirm this public issue contains no raw customer data",
        ):
            if required not in decoded_url:
                raise AssertionError(f"one-click issue URL missing required text: {required}")
    joined = json.dumps(payload, sort_keys=True)
    for phrase in (
        "Opening a one-click issue link is not evidence by itself.",
        "non-owner submits the public issue",
        "zero accepted evidence",
        "zero resume upgrades",
    ):
        if phrase not in joined:
            raise AssertionError(f"one-click evidence links missing phrase: {phrase}")
    return {
        "one_click_evidence_links_verified": True,
        "link_count": payload["link_count"],
        "target_metric_count": payload["target_metric_count"],
    }


def main() -> None:
    payload = build_one_click_evidence_links()
    verify_one_click_evidence_links(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    OUTPUT_HTML_PATH.write_text(render_html(payload))
    print(json.dumps(verify_one_click_evidence_links(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
