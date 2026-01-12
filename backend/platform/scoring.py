"""
PROJECT PREDATOR - ScoringEngine Stub
Scores strategies (STUB - no real logic)
"""
import logging


class ScoringEngine:
    """
    Strategy scoring engine (STUB)
    
    Phase 2: Returns dummy scores.
    Real scoring logic will be added in future phases.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("ScoringEngine initialized (STUB)")
    
    def score_strategy(self, strategy_name: str) -> float:
        """
        Score a strategy (STUB)
        
        Args:
            strategy_name: Strategy name
        
        Returns:
            Dummy score (always 0.5)
        """
        self.logger.debug(f"Scoring strategy {strategy_name} (STUB)")
        return 0.5  # Dummy score
    
    def get_all_scores(self) -> dict:
        """Get all strategy scores (STUB)"""
        return {"stub": 0.5}
