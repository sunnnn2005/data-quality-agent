import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPORT_TICKET_ARTIFACT_PATH = ROOT / "docs" / "verified-support-ticket-result.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "hypothesis-feedback.json"
OUTPUT_MD_PATH = ROOT / "docs" / "hypothesis-feedback.md"


def build_hypothesis_feedback_payload() -> dict[str, Any]:
    support_ticket = json.loads(SUPPORT_TICKET_ARTIFACT_PATH.read_text())
    hypotheses = support_ticket["root_cause_hypotheses"]
    labels = []
    for index, hypothesis in enumerate(hypotheses, start=1):
        labels.append(
            {
                "hypothesis_title": hypothesis["title"],
                "label": "accepted" if index <= 2 else "needs_review",
                "reason": _label_reason(hypothesis, index),
                "supporting_checks": hypothesis["supporting_checks"],
                "confidence": hypothesis["confidence"],
            }
        )
    accepted = sum(1 for item in labels if item["label"] == "accepted")
    needs_review = sum(1 for item in labels if item["label"] == "needs_review")
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_hypothesis_feedback.py",
        "source_artifact": "docs/verified-support-ticket-result.json",
        "label_count": len(labels),
        "accepted_count": accepted,
        "needs_review_count": needs_review,
        "labels": labels,
        "resume_safe_summary": (
            f"Added a human-review feedback artifact that labels {len(labels)} root-cause hypotheses "
            f"with {accepted} accepted and {needs_review} needing review."
        ),
        "not_claimed": [
            "external product feedback",
            "production incident confirmation",
            "paid human-labeling dataset",
        ],
    }


def _label_reason(hypothesis: dict[str, Any], index: int) -> str:
    checks = ", ".join(hypothesis["supporting_checks"])
    if index <= 2:
        return f"Accepted because the hypothesis is backed by high-severity checks: {checks}."
    return f"Needs review because the evidence is useful but lower priority than the top hypotheses: {checks}."


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        (
            f"| {item['hypothesis_title']} | `{item['label']}` | {item['confidence']} | "
            f"{', '.join(item['supporting_checks'])} |"
        )
        for item in payload["labels"]
    )
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Hypothesis Feedback

This generated artifact records human-review labels for the support-ticket root-cause hypotheses. It is a local project feedback loop for agent evaluation, not evidence of external product feedback.

| Hypothesis | Label | Confidence | Supporting checks |
| --- | --- | ---: | --- |
{rows}

## Summary

{payload["resume_safe_summary"]}

## Not Claimed

{not_claimed}
"""


def verify_hypothesis_feedback(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "label_count": 3,
        "accepted_count": 2,
        "needs_review_count": 1,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise AssertionError(f"{key} expected {value!r}, got {payload.get(key)!r}")
    if not all(item["supporting_checks"] for item in payload["labels"]):
        raise AssertionError("each hypothesis feedback label must include supporting checks")
    if "external product feedback" not in payload["not_claimed"]:
        raise AssertionError("hypothesis feedback must not claim external product feedback")
    return {"hypothesis_feedback_verified": True, **expected}


def main() -> None:
    payload = build_hypothesis_feedback_payload()
    verify_hypothesis_feedback(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
