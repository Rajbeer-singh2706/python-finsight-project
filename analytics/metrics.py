import numpy as np
import pandas as pd
from core.decorators import log_execution

class PortfolioMetrics:

    @staticmethod
    def sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.04) -> float:
        excess = returns - (risk_free_rate / 252)
        return float(np.mean(excess) / np.std(excess) * np.sqrt(252))

    @staticmethod
    def max_drawdown(cumulative_returns: np.ndarray) -> float:
        peak = np.maximum.accumulate(cumulative_returns + 1)
        drawdown = (cumulative_returns + 1 - peak) / peak
        return float(drawdown.min())

    @staticmethod
    def value_at_risk(returns: np.ndarray, confidence: float = 0.95) -> float:
        return float(np.percentile(returns, (1 - confidence) * 100))

    @staticmethod
    def annualised_volatility(returns: np.ndarray) -> float:
        return float(np.std(returns) * np.sqrt(252))

    @staticmethod
    def correlation_matrix(returns_df: pd.DataFrame) -> pd.DataFrame:
        return returns_df.corr()