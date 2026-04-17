import yfinance as yf
import pandas as pd
from ingestion.base import BaseDataReader
from core.decorators import retry
from core.exceptions import IngestionError

class ApiReader(BaseDataReader):
    @retry(max_attempts=3)
    def _read(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        df = yf.download(ticker, start=start, end=end, progress=False)
        if df.empty:
            raise IngestionError(f"No data returned for ticker: {ticker}")
        df = df.reset_index()
        df["Ticker"] = ticker
        return df