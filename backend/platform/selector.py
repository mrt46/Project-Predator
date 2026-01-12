"""
PROJECT PREDATOR - StrategySelector Stub
Selects active strategy (STUB - no real logic)
"""
import logging


class StrategySelector:
    """
    Strategy selector (STUB)
    
    Phase 2: Returns dummy selection.
    Real selection logic will be added in future phases.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("StrategySelector initialized (STUB)")
    
    def select_strategy(self, scores: dict) -> str:
        """
        Select active strategy (STUB)
        
        Args:
            scores: Strategy scores
        
        Returns:
            Selected strategy name (always "stub")
        """
        self.logger.debug(f"Selecting strategy from {len(scores)} candidates (STUB)")
        return "stub"  # Dummy selection
