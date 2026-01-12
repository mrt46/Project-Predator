"""
PROJECT PREDATOR - CRORiskAgent
FAZ 2: Agent skeleton - NO REAL LOGIC
"""
from backend.agents.base import BaseAgent
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry


class CRORiskAgent(BaseAgent):
    """
    CRO Risk Agent (FAZ 2 - SKELETON)
    
    Responsibilities (Blueprint):
    - On RiskEvent → log "risk check"
    
    FAZ 2: NO real risk management
    Just event subscription and logging.
    """
    
    def __init__(self, event_bus: EventBus, registry: Registry):
        super().__init__(event_bus, registry)
        self._risk_handler = None
        self.logger.info("CRORiskAgent initialized (SKELETON)")
    
    def _subscribe_events(self) -> None:
        """Subscribe to RISK_CHECK events"""
        self._risk_handler = self._on_risk_event
        self.event_bus.subscribe(EventType.RISK_CHECK, self._risk_handler)
        self.logger.info("Subscribed to RISK_CHECK events")
    
    def _unsubscribe_events(self) -> None:
        """Unsubscribe from events"""
        if self._risk_handler:
            self.event_bus.unsubscribe(EventType.RISK_CHECK, self._risk_handler)
    
    def _on_risk_event(self, event: Event) -> None:
        """
        Handle RISK_CHECK event
        
        Blueprint requirement: log "risk check"
        """
        self._log_event(event)
        self.logger.info("risk check")
