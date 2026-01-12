"""
PROJECT PREDATOR - DataEngineeringAgent
FAZ 2: Agent skeleton - NO REAL LOGIC
"""
from backend.agents.base import BaseAgent
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry


class DataEngineeringAgent(BaseAgent):
    """
    Data Engineering Agent (FAZ 2 - SKELETON)
    
    Responsibilities (Blueprint):
    - On Tick → log "processing data"
    
    FAZ 2: NO real data processing
    Just event subscription and logging.
    """
    
    def __init__(self, event_bus: EventBus, registry: Registry):
        super().__init__(event_bus, registry)
        self._tick_handler = None
        self.logger.info("DataEngineeringAgent initialized (SKELETON)")
    
    def _subscribe_events(self) -> None:
        """Subscribe to TICK events"""
        self._tick_handler = self._on_tick
        self.event_bus.subscribe(EventType.TICK, self._tick_handler)
        self.logger.info("Subscribed to TICK events")
    
    def _unsubscribe_events(self) -> None:
        """Unsubscribe from events"""
        if self._tick_handler:
            self.event_bus.unsubscribe(EventType.TICK, self._tick_handler)
    
    def _on_tick(self, event: Event) -> None:
        """
        Handle TICK event
        
        Blueprint requirement: log "processing data"
        """
        self._log_event(event)
        self.logger.debug("processing data")
