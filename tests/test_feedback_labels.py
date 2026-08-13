import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_feedback_metric_labels_are_declared():
    labels = json.loads((ROOT / ".github" / "labels.json").read_text())
    names = {label["name"] for label in labels}

    assert {"feedback", "confirmed-user", "reproducible", "bug", "enhancement"} <= names
    assert all(label.get("color") for label in labels)
    assert all(label.get("description") for label in labels)
