from abc import ABC, abstractmethod
from typing import List
from core.logger import get_logger

logger = get_logger(__name__)

class AlertObserver(ABC):
    @abstractmethod
    def notify(self, metric: str, value: float, threshold: float): ...

class LogAlertObserver(AlertObserver):
    def notify(self, metric, value, threshold):
        logger.warning(f"ALERT: {metric} = {value:.4f} breached threshold {threshold}")

class SlackAlertObserver(AlertObserver):
    """In production this would POST to a webhook. Here it just prints."""
    def notify(self, metric, value, threshold):
        print(f"[SLACK] {metric} = {round(value, 4)} | threshold: {threshold}")

class AlertManager:
    def __init__(self):
        self._observers: List[AlertObserver] = []

    def subscribe(self, observer: AlertObserver) -> None:
        self._observers.append(observer)

    def check(self, metric: str, value: float, threshold: float,
               condition: str = "below") -> None:
        triggered = (value < threshold) if condition == "below" else (value > threshold)
        if triggered:
            for obs in self._observers:
                obs.notify(metric, value, threshold)