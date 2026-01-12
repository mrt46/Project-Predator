"""
PROJECT PREDATOR - RRSAgent (Infra Sentinel)
FAZ 2: Agent skeleton - NO REAL LOGIC
"""
from backend.agents.base import BaseAgent
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry


class RRSAgent(BaseAgent):
    """
    RRS Agent - Infrastructure Sentinel (FAZ 2 - SKELETON)
    
    Responsibilities (Blueprint):
    - Every N seconds → log "infra OK"
    
    FAZ 2: NO real infrastructure monitoring
    Just event subscription and logging.
    """
    
    def __init__(self, event_bus: EventBus, registry: Registry):
        super().__init__(event_bus, registry)
        self._heartbeat_handler = None
        self.logger.info("RRSAgent initialized (SKELETON)")
    
    def _subscribe_events(self) -> None:
        """Subscribe to HEARTBEAT events"""
        self._heartbeat_handler = self._on_heartbeat
        self.event_bus.subscribe(EventType.HEARTBEAT, self._heartbeat_handler)
        self.logger.info("Subscribed to HEARTBEAT events")
    
    def _unsubscribe_events(self) -> None:
        """Unsubscribe from events"""
        if self._heartbeat_handler:
            self.event_bus.unsubscribe(EventType.HEARTBEAT, self._heartbeat_handler)
    
    def _on_heartbeat(self, event: Event) -> None:
        """
        Handle HEARTBEAT event
        
        Blueprint requirement: log "infra OK"
        """
        self._log_event(event)
        self.logger.info("infra OK")
