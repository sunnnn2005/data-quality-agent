import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LABELS_PATH = ROOT / ".github" / "labels.json"
REPO = "sunnnn2005/data-quality-agent"


def sync_labels() -> list[str]:
    labels = json.loads(LABELS_PATH.read_text())
    changed: list[str] = []
    for label in labels:
        args = [
            "gh",
            "label",
            "create",
            label["name"],
            "--repo",
            REPO,
            "--color",
            label["color"],
            "--description",
            label["description"],
            "--force",
        ]
        subprocess.run(args, check=True, cwd=ROOT)
        changed.append(label["name"])
    return changed


def main() -> None:
    print(json.dumps({"synced_labels": sync_labels()}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
