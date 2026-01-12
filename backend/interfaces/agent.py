"""
PROJECT PREDATOR - Agent Interface
Defines the contract for all agents in the system
"""
from abc import ABC, abstractmethod
from typing import Any


class IAgent(ABC):
    """Interface for all agents in the platform"""
    
    @abstractmethod
    def __init__(self, event_bus: Any, registry: Any):
        """
        Initialize agent with EventBus and Registry
        Args:
            event_bus: Reference to the EventBus
            registry: Reference to the Registry
        """
        pass
    
    @abstractmethod
    def start(self) -> bool:
        """
        Start the agent and subscribe to events
        Returns: True if started successfully
        """
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """
        Stop the agent and unsubscribe from events
        Returns: True if stopped successfully
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get agent name
        Returns: Agent name
        """
        pass
    
    @abstractmethod
    def health_check(self) -> dict:
        """
        Perform health check
        Returns: Dictionary with health status
        """
        pass
