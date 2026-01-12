"""
PROJECT PREDATOR - CapitalManager Stub
Manages capital allocation (STUB - no real logic)
"""
import logging


class CapitalManager:
    """
    Capital allocation manager (STUB)
    
    Phase 2: Returns dummy allocations.
    Real capital management will be added in future phases.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._total_capital = 0.0  # No real capital
        self.logger.info("CapitalManager initialized (STUB)")
    
    def allocate_to_strategy(self, strategy_name: str) -> float:
        """
        Allocate capital to strategy (STUB)
        
        Args:
            strategy_name: Strategy name
        
        Returns:
            Allocated capital (always 0.0)
        """
        self.logger.debug(f"Allocating capital to {strategy_name} (STUB)")
        return 0.0  # No real capital
    
    def get_total_capital(self) -> float:
        """Get total capital (STUB)"""
        return self._total_capital
