import json
import re
import subprocess
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
OUTREACH_TRACKER_PATH = ROOT / "docs" / "external-reviewer-outreach-tracker.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.json"
OUTPUT_MD_PATH = ROOT / "docs" / "external-reviewer-evidence-gate.md"
OWNER_LOGINS = {"sunnnn2005"}
SENSITIVE_TERMS = ("ssn", "api_key", "secret", "token", "password", "customer email", "raw production rows")
EXTERNAL_RUN_LABELS = {"feedback", "pilot", "reproducible", "confirmed-user"}
BUSINESS_CASE_LABELS = {"business-case"}
AI_ENGINEER_REVIEW_LABELS = {"ai-engineer-review"}
BUSINESS_DATA_REPLAY_LABELS = {"business-data-replay"}
REPO = "sunnnn2005/data-quality-agent"
PUBLIC_ISSUES_API = f"https://api.github.com/repos/{REPO}/issues"
TRACKED_LABELS = sorted(
    EXTERNAL_RUN_LABELS | BUSINESS_CASE_LABELS | AI_ENGINEER_REVIEW_LABELS | BUSINESS_DATA_REPLAY_LABELS
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _labels(issue: dict[str, Any]) -> set[str]:
    return {label["name"] for label in issue.get("labels", [])}


def _checked(body: str, label: str) -> bool:
    escaped = re.escape(label)
    return bool(re.search(rf"- \[[xX]\]\s+{escaped}", body))


def _section_text(body: str, heading: str) -> str:
    match = re.search(rf"##\s+{re.escape(heading)}\s*(.*?)(?=\n##\s+|\Z)", body, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _compact_section(body: str, heading: str, *, max_chars: int = 500) -> str:
    text = " ".join(_section_text(body, heading).split())
    return text[:max_chars].strip()


def _non_placeholder(section: str) -> bool:
    normalized = section.strip()
    if not normalized:
        return False
    placeholders = {
        "what worked, what was confusing, what failed, or what would make this more useful?",
        "paste only safe summaries, such as status, quality score, check names, endpoint names, or screenshots with private data removed.",
    }
    return normalized.lower() not in placeholders


def evaluate_issue(issue: dict[str, Any]) -> dict[str, Any]:
    body = issue.get("body") or ""
    labels = _labels(issue)
    author = issue.get("author", {}).get("login", "")
    failure_reasons: list[str] = []
    evidence_type = "unknown"
    counts_toward: list[str] = []
    extracted_business_impact: dict[str, str] = {}

    if author in OWNER_LOGINS:
        failure_reasons.append("self-authored issue")

    scan_body = "\n".join(
        line
        for line in body.splitlines()
        if "This issue contains no private business data, secrets, customer names, emails, addresses, or raw production rows."
        not in line
        and "This issue contains no customer names, emails, addresses, tokens, secrets, or raw production rows." not in line
    )
    lower_body = scan_body.lower()
    sensitive_hits = sorted(term for term in SENSITIVE_TERMS if term in lower_body)
    if sensitive_hits:
        failure_reasons.append("contains sensitive-data risk terms")

    if labels & BUSINESS_DATA_REPLAY_LABELS:
        evidence_type = "business_data_replay"
        if not _checked(body, "This issue contains no customer names, emails, addresses, tokens, secrets, or raw production rows."):
            failure_reasons.append("missing no-sensitive-data replay checkbox")
        if not _checked(body, "This can be counted as a confirmed anonymized replay."):
            failure_reasons.append("missing confirmed anonymized replay permission")
        if not _checked(body, "This can be counted as external feedback."):
            failure_reasons.append("missing external feedback permission")
        if _checked(body, "Repository/docs review before trying my own data"):
            failure_reasons.append("docs-only review is not a confirmed business-data replay")
        if not (
            _checked(body, "Sanitized CSV upload: `POST /business-data/agent-report`")
            or _checked(body, "Read-only PostgreSQL table: `POST /postgres/support-tickets/agent-report`")
            or _checked(body, "Local Docker Compose support-ticket replay")
        ):
            failure_reasons.append("missing business-data replay path tried")
        for heading in ("Data source type", "Dataset shape", "Agent run summary", "What did it catch or miss?"):
            if not _non_placeholder(_section_text(body, heading)):
                failure_reasons.append(f"missing {heading.lower()} evidence")
        run_summary = _section_text(body, "Agent run summary")
        for required_phrase in ("Command or endpoint used:", "Report status:", "Finding count:", "Selected tools shown in the agent trace:"):
            if required_phrase not in run_summary:
                failure_reasons.append(f"missing replay run summary field: {required_phrase}")
        counts_toward.extend(["confirmed_external_users", "external_feedback_items"])
        if _checked(body, "Local Docker Compose support-ticket replay"):
            counts_toward.append("reproducible_feedback_items")
    elif labels & EXTERNAL_RUN_LABELS:
        evidence_type = "external_run_review"
        if not _checked(body, "This issue contains no private business data, secrets, customer names, emails, addresses, or raw production rows."):
            failure_reasons.append("missing no-private-data checkbox")
        if not _checked(body, "This can be counted as public external run evidence."):
            failure_reasons.append("missing public external run permission")
        if not (_checked(body, "Public demo review") or _checked(body, "GHCR container smoke run") or _checked(body, "Docker Compose PostgreSQL replay")):
            failure_reasons.append("missing runnable path tried")
        if _checked(body, "I reviewed the docs but did not run it"):
            failure_reasons.append("docs-only review is not a confirmed run")
        if not _non_placeholder(_section_text(body, "Commands or URLs used")):
            failure_reasons.append("missing command or URL evidence")
        if not _non_placeholder(_section_text(body, "Observed result")):
            failure_reasons.append("missing observed result evidence")
        if not _non_placeholder(_section_text(body, "Main feedback")):
            failure_reasons.append("missing main feedback")
        if "feedback" in labels or _checked(body, "This can be counted as external feedback."):
            counts_toward.append("external_feedback_items")
        if _checked(body, "This can be counted as public external run evidence."):
            counts_toward.append("confirmed_external_users")
        if "reproducible" in labels or _checked(body, "This can be counted as a reproducible local replay, if I ran the container or Docker Compose path."):
            counts_toward.append("reproducible_feedback_items")
    elif labels & BUSINESS_CASE_LABELS:
        evidence_type = "business_case_review"
        if not _checked(body, "This can be counted as anonymized public business-case feedback."):
            failure_reasons.append("missing business-case counting permission")
        if not _checked(body, "This can be counted as an anonymized business-impact signal."):
            failure_reasons.append("missing business-impact counting permission")
        for heading in (
            "Business context",
            "Data-quality problem",
            "Business impact",
            "Fields involved",
            "Evidence from this project",
        ):
            if not _non_placeholder(_section_text(body, heading)):
                failure_reasons.append(f"missing {heading.lower()} evidence")
        extracted_business_impact = {
            "business_context": _compact_section(body, "Business context"),
            "data_quality_problem": _compact_section(body, "Data-quality problem"),
            "business_impact": _compact_section(body, "Business impact"),
            "fields_involved": _compact_section(body, "Fields involved"),
            "project_evidence_mapping": _compact_section(body, "Evidence from this project"),
        }
        counts_toward.append("business_case_feedback_items")
    elif labels & AI_ENGINEER_REVIEW_LABELS:
        evidence_type = "ai_engineer_review"
        if not _checked(body, "You may count this public issue as external AI Engineer project feedback."):
            failure_reasons.append("missing AI Engineer review counting permission")
        if _checked(body, "Do not count this issue publicly."):
            failure_reasons.append("reviewer opted out of public counting")
        inspected = _section_text(body, "What did you inspect?")
        if not _non_placeholder(inspected):
            inspected = _section_text(body, "Path or command used")
        if not _non_placeholder(inspected):
            failure_reasons.append("missing inspected path or command evidence")
        for heading in ("Strongest AI Engineer signals", "Missing or weak AI Engineer signals"):
            if not _non_placeholder(_section_text(body, heading)):
                failure_reasons.append(f"missing {heading.lower()} evidence")
        counts_toward.append("ai_engineer_review_items")
    else:
        failure_reasons.append("missing tracked evidence labels")

    counts_toward = sorted(set(counts_toward))
    accepted = not failure_reasons and bool(counts_toward)
    return {
        "issue_number": issue.get("number"),
        "title": issue.get("title"),
        "url": issue.get("url"),
        "author": author,
        "labels": sorted(labels),
        "evidence_type": evidence_type,
        "accepted": accepted,
        "counts_toward": counts_toward if accepted else [],
        "rejected_counts_toward": counts_toward if not accepted else [],
        "failure_reasons": failure_reasons,
        "sensitive_hits": sensitive_hits,
        "extracted_business_impact": extracted_business_impact if evidence_type == "business_case_review" else {},
    }


def evaluate_issues(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted((evaluate_issue(issue) for issue in issues), key=lambda item: item["issue_number"] or 0)


def count_accepted(evaluations: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
        "business_case_feedback_items": 0,
        "ai_engineer_review_items": 0,
    }
    for item in evaluations:
        if not item["accepted"]:
            continue
        for metric in item["counts_toward"]:
            counts[metric] += 1
    return counts


def collect_public_reviewer_issues() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    issues_by_number: dict[int, dict[str, Any]] = {}
    errors: list[str] = []
    used_public_api = False
    for label in TRACKED_LABELS:
        try:
            completed = subprocess.run(
                [
                    "gh",
                    "issue",
                    "list",
                    "--repo",
                    REPO,
                    "--label",
                    label,
                    "--state",
                    "all",
                    "--limit",
                    "1000",
                    "--json",
                    "number,title,url,author,labels,body",
                ],
                check=True,
                capture_output=True,
                text=True,
                cwd=ROOT,
            )
        except (FileNotFoundError, subprocess.CalledProcessError) as exc:
            try:
                issues = _collect_public_issues_by_label(label)
                used_public_api = True
            except (URLError, TimeoutError, json.JSONDecodeError) as api_exc:
                errors.append(f"{label}: gh={exc.__class__.__name__}; public_api={api_exc.__class__.__name__}")
                continue
        else:
            issues = json.loads(completed.stdout)
        for issue in issues:
            number = issue.get("number")
            if isinstance(number, int):
                issues_by_number[number] = issue

    issues = [issues_by_number[number] for number in sorted(issues_by_number)]
    return issues, {
        "source": "github_public_api" if used_public_api else "github_issues",
        "repo": REPO,
        "tracked_labels": TRACKED_LABELS,
        "collected_issue_count": len(issues),
        "error_count": len(errors),
        "errors": errors,
    }


def _collect_public_issues_by_label(label: str) -> list[dict[str, Any]]:
    query = urlencode({"state": "all", "labels": label, "per_page": "100"})
    request = Request(
        f"{PUBLIC_ISSUES_API}?{query}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "data-quality-agent-external-reviewer-evidence-gate",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(request, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return [_normalize_public_api_issue(issue) for issue in payload if "pull_request" not in issue]


def _normalize_public_api_issue(issue: dict[str, Any]) -> dict[str, Any]:
    return {
        "number": issue.get("number"),
        "title": issue.get("title"),
        "url": issue.get("html_url"),
        "author": {"login": (issue.get("user") or {}).get("login", "")},
        "labels": [{"name": label.get("name", "")} for label in issue.get("labels", [])],
        "body": issue.get("body") or "",
    }


def build_external_reviewer_evidence_gate(issues: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    feedback = load_json(FEEDBACK_METRICS_PATH)
    outreach = load_json(OUTREACH_TRACKER_PATH)
    if issues is None:
        issues, collection = collect_public_reviewer_issues()
    else:
        collection = {
            "source": "provided_issues",
            "repo": REPO,
            "tracked_labels": TRACKED_LABELS,
            "collected_issue_count": len(issues),
            "error_count": 0,
            "errors": [],
        }
    evaluations = evaluate_issues(issues)
    accepted_counts = count_accepted(evaluations)
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_external_reviewer_evidence_gate.py",
        "purpose": (
            "Validate public reviewer issues before they can increase resume-safe user, feedback, reproducible-run, "
            "business-case, or AI Engineer review metrics."
        ),
        "evaluated_issue_count": len(evaluations),
        "issue_collection": collection,
        "accepted_issue_count": sum(1 for item in evaluations if item["accepted"]),
        "rejected_issue_count": sum(1 for item in evaluations if not item["accepted"]),
        "evaluations": evaluations,
        "accepted_counts": accepted_counts,
        "current_public_counts": {
            "external_feedback_items": feedback["external_feedback_items"],
            "confirmed_external_users": feedback["confirmed_external_users"],
            "reproducible_feedback_items": feedback["reproducible_feedback_items"],
            "business_case_feedback_items": feedback["business_case_feedback_items"],
            "ai_engineer_review_items": feedback.get("ai_engineer_review_items", 0),
        },
        "linked_outreach_queue_count": outreach["queue_count"],
        "gate_rules": [
            "Self-authored issues do not count as external evidence.",
            "Reviewer must grant explicit permission before a run or feedback is counted.",
            "A docs-only review does not count as a confirmed run.",
            "Commands or URLs used, observed result, and main feedback must be non-placeholder text.",
            "AI Engineer review issues require explicit permission plus inspected paths and concrete signal feedback.",
            "Business-data replay issues require a sanitized data source type, dataset shape, agent run summary, and catch-or-miss feedback.",
            "Issues containing sensitive-data risk terms are rejected until redacted.",
            "The default artifact collects tracked public GitHub issues before applying the evidence gate.",
            "When GitHub CLI auth is unavailable, collection falls back to the public GitHub Issues API.",
        ],
        "resume_safe_summary": (
            "Published a CI-verified external reviewer evidence gate that validates issue body fields, explicit "
            "permission, non-owner authorship, runnable-path evidence, and sensitive-data guardrails before any "
            "reviewer issue can increase resume-safe usage, feedback, or AI Engineer review metrics."
        ),
        "not_claimed": [
            "No accepted external reviewer issue exists yet.",
            "No user, feedback, reproducible-run, business-case, or AI Engineer review count is increased by planning issues.",
            "No private business data is accepted as evidence.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    counts = "\n".join(f"| {key.replace('_', ' ').title()} | {value} |" for key, value in payload["accepted_counts"].items())
    rules = "\n".join(f"- {item}" for item in payload["gate_rules"])
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    rows = "\n".join(
        "| #{issue_number} | [{title}]({url}) | {author} | {evidence_type} | {accepted} | {metrics} | {reasons} |".format(
            issue_number=item["issue_number"],
            title=item["title"],
            url=item["url"],
            author=item["author"],
            evidence_type=item["evidence_type"],
            accepted=item["accepted"],
            metrics=", ".join(item["counts_toward"]),
            reasons=", ".join(item["failure_reasons"]),
        )
        for item in payload["evaluations"]
    )
    if not rows:
        rows = "| - | - | - | - | - | - | - |"
    return f"""# External Reviewer Evidence Gate

This generated gate validates public reviewer issues before they can become resume-safe outcome metrics.

## Summary

| Metric | Value |
| --- | ---: |
| Evaluated issues | {payload["evaluated_issue_count"]} |
| Accepted issues | {payload["accepted_issue_count"]} |
| Rejected issues | {payload["rejected_issue_count"]} |
| Collected public issues | {payload["issue_collection"]["collected_issue_count"]} |
| Collection errors | {payload["issue_collection"]["error_count"]} |
| Linked outreach queue | {payload["linked_outreach_queue_count"]} |

## Accepted Counts

| Metric | Accepted count |
| --- | ---: |
{counts}

## Evaluations

| Issue | Title | Author | Evidence Type | Accepted | Counts Toward | Failure Reasons |
| --- | --- | --- | --- | --- | --- | --- |
{rows}

## Gate Rules

{rules}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_external_reviewer_evidence_gate(payload: dict[str, Any]) -> dict[str, Any]:
    expected_zero = {
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "reproducible_feedback_items": 0,
        "business_case_feedback_items": 0,
        "ai_engineer_review_items": 0,
    }
    if payload["linked_outreach_queue_count"] != 3:
        raise AssertionError("external reviewer evidence gate must link the 3 queued reviewer segments")
    if payload["accepted_counts"] != expected_zero:
        raise AssertionError("external reviewer evidence gate must not count evidence before accepted public issues")
    if len(payload["gate_rules"]) != 9:
        raise AssertionError("external reviewer evidence gate must document nine counting rules")
    for required in (
        "Self-authored issues do not count as external evidence.",
        "Reviewer must grant explicit permission before a run or feedback is counted.",
        "AI Engineer review issues require explicit permission plus inspected paths and concrete signal feedback.",
        "Business-data replay issues require a sanitized data source type, dataset shape, agent run summary, and catch-or-miss feedback.",
        "Issues containing sensitive-data risk terms are rejected until redacted.",
        "The default artifact collects tracked public GitHub issues before applying the evidence gate.",
        "When GitHub CLI auth is unavailable, collection falls back to the public GitHub Issues API.",
    ):
        if required not in payload["gate_rules"]:
            raise AssertionError(f"external reviewer evidence gate missing rule: {required}")
    if payload["issue_collection"]["source"] not in {"github_issues", "github_public_api", "provided_issues"}:
        raise AssertionError("external reviewer evidence gate must document issue collection source")
    for required in (
        "No accepted external reviewer issue exists yet.",
        "No private business data is accepted as evidence.",
    ):
        if required not in payload["not_claimed"]:
            raise AssertionError(f"external reviewer evidence gate must preserve not-claimed signal: {required}")
    return {"external_reviewer_evidence_gate_verified": True}


def main() -> None:
    payload = build_external_reviewer_evidence_gate()
    verify_external_reviewer_evidence_gate(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
