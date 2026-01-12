"""
PROJECT PREDATOR - OrderBookStub
Simple fill logic for fake execution.
"""
from typing import Dict
from backend.market.candle import Candle


class OrderBookStub:
    """
    Extremely simple orderbook model:
    - Fills at provided price (or candle close).
    - Optional slippage_percent.
    """
    def __init__(self, slippage_percent: float = 0.0):
        self.slippage_percent = max(slippage_percent, 0.0)

    def fill_order(self, order: Dict, last_candle: Candle) -> Dict:
        price = order.get("price") or last_candle.close
        slip = price * self.slippage_percent / 100.0
        if order.get("side") == "BUY":
            price = price + slip
        elif order.get("side") == "SELL":
            price = price - slip
        return {
            "order_id": order.get("order_id"),
            "symbol": order.get("symbol", "BTC/USD"),
            "side": order.get("side"),
            "quantity": order.get("quantity", 0.0),
            "price": price,
            "status": "FILLED",
            "fake": True,
        }
