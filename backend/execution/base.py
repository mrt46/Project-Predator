"""
PROJECT PREDATOR - Base Executor
Base classes for order execution
"""
from dataclasses import dataclass
from backend.interfaces.executor import OrderSide, OrderType, OrderStatus


@dataclass
class Order:
    """Order data structure"""
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: float = 0.0  # For limit orders
    order_id: str = ""
    status: OrderStatus = OrderStatus.PENDING
