"""
PROJECT PREDATOR - Executor Interface
Defines the contract for order execution
"""
from abc import ABC, abstractmethod
from typing import Any, Optional
from enum import Enum


class OrderSide(Enum):
    """Order side"""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    """Order type"""
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderStatus(Enum):
    """Order status"""
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class IExecutor(ABC):
    """Interface for order execution"""
    
    @abstractmethod
    def submit_order(self, order: Any) -> str:
        """
        Submit an order
        Args:
            order: Order object
        Returns: Order ID
        """
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order
        Args:
            order_id: Order identifier
        Returns: True if cancelled successfully
        """
        pass
    
    @abstractmethod
    def get_order_status(self, order_id: str) -> Optional[OrderStatus]:
        """
        Get order status
        Args:
            order_id: Order identifier
        Returns: OrderStatus or None
        """
        pass
