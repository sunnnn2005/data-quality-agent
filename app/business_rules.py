from dataclasses import dataclass
from pathlib import Path

from app.models import BusinessRuleReference, DatasetSummary, QualityFinding


RULES_DIR = Path(__file__).resolve().parents[1] / "docs" / "business-rules"


@dataclass(frozen=True)
class BusinessRule:
    rule_id: str
    source: str
    title: str
    text: str
    keywords: tuple[str, ...]
    check_names: tuple[str, ...]


class BusinessRuleRetriever:
    name = "business_rule_retriever"

    def __init__(self, rules_dir: Path = RULES_DIR) -> None:
        self.rules_dir = rules_dir

    def retrieve(self, dataset: DatasetSummary, findings: list[QualityFinding], limit: int = 4) -> list[BusinessRuleReference]:
        rules = self._load_rules(dataset.id)
        if not rules or not findings:
            return []

        finding_checks = {finding.check_name for finding in findings}
        finding_columns = {finding.column for finding in findings if finding.column}
        scored = []
        for rule in rules:
            matched_checks = sorted(finding_checks & set(rule.check_names))
            score = len(matched_checks) * 3
            score += sum(1 for keyword in rule.keywords if keyword in finding_checks or keyword in finding_columns)
            if score:
                scored.append((score, rule, matched_checks))

        scored.sort(key=lambda item: (-item[0], item[1].rule_id))
        return [
            BusinessRuleReference(
                rule_id=rule.rule_id,
                source=rule.source,
                title=rule.title,
                text=rule.text,
                matched_checks=matched_checks,
            )
            for _, rule, matched_checks in scored[:limit]
        ]

    def _load_rules(self, dataset_id: str) -> list[BusinessRule]:
        path = self.rules_dir / f"{dataset_id}.md"
        if not path.exists():
            return []

        rules: list[BusinessRule] = []
        current: dict[str, str] = {}
        for raw_line in path.read_text().splitlines():
            line = raw_line.strip()
            if line.startswith("## "):
                if current:
                    rules.append(self._parse_rule(current, path))
                current = {"title": line.removeprefix("## ").strip()}
            elif ":" in line and current:
                key, value = line.split(":", 1)
                current[key.strip().lower()] = value.strip()
        if current:
            rules.append(self._parse_rule(current, path))
        return rules

    def _parse_rule(self, payload: dict[str, str], path: Path) -> BusinessRule:
        rule_id = payload.get("id", payload["title"].lower().replace(" ", "_"))
        return BusinessRule(
            rule_id=rule_id,
            source=f"{path.relative_to(path.parents[1])}#{rule_id}",
            title=payload["title"],
            text=payload.get("text", ""),
            keywords=tuple(_split_csv(payload.get("keywords", ""))),
            check_names=tuple(_split_csv(payload.get("checks", ""))),
        )


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]
