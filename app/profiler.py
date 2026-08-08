import pandas as pd

from app.models import ColumnProfile, DatasetProfile, DatasetSummary


class DatasetProfiler:
    name = "dataset_profiler"

    def profile(self, dataset: DatasetSummary, frame: pd.DataFrame) -> DatasetProfile:
        columns = []
        for column in frame.columns:
            values = frame[column]
            samples = [str(value) for value in values.dropna().head(3).tolist()]
            columns.append(
                ColumnProfile(
                    column=column,
                    dtype=str(values.dtype),
                    missing_count=int(values.isna().sum()),
                    missing_rate=float(values.isna().mean()),
                    unique_count=int(values.nunique(dropna=True)),
                    sample_values=samples,
                )
            )

        return DatasetProfile(
            dataset=dataset,
            row_count=len(frame),
            column_count=len(frame.columns),
            columns=columns,
        )
