"""
PROJECT PREDATOR - FakeStrategyTrend
Simple moving-average cross for flow testing (stub).
"""
from collections import deque
from typing import Optional, Dict
from backend.strategies.base import StrategyBase
from backend.interfaces.executor import OrderSide, OrderType


class FakeStrategyTrend(StrategyBase):
    def __init__(self, event_bus, fast: int = 3, slow: int = 8):
        super().__init__(event_bus)
        self.fast = fast
        self.slow = slow
        self.fast_q = deque(maxlen=fast)
        self.slow_q = deque(maxlen=slow)
        self.last_signal = None

    def _avg(self, q):
        return sum(q) / len(q) if q else 0.0

    def on_candle(self, candle: Dict) -> Optional[Dict]:
        close = candle.get("close", 0.0)
        self.fast_q.append(close)
        self.slow_q.append(close)
        if len(self.fast_q) < self.fast or len(self.slow_q) < self.slow:
            return None

        fast_ma = self._avg(self.fast_q)
        slow_ma = self._avg(self.slow_q)

        if fast_ma > slow_ma and self.last_signal != "LONG":
            self.last_signal = "LONG"
            return {
                "symbol": "BTC/USD",
                "side": OrderSide.BUY.value,
                "order_type": OrderType.MARKET.value,
                "quantity": 0.1,
                "price": close,
                "fake": True,
            }
        if fast_ma < slow_ma and self.last_signal != "SHORT":
            self.last_signal = "SHORT"
            return {
                "symbol": "BTC/USD",
                "side": OrderSide.SELL.value,
                "order_type": OrderType.MARKET.value,
                "quantity": 0.1,
                "price": close,
                "fake": True,
            }
        return None
