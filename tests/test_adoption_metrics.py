import json

from scripts import update_adoption_metrics
from scripts.update_adoption_metrics import append_history, collect_metrics


def test_adoption_metrics_uses_safe_fallback_values(monkeypatch):
    monkeypatch.setenv("ADOPTION_STARS", "0")
    monkeypatch.setenv("ADOPTION_FORKS", "1")
    monkeypatch.setenv("ADOPTION_WATCHERS", "0")
    monkeypatch.setenv("ADOPTION_ISSUES_TOTAL", "10")

    metrics = collect_metrics()

    assert metrics["stars"] == 0
    assert metrics["forks"] == 1
    assert metrics["watchers"] == 0
    assert metrics["issues_total"] == 10
    assert metrics["test_count"] == 48
    assert metrics["commit"] is not None
    assert metrics["container_image"]["image"] == "ghcr.io/sunnnn2005/data-quality-agent:latest"
    assert metrics["release"]["tagName"] == "v0.1.0"


def test_adoption_history_dedupes_same_date_and_commit(tmp_path, monkeypatch):
    history_path = tmp_path / "adoption-history.jsonl"
    monkeypatch.setattr(update_adoption_metrics, "HISTORY_PATH", history_path)
    metrics = {
        "generated_at": "2026-08-13T04:10:00+00:00",
        "commit": "abc1234",
        "stars": 0,
        "forks": 1,
        "watchers": 0,
        "issues_total": 10,
        "test_count": 47,
        "release": {"tagName": "v0.1.0"},
    }

    append_history(metrics)
    append_history(metrics)

    rows = [json.loads(line) for line in history_path.read_text().splitlines()]
    assert len(rows) == 1
    assert rows[0]["commit"] == "abc1234"
    assert rows[0]["test_count"] == 47
