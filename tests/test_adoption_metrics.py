from scripts.update_adoption_metrics import collect_metrics


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
    assert metrics["test_count"] == 42
    assert metrics["container_image"]["image"] == "ghcr.io/sunnnn2005/data-quality-agent:latest"
    assert metrics["release"]["tagName"] == "v0.1.0"
