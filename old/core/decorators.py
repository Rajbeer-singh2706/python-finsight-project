import time
import functools
from core.logger import get_logger

logger = get_logger(__name__)

def log_execution(func):
    """Logs function name, args, and execution time."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Starting: {func.__name__}")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = round(time.time() - start, 3)
        logger.info(f"Completed: {func.__name__} in {elapsed}s")
        return result
    return wrapper

def track_performance(func):
    """Adds row count reporting for DataFrame-returning functions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if hasattr(result, '__len__'):
            logger.info(f"{func.__name__} produced {len(result)} rows")
        return result
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retries a function on failure, useful for network calls."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    logger.warning(f"{func.__name__} failed (attempt {attempt}): {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator