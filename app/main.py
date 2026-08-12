from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.agent import DataQualityAgent
from app.business_data import BusinessDataRequest, load_business_csv
from app.dashboard import render_dashboard
from app.data import DATASETS, load_dataset
from app.models import AgentRunReport, DatasetProfile, DatasetSummary, QualityReport
from app.profiler import DatasetProfiler
from app.tool_agent import LLMDataQualityAgent

app = FastAPI(title="Data Quality Agent", version="1.0.0")
agent = DataQualityAgent()
llm_agent = LLMDataQualityAgent()
profiler = DatasetProfiler()


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
    return agent.analyze(dataset, load_dataset(dataset_id))


@app.post("/datasets/{dataset_id}/agent-report", response_model=AgentRunReport)
def create_agent_report(dataset_id: str):
    dataset = DATASETS.get(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return llm_agent.run(dataset, load_dataset(dataset_id))


@app.post("/business-data/quality-report", response_model=QualityReport)
async def create_business_quality_report(request: Annotated[BusinessDataRequest, Depends()]):
    dataset, frame = await load_business_csv(request)
    return agent.analyze(dataset, frame)


@app.post("/business-data/agent-report", response_model=AgentRunReport)
async def create_business_agent_report(request: Annotated[BusinessDataRequest, Depends()]):
    dataset, frame = await load_business_csv(request)
    return llm_agent.run(dataset, frame)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return render_dashboard()
