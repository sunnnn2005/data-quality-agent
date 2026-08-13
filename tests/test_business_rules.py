import pandas as pd

from app.agent import DataQualityAgent
from app.business_data import _slugify
from app.models import DatasetSummary
from datetime import datetime, timezone


def test_support_ticket_business_rules_are_source_cited_and_relevant():
    frame = pd.DataFrame(
        [
            {"ticket_id": 1, "team": "support", "priority": "high", "status": "open", "amount": 10},
            {"ticket_id": 1, "team": None, "priority": None, "status": "open", "amount": -5},
            {"ticket_id": 2, "team": "billing", "priority": "low", "status": "closed", "amount": 9999},
            {"ticket_id": 3, "team": "support", "priority": "medium", "status": "open", "amount": 22},
        ]
    )
    dataset = DatasetSummary(
        id="support_tickets",
        name="Support Tickets",
        owner="support-ops",
        primary_key="ticket_id",
        expected_columns=["ticket_id", "team", "priority", "status", "amount"],
        description="Support ticket export used by operations dashboards.",
        last_loaded_at=datetime.now(timezone.utc),
    )

    report = DataQualityAgent().analyze(dataset, frame)
    rule_ids = {rule.rule_id for rule in report.business_rule_references}

    assert "support_tickets:R1" in rule_ids
    assert "support_tickets:R2" in rule_ids
    assert "support_tickets:R3" in rule_ids
    assert "support_tickets:R5" not in rule_ids
    assert all(rule.source.startswith("business-rules/support_tickets.md#") for rule in report.business_rule_references)


def test_unknown_dataset_has_no_business_rule_references():
    frame = pd.DataFrame([{"id": 1, "value": None}])
    dataset = DatasetSummary(
        id=_slugify("Unknown Export"),
        name="Unknown Export",
        owner="ops",
        primary_key="id",
        expected_columns=["id", "value"],
        description="Dataset without business-rule documentation.",
        last_loaded_at=datetime.now(timezone.utc),
    )

    report = DataQualityAgent().analyze(dataset, frame)

    assert report.business_rule_references == []
