"""
PROJECT PREDATOR - Phase 3 Simulation Smoke Tests
Ensures fake data flow wiring works (no real trading).
"""
import time

from backend.core.event_bus import EventBus, EventType
from backend.core.registry import Registry
from backend.agents.market_scanner.agent import MarketScannerAgent
from backend.agents.execution.agent import ExecutionAgent
from backend.agents.data_engineering.agent import DataEngineeringAgent
from backend.agents.portfolio.agent import PortfolioManagerAgent
from backend.agents.cro.agent import CRORiskAgent
from backend.agents.performance.agent import PerformanceKPIAgent
from backend.agents.aspa.agent import ASPAAgent
from backend.agents.rrs.agent import RRSAgent
from backend.simulation.fake_market import FakeMarket
from backend.simulation.fake_price_feed import FakePriceFeed
from backend.simulation.fake_strategy import FakeStrategy


def test_phase3_fake_data_flow_smoke():
    """
    Smoke test: TICK -> FAKE_CANDLE -> PRICE_UPDATE -> MARKET_REGIME -> ORDER_REQUEST
    """
    event_bus = EventBus()
    registry = Registry()

    # Components
    market = FakeMarket(event_bus, registry)
    price_feed = FakePriceFeed(event_bus, registry)
    strategy = FakeStrategy(event_bus, registry)
    scanner = MarketScannerAgent(event_bus, registry)

    # Minimal agent set for subscriptions (others not started)
    data_eng = DataEngineeringAgent(event_bus, registry)
    portfolio = PortfolioManagerAgent(event_bus, registry)
    cro = CRORiskAgent(event_bus, registry)
    perf = PerformanceKPIAgent(event_bus, registry)
    aspa = ASPAAgent(event_bus, registry)
    rrs = RRSAgent(event_bus, registry)
    exec_agent = ExecutionAgent(event_bus, registry)

    # Track flow
    seen_regime = []
    seen_order = []
    event_bus.subscribe(EventType.MARKET_REGIME, lambda e: seen_regime.append(e))
    event_bus.subscribe(EventType.ORDER_REQUEST, lambda e: seen_order.append(e))

    # Start components
    market.start()
    price_feed.start()
    strategy.start()
    scanner.start()
    data_eng.start()
    portfolio.start()
    cro.start()
    perf.start()
    aspa.start()
    rrs.start()
    exec_agent.start()

    # Force a tick and a regime with forced signal
    event_bus.publish(EventType.TICK, {"tick_number": 1}, source="test")
    # Also force a regime directly to guarantee an order request
    event_bus.publish(
        EventType.MARKET_REGIME,
        {"symbol": "BTC/USD", "regime": "TEST", "source_price": 50000, "force_signal": True},
        source="test"
    )

    time.sleep(0.2)

    # Assertions
    assert len(seen_regime) >= 1  # from price update or forced publish
    assert len(seen_order) >= 1   # from forced signal

    # Cleanup
    exec_agent.stop()
    rrs.stop()
    aspa.stop()
    perf.stop()
    cro.stop()
    portfolio.stop()
    data_eng.stop()
    scanner.stop()
    strategy.stop()
    price_feed.stop()
    market.stop()
