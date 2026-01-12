"""
PROJECT PREDATOR - BaseAgent
Base class for all agents
"""
import logging
from typing import Any
from backend.interfaces.agent import IAgent
from backend.core.event_bus import EventBus
from backend.core.registry import Registry


class BaseAgent(IAgent):
    """
    Base agent implementation
    
    All agents inherit from this class.
    Provides common functionality for event subscription and lifecycle.
    """
    
    def __init__(self, event_bus: EventBus, registry: Registry):
        """
        Initialize base agent
        
        Args:
            event_bus: Reference to EventBus
            registry: Reference to Registry
        """
        self.event_bus = event_bus
        self.registry = registry
        self.logger = logging.getLogger(self.__class__.__name__)
        self._running = False
        self._event_count = 0
    
    def start(self) -> bool:
        """
        Start the agent
        
        Subclasses should override _subscribe_events() to subscribe to events.
        """
        if self._running:
            self.logger.warning(f"{self.get_name()} already running")
            return False
        
        self._running = True
        self._subscribe_events()
        self.logger.info(f"{self.get_name()} started")
        return True
    
    def stop(self) -> bool:
        """
        Stop the agent
        
        Subclasses should override _unsubscribe_events() to clean up.
        """
        if not self._running:
            self.logger.warning(f"{self.get_name()} not running")
            return False
        
        self._running = False
        self._unsubscribe_events()
        self.logger.info(f"{self.get_name()} stopped")
        return True
    
    def get_name(self) -> str:
        """Get agent name"""
        return self.__class__.__name__
    
    def health_check(self) -> dict:
        """Perform health check"""
        return {
            "name": self.get_name(),
            "running": self._running,
            "events_processed": self._event_count
        }
    
    def _subscribe_events(self) -> None:
        """
        Subscribe to events
        
        Override in subclasses to subscribe to specific events.
        """
        pass
    
    def _unsubscribe_events(self) -> None:
        """
        Unsubscribe from events
        
        Override in subclasses to clean up subscriptions.
        """
        pass
    
    def _log_event(self, event: Any) -> None:
        """
        Log event receipt
        
        Args:
            event: Event object
        """
        self._event_count += 1
        self.logger.debug(f"Received {event.event_type.value} from {event.source}")
