import pytest
from ingestion.factory import DataReaderFactory
from core.exceptions import IngestionError

def test_factory_creates_csv_reader():
    reader = DataReaderFactory.create("csv")
    assert reader is not None

def test_factory_raises_on_unknown_source():
    with pytest.raises(IngestionError):
        DataReaderFactory.create("ftp")

def test_api_reader_returns_dataframe():
    reader = DataReaderFactory.create("api")
    df = reader.read(ticker="AAPL", start="2023-01-01", end="2023-03-01")
    assert not df.empty
    assert "Close" in df.columns