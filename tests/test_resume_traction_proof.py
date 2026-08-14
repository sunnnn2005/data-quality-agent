import json
from pathlib import Path

from scripts.build_resume_traction_proof import (
    build_resume_traction_proof,
    render_markdown,
    verify_resume_traction_proof,
)

ROOT = Path(__file__).resolve().parents[1]


def test_resume_traction_proof_separates_claimable_launch_from_unproven_growth():
    payload = build_resume_traction_proof()
    verification = verify_resume_traction_proof(payload)
    markdown = render_markdown(payload)
    traffic = json.loads((ROOT / "docs" / "github-traffic-snapshot.json").read_text())[
        "traffic_metrics"
    ]

    assert verification["resume_traction_proof_verified"] is True
    assert payload["claimable_now_count"] == 6
    assert payload["future_claim_count"] == 4
    assert payload["blocked_claim_count"] == 5
    assert payload["public_counts"]["stars"] == 0
    assert payload["public_counts"]["confirmed_external_users"] == 0
    assert payload["public_counts"]["external_feedback_items"] == 0
    assert payload["linked_public_traction_surfaces"] == 4
    assert payload["linked_growth_channels"] == 21
    assert all(item["status"] == "claimable" for item in payload["claimable_now"])
    assert all(item["status"] == "not_claimable_yet" for item in payload["future_claims"])
    assert "Launched a public GitHub Pages demo" in markdown
    assert "early repository interest" in markdown
    assert (
        f"{traffic['unique_cloners']} unique cloners without counting traffic as users"
        in markdown
    )
    assert "public availability evidence" in markdown
    assert "Verified 4/4 public project surfaces and 3/3 main-branch workflows" in markdown
    assert "Do not claim active users" in markdown
    assert "Do not convert GitHub traffic views into user counts" in markdown
