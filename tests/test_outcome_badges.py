from scripts.build_outcome_badges import build_outcome_badges, render_markdown, verify_outcome_badges


def test_outcome_badges_keep_blocked_outcomes_visibly_separate():
    payload = build_outcome_badges()
    verification = verify_outcome_badges(payload)
    markdown = render_markdown(payload)
    badges = {badge["id"]: badge for badge in payload["badges"]}

    assert verification["outcome_badges_verified"] is True
    assert payload["badge_count"] == 6
    assert badges["ci-tests"]["resume_claimable"] is True
    assert badges["github-stars"]["message"] == "0 public"
    assert badges["github-stars"]["resume_claimable"] is False
    assert badges["github-stars"]["color"] == "lightgrey"
    assert badges["confirmed-users"]["message"] == "0 accepted"
    assert badges["confirmed-users"]["resume_claimable"] is False
    assert badges["external-feedback"]["resume_claimable"] is False
    assert badges["ai-review"]["resume_claimable"] is False
    assert "production usage" in payload["resume_policy"]
    assert "business impact" in payload["resume_policy"]
    assert "# Outcome Badges" in markdown
