"""
PROJECT PREDATOR - PortfolioManagerAgent
FAZ 2: Agent skeleton - NO REAL LOGIC
"""
from backend.agents.base import BaseAgent
from backend.core.event_bus import EventBus, EventType, Event
from backend.core.registry import Registry


class PortfolioManagerAgent(BaseAgent):
    """
    Portfolio Manager Agent (FAZ 3 - Fake PnL)
    
    Responsibilities:
    - On ORDER_FILLED -> update positions, realized PnL
    - On PRICE_UPDATE -> update unrealized PnL
    - Publish POSITION_UPDATE
    """
    
    def __init__(self, event_bus: EventBus, registry: Registry):
        super().__init__(event_bus, registry)
        self._fill_handler = None
        self._price_handler = None
        self._positions = {}  # symbol -> {"qty": float, "avg_cost": float, "last_price": float}
        self._realized = 0.0
        self.logger.info("PortfolioManagerAgent initialized (FAKE PnL)")
    
    def _subscribe_events(self) -> None:
        """Subscribe to ORDER_FILLED and PRICE_UPDATE"""
        self._fill_handler = self._on_fill
        self._price_handler = self._on_price_update
        self.event_bus.subscribe(EventType.ORDER_FILLED, self._fill_handler)
        self.event_bus.subscribe(EventType.PRICE_UPDATE, self._price_handler)
        self.logger.info("Subscribed to ORDER_FILLED and PRICE_UPDATE")
    
    def _unsubscribe_events(self) -> None:
        """Unsubscribe from events"""
        if self._fill_handler:
            self.event_bus.unsubscribe(EventType.ORDER_FILLED, self._fill_handler)
        if self._price_handler:
            self.event_bus.unsubscribe(EventType.PRICE_UPDATE, self._price_handler)
    
    def _on_fill(self, event: Event) -> None:
        """Handle ORDER_FILLED to update positions and realized PnL"""
        self._log_event(event)
        data = event.data or {}
        symbol = data.get("symbol", "UNKNOWN")
        side = data.get("side")
        qty = float(data.get("quantity", 0.0))
        price = float(data.get("price", 0.0))
        pos = self._positions.get(symbol, {"qty": 0.0, "avg_cost": 0.0, "last_price": price})
        old_qty = pos["qty"]
        avg = pos["avg_cost"]
        
        if side == "BUY":
            new_qty = old_qty + qty
            if new_qty != 0:
                new_avg = (avg * old_qty + price * qty) / new_qty
            else:
                new_avg = 0.0
            pos["qty"] = new_qty
            pos["avg_cost"] = new_avg
        elif side == "SELL":
            # Realized PnL on sold quantity
            sell_qty = qty
            self._realized += (price - avg) * sell_qty
            new_qty = old_qty - sell_qty
            pos["qty"] = new_qty
            if new_qty == 0:
                pos["avg_cost"] = 0.0
        else:
            self.logger.warning("Unknown side in fill")
        
        pos["last_price"] = price
        self._positions[symbol] = pos
        self._publish_position(symbol)
    
    def _on_price_update(self, event: Event) -> None:
        """Update unrealized PnL with latest price"""
        data = event.data or {}
        symbol = data.get("symbol", "UNKNOWN")
        price = float(data.get("price", 0.0))
        pos = self._positions.get(symbol)
        if not pos:
            return
        pos["last_price"] = price
        self._positions[symbol] = pos
        self._publish_position(symbol)
    
    def _publish_position(self, symbol: str) -> None:
        pos = self._positions.get(symbol, {"qty": 0.0, "avg_cost": 0.0, "last_price": 0.0})
        qty = pos["qty"]
        avg = pos["avg_cost"]
        price = pos["last_price"]
        unrealized = qty * (price - avg)
        snapshot = {
            "symbol": symbol,
            "qty": qty,
            "avg_cost": avg,
            "last_price": price,
            "unrealized": unrealized,
            "realized": self._realized,
            "fake": True,
        }
        self.event_bus.publish(EventType.POSITION_UPDATE, snapshot, source=self.get_name())
        self.logger.debug(f"POSITION_UPDATE {snapshot}")
    
    def get_equity(self) -> float:
        total = self._realized
        for symbol, pos in self._positions.items():
            total += pos["qty"] * (pos["last_price"] - pos["avg_cost"])
        return total
    def get_portfolio_state(self) -> dict:
        """Get full portfolio state for backtest reporting"""
        unrealized = 0.0
        for symbol, pos in self._positions.items():
            unrealized += pos["qty"] * (pos["last_price"] - pos["avg_cost"])
        return {
            "total_equity": self._realized + unrealized,
            "realized_pnl": self._realized,
            "unrealized_pnl": unrealized,
            "positions": {k: v.copy() for k, v in self._positions.items()}
        }

