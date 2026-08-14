import json
from types import SimpleNamespace

from scripts import update_adoption_metrics
from scripts.update_adoption_metrics import append_history, collect_metrics


def test_adoption_metrics_uses_safe_fallback_values(monkeypatch):
    monkeypatch.setenv("ADOPTION_STARS", "0")
    monkeypatch.setenv("ADOPTION_FORKS", "1")
    monkeypatch.setenv("ADOPTION_WATCHERS", "0")
    monkeypatch.setenv("ADOPTION_ISSUES_TOTAL", "11")
    monkeypatch.setenv("ADOPTION_TEST_COUNT", "90")
    monkeypatch.setattr(update_adoption_metrics, "_load_existing_metrics", lambda: {})
    monkeypatch.setattr(
        update_adoption_metrics,
        "_load_feedback_metrics",
        lambda: {
            "external_feedback_items": 0,
            "confirmed_external_users": 0,
            "reproducible_feedback_items": 0,
        },
    )

    def fake_run(args, **_kwargs):
        if args[:3] == [update_adoption_metrics.sys.executable, "-m", "pytest"]:
            raise FileNotFoundError()
        if args[:3] == ["git", "rev-parse", "--short"]:
            return SimpleNamespace(stdout="abc1234\n")
        return SimpleNamespace(stdout="{}")

    monkeypatch.setattr(update_adoption_metrics.subprocess, "run", fake_run)

    metrics = collect_metrics()

    assert metrics["stars"] == 0
    assert metrics["forks"] == 1
    assert metrics["watchers"] == 0
    assert metrics["issues_total"] == 11
    assert metrics["external_feedback_items"] == 0
    assert metrics["confirmed_external_users"] == 0
    assert metrics["test_count"] == 90
    assert metrics["commit"] is not None
    assert metrics["container_image"]["image"] == "ghcr.io/sunnnn2005/data-quality-agent:latest"
    assert metrics["release"]["tagName"] == "v0.3.0"


def test_adoption_metrics_falls_back_to_public_github_api_when_gh_auth_fails(monkeypatch):
    monkeypatch.delenv("ADOPTION_STARS", raising=False)
    monkeypatch.delenv("ADOPTION_FORKS", raising=False)
    monkeypatch.delenv("ADOPTION_WATCHERS", raising=False)
    monkeypatch.delenv("ADOPTION_ISSUES_TOTAL", raising=False)
    monkeypatch.setenv("ADOPTION_TEST_COUNT", "90")
    monkeypatch.setattr(update_adoption_metrics, "_load_existing_metrics", lambda: {})
    monkeypatch.setattr(
        update_adoption_metrics,
        "_load_feedback_metrics",
        lambda: {
            "external_feedback_items": 0,
            "confirmed_external_users": 0,
            "reproducible_feedback_items": 0,
        },
    )

    def fake_run(args, **_kwargs):
        if args[:3] == [update_adoption_metrics.sys.executable, "-m", "pytest"]:
            raise FileNotFoundError()
        if args[:3] == ["git", "rev-parse", "--short"]:
            return SimpleNamespace(stdout="def5678\n")
        raise update_adoption_metrics.subprocess.CalledProcessError(returncode=1, cmd=args)

    def fake_public_get(url):
        if url.endswith("/releases/tags/v0.3.0"):
            return {
                "tag_name": "v0.3.0",
                "html_url": "https://github.com/sunnnn2005/data-quality-agent/releases/tag/v0.3.0",
                "published_at": "2026-08-13T12:05:26Z",
                "draft": False,
                "prerelease": False,
            }
        return {
            "stargazers_count": 3,
            "forks_count": 2,
            "subscribers_count": 4,
            "open_issues_count": 25,
            "html_url": "https://github.com/sunnnn2005/data-quality-agent",
        }

    monkeypatch.setattr(update_adoption_metrics.subprocess, "run", fake_run)
    monkeypatch.setattr(update_adoption_metrics, "_github_api_get", fake_public_get)

    metrics = collect_metrics()

    assert metrics["stars"] == 3
    assert metrics["forks"] == 2
    assert metrics["watchers"] == 4
    assert metrics["issues_total"] == 25
    assert metrics["release"]["tagName"] == "v0.3.0"
    assert metrics["commit"] == "def5678"


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
        "external_feedback_items": 0,
        "confirmed_external_users": 0,
        "test_count": 47,
        "release": {"tagName": "v0.3.0"},
    }

    append_history(metrics)
    append_history(metrics)

    rows = [json.loads(line) for line in history_path.read_text().splitlines()]
    assert len(rows) == 1
    assert rows[0]["commit"] == "abc1234"
    assert rows[0]["test_count"] == 47
    assert rows[0]["external_feedback_items"] == 0
    assert rows[0]["confirmed_external_users"] == 0
