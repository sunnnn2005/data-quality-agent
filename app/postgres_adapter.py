from datetime import datetime, timezone
from os import getenv
from re import search
from typing import Any, Protocol

import pandas as pd

from app.models import DatasetSummary


DEFAULT_ROW_LIMIT = 1_000
MAX_ROW_LIMIT = 10_000
READ_ONLY_TIMEOUT_MS = 5_000
WRITE_PATTERN = r"\b(insert|update|delete|drop|alter|truncate|create|grant|revoke|copy|call|merge)\b"


class PostgresAdapterError(ValueError):
    pass


class CursorLike(Protocol):
    description: Any

    def execute(self, query: str, params: tuple[Any, ...] | None = None) -> None:
        ...

    def fetchall(self) -> list[tuple[Any, ...]]:
        ...

    def __enter__(self) -> "CursorLike":
        ...

    def __exit__(self, exc_type, exc, tb) -> None:
        ...


class ConnectionLike(Protocol):
    def cursor(self) -> CursorLike:
        ...

    def __enter__(self) -> "ConnectionLike":
        ...

    def __exit__(self, exc_type, exc, tb) -> None:
        ...


class PostgresDatasetAdapter:
    name = "postgres_dataset_adapter"

    def __init__(self, dsn: str | None = None, row_limit: int = DEFAULT_ROW_LIMIT) -> None:
        self.dsn = dsn or getenv("POSTGRES_DSN")
        self.row_limit = self._validate_row_limit(row_limit)

    @property
    def enabled(self) -> bool:
        return getenv("ENABLE_POSTGRES_ADAPTER", "").lower() in {"1", "true", "yes"}

    def load_table(
        self,
        table: str,
        *,
        dataset_name: str,
        owner: str,
        primary_key: str,
        expected_columns: list[str],
        description: str,
        connection: ConnectionLike | None = None,
    ) -> tuple[DatasetSummary, pd.DataFrame]:
        if not self.enabled and connection is None:
            raise PostgresAdapterError("PostgreSQL adapter is disabled; set ENABLE_POSTGRES_ADAPTER=true")
        if not self.dsn and connection is None:
            raise PostgresAdapterError("POSTGRES_DSN is required when no connection is provided")
        if not primary_key:
            raise PostgresAdapterError("primary_key is required")
        if not expected_columns:
            raise PostgresAdapterError("expected_columns is required")

        query = self._build_select_query(table)
        frame = self._query_frame(query, connection)
        if primary_key not in frame.columns:
            raise PostgresAdapterError("primary_key must exist in selected table columns")

        dataset = DatasetSummary(
            id=self._slugify(dataset_name),
            name=dataset_name,
            owner=owner,
            primary_key=primary_key,
            expected_columns=expected_columns,
            description=description,
            last_loaded_at=datetime.now(timezone.utc),
        )
        return dataset, frame

    def _query_frame(self, query: str, connection: ConnectionLike | None = None) -> pd.DataFrame:
        self._validate_read_only_query(query)
        managed_connection = connection or self._connect()
        with managed_connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SET LOCAL statement_timeout = {READ_ONLY_TIMEOUT_MS}")
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
        return pd.DataFrame(rows, columns=columns)

    def _connect(self) -> ConnectionLike:
        import psycopg

        return psycopg.connect(self.dsn, autocommit=False)

    def _build_select_query(self, table: str) -> str:
        if not self._is_safe_identifier_path(table):
            raise PostgresAdapterError("table must be a dot-separated identifier path")
        return f"SELECT * FROM {table} LIMIT {self.row_limit}"

    def _validate_read_only_query(self, query: str) -> None:
        normalized = query.strip().lower()
        if not normalized.startswith("select "):
            raise PostgresAdapterError("only SELECT queries are allowed")
        if ";" in normalized.rstrip(";"):
            raise PostgresAdapterError("multiple statements are not allowed")
        if search(WRITE_PATTERN, normalized):
            raise PostgresAdapterError("write operations are not allowed")
        if " limit " not in normalized:
            raise PostgresAdapterError("bounded SELECT query must include LIMIT")

    def _validate_row_limit(self, row_limit: int) -> int:
        if row_limit < 1 or row_limit > MAX_ROW_LIMIT:
            raise PostgresAdapterError(f"row_limit must be between 1 and {MAX_ROW_LIMIT}")
        return row_limit

    def _is_safe_identifier_path(self, value: str) -> bool:
        return all(part.isidentifier() for part in value.split("."))

    def _slugify(self, value: str) -> str:
        return "_".join(part for part in value.lower().split() if part) or "postgres_dataset"
