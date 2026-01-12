"""
PROJECT PREDATOR - Scheduler
Generates system heartbeat and tick events
"""
import logging
import time
import threading
from typing import Optional
from backend.core.event_bus import EventBus, EventType


class Scheduler:
    """
    System scheduler
    
    Generates:
    - HEARTBEAT: System health signal
    - TICK: Market tick signal (stub)
    
    Drives the system clock.
    """
    
    def __init__(self, event_bus: EventBus, tick_interval: float = 1.0, heartbeat_interval: float = 5.0):
        """
        Initialize scheduler
        
        Args:
            event_bus: EventBus instance
            tick_interval: Seconds between ticks
            heartbeat_interval: Seconds between heartbeats
        """
        self.logger = logging.getLogger(__name__)
        self.event_bus = event_bus
        self.tick_interval = tick_interval
        self.heartbeat_interval = heartbeat_interval
        
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._tick_count = 0
        self._heartbeat_count = 0
        
        self.logger.info(f"Scheduler initialized (tick={tick_interval}s, heartbeat={heartbeat_interval}s)")
    
    def start(self) -> bool:
        """Start the scheduler"""
        if self._running:
            self.logger.warning("Scheduler already running")
            return False
        
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self.logger.info("Scheduler started")
        return True
    
    def stop(self) -> bool:
        """Stop the scheduler"""
        if not self._running:
            self.logger.warning("Scheduler not running")
            return False
        
        self._running = False
        if self._thread:
            self._thread.join(timeout=5.0)
        
        self.logger.info("Scheduler stopped")
        return True
    
    def _run(self) -> None:
        """Main scheduler loop"""
        last_tick = time.time()
        last_heartbeat = time.time()
        
        while self._running:
            now = time.time()
            
            # Generate tick
            if now - last_tick >= self.tick_interval:
                self._tick_count += 1
                self.event_bus.publish(
                    EventType.TICK,
                    {"tick_number": self._tick_count, "timestamp": now},
                    source="Scheduler"
                )
                last_tick = now
            
            # Generate heartbeat
            if now - last_heartbeat >= self.heartbeat_interval:
                self._heartbeat_count += 1
                self.event_bus.publish(
                    EventType.HEARTBEAT,
                    {
                        "heartbeat_number": self._heartbeat_count,
                        "timestamp": now,
                        "ticks_generated": self._tick_count
                    },
                    source="Scheduler"
                )
                last_heartbeat = now
            
            # Sleep to avoid busy-waiting
            time.sleep(0.1)
    
    def get_stats(self) -> dict:
        """Get scheduler statistics"""
        return {
            "running": self._running,
            "ticks_generated": self._tick_count,
            "heartbeats_generated": self._heartbeat_count
        }
