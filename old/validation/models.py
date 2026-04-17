from dataclasses import dataclass, field
import pandas as pd

@dataclass
class ValidationResult:
    rule_name: str
    passed: int
    failed: int
    failed_rows: pd.DataFrame = field(default_factory=pd.DataFrame)

    @property
    def quality_score(self) -> float:
        total = self.passed + self.failed
        return round((self.passed / total) * 100, 2) if total > 0 else 0.0

    @property
    def is_passing(self) -> bool:
        return self.failed == 0