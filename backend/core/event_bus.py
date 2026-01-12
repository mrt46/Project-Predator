"""
PROJECT PREDATOR - EventBus
Central pub/sub event system for component communication
"""
import logging
from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventType(Enum):
    """System event types"""
    # System events
    SYSTEM_BOOT = "SYSTEM_BOOT"
    SYSTEM_SHUTDOWN = "SYSTEM_SHUTDOWN"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    HEARTBEAT = "HEARTBEAT"
    
    # Scheduler events
    TICK = "TICK"
    
    # Market data events (stub)
    MARKET_TICK = "MARKET_TICK"
    
    # Order events (stub)
    ORDER_REQUEST = "ORDER_REQUEST"
    ORDER_SUBMITTED = "ORDER_SUBMITTED"
    ORDER_FILLED = "ORDER_FILLED"
    ORDER_REJECTED = "ORDER_REJECTED"
    
    # Portfolio events (stub)
    POSITION_UPDATE = "POSITION_UPDATE"
    
    # Risk events (stub)
    RISK_CHECK = "RISK_CHECK"
    RISK_BREACH = "RISK_BREACH"
    KILL_SWITCH_ACTIVATED = "KILL_SWITCH_ACTIVATED"
    
    # Performance events (stub)
    PERFORMANCE_UPDATE = "PERFORMANCE_UPDATE"
    
    # Infrastructure events (stub)
    HEALTH_CHECK = "HEALTH_CHECK"
    METRIC_PUBLISHED = "METRIC_PUBLISHED"


@dataclass
class Event:
    """Event data structure"""
    event_type: EventType
    data: Any
    timestamp: datetime
    source: str


class EventBus:
    """
    Central event bus for pub/sub communication
    
    All components communicate via events, not direct calls.
    This ensures:
    - Loose coupling
    - Observability
    - Auditability
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._subscribers: Dict[EventType, List[Callable]] = {}
        self._event_count = 0
        self.logger.info("EventBus initialized")
    
    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        """
        Subscribe to an event type
        
        Args:
            event_type: Type of event to subscribe to
            handler: Callback function to handle the event
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        self._subscribers[event_type].append(handler)
        self.logger.info(f"Subscribed to {event_type.value}: {handler.__name__}")
    
    def unsubscribe(self, event_type: EventType, handler: Callable) -> None:
        """
        Unsubscribe from an event type
        
        Args:
            event_type: Type of event to unsubscribe from
            handler: Callback function to remove
        """
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(handler)
                self.logger.info(f"Unsubscribed from {event_type.value}: {handler.__name__}")
            except ValueError:
                self.logger.warning(f"Handler {handler.__name__} not found for {event_type.value}")
    
    def publish(self, event_type: EventType, data: Any, source: str = "unknown") -> None:
        """
        Publish an event
        
        Args:
            event_type: Type of event
            data: Event data
            source: Source component name
        """
        event = Event(
            event_type=event_type,
            data=data,
            timestamp=datetime.utcnow(),
            source=source
        )
        
        self._event_count += 1
        
        # Log critical events
        if event_type in [EventType.SYSTEM_ERROR, EventType.RISK_BREACH, 
                          EventType.KILL_SWITCH_ACTIVATED]:
            self.logger.warning(f"CRITICAL EVENT: {event_type.value} from {source}")
        
        # Notify all subscribers
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    self.logger.error(f"Error in event handler {handler.__name__}: {e}")
    
    def get_stats(self) -> dict:
        """Get EventBus statistics"""
        return {
            "total_events_published": self._event_count,
            "subscriber_count": sum(len(handlers) for handlers in self._subscribers.values()),
            "event_types_subscribed": len(self._subscribers)
        }
