"""
PROJECT PREDATOR - FakePriceFeed
Transforms FAKE_CANDLE into PRICE_UPDATE events (Phase 3)
"""
import logging
from typing import Optional
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry


class FakePriceFeed:
    """
    Fake price feed (stub).
    
    Listens to FAKE_CANDLE and publishes PRICE_UPDATE.
    """
    def __init__(self, event_bus: EventBus, registry: Registry):
        self.event_bus = event_bus
        self.registry = registry
        self.logger = logging.getLogger(self.__class__.__name__)
        self._candle_handler: Optional = None
        self._running = False
        self.logger.info("FakePriceFeed initialized (STUB)")

    def get_name(self) -> str:
        return self.__class__.__name__

    def start(self) -> bool:
        if self._running:
            self.logger.warning("FakePriceFeed already running")
            return False
        self._running = True
        self._candle_handler = self._on_candle
        self.event_bus.subscribe(EventType.FAKE_CANDLE, self._candle_handler)
        self.logger.info("FakePriceFeed started (listening to FAKE_CANDLE)")
        return True

    def stop(self) -> bool:
        if not self._running:
            self.logger.warning("FakePriceFeed not running")
            return False
        self._running = False
        if self._candle_handler:
            self.event_bus.unsubscribe(EventType.FAKE_CANDLE, self._candle_handler)
        self.logger.info("FakePriceFeed stopped")
        return True

    def _on_candle(self, event: Event) -> None:
        data = event.data or {}
        price_update = {
            "symbol": data.get("symbol", "BTC/USD"),
            "price": data.get("close", 0.0),
            "source": "FakePriceFeed",
            "fake": True
        }
        self.event_bus.publish(EventType.PRICE_UPDATE, price_update, source=self.get_name())
        self.logger.debug(f"Published PRICE_UPDATE: {price_update}")
