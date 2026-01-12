"""
PROJECT PREDATOR - MarketClock
Drives periodic TICK events using TimeSource.
"""
import logging
import threading
import time
from typing import Optional
from backend.core.event_bus import EventBus, EventType
from backend.simulation.time_source import TimeSource


class MarketClock:
    def __init__(self, event_bus: EventBus, time_source: TimeSource, tick_interval: float = 1.0):
        self.event_bus = event_bus
        self.time_source = time_source
        self.tick_interval = tick_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._tick = 0

    def start(self) -> bool:
        if self._running:
            self.logger.warning("MarketClock already running")
            return False
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self.logger.info("MarketClock started")
        return True

    def stop(self) -> bool:
        if not self._running:
            self.logger.warning("MarketClock not running")
            return False
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        self.logger.info("MarketClock stopped")
        return True

    def _run(self) -> None:
        while self._running:
            self._tick += 1
            self.event_bus.publish(
                EventType.TICK,
                {"tick_number": self._tick, "sim_time": self.time_source.now().isoformat()},
                source=self.get_name()
            )
            self.time_source.sleep(self.tick_interval)

    def get_name(self) -> str:
        return self.__class__.__name__
