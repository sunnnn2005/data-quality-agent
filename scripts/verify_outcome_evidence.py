import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "docs" / "outcome-evidence.json"
METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
FEEDBACK_METRICS_PATH = ROOT / "docs" / "feedback-metrics.json"
HISTORY_PATH = ROOT / "docs" / "adoption-history.jsonl"
BUSINESS_IMPACT_PATH = ROOT / "docs" / "business-impact.json"
PUBLIC_HEALTH_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "public-evidence-health.yml"
PUBLIC_HEALTH_SCRIPT_PATH = ROOT / "scripts" / "verify_public_evidence_health.py"
RESUME_EVIDENCE_PATH = ROOT / "docs" / "resume-evidence.md"
FEEDBACK_LOG_PATH = ROOT / "docs" / "feedback-log.md"
REQUIRED_CLAIM_FIELDS = {"id", "resume_signal", "claim", "evidence_type", "url", "status"}
FORBIDDEN_UNVERIFIED_TERMS = {"users", "customers", "enterprise production", "github stars gained"}


def load_payload(path: Path) -> dict:
    return json.loads(path.read_text())


def validate_url(value: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise AssertionError(f"invalid evidence url: {value}")


def verify_manifest() -> dict[str, int]:
    evidence = load_payload(EVIDENCE_PATH)
    metrics = load_payload(METRICS_PATH)
    feedback_metrics = load_payload(FEEDBACK_METRICS_PATH)
    business_impact = load_payload(BUSINESS_IMPACT_PATH)
    history = [json.loads(line) for line in HISTORY_PATH.read_text().splitlines() if line.strip()]
    resume_page = RESUME_EVIDENCE_PATH.read_text().lower()
    feedback_log = FEEDBACK_LOG_PATH.read_text().lower()
    claims = evidence.get("claims", [])
    if len(claims) < 6:
        raise AssertionError("outcome evidence manifest must include at least six public claims")

    claim_ids = set()
    for claim in claims:
        missing = REQUIRED_CLAIM_FIELDS - set(claim)
        if missing:
            raise AssertionError(f"claim {claim.get('id')} missing fields: {sorted(missing)}")
        if claim["id"] in claim_ids:
            raise AssertionError(f"duplicate claim id: {claim['id']}")
        claim_ids.add(claim["id"])
        if claim["status"] != "verified":
            raise AssertionError(f"claim {claim['id']} must not be marked as a resume signal until verified")
        validate_url(claim["url"])

        text = f"{claim['resume_signal']} {claim['claim']}".lower()
        for forbidden in FORBIDDEN_UNVERIFIED_TERMS:
            if forbidden in text and claim["id"] != "adoption-baseline":
                raise AssertionError(f"claim {claim['id']} uses unverified outcome language: {forbidden}")

        metric_name = claim.get("metric_name")
        if metric_name:
            if metric_name == "external_feedback_items":
                if feedback_metrics.get("external_feedback_items") != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: external_feedback_items={claim.get('metric_value')} "
                        f"but feedback metrics has {feedback_metrics.get('external_feedback_items')}"
                    )
            elif metric_name == "support_ticket_issue_categories":
                if business_impact.get("issue_category_count") != claim.get("metric_value"):
                    raise AssertionError(
                        f"claim {claim['id']} metric mismatch: {metric_name}={claim.get('metric_value')} "
                        f"but business impact has {business_impact.get('issue_category_count')}"
                    )
            elif metrics.get(metric_name) != claim.get("metric_value"):
                raise AssertionError(
                    f"claim {claim['id']} metric mismatch: {metric_name}={claim.get('metric_value')} "
                    f"but adoption metrics has {metrics.get(metric_name)}"
                )
        if claim["id"] not in resume_page:
            raise AssertionError(f"resume evidence page must mention claim id or anchor text: {claim['id']}")

    if "public-evidence-health" in claim_ids:
        workflow_text = PUBLIC_HEALTH_WORKFLOW_PATH.read_text()
        script_text = PUBLIC_HEALTH_SCRIPT_PATH.read_text()
        if "schedule:" not in workflow_text or "workflow_dispatch:" not in workflow_text:
            raise AssertionError("public evidence health workflow must support scheduled and manual runs")
        for required in ["public-demo", "business-impact-artifact", "github-release"]:
            if required not in script_text:
                raise AssertionError(f"public evidence health script must check {required}")

    not_claimed = {item["metric"] for item in evidence.get("not_claimed", [])}
    for required in {"users", "customer_feedback", "production_company_usage"}:
        if required not in not_claimed:
            raise AssertionError(f"missing explicit not_claimed entry for {required}")
        if required.replace("_", " ") not in resume_page and required not in resume_page:
            raise AssertionError(f"resume evidence page must mention not-claimed signal: {required}")

    if "external feedback items | 0" not in feedback_log:
        raise AssertionError("feedback log must keep an explicit zero external feedback baseline")
    if "confirmed external users | 0" not in feedback_log:
        raise AssertionError("feedback log must keep an explicit zero external user baseline")
    for key in ("external_feedback_items", "confirmed_external_users", "reproducible_feedback_items"):
        if metrics.get(key) != feedback_metrics.get(key):
            raise AssertionError(f"adoption metrics {key} must match feedback metrics")
    if not history:
        raise AssertionError("adoption history must include at least one point")
    latest = history[-1]
    for key in ("stars", "forks", "watchers", "issues_total", "test_count"):
        if latest.get(key) != metrics.get(key):
            raise AssertionError(f"adoption history latest {key} must match adoption metrics")

    return {
        "claim_count": len(claims),
        "not_claimed_count": len(not_claimed),
        "resume_evidence_page": 1,
        "feedback_log": 1,
        "adoption_history_count": len(history),
    }


def main() -> None:
    print(json.dumps(verify_manifest(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
