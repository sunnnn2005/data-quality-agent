import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESUME_OUTCOME_SCOREBOARD_PATH = ROOT / "docs" / "resume-outcome-scoreboard.json"
REVIEWER_SEND_QUEUE_PATH = ROOT / "docs" / "reviewer-send-queue.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "resume-outcome-conversion-plan.json"
OUTPUT_MD_PATH = ROOT / "docs" / "resume-outcome-conversion-plan.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _send_by_metric(send_queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["target_metric"]: item for item in send_queue["next_sends"]}


def build_resume_outcome_conversion_plan() -> dict[str, Any]:
    scoreboard = load_json(RESUME_OUTCOME_SCOREBOARD_PATH)
    send_queue = load_json(REVIEWER_SEND_QUEUE_PATH)
    sends = _send_by_metric(send_queue)

    conversion_rows = []
    for row in scoreboard["blocked_outcomes"]:
        metric = row["metric"]
        send = sends.get(metric)
        if send is None and metric == "github_stars":
            next_action = {
                "recommended_channel": "GitHub README, public demo, class Discord, or LinkedIn project post",
                "reviewer_profile": "developer or data/AI peer who finds the project useful",
                "who_to_choose": "Choose someone who has actually inspected the repo or demo; ask for a star only if the project is useful.",
                "submission_url": "https://github.com/sunnnn2005/data-quality-agent",
                "public_issue_url": "https://github.com/sunnnn2005/data-quality-agent/stargazers",
                "copy_ready_message": (
                    "I published a local-first LLM data-quality agent with a public demo, tests, "
                    "tool-calling evidence, and conservative outcome tracking. If the project is genuinely useful "
                    "after you inspect it, and only if the project is useful to you, a GitHub star would help signal public interest: "
                    "https://github.com/sunnnn2005/data-quality-agent"
                ),
                "counts_only_after": "The public GitHub stargazer count reaches the threshold organically.",
            }
        else:
            next_action = {
                "recommended_channel": send["recommended_channel"],
                "reviewer_profile": send["reviewer_profile"],
                "who_to_choose": send["who_to_choose"],
                "submission_url": send["submission_url"],
                "public_issue_url": send["public_issue_url"],
                "copy_ready_message": send["copy_ready_message"],
                "counts_only_after": send["counts_only_after"],
            }

        conversion_rows.append(
            {
                "metric": metric,
                "current_count": row["current_count"],
                "required_count": row["required_count"],
                "remaining_to_threshold": row["remaining_to_threshold"],
                "status": "blocked_until_public_evidence",
                "future_resume_line": row["future_resume_line"],
                "evidence_gate": row["evidence_gate"],
                "recommended_channel": next_action["recommended_channel"],
                "reviewer_profile": next_action["reviewer_profile"],
                "who_to_choose": next_action["who_to_choose"],
                "submission_url": next_action["submission_url"],
                "public_issue_url": next_action["public_issue_url"],
                "copy_ready_message": next_action["copy_ready_message"],
                "counts_only_after": next_action["counts_only_after"],
            }
        )

    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_resume_outcome_conversion_plan.py",
        "purpose": (
            "Turn blocked resume outcomes into a concrete conversion plan: one next action, one reviewer profile, "
            "one evidence gate, and one copy-ready message per future outcome claim."
        ),
        "conversion_row_count": len(conversion_rows),
        "conversion_rows": conversion_rows,
        "one_click_evidence_url": send_queue["one_click_evidence_url"],
        "claimable_now_count": scoreboard["claimable_now_count"],
        "blocked_outcome_count": scoreboard["blocked_outcome_count"],
        "current_public_counts": scoreboard["current_public_counts"],
        "execution_rule": (
            "Do not upgrade a resume line from blocked to claimable until the public evidence gate is satisfied by "
            "a non-owner issue, accepted public metric, or public GitHub count. Outreach attempts alone do not count."
        ),
        "resume_safe_summary": (
            f"Published a conversion plan for {len(conversion_rows)} blocked resume outcomes with one-click evidence routing, "
            "copy-ready reviewer asks, public issue gates, and zero upgraded outcome claims until evidence is accepted."
        ),
        "not_claimed": scoreboard["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        "| {metric} | {current_count} | {required_count} | {remaining_to_threshold} | {reviewer_profile} | {recommended_channel} | [submit]({submission_url}) |".format(
            **item
        )
        for item in payload["conversion_rows"]
    )
    messages = "\n\n".join(
        "### {metric}\n\nEvidence gate: {evidence_gate}\n\nCounts only after: {counts_only_after}\n\n```text\n{copy_ready_message}\n```".format(
            **item
        )
        for item in payload["conversion_rows"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Resume Outcome Conversion Plan

{payload["purpose"]}

## Summary

| Metric | Value |
| --- | ---: |
| Claimable now | {payload["claimable_now_count"]} |
| Blocked outcomes | {payload["blocked_outcome_count"]} |
| Conversion rows | {payload["conversion_row_count"]} |

One-click evidence page: [{payload["one_click_evidence_url"]}]({payload["one_click_evidence_url"]})

## Conversion Queue

| Metric | Current | Required | Remaining | Reviewer Profile | Channel | Submission |
| --- | ---: | ---: | ---: | --- | --- | --- |
{rows}

## Copy-Ready Asks

{messages}

## Execution Rule

{payload["execution_rule"]}

## Resume-Safe Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_resume_outcome_conversion_plan(payload: dict[str, Any]) -> dict[str, Any]:
    if payload["conversion_row_count"] != 6:
        raise AssertionError("conversion plan must cover all six blocked resume outcomes")
    if payload["claimable_now_count"] != 6:
        raise AssertionError("conversion plan must preserve six current claimable lines")
    if payload["blocked_outcome_count"] != 6:
        raise AssertionError("conversion plan must preserve six blocked outcome claims")
    if not payload["one_click_evidence_url"].endswith("/one-click-evidence-links.html"):
        raise AssertionError("conversion plan must route reviewers through one-click evidence")

    required_metrics = {
        "confirmed_external_users",
        "external_feedback_items",
        "reproducible_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
        "github_stars",
    }
    actual_metrics = {item["metric"] for item in payload["conversion_rows"]}
    if actual_metrics != required_metrics:
        raise AssertionError("conversion plan must cover every future resume metric")

    for item in payload["conversion_rows"]:
        if item["status"] != "blocked_until_public_evidence":
            raise AssertionError("conversion rows must remain blocked until evidence exists")
        if item["current_count"] != 0:
            raise AssertionError(f"{item['metric']} must stay at zero until public evidence exists")
        if item["remaining_to_threshold"] < 1:
            raise AssertionError("each blocked outcome must still need public evidence")
        if "public" not in item["evidence_gate"].lower() and item["metric"] != "github_stars":
            raise AssertionError("non-star outcome gates must require public evidence")
        if "copy_ready_message" not in item or not item["copy_ready_message"]:
            raise AssertionError("each conversion row needs a copy-ready message")

    execution_rule = payload["execution_rule"].lower()
    for phrase in ("do not upgrade", "public evidence gate", "outreach attempts alone do not count"):
        if phrase not in execution_rule:
            raise AssertionError(f"conversion plan execution rule missing: {phrase}")
    summary = payload["resume_safe_summary"].lower()
    for phrase in ("zero upgraded outcome claims", "public issue gates", "copy-ready"):
        if phrase not in summary:
            raise AssertionError(f"conversion plan summary missing: {phrase}")
    markdown = render_markdown(payload)
    for section in ("Conversion Queue", "Copy-Ready Asks", "Execution Rule", "Not Claimed"):
        if section not in markdown:
            raise AssertionError(f"conversion plan markdown missing section: {section}")
    return {
        "resume_outcome_conversion_plan_verified": True,
        "conversion_row_count": payload["conversion_row_count"],
        "blocked_outcome_count": payload["blocked_outcome_count"],
    }


def main() -> None:
    payload = build_resume_outcome_conversion_plan()
    verify_resume_outcome_conversion_plan(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
