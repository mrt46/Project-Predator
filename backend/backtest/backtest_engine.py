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
    def __init__(self, candles: List[Candle], strategy_name: str = "fake_trend", speed: float = 100.0, seed: int = 1337, emit_ticks: bool = False, deterministic: bool = False):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.event_bus = EventBus()
        self.registry = Registry()
        self.time_source = TimeSource(speed=speed)
        self.replayer = HistoricalReplayer(self.event_bus, self.time_source, emit_ticks=emit_ticks, deterministic=deterministic)
        self.market = FakeMarket(self.event_bus)
        self.strategy = self._build_strategy(strategy_name, seed)
        self.execution = ExecutionAgent(self.event_bus, self.registry)
        self.portfolio = PortfolioManagerAgent(self.event_bus, self.registry)
        self.trades: List[Dict[str, Any]] = []
        self.equity_curve: List[Dict[str, Any]] = []
        self._last_price = 0.0
        self.seed = seed
        # register components for lookup
        self.registry.register("FakeMarket", self.market)
        self.registry.register("ExecutionAgent", self.execution)
        self.registry.register("PortfolioManagerAgent", self.portfolio)
        # collect fills
        self.event_bus.subscribe(EventType.ORDER_FILLED, self._on_fill)
        # track price updates for equity curve
        self.event_bus.subscribe(EventType.PRICE_UPDATE, self._on_price)
        self.candles = candles
        self.logger.info(f"BacktestEngine initialized (strategy={strategy_name}, speed={speed}, seed={seed})")

    def _build_strategy(self, name: str, seed: int):
        if name == "fake_random":
            return FakeStrategyRandom(self.event_bus, seed=seed)
        return FakeStrategyTrend(self.event_bus)

    def run(self) -> Dict[str, Any]:
        self.logger.info(f"Starting backtest with {len(self.candles)} candles, strategy={self.strategy.get_name()}")
        self.market.start()
        self.execution.start()
        self.portfolio.start()
        self.strategy.start()
        # Replayer emits FAKE_CANDLE; FakePriceFeed inside FakeMarket re-publishes PRICE_UPDATE/CANDLE_EVENT
        self.replayer.replay_with_spacing(self.candles)
        # Final equity snapshot
        final_state = self.portfolio.get_portfolio_state()
        self.strategy.stop()
        self.portfolio.stop()
        self.execution.stop()
        self.market.stop()
        
        # Calculate final metrics
        from backend.backtest.backtest_report import BacktestReport
        report = BacktestReport.summarize(self.trades, self.equity_curve)
        
        return {
            "trades": self.trades,
            "equity_curve": self.equity_curve,
            "total_return": report["total_return"],
            "num_trades": report["num_trades"],
            "winrate": report["winrate"],
            "max_drawdown": report["max_drawdown"],
            "final_equity": final_state.get("total_equity", 0.0),
            "final_realized_pnl": final_state.get("realized_pnl", 0.0),
            "final_unrealized_pnl": final_state.get("unrealized_pnl", 0.0),
        }

    def _on_fill(self, event):
        data = event.data or {}
        self.trades.append(data)

    def _on_price(self, event):
        data = event.data or {}
        self._last_price = data.get("price", self._last_price)
        # Get equity from portfolio (includes realized + unrealized PnL)
        portfolio_state = self.portfolio.get_portfolio_state()
        equity = portfolio_state.get("total_equity", 0.0)
        timestamp = data.get("timestamp", self.time_source.now())
        self.equity_curve.append({
            "timestamp": timestamp,
            "price": self._last_price,
            "equity": equity,
            "realized_pnl": portfolio_state.get("realized_pnl", 0.0),
            "unrealized_pnl": portfolio_state.get("unrealized_pnl", 0.0)
        })

