from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from validation.models import ValidationResult

class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> ValidationResult: ...

class NullCheckStrategy(ValidationStrategy):
    def __init__(self, column: str):
        self.column = column

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        null_mask = df[self.column].isnull()
        return ValidationResult(
            rule_name=f"null_check:{self.column}",
            passed=int((~null_mask).sum()),
            failed=int(null_mask.sum()),
            failed_rows=df[null_mask]
        )

class RangeCheckStrategy(ValidationStrategy):
    def __init__(self, column: str, min_val: float, max_val: float):
        self.column, self.min_val, self.max_val = column, min_val, max_val

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        mask = df[self.column].between(self.min_val, self.max_val)
        return ValidationResult(
            rule_name=f"range_check:{self.column}[{self.min_val},{self.max_val}]",
            passed=int(mask.sum()),
            failed=int((~mask).sum()),
            failed_rows=df[~mask]
        )

class OutlierStrategy(ValidationStrategy):
    """Uses NumPy Z-score to flag statistical outliers."""
    def __init__(self, column: str, threshold: float = 3.0):
        self.column, self.threshold = column, threshold

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        values = df[self.column].dropna().values
        mean, std = np.mean(values), np.std(values)
        z_scores = np.abs((df[self.column] - mean) / std)
        outlier_mask = z_scores > self.threshold
        return ValidationResult(
            rule_name=f"outlier_check:{self.column}(z>{self.threshold})",
            passed=int((~outlier_mask).sum()),
            failed=int(outlier_mask.sum()),
            failed_rows=df[outlier_mask]
        )