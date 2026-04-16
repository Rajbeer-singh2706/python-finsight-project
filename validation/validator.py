import pandas as pd
from pathlib import Path
from typing import List
from validation.strategies import ValidationStrategy
from validation.models import ValidationResult
from core.decorators import log_execution
from core.logger import get_logger

logger = get_logger(__name__)

class DataValidator:
    def __init__(self, strategies: List[ValidationStrategy]):
        self.strategies = strategies

    @log_execution
    def validate(self, df: pd.DataFrame) -> tuple[pd.DataFrame, List[ValidationResult]]:
        results = []
        quarantine_frames = []

        for strategy in self.strategies:
            result = strategy.validate(df)
            results.append(result)
            logger.info(f"Rule '{result.rule_name}': score={result.quality_score}%")
            if not result.failed_rows.empty:
                quarantine_frames.append(result.failed_rows)

        # Remove all quarantined rows from the clean DataFrame
        if quarantine_frames:
            bad_indices = pd.concat(quarantine_frames).index.unique()
            df = df.drop(index=bad_indices)

        return df, results

    def save_quarantine(self, results: List[ValidationResult], path: str) -> None:
        all_bad = pd.concat([r.failed_rows for r in results if not r.failed_rows.empty])
        if not all_bad.empty:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            all_bad.to_csv(path, index=False)
            logger.info(f"Quarantine saved: {len(all_bad)} rows → {path}")