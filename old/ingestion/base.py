from abc import ABC, abstractmethod
import pandas as pd
from core.decorators import log_execution, track_performance

class BaseDataReader(ABC):
    """All readers must implement read(). Decorators apply universally."""

    @log_execution
    @track_performance
    def read(self, **kwargs) -> pd.DataFrame:
        return self._read(**kwargs)

    @abstractmethod
    def _read(self, **kwargs) -> pd.DataFrame:
        """Subclasses implement the actual reading logic here."""
        pass 