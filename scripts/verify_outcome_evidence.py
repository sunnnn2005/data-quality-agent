import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "docs" / "outcome-evidence.json"
METRICS_PATH = ROOT / "docs" / "adoption-metrics.json"
RESUME_EVIDENCE_PATH = ROOT / "docs" / "resume-evidence.md"
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
    resume_page = RESUME_EVIDENCE_PATH.read_text().lower()
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
            if metrics.get(metric_name) != claim.get("metric_value"):
                raise AssertionError(
                    f"claim {claim['id']} metric mismatch: {metric_name}={claim.get('metric_value')} "
                    f"but adoption metrics has {metrics.get(metric_name)}"
                )
        if claim["id"] not in resume_page:
            raise AssertionError(f"resume evidence page must mention claim id or anchor text: {claim['id']}")

    not_claimed = {item["metric"] for item in evidence.get("not_claimed", [])}
    for required in {"users", "customer_feedback", "production_company_usage"}:
        if required not in not_claimed:
            raise AssertionError(f"missing explicit not_claimed entry for {required}")
        if required.replace("_", " ") not in resume_page and required not in resume_page:
            raise AssertionError(f"resume evidence page must mention not-claimed signal: {required}")

    return {
        "claim_count": len(claims),
        "not_claimed_count": len(not_claimed),
        "resume_evidence_page": 1,
    }


def main() -> None:
    print(json.dumps(verify_manifest(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
