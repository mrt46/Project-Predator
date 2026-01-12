"""
PROJECT PREDATOR - FakeStrategy
Listens to MARKET_REGIME and emits ORDER_REQUEST (stub)
"""
import logging
import random
from typing import Optional
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry
from backend.interfaces.executor import OrderSide, OrderType


class FakeStrategy:
    """
    Fake strategy (STUB).
    
    Listens to MARKET_REGIME and sometimes emits ORDER_REQUEST.
    No real trading logic, only placeholder behavior.
    """
    def __init__(self, event_bus: EventBus, registry: Registry):
        self.event_bus = event_bus
        self.registry = registry
        self.logger = logging.getLogger(self.__class__.__name__)
        self._regime_handler: Optional = None
        self._running = False
        random.seed(1337)
        self.logger.info("FakeStrategy initialized (STUB)")

    def get_name(self) -> str:
        return self.__class__.__name__

    def start(self) -> bool:
        if self._running:
            self.logger.warning("FakeStrategy already running")
            return False
        self._running = True
        self._regime_handler = self._on_regime
        self.event_bus.subscribe(EventType.MARKET_REGIME, self._regime_handler)
        self.logger.info("FakeStrategy started (listening to MARKET_REGIME)")
        return True

    def stop(self) -> bool:
        if not self._running:
            self.logger.warning("FakeStrategy not running")
            return False
        self._running = False
        if self._regime_handler:
            self.event_bus.unsubscribe(EventType.MARKET_REGIME, self._regime_handler)
        self.logger.info("FakeStrategy stopped")
        return True

    def _on_regime(self, event: Event) -> None:
        """
        On MARKET_REGIME, optionally emit a fake ORDER_REQUEST.
        Probability-based unless force_signal=True in event data.
        """
        data = event.data or {}
        force = data.get("force_signal", False)
        should_emit = force or random.random() < 0.3
        self.logger.debug(f"Regime received: {data}, emit={should_emit}")
        if not should_emit:
            return

        order = {
            "symbol": data.get("symbol", "BTC/USD"),
            "side": OrderSide.BUY.value,
            "order_type": OrderType.MARKET.value,
            "quantity": 0.1,
            "price": data.get("source_price", 0.0),
            "fake": True
        }
        self.event_bus.publish(EventType.ORDER_REQUEST, order, source=self.get_name())
        self.logger.info("Emitted fake ORDER_REQUEST (stub)")
