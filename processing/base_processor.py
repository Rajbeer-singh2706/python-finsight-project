from abc import ABC, abstractmethod
import pandas as pd
from core.decorators import log_execution

class BaseProcessor(ABC):
    """Defines the skeleton. Subclasses override only what changes."""

    @log_execution
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.clean(df)
        df = self.transform(df)
        df = self.enrich(df)
        return df

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Default: drop dupes, sort by date."""
        return df.drop_duplicates().sort_values("Date").reset_index(drop=True)

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame: ...

    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optional override for adding external reference data."""
        return df