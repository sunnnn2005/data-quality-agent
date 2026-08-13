import pytest

from app.postgres_adapter import PostgresAdapterError, PostgresDatasetAdapter


class FakeCursor:
    def __init__(self, rows, columns):
        self.rows = rows
        self.description = [(column,) for column in columns]
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchall(self):
        return self.rows

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None


class FakeConnection:
    def __init__(self, rows, columns):
        self.cursor_instance = FakeCursor(rows, columns)

    def cursor(self):
        return self.cursor_instance

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None


def test_postgres_adapter_loads_bounded_read_only_table_with_fake_connection():
    adapter = PostgresDatasetAdapter(row_limit=2)
    connection = FakeConnection(rows=[(1, "open"), (2, "closed")], columns=["ticket_id", "status"])

    dataset, frame = adapter.load_table(
        "public.support_tickets",
        dataset_name="Support Tickets",
        owner="support-ops",
        primary_key="ticket_id",
        expected_columns=["ticket_id", "status"],
        description="Support ticket table from PostgreSQL.",
        connection=connection,
    )

    assert dataset.id == "support_tickets"
    assert dataset.primary_key == "ticket_id"
    assert frame.shape == (2, 2)
    assert connection.cursor_instance.executed[0][0].startswith("SET LOCAL statement_timeout")
    assert connection.cursor_instance.executed[1][0] == "SELECT * FROM public.support_tickets LIMIT 2"


@pytest.mark.parametrize(
    "query",
    [
        "DELETE FROM support_tickets LIMIT 10",
        "UPDATE support_tickets SET status = 'closed' LIMIT 10",
        "SELECT * FROM support_tickets; DROP TABLE support_tickets",
        "SELECT * FROM support_tickets",
    ],
)
def test_postgres_adapter_rejects_unbounded_or_write_queries(query):
    adapter = PostgresDatasetAdapter()

    with pytest.raises(PostgresAdapterError):
        adapter._validate_read_only_query(query)


def test_postgres_adapter_rejects_missing_primary_key_config():
    adapter = PostgresDatasetAdapter()

    with pytest.raises(PostgresAdapterError, match="primary_key is required"):
        adapter.load_table(
            "public.support_tickets",
            dataset_name="Support Tickets",
            owner="support-ops",
            primary_key="",
            expected_columns=["ticket_id"],
            description="Support ticket table from PostgreSQL.",
            connection=FakeConnection(rows=[(1,)], columns=["ticket_id"]),
        )


def test_postgres_adapter_rejects_primary_key_missing_from_selected_columns():
    adapter = PostgresDatasetAdapter()

    with pytest.raises(PostgresAdapterError, match="primary_key must exist"):
        adapter.load_table(
            "public.support_tickets",
            dataset_name="Support Tickets",
            owner="support-ops",
            primary_key="ticket_id",
            expected_columns=["ticket_id", "status"],
            description="Support ticket table from PostgreSQL.",
            connection=FakeConnection(rows=[("open",)], columns=["status"]),
        )


def test_postgres_adapter_rejects_unsafe_table_name_and_row_limit():
    with pytest.raises(PostgresAdapterError):
        PostgresDatasetAdapter(row_limit=20_000)

    adapter = PostgresDatasetAdapter(row_limit=10)
    with pytest.raises(PostgresAdapterError, match="dot-separated identifier"):
        adapter._build_select_query("public.support_tickets;drop")
