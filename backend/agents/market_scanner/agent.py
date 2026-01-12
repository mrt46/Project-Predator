"""
PROJECT PREDATOR - MarketScannerAgent
FAZ 2: Agent skeleton - NO REAL LOGIC
"""
from backend.agents.base import BaseAgent
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry


class MarketScannerAgent(BaseAgent):
    """
    Market Scanner Agent (FAZ 2 - SKELETON)
    
    Responsibilities (Blueprint):
    - On Tick → log "scanning market"
    
    FAZ 2: NO intelligence, NO real scanning
    Just event subscription and logging.
    """
    
    def __init__(self, event_bus: EventBus, registry: Registry):
        super().__init__(event_bus, registry)
        self._tick_handler = None
        self._price_handler = None
        self.logger.info("MarketScannerAgent initialized (SKELETON)")
    
    def _subscribe_events(self) -> None:
        """Subscribe to TICK and PRICE_UPDATE events"""
        self._tick_handler = self._on_tick
        self._price_handler = self._on_price_update
        self.event_bus.subscribe(EventType.TICK, self._tick_handler)
        self.event_bus.subscribe(EventType.PRICE_UPDATE, self._price_handler)
        self.logger.info("Subscribed to TICK and PRICE_UPDATE events")
    
    def _unsubscribe_events(self) -> None:
        """Unsubscribe from events"""
        if self._tick_handler:
            self.event_bus.unsubscribe(EventType.TICK, self._tick_handler)
        if self._price_handler:
            self.event_bus.unsubscribe(EventType.PRICE_UPDATE, self._price_handler)
    
    def _on_tick(self, event: Event) -> None:
        """
        Handle TICK event
        
        Blueprint requirement: log "scanning market"
        """
        self._log_event(event)
        self.logger.debug("scanning market")

    def _on_price_update(self, event: Event) -> None:
        """
        Handle PRICE_UPDATE event (Phase 3 simulation path)
        
        Publishes a MARKET_REGIME event (stub) based on incoming price update.
        """
        self._log_event(event)
        data = event.data or {}
        regime = "RANGE"  # stub/placeholder regime
        self.event_bus.publish(
            EventType.MARKET_REGIME,
            {
                "symbol": data.get("symbol", "BTC/USD"),
                "regime": regime,
                "source_price": data.get("price"),
                "fake": True
            },
            source=self.get_name()
        )
        self.logger.debug(f"Published MARKET_REGIME: {regime}")
