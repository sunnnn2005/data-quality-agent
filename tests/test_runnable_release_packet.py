from scripts.build_runnable_release_packet import (
    build_runnable_release_packet,
    render_markdown,
    verify_runnable_release_packet,
)


def test_runnable_release_packet_exposes_installable_surfaces_without_usage_claims():
    payload = build_runnable_release_packet()
    verification = verify_runnable_release_packet(payload)
    markdown = render_markdown(payload)

    assert verification["runnable_release_packet_verified"] is True
    assert verification["runnable_surface_count"] == 3
    assert verification["acceptance_check_count"] == 4
    assert verification["openapi_required_path_count"] == 6
    assert any(surface["name"] == "ghcr_container" for surface in payload["runnable_surfaces"])
    assert any("docker run" in surface.get("command", "") for surface in payload["runnable_surfaces"])
    assert any("docker compose up --build" in surface.get("command", "") for surface in payload["runnable_surfaces"])
    assert "No package download count is claimed." in payload["not_claimed"]
    assert "No external installs are claimed." in payload["not_claimed"]
    assert "Runnable Release Packet" in markdown


def test_runnable_release_packet_covers_required_api_paths():
    payload = build_runnable_release_packet()

    assert set(payload["openapi_coverage"]["required_paths"]) <= set(payload["openapi_coverage"]["published_paths"])
    assert "/business-data/agent-report" in payload["openapi_coverage"]["published_paths"]
    assert "/postgres/support-tickets/agent-report" in payload["openapi_coverage"]["published_paths"]
