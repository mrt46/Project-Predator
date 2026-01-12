"""
PROJECT PREDATOR - Configuration
Central configuration loader
"""
import os
import logging
from typing import Optional
from dotenv import load_dotenv


class Config:
    """
    Central configuration
    
    Loads from environment variables.
    No secrets in repo.
    """
    
    def __init__(self):
        # Load .env if it exists
        load_dotenv()
        
        # System
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        
        # Core Engine
        self.SCHEDULER_TICK_INTERVAL = float(os.getenv("SCHEDULER_TICK_INTERVAL", "1.0"))
        self.HEARTBEAT_INTERVAL = float(os.getenv("HEARTBEAT_INTERVAL", "5.0"))
        
        # Policy Guard
        self.GLOBAL_KILL_SWITCH = os.getenv("GLOBAL_KILL_SWITCH", "false").lower() == "true"
        self.MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "0.0"))
        self.MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "0.0"))
        
        # Monitoring
        self.HEALTH_CHECK_PORT = int(os.getenv("HEALTH_CHECK_PORT", "8000"))
        self.METRICS_ENABLED = os.getenv("METRICS_ENABLED", "true").lower() == "true"
        
        # Phase Control
        self.CURRENT_PHASE = int(os.getenv("CURRENT_PHASE", "2"))
        self.ALLOW_REAL_EXCHANGE = os.getenv("ALLOW_REAL_EXCHANGE", "false").lower() == "true"
        self.ALLOW_REAL_TRADING = os.getenv("ALLOW_REAL_TRADING", "false").lower() == "true"
    
    def validate(self) -> bool:
        """
        Validate configuration
        
        Enforces phase boundaries and governance rules.
        """
        logger = logging.getLogger(__name__)
        
        # Phase 2 validation
        if self.CURRENT_PHASE <= 2:
            if self.ALLOW_REAL_EXCHANGE:
                logger.error("INVALID CONFIG: Real exchange not allowed in Phase 2")
                return False
            if self.ALLOW_REAL_TRADING:
                logger.error("INVALID CONFIG: Real trading not allowed in Phase 2")
                return False
        
        logger.info(f"Configuration valid (Phase {self.CURRENT_PHASE})")
        return True


# Global config instance
config = Config()
