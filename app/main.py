from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse

from app.agent import DataQualityAgent
from app.business_data import BusinessDataRequest, load_business_csv
from app.dashboard import render_dashboard
from app.data import DATASETS, load_dataset
from app.incident_export import render_incident_markdown
from app.models import AgentRunReport, DatasetMemorySummary, DatasetProfile, DatasetSummary, QualityReport
from app.postgres_adapter import PostgresAdapterError, PostgresDatasetAdapter
from app.profiler import DatasetProfiler
from app.tool_agent import LLMDataQualityAgent
from app.traces import RunTraceStore

app = FastAPI(title="Data Quality Agent", version="1.0.0")
agent = DataQualityAgent()
llm_agent = LLMDataQualityAgent()
profiler = DatasetProfiler()
trace_store = RunTraceStore()
postgres_adapter = PostgresDatasetAdapter()


@app.get("/health")
def health():
    return {"status": "ok", "service": "data-quality-agent"}


@app.get("/datasets", response_model=list[DatasetSummary])
def list_datasets():
    return list(DATASETS.values())


@app.get("/datasets/{dataset_id}", response_model=DatasetSummary)
def get_dataset(dataset_id: str):
    dataset = DATASETS.get(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


@app.get("/datasets/{dataset_id}/profile", response_model=DatasetProfile)
def profile_dataset(dataset_id: str):
    dataset = DATASETS.get(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return profiler.profile(dataset, load_dataset(dataset_id))


@app.post("/datasets/{dataset_id}/quality-report", response_model=QualityReport)
def create_quality_report(dataset_id: str):
    dataset = DATASETS.get(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return trace_store.save_quality_report(agent.analyze(dataset, load_dataset(dataset_id)))


@app.post("/datasets/{dataset_id}/incident-report.md", response_class=PlainTextResponse)
def create_incident_report_markdown(dataset_id: str):
    dataset = DATASETS.get(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    report = trace_store.save_quality_report(agent.analyze(dataset, load_dataset(dataset_id)))
    return render_incident_markdown(report)


@app.post("/datasets/{dataset_id}/agent-report", response_model=AgentRunReport)
def create_agent_report(dataset_id: str):
    dataset = DATASETS.get(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return trace_store.save_agent_report(llm_agent.run(dataset, load_dataset(dataset_id)))


@app.post("/business-data/quality-report", response_model=QualityReport)
async def create_business_quality_report(request: Annotated[BusinessDataRequest, Depends()]):
    dataset, frame = await load_business_csv(request)
    return trace_store.save_quality_report(agent.analyze(dataset, frame))


@app.post("/business-data/agent-report", response_model=AgentRunReport)
async def create_business_agent_report(request: Annotated[BusinessDataRequest, Depends()]):
    dataset, frame = await load_business_csv(request)
    return trace_store.save_agent_report(llm_agent.run(dataset, frame))


@app.post("/postgres/support-tickets/quality-report", response_model=QualityReport)
def create_postgres_support_ticket_report():
    dataset, frame = _load_postgres_support_tickets()
    return trace_store.save_quality_report(agent.analyze(dataset, frame))


@app.post("/postgres/support-tickets/agent-report", response_model=AgentRunReport)
def create_postgres_support_ticket_agent_report():
    dataset, frame = _load_postgres_support_tickets()
    return trace_store.save_agent_report(llm_agent.run(dataset, frame))


def _load_postgres_support_tickets():
    try:
        return postgres_adapter.load_table(
            "support_tickets",
            dataset_name="Support Tickets",
            owner="support-ops",
            primary_key="ticket_id",
            expected_columns=["ticket_id", "team", "priority", "status", "amount", "created_at"],
            description="Read-only PostgreSQL support-ticket table used by operations dashboards.",
        )
    except PostgresAdapterError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/runs/{trace_id}")
def get_run_trace(trace_id: str):
    trace = trace_store.get(trace_id)
    if trace is None:
        raise HTTPException(status_code=404, detail="Run trace not found")
    return trace


@app.get("/datasets/{dataset_id}/memory", response_model=DatasetMemorySummary)
def get_dataset_memory(dataset_id: str, limit: int = 5):
    dataset_exists = dataset_id in DATASETS
    if not dataset_exists:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return trace_store.list_by_dataset(dataset_id, limit=limit)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return render_dashboard()
