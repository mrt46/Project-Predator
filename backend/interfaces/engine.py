"""
PROJECT PREDATOR - Engine Interface
Defines the contract for all engines in the system
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class EngineState(Enum):
    """Engine lifecycle states"""
    INIT = "INIT"
    BOOTING = "BOOTING"
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    HALTED = "HALTED"
    ERROR = "ERROR"


class IEngine(ABC):
    """Interface for all engines in the platform"""
    
    @abstractmethod
    def start(self) -> bool:
        """
        Start the engine
        Returns: True if started successfully
        """
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """
        Stop the engine
        Returns: True if stopped successfully
        """
        pass
    
    @abstractmethod
    def get_state(self) -> EngineState:
        """
        Get current engine state
        Returns: Current EngineState
        """
        pass
    
    @abstractmethod
    def health_check(self) -> dict:
        """
        Perform health check
        Returns: Dictionary with health status
        """
        pass
