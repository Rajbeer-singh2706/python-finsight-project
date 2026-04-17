from ingestion.base import BaseDataReader
from ingestion.csv_reader import CsvReader
from ingestion.api_reader import ApiReader
from core.exceptions import IngestionError

class DataReaderFactory:
    _registry = {
        "csv": CsvReader,
        "api": ApiReader,
    }

    @classmethod
    def create(cls, source_type: str) -> BaseDataReader:
        source_type = source_type.lower()
        if source_type not in cls._registry:
            raise IngestionError(f"Unknown source type: '{source_type}'. Available: {list(cls._registry)}")
        return cls._registry[source_type]()

    @classmethod
    def register(cls, name: str, reader_class):
        """Allows adding new reader types at runtime — open/closed principle."""
        cls._registry[name] = reader_class