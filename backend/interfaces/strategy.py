"""
PROJECT PREDATOR - Strategy Interface
Defines the contract for all trading strategies
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional


class StrategyClass(Enum):
    """Strategy classification"""
    CORE = "CORE"
    AGGRESSIVE = "AGGRESSIVE"
    TAIL_RISK = "TAIL_RISK"


class IStrategy(ABC):
    """Interface for all trading strategies"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Get strategy name"""
        pass
    
    @abstractmethod
    def get_class(self) -> StrategyClass:
        """Get strategy classification"""
        pass
    
    @abstractmethod
    def on_tick(self, market_data: Any) -> Optional[Any]:
        """
        Process market tick
        Args:
            market_data: Market data event
        Returns: Optional signal
        """
        pass
    
    @abstractmethod
    def get_score(self) -> float:
        """
        Get current strategy score
        Returns: Score between 0.0 and 1.0
        """
        pass
