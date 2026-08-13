import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCORECARD_PATH = ROOT / "docs" / "live-project-scorecard.json"
OUTPUT_JSON_PATH = ROOT / "docs" / "recruiter-pitch.json"
OUTPUT_MD_PATH = ROOT / "docs" / "recruiter-pitch.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_recruiter_pitch_payload() -> dict[str, Any]:
    scorecard = load_json(SCORECARD_PATH)
    metrics = scorecard["headline_metrics"]
    footprint = scorecard["live_footprint"]
    return {
        "project": "Data Quality Agent",
        "generated_by": "scripts/build_recruiter_pitch.py",
        "target_roles": [
            "AI Engineer Intern",
            "Software Engineer Intern",
            "Data Engineering Intern",
            "Data Science Intern",
        ],
        "resume_bullets": [
            (
                "Built an LLM tool-calling data-quality agent for real business CSV and read-only PostgreSQL data, "
                f"with {metrics['agent_tools_allowed']} allowed tools, dynamic strategy selection, "
                "memory-informed planning, source-cited business-rule retrieval, "
                f"{metrics['openapi_required_endpoints']} verified API integration endpoints, and safe model-key fallback."
            ),
            (
                f"Published a public demo, {scorecard['release']} release, GHCR container image, "
                f"and CI-verified live project scorecard with {metrics['passing_tests']} passing tests, "
                f"{metrics['verified_resume_claims']} verified resume claims, and "
                f"{metrics['implemented_agent_capabilities']} implemented LLM agent-readiness capabilities."
            ),
            (
                "Added enterprise-style guardrails for agent reliability, including read-only PostgreSQL query limits, "
                f"{metrics['unsafe_postgres_queries_rejected']} rejected unsafe SQL queries, sensitive-field redaction, "
                "trace observability, incident-pattern memory, evidence-backed root-cause hypotheses, and deterministic report verification."
            ),
        ],
        "linkedin_project_description": (
            "Data Quality Agent is a local-first LLM agent project for data reliability workflows. "
            "It analyzes business CSV exports and read-only PostgreSQL tables, chooses data-quality tools through an optional "
            "OpenAI-compatible tool-calling loop, and produces structured, evidence-backed reports with guardrails, traceability, "
            "incident-pattern memory, OpenAPI docs, public metrics, and safe fallback behavior."
        ),
        "thirty_second_pitch": (
            "I built Data Quality Agent to show that I can ship more than a one-off LLM demo. "
            "It has a public demo, containerized FastAPI backend, OpenAPI contract, read-only database path, tool-calling agent loop, "
            "safety boundaries, observability artifacts, memory over sanitized traces, and CI-verified evidence pages so reviewers can audit every claim."
        ),
        "interview_talking_points": [
            "Why the deterministic report remains the source of truth while the LLM chooses tools and improves reasoning.",
            "How the read-only PostgreSQL adapter rejects writes, enforces row limits, and avoids unrestricted SQL execution.",
            "How safety artifacts separate verified engineering boundaries from claims not yet supported by production evidence.",
            "How the public scorecard keeps adoption metrics honest by showing current stars, forks, feedback, and user baselines.",
        ],
        "evidence_links": scorecard["reviewer_paths"],
        "honest_baseline": {
            "stars": footprint["stars"],
            "confirmed_external_users": footprint["confirmed_external_users"],
            "external_feedback_items": footprint["external_feedback_items"],
        },
        "not_claimed": scorecard["not_claimed"],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    roles = ", ".join(payload["target_roles"])
    bullets = "\n".join(f"- {item}" for item in payload["resume_bullets"])
    talking_points = "\n".join(f"- {item}" for item in payload["interview_talking_points"])
    links = "\n".join(f"- [{item['label']}]({item['url']})" for item in payload["evidence_links"])
    baseline = "\n".join(f"- `{key}`: {value}" for key, value in payload["honest_baseline"].items())
    not_claimed = "\n".join(f"- {item}" for item in payload["not_claimed"])
    return f"""# Recruiter Pitch

This generated artifact turns verified project evidence into recruiter-facing language for {roles}. It intentionally preserves honest adoption baselines.

## Resume Bullets

{bullets}

## LinkedIn Project Description

{payload["linkedin_project_description"]}

## 30-Second Pitch

{payload["thirty_second_pitch"]}

## Interview Talking Points

{talking_points}

## Evidence Links

{links}

## Honest Baseline

{baseline}

## Not Claimed

{not_claimed}
"""


def verify_recruiter_pitch(payload: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "resume_bullet_count": 3,
        "target_role_count": 4,
        "evidence_link_count": 6,
    }
    if len(payload["resume_bullets"]) != expected["resume_bullet_count"]:
        raise AssertionError("recruiter pitch must include exactly 3 resume bullets")
    if len(payload["target_roles"]) != expected["target_role_count"]:
        raise AssertionError("recruiter pitch must include 4 target roles")
    if len(payload["evidence_links"]) != expected["evidence_link_count"]:
        raise AssertionError("recruiter pitch must include 6 evidence links")
    joined = json.dumps(payload, sort_keys=True).lower()
    for forbidden in ("used by customers", "production users", "gained github stars"):
        if forbidden in joined:
            raise AssertionError(f"recruiter pitch must not claim {forbidden}")
    if payload["honest_baseline"]["stars"] != 0:
        raise AssertionError("recruiter pitch must preserve current star baseline")
    if payload["honest_baseline"]["confirmed_external_users"] != 0:
        raise AssertionError("recruiter pitch must preserve current user baseline")
    for required in ("AI Engineer Intern", "Software Engineer Intern"):
        if required not in payload["target_roles"]:
            raise AssertionError(f"recruiter pitch missing target role {required}")
    return {"recruiter_pitch_verified": True, **expected}


def main() -> None:
    payload = build_recruiter_pitch_payload()
    verify_recruiter_pitch(payload)
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    OUTPUT_MD_PATH.write_text(render_markdown(payload))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
