"""
PROJECT PREDATOR - FakePriceFeed
Transforms Candle into PRICE_UPDATE and FAKE_CANDLE events.
"""
import logging
from typing import Optional
from backend.core.event_bus import EventBus, EventType, Event
from backend.market.candle import Candle


class FakePriceFeed:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.logger = logging.getLogger(self.__class__.__name__)
        self._candle_handler: Optional = None
        self._running = False
        self._last_candle: Optional[Candle] = None
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
        candle = Candle(
            timestamp=data.get("timestamp", 0.0),
            open=data.get("open", 0.0),
            high=data.get("high", 0.0),
            low=data.get("low", 0.0),
            close=data.get("close", 0.0),
            volume=data.get("volume", 0.0),
        )
        self._last_candle = candle

        # Publish price update
        price_update = {
            "symbol": "BTC/USD",
            "price": candle.close,
            "timestamp": candle.timestamp,
            "fake": True,
        }
        self.event_bus.publish(EventType.PRICE_UPDATE, price_update, source=self.get_name())
        # Also publish canonical candle event
        self.event_bus.publish(EventType.CANDLE_EVENT, data, source=self.get_name())
        self.logger.debug(f"Published PRICE_UPDATE {price_update}")
