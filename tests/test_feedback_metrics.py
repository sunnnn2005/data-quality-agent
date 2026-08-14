from scripts import update_feedback_metrics
from scripts.update_feedback_metrics import _count_issues_by_label, collect_feedback_metrics


def test_feedback_metrics_uses_honest_zero_fallback(monkeypatch):
    monkeypatch.setenv("FEEDBACK_ITEMS", "0")
    monkeypatch.setenv("CONFIRMED_EXTERNAL_USERS", "0")
    monkeypatch.setenv("REPRODUCIBLE_FEEDBACK_ITEMS", "0")
    monkeypatch.setenv("BUG_FEEDBACK_ITEMS", "0")
    monkeypatch.setenv("FEATURE_FEEDBACK_ITEMS", "0")
    monkeypatch.setenv("BUSINESS_CASE_FEEDBACK_ITEMS", "0")
    monkeypatch.setenv("AI_ENGINEER_REVIEW_ITEMS", "0")

    metrics = collect_feedback_metrics()

    assert metrics["external_feedback_items"] == 0
    assert metrics["confirmed_external_users"] == 0
    assert metrics["reproducible_feedback_items"] == 0
    assert metrics["tracking_labels"]["external_feedback_items"] == "feedback"
    assert metrics["tracking_labels"]["confirmed_external_users"] == "confirmed-user"
    assert metrics["business_case_feedback_items"] == 0
    assert metrics["tracking_labels"]["business_case_feedback_items"] == "business-case"
    assert metrics["ai_engineer_review_items"] == 0
    assert metrics["tracking_labels"]["ai_engineer_review_items"] == "ai-engineer-review"
    assert {channel["counts_toward"] for channel in metrics["feedback_channels"]} >= {
        "external_feedback_items",
        "bug_feedback_items",
        "feature_feedback_items",
        "business_case_feedback_items",
        "ai_engineer_review_items",
    }
    assert metrics["status"] == "TRACKING"
    assert metrics["self_authored_planning_excluded"] is True
    assert "Do not claim users" in metrics["resume_policy"]


def test_feedback_metrics_excludes_self_authored_planning_from_external_counts(monkeypatch):
    completed = type(
        "Completed",
        (),
        {
            "stdout": """
            [
              {
                "number": 17,
                "author": {"login": "sunnnn2005"},
                "labels": [{"name": "feedback"}, {"name": "pilot"}]
              },
              {
                "number": 21,
                "author": {"login": "external-reviewer"},
                "labels": [{"name": "feedback"}]
              }
            ]
            """
        },
    )()

    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: completed)

    assert _count_issues_by_label("feedback", exclude_self_authored_planning=True) == 1
    assert _count_issues_by_label("feedback", exclude_self_authored_planning=False) == 2


def test_feedback_metrics_falls_back_to_public_issue_api_when_gh_auth_fails(monkeypatch):
    def fake_run(*args, **kwargs):
        raise update_feedback_metrics.subprocess.CalledProcessError(returncode=1, cmd=args[0])

    monkeypatch.setattr(update_feedback_metrics.subprocess, "run", fake_run)
    monkeypatch.setattr(
        update_feedback_metrics,
        "_collect_public_issues_by_label",
        lambda label: [
            {
                "number": 17,
                "author": {"login": "sunnnn2005"},
                "labels": [{"name": label}, {"name": "pilot"}],
            },
            {
                "number": 21,
                "author": {"login": "external-reviewer"},
                "labels": [{"name": label}],
            },
        ],
    )

    assert _count_issues_by_label("feedback", exclude_self_authored_planning=True) == 1
    assert _count_issues_by_label("feedback", exclude_self_authored_planning=False) == 2


def test_feedback_metrics_uses_evidence_gate_for_external_outcome_counts(tmp_path, monkeypatch):
    gate_path = tmp_path / "external-reviewer-evidence-gate.json"
    gate_path.write_text(
        """
        {
          "accepted_counts": {
            "external_feedback_items": 0,
            "confirmed_external_users": 0,
            "reproducible_feedback_items": 0,
            "business_case_feedback_items": 0,
            "ai_engineer_review_items": 0
          }
        }
        """
    )
    monkeypatch.setattr(update_feedback_metrics, "EXTERNAL_REVIEWER_GATE_PATH", gate_path)
    monkeypatch.delenv("FEEDBACK_ITEMS", raising=False)
    monkeypatch.delenv("CONFIRMED_EXTERNAL_USERS", raising=False)
    monkeypatch.delenv("REPRODUCIBLE_FEEDBACK_ITEMS", raising=False)
    monkeypatch.delenv("BUSINESS_CASE_FEEDBACK_ITEMS", raising=False)
    monkeypatch.delenv("AI_ENGINEER_REVIEW_ITEMS", raising=False)
    monkeypatch.setenv("BUG_FEEDBACK_ITEMS", "0")
    monkeypatch.setenv("FEATURE_FEEDBACK_ITEMS", "8")

    monkeypatch.setattr(
        update_feedback_metrics,
        "_count_issues_by_label",
        lambda label, *, exclude_self_authored_planning=False: 99,
    )

    metrics = collect_feedback_metrics()

    assert metrics["external_feedback_items"] == 0
    assert metrics["confirmed_external_users"] == 0
    assert metrics["reproducible_feedback_items"] == 0
    assert metrics["business_case_feedback_items"] == 0
    assert metrics["ai_engineer_review_items"] == 0
    assert metrics["feature_feedback_items"] == 8
