# tests/conftest.py
import sys
from pathlib import Path

# Add project root to path so tests can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_ohlcv():
    dates = pd.date_range("2023-01-01", periods=100, freq="B")
    return pd.DataFrame({
        "Date": dates, "Ticker": "TEST",
        "Open": np.random.uniform(100, 200, 100),
        "High": np.random.uniform(200, 220, 100),
        "Low": np.random.uniform(80, 100, 100),
        "Close": np.random.uniform(100, 200, 100),
        "Volume": np.random.randint(1_000_000, 50_000_000, 100)
    })