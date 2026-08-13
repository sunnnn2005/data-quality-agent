from scripts.update_feedback_metrics import collect_feedback_metrics


def test_feedback_metrics_uses_honest_zero_fallback(monkeypatch):
    monkeypatch.setenv("FEEDBACK_ITEMS", "0")
    monkeypatch.setenv("CONFIRMED_EXTERNAL_USERS", "0")
    monkeypatch.setenv("REPRODUCIBLE_FEEDBACK_ITEMS", "0")
    monkeypatch.setenv("BUG_FEEDBACK_ITEMS", "0")
    monkeypatch.setenv("FEATURE_FEEDBACK_ITEMS", "0")
    monkeypatch.setenv("BUSINESS_CASE_FEEDBACK_ITEMS", "0")

    metrics = collect_feedback_metrics()

    assert metrics["external_feedback_items"] == 0
    assert metrics["confirmed_external_users"] == 0
    assert metrics["reproducible_feedback_items"] == 0
    assert metrics["tracking_labels"]["external_feedback_items"] == "feedback"
    assert metrics["tracking_labels"]["confirmed_external_users"] == "confirmed-user"
    assert metrics["business_case_feedback_items"] == 0
    assert metrics["tracking_labels"]["business_case_feedback_items"] == "business-case"
    assert {channel["counts_toward"] for channel in metrics["feedback_channels"]} >= {
        "external_feedback_items",
        "bug_feedback_items",
        "feature_feedback_items",
        "business_case_feedback_items",
    }
    assert metrics["status"] == "TRACKING"
    assert "Do not claim users" in metrics["resume_policy"]
