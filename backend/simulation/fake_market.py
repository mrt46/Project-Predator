"""
PROJECT PREDATOR - FakeMarket
Generates fake candles on TICK events (Phase 3 simulation)
"""
import logging
import random
from typing import Optional
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry


class FakeMarket:
    """
    Fake market data generator (stub).
    
    Listens to TICK and publishes FAKE_CANDLE.
    """
    def __init__(self, event_bus: EventBus, registry: Registry):
        self.event_bus = event_bus
        self.registry = registry
        self.logger = logging.getLogger(self.__class__.__name__)
        self._tick_handler: Optional = None
        self._running = False
        self.logger.info("FakeMarket initialized (STUB)")

    def get_name(self) -> str:
        return self.__class__.__name__

    def start(self) -> bool:
        if self._running:
            self.logger.warning("FakeMarket already running")
            return False
        self._running = True
        self._tick_handler = self._on_tick
        self.event_bus.subscribe(EventType.TICK, self._tick_handler)
        self.logger.info("FakeMarket started (listening to TICK)")
        return True

    def stop(self) -> bool:
        if not self._running:
            self.logger.warning("FakeMarket not running")
            return False
        self._running = False
        if self._tick_handler:
            self.event_bus.unsubscribe(EventType.TICK, self._tick_handler)
        self.logger.info("FakeMarket stopped")
        return True

    def _on_tick(self, event: Event) -> None:
        """
        On each TICK publish a fake candle (stub/random).
        """
        price = round(50000.0 + random.uniform(-150, 150), 2)
        candle = {
            "symbol": "BTC/USD",
            "open": price,
            "high": price + random.uniform(0, 50),
            "low": price - random.uniform(0, 50),
            "close": price + random.uniform(-25, 25),
            "volume": round(random.uniform(1, 20), 4),
            "tick_number": event.data.get("tick_number", 0),
            "fake": True,
        }
        self.event_bus.publish(EventType.FAKE_CANDLE, candle, source=self.get_name())
        self.logger.debug(f"Published FAKE_CANDLE: {candle}")
