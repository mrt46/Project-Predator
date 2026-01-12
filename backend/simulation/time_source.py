"""
PROJECT PREDATOR - TimeSource
Abstract time provider for simulation/backtest.

Modes:
- realtime: speed=1.0
- accelerated: speed>1.0 (wallclock / speed)
- paused/backtest: caller controls stepping
"""
import time
from datetime import datetime, timedelta, timezone


class TimeSource:
    """
    Simple time source with speed control.
    Deterministic and minimal; no threading inside.
    """
    def __init__(self, speed: float = 1.0):
        self._speed = max(speed, 0.0001)  # avoid zero division
        self._start_wall = time.time()
        self._start_sim = datetime.now(timezone.utc)

    def now(self) -> datetime:
        """
        Current simulation time (UTC).
        """
        elapsed_wall = time.time() - self._start_wall
        elapsed_sim = elapsed_wall * self._speed
        return self._start_sim + timedelta(seconds=elapsed_sim)

    def sleep(self, dt_seconds: float) -> None:
        """
        Sleep dt_seconds in simulation time (scaled by speed).
        """
        if dt_seconds <= 0:
            return
        time.sleep(dt_seconds / self._speed)

    def set_speed(self, speed: float) -> None:
        """
        Update speed multiplier.
        """
        self._speed = max(speed, 0.0001)
