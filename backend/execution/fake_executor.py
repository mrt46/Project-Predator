"""
PROJECT PREDATOR - FakeExecutor
Simulated order execution (NO real exchange connection)
"""
import logging
import uuid
from typing import Dict, Optional
from backend.interfaces.executor import IExecutor, OrderStatus
from backend.execution.base import Order
from backend.core.event_bus import EventBus, EventType


class FakeExecutor(IExecutor):
    """
    Fake order executor
    
    Simulates order execution without touching real markets.
    
    Phase 2: This is a STUB.
    - Immediately "fills" all orders
    - Publishes fake events
    - NO real exchange connection
    """
    
    def __init__(self, event_bus: EventBus):
        """
        Initialize FakeExecutor
        
        Args:
            event_bus: EventBus instance
        """
        self.logger = logging.getLogger(__name__)
        self.event_bus = event_bus
        self._orders: Dict[str, Order] = {}
        self.logger.info("FakeExecutor initialized (STUB - no real execution)")
    
    def submit_order(self, order: Order) -> str:
        """
        Submit a fake order
        
        Args:
            order: Order object
        
        Returns:
            Order ID
        """
        # Generate order ID
        order.order_id = str(uuid.uuid4())
        order.status = OrderStatus.SUBMITTED
        
        self._orders[order.order_id] = order
        
        self.logger.info(f"FAKE ORDER SUBMITTED: {order.symbol} {order.side.value} {order.quantity} @ {order.price}")
        
        # Publish submitted event
        self.event_bus.publish(
            EventType.ORDER_SUBMITTED,
            {
                "order_id": order.order_id,
                "symbol": order.symbol,
                "side": order.side.value,
                "quantity": order.quantity
            },
            source="FakeExecutor"
        )
        
        # Immediately "fill" the order (fake)
        self._fake_fill(order)
        
        return order.order_id
    
    def _fake_fill(self, order: Order) -> None:
        """
        Fake fill the order
        
        Args:
            order: Order object
        """
        order.status = OrderStatus.FILLED
        
        self.logger.info(f"FAKE ORDER FILLED: {order.order_id}")
        
        # Publish filled event
        self.event_bus.publish(
            EventType.ORDER_FILLED,
            {
                "order_id": order.order_id,
                "symbol": order.symbol,
                "side": order.side.value,
                "quantity": order.quantity,
                "price": order.price,
                "fake": True
            },
            source="FakeExecutor"
        )
    
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel a fake order
        
        Args:
            order_id: Order identifier
        
        Returns:
            True if cancelled successfully
        """
        if order_id not in self._orders:
            self.logger.warning(f"Order {order_id} not found")
            return False
        
        order = self._orders[order_id]
        order.status = OrderStatus.CANCELLED
        
        self.logger.info(f"FAKE ORDER CANCELLED: {order_id}")
        return True
    
    def get_order_status(self, order_id: str) -> Optional[OrderStatus]:
        """
        Get order status
        
        Args:
            order_id: Order identifier
        
        Returns:
            OrderStatus or None
        """
        if order_id not in self._orders:
            return None
        
        return self._orders[order_id].status
    
    def get_stats(self) -> dict:
        """Get executor statistics"""
        return {
            "total_orders": len(self._orders),
            "mode": "FAKE",
            "real_execution": False
        }
