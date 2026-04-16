import numpy as np
import pandas as pd
from processing.base_processor import BaseProcessor

class StockProcessor(BaseProcessor):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # Daily log return
        df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))
        # Simple daily return
        df["daily_return"] = df["Close"].pct_change()
        # Cumulative return
        df["cumulative_return"] = (1 + df["daily_return"]).cumprod() - 1
        # Rolling 20-day volatility (annualised)
        df["rolling_vol_20d"] = df["log_return"].rolling(20).std() * np.sqrt(252)
        # Moving averages
        df["sma_50"] = df["Close"].rolling(50).mean()
        df["sma_200"] = df["Close"].rolling(200).mean()
        # Drop first row (NaN return)
        return df.dropna(subset=["log_return"]).reset_index(drop=True)