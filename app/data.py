from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

from app.models import DatasetSummary


NOW = datetime(2026, 8, 8, 12, 0, tzinfo=timezone.utc)


DATASETS = {
    "orders_daily": DatasetSummary(
        id="orders_daily",
        name="Daily Orders",
        owner="growth-data",
        primary_key="order_id",
        expected_columns=["order_id", "user_id", "order_total", "currency", "status", "created_at"],
        description="Daily order events used for revenue reporting and growth dashboards.",
        last_loaded_at=NOW - timedelta(hours=2),
    ),
    "payments_events": DatasetSummary(
        id="payments_events",
        name="Payment Events",
        owner="payments-analytics",
        primary_key="payment_id",
        expected_columns=["payment_id", "order_id", "provider", "amount", "status", "processed_at"],
        description="Payment processor events used for settlement and reconciliation analysis.",
        last_loaded_at=NOW - timedelta(hours=31),
    ),
    "customer_profiles": DatasetSummary(
        id="customer_profiles",
        name="Customer Profiles",
        owner="crm-data",
        primary_key="customer_id",
        expected_columns=["customer_id", "email", "signup_channel", "country", "lifetime_value", "updated_at"],
        description="Customer-level profile table used by marketing and retention models.",
        last_loaded_at=NOW - timedelta(hours=4),
    ),
}


def load_dataset(dataset_id: str) -> pd.DataFrame:
    if dataset_id == "orders_daily":
        return pd.DataFrame(
            [
                ["ord_001", "usr_001", 48.2, "USD", "paid", NOW - timedelta(hours=5)],
                ["ord_002", "usr_002", 19.0, "USD", "paid", NOW - timedelta(hours=5)],
                ["ord_003", "usr_003", np.nan, "USD", "paid", NOW - timedelta(hours=4)],
                ["ord_004", "usr_004", 21.5, "USD", "refunded", NOW - timedelta(hours=4)],
                ["ord_004", "usr_004", 21.5, "USD", "refunded", NOW - timedelta(hours=4)],
                ["ord_006", "usr_006", 2099.0, "USD", "paid", NOW - timedelta(hours=3)],
                ["ord_007", "usr_007", 31.4, "USD", "paid", NOW - timedelta(hours=3)],
            ],
            columns=["order_id", "user_id", "order_total", "currency", "status", "created_at"],
        )
    if dataset_id == "payments_events":
        return pd.DataFrame(
            [
                ["pay_001", "ord_001", "stripe", 48.2, "captured", NOW - timedelta(hours=34)],
                ["pay_002", "ord_002", "stripe", 19.0, "captured", NOW - timedelta(hours=34)],
                ["pay_003", "ord_003", "adyen", 0.0, "failed", NOW - timedelta(hours=33)],
                ["pay_004", "ord_004", "stripe", 21.5, None, NOW - timedelta(hours=33)],
                ["pay_005", "ord_005", "stripe", -9.99, "captured", NOW - timedelta(hours=32)],
            ],
            columns=["payment_id", "order_id", "provider", "amount", "status", "processed_at"],
        )
    if dataset_id == "customer_profiles":
        return pd.DataFrame(
            [
                ["cus_001", "a@example.com", "organic", "US", 120.4, NOW - timedelta(days=1), "legacy"],
                ["cus_002", None, "paid_search", "US", 42.0, NOW - timedelta(days=1), "legacy"],
                ["cus_003", "c@example.com", "organic", "CA", 9999.0, NOW - timedelta(days=1), "legacy"],
                ["cus_004", "d@example.com", None, "US", 8.5, NOW - timedelta(days=1), "legacy"],
            ],
            columns=["customer_id", "email", "signup_channel", "country", "lifetime_value", "updated_at", "legacy_segment"],
        )
    raise KeyError(dataset_id)
