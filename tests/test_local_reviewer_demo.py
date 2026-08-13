from scripts.build_local_reviewer_demo import (
    build_local_reviewer_demo_payload,
    render_markdown,
    verify_local_reviewer_demo,
)


def test_local_reviewer_demo_documents_seeded_compose_path_without_usage_claims():
    payload = build_local_reviewer_demo_payload()
    verification = verify_local_reviewer_demo(payload)
    markdown = render_markdown(payload)

    assert verification["local_reviewer_demo_verified"] is True
    assert payload["reviewer_command"] == "docker compose up --build"
    assert payload["seeded_business_table"]["row_count"] == 8
    assert payload["read_only_database"]["readonly_user"] == "readonly_agent"
    assert len(payload["reviewer_routes"]) == 3
    assert "curl -X POST http://127.0.0.1:8000/postgres/support-tickets/quality-report" in markdown
    assert "No external reviewer completion is claimed." in markdown
