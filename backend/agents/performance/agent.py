"""
PROJECT PREDATOR - PerformanceKPIAgent
FAZ 2: Agent skeleton - NO REAL LOGIC
"""
from backend.agents.base import BaseAgent
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry


class PerformanceKPIAgent(BaseAgent):
    """
    Performance KPI Agent (FAZ 2 - SKELETON)
    
    Responsibilities (Blueprint):
    - On ExecutionResult → log "recording KPI"
    
    FAZ 2: NO real KPI recording
    Just event subscription and logging.
    """
    
    def __init__(self, event_bus: EventBus, registry: Registry):
        super().__init__(event_bus, registry)
        self._execution_handler = None
        self.logger.info("PerformanceKPIAgent initialized (SKELETON)")
    
    def _subscribe_events(self) -> None:
        """Subscribe to ORDER_FILLED events (ExecutionResult)"""
        self._execution_handler = self._on_execution_result
        self.event_bus.subscribe(EventType.ORDER_FILLED, self._execution_handler)
        self.logger.info("Subscribed to ORDER_FILLED events")
    
    def _unsubscribe_events(self) -> None:
        """Unsubscribe from events"""
        if self._execution_handler:
            self.event_bus.unsubscribe(EventType.ORDER_FILLED, self._execution_handler)
    
    def _on_execution_result(self, event: Event) -> None:
        """
        Handle ORDER_FILLED event (ExecutionResult)
        
        Blueprint requirement: log "recording KPI"
        """
        self._log_event(event)
        self.logger.info("recording KPI")
