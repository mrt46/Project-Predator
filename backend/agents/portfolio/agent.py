"""
PROJECT PREDATOR - PortfolioManagerAgent
FAZ 2: Agent skeleton - NO REAL LOGIC
"""
from backend.agents.base import BaseAgent
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry


class PortfolioManagerAgent(BaseAgent):
    """
    Portfolio Manager Agent (FAZ 2 - SKELETON)
    
    Responsibilities (Blueprint):
    - On Tick → log "checking portfolio"
    
    FAZ 2: NO real portfolio management
    Just event subscription and logging.
    """
    
    def __init__(self, event_bus: EventBus, registry: Registry):
        super().__init__(event_bus, registry)
        self._tick_handler = None
        self.logger.info("PortfolioManagerAgent initialized (SKELETON)")
    
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
        
        Blueprint requirement: log "checking portfolio"
        """
        self._log_event(event)
        self.logger.debug("checking portfolio")
