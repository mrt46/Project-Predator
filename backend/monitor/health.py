"""
PROJECT PREDATOR - Health Check
FastAPI health endpoint
"""
import logging
from fastapi import FastAPI
from typing import Optional


class HealthMonitor:
    """
    Health check monitor
    
    Provides /health endpoint for system monitoring.
    """
    
    def __init__(self, core_engine):
        """
        Initialize HealthMonitor
        
        Args:
            core_engine: Reference to CoreEngine
        """
        self.logger = logging.getLogger(__name__)
        self.core_engine = core_engine
        self.app = FastAPI(title="PROJECT PREDATOR Health API")
        
        # Register routes
        @self.app.get("/health")
        async def health():
            """Health check endpoint"""
            return self.core_engine.health_check()
        
        @self.app.get("/")
        async def root():
            """Root endpoint"""
            return {
                "name": "PROJECT PREDATOR",
                "version": "0.2.0-faz2",
                "status": self.core_engine.get_state().value
            }
        
        self.logger.info("HealthMonitor initialized")
    
    def get_app(self):
        """Get FastAPI app"""
        return self.app
