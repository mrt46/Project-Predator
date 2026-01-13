"""
PROJECT PREDATOR - Strategy Base
Simple interface + EventBus adapter.
"""
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict
from backend.core.event_bus import EventBus, EventType, Event


class StrategyBase(ABC):
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.logger = logging.getLogger(self.__class__.__name__)
        self._candle_handler: Optional = None
        self._running = False
    
    def get_name(self) -> str:
        """Get strategy name"""
        return self.__class__.__name__

    def start(self) -> bool:
        if self._running:
            self.logger.warning("Strategy already running")
            return False
        self._running = True
        self._candle_handler = self._on_candle_event
        self.event_bus.subscribe(EventType.CANDLE_EVENT, self._candle_handler)
        self.logger.info("Strategy started (listening to CANDLE_EVENT)")
        return True

    def stop(self) -> bool:
        if not self._running:
            self.logger.warning("Strategy not running")
            return False
        self._running = False
        if self._candle_handler:
            self.event_bus.unsubscribe(EventType.CANDLE_EVENT, self._candle_handler)
        self.logger.info("Strategy stopped")
        return True

    def _on_candle_event(self, event: Event) -> None:
        order = self.on_candle(event.data or {})
        if order:
            self.event_bus.publish(EventType.ORDER_REQUEST, order, source=self.__class__.__name__)

    @abstractmethod
    def on_candle(self, candle: Dict) -> Optional[Dict]:
        """
        Handle a candle dict. Return an order dict or None.
        """
        raise NotImplementedError
