"""
PROJECT PREDATOR - BacktestEngine
Wires replayer, fake market, strategy, portfolio skeleton.
"""
import logging
from typing import List, Dict, Any

from backend.core.event_bus import EventBus, EventType
from backend.core.registry import Registry
from backend.simulation.time_source import TimeSource
from backend.simulation.historical_replayer import HistoricalReplayer
from backend.market.fake_market import FakeMarket
from backend.market.candle import Candle
from backend.strategies.fake_strategy_random import FakeStrategyRandom
from backend.strategies.fake_strategy_trend import FakeStrategyTrend
from backend.agents.execution.agent import ExecutionAgent
from backend.agents.portfolio.agent import PortfolioManagerAgent


class BacktestEngine:
    """
    Minimal backtest orchestrator (stub).
    """
    def __init__(self, candles: List[Candle], strategy_name: str = "fake_trend", speed: float = 100.0, seed: int = 1337):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.event_bus = EventBus()
        self.registry = Registry()
        self.time_source = TimeSource(speed=speed)
        self.replayer = HistoricalReplayer(self.event_bus, self.time_source)
        self.market = FakeMarket(self.event_bus)
        self.strategy = self._build_strategy(strategy_name, seed)
        self.execution = ExecutionAgent(self.event_bus, self.registry)
        self.portfolio = PortfolioManagerAgent(self.event_bus, self.registry)
        self.trades: List[Dict[str, Any]] = []
        self.equity_curve: List[Dict[str, Any]] = []
        self._last_price = 0.0
        # register components for lookup
        self.registry.register("FakeMarket", self.market)
        self.registry.register("ExecutionAgent", self.execution)
        self.registry.register("PortfolioManagerAgent", self.portfolio)
        # collect fills
        self.event_bus.subscribe(EventType.ORDER_FILLED, self._on_fill)
        # track price updates for equity curve
        self.event_bus.subscribe(EventType.PRICE_UPDATE, self._on_price)
        self.candles = candles
        self.logger.info("BacktestEngine initialized")

    def _build_strategy(self, name: str, seed: int):
        if name == "fake_random":
            return FakeStrategyRandom(self.event_bus, seed=seed)
        return FakeStrategyTrend(self.event_bus)

    def run(self) -> Dict[str, Any]:
        self.logger.info("Starting backtest...")
        self.market.start()
        self.execution.start()
        self.portfolio.start()
        self.strategy.start()
        # Replayer emits FAKE_CANDLE; FakePriceFeed inside FakeMarket re-publishes PRICE_UPDATE/CANDLE_EVENT
        self.replayer.replay(self.candles)
        self.strategy.stop()
        self.portfolio.stop()
        self.execution.stop()
        self.market.stop()
        return {
            "trades": self.trades,
            "equity_curve": self.equity_curve,
            "total_return": self._total_return(),
            "num_trades": len(self.trades),
        }

    def _on_fill(self, event):
        data = event.data or {}
        self.trades.append(data)

    def _on_price(self, event):
        data = event.data or {}
        self._last_price = data.get("price", self._last_price)
        equity = self.portfolio.get_equity() if hasattr(self.portfolio, "get_equity") else self._last_price
        self.equity_curve.append({"price": self._last_price, "equity": equity})

    def _total_return(self) -> float:
        if not self.trades:
            return 0.0
        # simple sum of signed PnL stub
        pnl = 0.0
        for t in self.trades:
            qty = t.get("quantity", 0.0)
            price = t.get("price", 0.0)
            if t.get("side") == "BUY":
                pnl -= qty * price
            else:
                pnl += qty * price
        return pnl
