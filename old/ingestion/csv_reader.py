import pandas as pd
from pathlib import Path
from ingestion.base import BaseDataReader
from core.exceptions import IngestionError

class CsvReader(BaseDataReader):
    def _read(self, filepath: str) -> pd.DataFrame:
        path = Path(filepath)
        if not path.exists():
            raise IngestionError(f"File not found: {filepath}")
        return pd.read_csv(path, parse_dates=["Date"])