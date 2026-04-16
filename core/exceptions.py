class FinSightError(Exception):
    """Base exception for all pipeline errors."""

class IngestionError(FinSightError): pass
class ValidationError(FinSightError): pass
class ProcessingError(FinSightError): pass
class AnalyticsError(FinSightError): pass
class ReportingError(FinSightError): pass
class ConfigurationError(FinSightError): pass