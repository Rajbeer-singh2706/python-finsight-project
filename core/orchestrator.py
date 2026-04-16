from core.config import ConfigManager
from core.logger import get_logger
from ingestion.factory import DataReaderFactory
from validation.validator import DataValidator
from validation.strategies import NullCheckStrategy, RangeCheckStrategy, OutlierStrategy
from processing.stock_processor import StockProcessor
from analytics.metrics import PortfolioMetrics
from reporting.alerts import AlertManager, LogAlertObserver
from reporting.charts import plot_cumulative_returns, plot_correlation_heatmap
from reporting.dashboard import build_dashboard
import numpy as np

logger = get_logger(__name__)

class PipelineOrchestrator:
    def __init__(self):
        self.config = ConfigManager.get_instance()
        self.config.load()
        self.alert_manager = AlertManager()
        self.alert_manager.subscribe(LogAlertObserver())

    def run(self, ticker: str) -> None:
        logger.info(f"Pipeline starting for {ticker}")

        # Ingest
        reader = DataReaderFactory.create("api")
        df = reader.read(ticker=ticker,
                         start=self.config.get("pipeline", "start_date"),
                         end=self.config.get("pipeline", "end_date"))

        # Validate
        validator = DataValidator([
            NullCheckStrategy("Close"),
            RangeCheckStrategy("Close",
                self.config.get("validation", "price_min"),
                self.config.get("validation", "price_max")),
            OutlierStrategy("Volume")
        ])
        df, val_results = validator.validate(df)
        validator.save_quarantine(val_results, f"data/processed/{ticker}_quarantine.csv")

        # Process
        processor = StockProcessor()
        df = processor.run(df)

        # Analytics
        metrics = {
            "sharpe_ratio": PortfolioMetrics.sharpe_ratio(df["daily_return"].dropna().values),
            "max_drawdown": PortfolioMetrics.max_drawdown(df["cumulative_return"].values),
            "var_95": PortfolioMetrics.value_at_risk(df["daily_return"].dropna().values),
            "annualised_vol": PortfolioMetrics.annualised_volatility(df["daily_return"].dropna().values),
        }

        # Alerts
        self.alert_manager.check("sharpe_ratio", metrics["sharpe_ratio"],
            self.config.get("alerts", "sharpe_threshold"), "below")
        self.alert_manager.check("var_95", metrics["var_95"],
            self.config.get("alerts", "var_threshold"), "below")

        # Report
        output_dir = self.config.get("data", "reports_path")
        plot_cumulative_returns(df, ticker, output_dir)
        build_dashboard(df, metrics, f"{output_dir}/{ticker}_dashboard.html")

        logger.info(f"Pipeline complete for {ticker}. Metrics: {metrics}")
        return df, metrics