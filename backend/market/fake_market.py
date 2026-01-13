"""
PROJECT PREDATOR - FakeMarket
Listens to ORDER_REQUEST and produces fake ORDER_FILLED via OrderBookStub.
Owns FakePriceFeed for price updates.
"""
import logging
import uuid
from typing import Optional, Dict

from backend.core.event_bus import EventBus, EventType, Event
from backend.market.orderbook_stub import OrderBookStub
from backend.market.fake_price_feed import FakePriceFeed
from backend.market.candle import Candle


class FakeMarket:
    """
    Minimal fake market:
    - Subscribes to ORDER_REQUEST
    - Uses last candle price to fill orders
    - Publishes ORDER_FILLED
    """
    def __init__(self, event_bus: EventBus, slippage_percent: float = 0.0):
        self.event_bus = event_bus
        self.orderbook = OrderBookStub(slippage_percent)
        self.price_feed = FakePriceFeed(event_bus)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._last_candle: Optional[Candle] = None
        self._running = False
        self.logger.info("FakeMarket initialized (STUB)")

    def get_name(self) -> str:
        return self.__class__.__name__

    def start(self) -> bool:
        if self._running:
            self.logger.warning("FakeMarket already running")
            return False
        self._running = True
        self.price_feed.start()
        self.logger.info("FakeMarket started")
        return True

    def stop(self) -> bool:
        if not self._running:
            self.logger.warning("FakeMarket not running")
            return False
        self._running = False
        self.price_feed.stop()
        self.logger.info("FakeMarket stopped")
        return True

    def process_order(self, order: Dict) -> None:
        """
        Process order and emit ORDER_FILLED + EXECUTION_RESULT.
        """
        order = dict(order or {})
        if "order_id" not in order:
            order["order_id"] = str(uuid.uuid4())
        candle_data = {"close": order.get("price", 0.0)}
        if self.price_feed._last_candle:
            candle_data = self.price_feed._last_candle.to_dict()
        candle = Candle(
            timestamp=candle_data.get("timestamp", 0.0),
            open=candle_data.get("open", candle_data.get("close", 0.0)),
            high=candle_data.get("high", candle_data.get("close", 0.0)),
            low=candle_data.get("low", candle_data.get("close", 0.0)),
            close=candle_data.get("close", 0.0),
            volume=candle_data.get("volume", 0.0),
        )
        fill = self.orderbook.fill_order(order, candle)
        self.event_bus.publish(EventType.ORDER_FILLED, fill, source=self.get_name())
        self.event_bus.publish(EventType.EXECUTION_RESULT, fill, source=self.get_name())
        self.logger.info(f"Filled fake order {order.get('order_id')} at {fill['price']}")
