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
