"""
PROJECT PREDATOR - ExecutionAgent
FAZ 2: Agent skeleton - NO REAL LOGIC
"""
from backend.agents.base import BaseAgent
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry
from backend.market.fake_market import FakeMarket


class ExecutionAgent(BaseAgent):
    """
    Execution Agent (FAZ 2 - SKELETON)
    
    Responsibilities (Blueprint):
    - On OrderRequest → log "would execute"
    
    FAZ 2: NO real execution
    Just event subscription and logging.
    """
    
    def __init__(self, event_bus: EventBus, registry: Registry):
        super().__init__(event_bus, registry)
        self._order_handler = None
        self._fake_market = None
        self.logger.info("ExecutionAgent initialized (SKELETON)")
    
    def _subscribe_events(self) -> None:
        """Subscribe to ORDER_REQUEST events"""
        self._order_handler = self._on_order_request
        self.event_bus.subscribe(EventType.ORDER_REQUEST, self._order_handler)
        # Try to obtain FakeMarket from registry (Phase 3)
        fm = self.registry.get("FakeMarket")
        if isinstance(fm, FakeMarket):
            self._fake_market = fm
            self.logger.info("ExecutionAgent bound to FakeMarket")
        self.logger.info("Subscribed to ORDER_REQUEST events")
    
    def _unsubscribe_events(self) -> None:
        """Unsubscribe from events"""
        if self._order_handler:
            self.event_bus.unsubscribe(EventType.ORDER_REQUEST, self._order_handler)
    
    def _on_order_request(self, event: Event) -> None:
        """
        Handle ORDER_REQUEST event
        
        Blueprint requirement: log "would execute"
        """
        self._log_event(event)
        order = event.data or {}
        self.logger.info("would execute (routing to FakeMarket)")
        if self._fake_market:
            self._fake_market.process_order(order)
        else:
            # fallback: just publish as submitted
            self.logger.warning("FakeMarket not available; order ignored in stub mode")
