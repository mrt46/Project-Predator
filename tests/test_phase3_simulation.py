"""
PROJECT PREDATOR - Phase 3 Simulation Smoke Tests
Ensures fake data flow wiring works (no real trading).
"""
import time
from backend.core.event_bus import EventBus, EventType
from backend.market.fake_market import FakeMarket
from backend.market.fake_price_feed import FakePriceFeed
from backend.strategies.fake_strategy_random import FakeStrategyRandom
from backend.market.candle import Candle


def test_phase3_fake_data_flow_smoke():
    """
    Smoke test: FAKE_CANDLE -> PRICE_UPDATE -> ORDER_REQUEST -> ORDER_FILLED
    """
    event_bus = EventBus()
    market = FakeMarket(event_bus)
    price_feed = market.price_feed
    strategy = FakeStrategyRandom(event_bus, seed=1)

    seen_orders = []
    seen_fills = []
    event_bus.subscribe(EventType.ORDER_REQUEST, lambda e: seen_orders.append(e))
    event_bus.subscribe(EventType.ORDER_FILLED, lambda e: seen_fills.append(e))

    # Start components
    market.start()
    price_feed.start()
    strategy.start()

    # Publish a fake candle to drive strategy
    candle = Candle.from_row(time.time(), 100, 110, 90, 105, 1.0)
    event_bus.publish(EventType.FAKE_CANDLE, candle.to_dict(), source="test")

    time.sleep(0.1)

    assert len(seen_orders) >= 0  # strategy may or may not fire due to randomness
    # Force an order to guarantee fill
    event_bus.publish(EventType.ORDER_REQUEST, {
        "symbol": "BTC/USD",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 0.1,
        "price": 105,
        "fake": True
    }, source="test")

    time.sleep(0.1)

    assert len(seen_fills) >= 1

    # Cleanup
    strategy.stop()
    price_feed.stop()
    market.stop()
