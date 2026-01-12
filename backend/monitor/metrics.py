"""
PROJECT PREDATOR - Metrics
Basic metrics hooks (STUB)
"""
import logging


class MetricsCollector:
    """
    Metrics collector (STUB)
    
    Phase 2: Basic event counting.
    Full metrics system will be added in future phases.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._metrics = {}
        self.logger.info("MetricsCollector initialized (STUB)")
    
    def increment(self, metric_name: str, value: int = 1) -> None:
        """
        Increment a metric
        
        Args:
            metric_name: Metric name
            value: Increment value
        """
        if metric_name not in self._metrics:
            self._metrics[metric_name] = 0
        self._metrics[metric_name] += value
    
    def get_metrics(self) -> dict:
        """Get all metrics"""
        return self._metrics.copy()
