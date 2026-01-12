"""
PROJECT PREDATOR - ASPAAgent
FAZ 2: Agent skeleton - NO REAL LOGIC
"""
from backend.agents.base import BaseAgent
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry


class ASPAAgent(BaseAgent):
    """
    ASPA Agent (FAZ 2 - SKELETON)
    
    Responsibilities (Blueprint):
    - On StrategyReviewEvent → log "analyzing strategy"
    
    FAZ 2: NO real strategy analysis
    Just event subscription and logging.
    
    Note: StrategyReviewEvent doesn't exist yet, using HEARTBEAT as placeholder
    """
    
    def __init__(self, event_bus: EventBus, registry: Registry):
        super().__init__(event_bus, registry)
        self._strategy_handler = None
        self.logger.info("ASPAAgent initialized (SKELETON)")
    
    def _subscribe_events(self) -> None:
        """Subscribe to HEARTBEAT events (placeholder for StrategyReviewEvent)"""
        self._strategy_handler = self._on_strategy_review
        self.event_bus.subscribe(EventType.HEARTBEAT, self._strategy_handler)
        self.logger.info("Subscribed to HEARTBEAT events (placeholder)")
    
    def _unsubscribe_events(self) -> None:
        """Unsubscribe from events"""
        if self._strategy_handler:
            self.event_bus.unsubscribe(EventType.HEARTBEAT, self._strategy_handler)
    
    def _on_strategy_review(self, event: Event) -> None:
        """
        Handle StrategyReviewEvent
        
        Blueprint requirement: log "analyzing strategy"
        """
        self._log_event(event)
        self.logger.debug("analyzing strategy")
