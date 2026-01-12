"""
PROJECT PREDATOR - FakeStrategyRandom
Random buy/sell/do-nothing for flow testing.
"""
import random
from typing import Optional, Dict
from backend.strategies.base import StrategyBase
from backend.interfaces.executor import OrderSide, OrderType


class FakeStrategyRandom(StrategyBase):
    def __init__(self, event_bus, seed: int = 1337):
        super().__init__(event_bus)
        random.seed(seed)

    def on_candle(self, candle: Dict) -> Optional[Dict]:
        r = random.random()
        if r < 0.33:
            side = OrderSide.BUY.value
        elif r < 0.66:
            side = OrderSide.SELL.value
        else:
            return None
        return {
            "symbol": "BTC/USD",
            "side": side,
            "order_type": OrderType.MARKET.value,
            "quantity": 0.1,
            "price": candle.get("close", 0.0),
            "fake": True,
        }
