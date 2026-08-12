from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


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
    assert payload["findings"]
    assert payload["agent_trace"]


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
    assert payload["dataset"]["name"] == "Customer Export"
    assert payload["error"] == "OPENAI_API_KEY is not configured"


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
