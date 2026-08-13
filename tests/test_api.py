from fastapi.testclient import TestClient
from pathlib import Path

import pandas as pd

from app.models import DatasetSummary
from app.main import app
import app.main as main_module


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "data-quality-agent"}


def test_dataset_catalog():
    response = client.get("/datasets")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 3
    assert {dataset["id"] for dataset in payload} >= {"orders_daily", "payments_events", "customer_profiles"}


def test_profile_endpoint_returns_column_profiles():
    response = client.get("/datasets/orders_daily/profile")

    assert response.status_code == 200
    payload = response.json()
    assert payload["row_count"] == 7
    assert any(column["column"] == "order_total" for column in payload["columns"])


def test_quality_report_endpoint_returns_findings():
    response = client.post("/datasets/orders_daily/quality-report")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "FAIL"
    assert payload["trace_id"].startswith("run_")
    assert payload["findings"]
    assert payload["agent_trace"]


def test_incident_report_endpoint_returns_ticket_ready_markdown():
    response = client.post("/datasets/orders_daily/incident-report.md")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "# Data Quality Incident: Daily Orders" in response.text
    assert "## Recommended Actions" in response.text
    assert "`duplicate_primary_key`" in response.text
    assert "Trace ID: `run_" in response.text


def test_missing_dataset_returns_404():
    response = client.post("/datasets/missing/quality-report")

    assert response.status_code == 404
    assert response.json()["detail"] == "Dataset not found"


def test_dashboard_renders():
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "Data Quality Agent" in response.text
    assert "/datasets" in response.text


def test_business_csv_quality_report_accepts_uploaded_data():
    csv = "ticket_id,team,priority,status,amount\n1,support,high,open,10\n1,support,high,open,10\n2,sales,,closed,9999\n"
    response = client.post(
        "/business-data/quality-report",
        data={
            "dataset_name": "Support Tickets",
            "owner": "support-ops",
            "primary_key": "ticket_id",
            "expected_columns": "ticket_id,team,priority,status,amount",
            "description": "Support ticket export used by operations dashboards.",
        },
        files={"file": ("tickets.csv", csv, "text/csv")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["dataset"]["id"] == "support_tickets"
    assert payload["row_count"] == 3
    assert any(finding["check_name"] == "duplicate_primary_key" for finding in payload["findings"])


def test_business_csv_agent_report_is_disabled_without_key_but_uses_real_dataset_context():
    csv = "customer_id,email,lifetime_value\n1,a@example.com,10\n2,,20\n"
    response = client.post(
        "/business-data/agent-report",
        data={
            "dataset_name": "Customer Export",
            "owner": "growth",
            "primary_key": "customer_id",
            "expected_columns": "customer_id,email,lifetime_value",
        },
        files={"file": ("customers.csv", csv, "text/csv")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "DISABLED"
    assert payload["trace_id"].startswith("run_")
    assert payload["dataset"]["name"] == "Customer Export"
    assert payload["error"] == "OPENAI_API_KEY is not configured"


def test_postgres_support_ticket_report_uses_read_only_adapter(monkeypatch):
    class FakePostgresAdapter:
        def load_table(
            self,
            table,
            *,
            dataset_name,
            owner,
            primary_key,
            expected_columns,
            description,
        ):
            assert table == "support_tickets"
            assert owner == "support-ops"
            dataset = DatasetSummary(
                id="support_tickets",
                name=dataset_name,
                owner=owner,
                primary_key=primary_key,
                expected_columns=expected_columns,
                description=description,
                last_loaded_at=main_module.DATASETS["orders_daily"].last_loaded_at,
            )
            csv = ROOT / "examples" / "support_tickets.csv"

            return dataset, pd.read_csv(csv)

    monkeypatch.setattr(main_module, "postgres_adapter", FakePostgresAdapter())

    response = client.post("/postgres/support-tickets/quality-report")

    assert response.status_code == 200
    payload = response.json()
    checks = {finding["check_name"] for finding in payload["findings"]}

    assert payload["dataset"]["id"] == "support_tickets"
    assert payload["row_count"] == 8
    assert payload["status"] == "FAIL"
    assert "duplicate_primary_key" in checks
    assert "negative_amount" in checks


def test_business_csv_rejects_missing_primary_key_column():
    response = client.post(
        "/business-data/quality-report",
        data={
            "dataset_name": "Bad Export",
            "owner": "ops",
            "primary_key": "missing_id",
        },
        files={"file": ("bad.csv", "id,value\n1,2\n", "text/csv")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Primary key must match a CSV column"


def test_support_ticket_case_study_produces_reproducible_business_findings():
    csv = (ROOT / "examples" / "support_tickets.csv").read_text()
    response = client.post(
        "/business-data/quality-report",
        data={
            "dataset_name": "Support Tickets",
            "owner": "support-ops",
            "primary_key": "ticket_id",
            "expected_columns": "ticket_id,team,priority,status,amount,created_at",
            "description": "Support ticket export used by operations dashboards.",
        },
        files={"file": ("support_tickets.csv", csv, "text/csv")},
    )

    assert response.status_code == 200
    payload = response.json()
    checks = {finding["check_name"] for finding in payload["findings"]}
    rule_ids = {rule["rule_id"] for rule in payload["business_rule_references"]}

    assert payload["row_count"] == 8
    assert payload["status"] == "FAIL"
    assert "duplicate_primary_key" in checks
    assert "missing_values" in checks
    assert "negative_amount" in checks
    assert "numeric_outliers" in checks
    assert {"support_tickets:R1", "support_tickets:R2", "support_tickets:R3", "support_tickets:R4"} <= rule_ids


def test_run_trace_endpoint_returns_sanitized_quality_report_trace():
    response = client.post("/datasets/orders_daily/quality-report")
    trace_id = response.json()["trace_id"]

    trace_response = client.get(f"/runs/{trace_id}")

    assert trace_response.status_code == 200
    payload = trace_response.json()
    assert payload["trace_id"] == trace_id
    assert payload["report_type"] == "quality_report"
    assert payload["summary"]["finding_count"] >= 1
    assert "business_rule_count" in payload["summary"]
    assert payload["evaluation"]["final_report_attached"] is True
    assert "agent_trace" not in payload


def test_run_trace_endpoint_records_disabled_agent_fallback_without_raw_rows():
    csv = "customer_id,email,lifetime_value\n1,a@example.com,10\n2,,20\n"
    response = client.post(
        "/business-data/agent-report",
        data={
            "dataset_name": "Customer Export",
            "owner": "growth",
            "primary_key": "customer_id",
            "expected_columns": "customer_id,email,lifetime_value",
        },
        files={"file": ("customers.csv", csv, "text/csv")},
    )
    trace_id = response.json()["trace_id"]

    trace_response = client.get(f"/runs/{trace_id}")

    assert trace_response.status_code == 200
    payload = trace_response.json()
    assert payload["report_type"] == "agent_report"
    assert payload["fallback_status"] == "agent_disabled"
    assert payload["error"] == "OPENAI_API_KEY is not configured"
    assert "a@example.com" not in trace_response.text


def test_run_trace_endpoint_returns_404_for_unknown_trace():
    response = client.get("/runs/run_missing")

    assert response.status_code == 404
    assert response.json()["detail"] == "Run trace not found"
