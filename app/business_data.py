from datetime import datetime, timezone
from io import BytesIO
from re import sub
from typing import Annotated

import pandas as pd
from fastapi import File, Form, HTTPException, UploadFile

from app.models import DatasetSummary


MAX_UPLOAD_BYTES = 2_000_000
MAX_ROWS = 10_000
MAX_COLUMNS = 80


class BusinessDataRequest:
    def __init__(
        self,
        file: Annotated[UploadFile, File(description="CSV file exported from a business workflow")],
        dataset_name: Annotated[str, Form(description="Human-readable business dataset name")],
        owner: Annotated[str, Form(description="Owning team or business function")],
        primary_key: Annotated[str, Form(description="Column that should uniquely identify rows")],
        expected_columns: Annotated[str | None, Form(description="Comma-separated expected column list")] = None,
        description: Annotated[str | None, Form(description="Business use case for this dataset")] = None,
    ) -> None:
        self.file = file
        self.dataset_name = dataset_name
        self.owner = owner
        self.primary_key = primary_key
        self.expected_columns = expected_columns
        self.description = description


async def load_business_csv(request: BusinessDataRequest) -> tuple[DatasetSummary, pd.DataFrame]:
    if not request.file.filename or not request.file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV uploads are supported")

    content = await request.file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"CSV exceeds {MAX_UPLOAD_BYTES} byte limit")

    try:
        frame = pd.read_csv(BytesIO(content))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Unable to parse CSV: {exc.__class__.__name__}") from exc

    if frame.empty:
        raise HTTPException(status_code=400, detail="CSV must contain at least one row")
    if len(frame) > MAX_ROWS:
        raise HTTPException(status_code=413, detail=f"CSV exceeds {MAX_ROWS} row limit")
    if len(frame.columns) > MAX_COLUMNS:
        raise HTTPException(status_code=413, detail=f"CSV exceeds {MAX_COLUMNS} column limit")
    if request.primary_key not in frame.columns:
        raise HTTPException(status_code=400, detail="Primary key must match a CSV column")

    expected_columns = _parse_expected_columns(request.expected_columns) or list(frame.columns)
    dataset = DatasetSummary(
        id=_slugify(request.dataset_name),
        name=request.dataset_name.strip(),
        owner=request.owner.strip(),
        primary_key=request.primary_key.strip(),
        expected_columns=expected_columns,
        description=(request.description or "Uploaded business dataset for data-quality analysis.").strip(),
        last_loaded_at=datetime.now(timezone.utc),
    )
    return dataset, frame


def _parse_expected_columns(value: str | None) -> list[str]:
    if not value:
        return []
    return [column.strip() for column in value.split(",") if column.strip()]


def _slugify(value: str) -> str:
    slug = sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "business_dataset"
