"""
PROJECT PREDATOR - HistoricalReplayer
Replays a list of candles using a TimeSource.
"""
import logging
from typing import Iterable, List
from backend.core.event_bus import EventBus, EventType
from backend.market.candle import Candle
from backend.simulation.time_source import TimeSource


class HistoricalReplayer:
    """
    Simple candle replayer.
    Publishes FAKE_CANDLE (and PRICE_UPDATE via feed downstream) respecting speed.
    """
    def __init__(self, event_bus: EventBus, time_source: TimeSource, emit_ticks: bool = False, deterministic: bool = False):
        self.event_bus = event_bus
        self.time_source = time_source
        self.emit_ticks = emit_ticks
        self.deterministic = deterministic
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"HistoricalReplayer initialized (emit_ticks={emit_ticks}, deterministic={deterministic})")

    def replay(self, candles: Iterable[Candle]) -> None:
        """
        Replay candles sequentially (blocking) - fast mode (minimal spacing).
        """
        for candle in candles:
            # Emit candle
            self.event_bus.publish(EventType.FAKE_CANDLE, candle.to_dict(), source=self.__class__.__name__)
            # Optionally emit tick
            if self.emit_ticks:
                self.event_bus.publish(EventType.TICK, {"tick_number": candle.timestamp}, source=self.__class__.__name__)
            # Sleep according to speed (minimal pause for fast replay)
            if self.deterministic:
                self.time_source.sleep(0.001)  # Fixed small delay for determinism
            else:
                self.time_source.sleep(0.01)  # Accelerated minimal pause

    def replay_with_spacing(self, candles: List[Candle]) -> None:
        """
        Replay respecting original timestamp spacing (scaled by speed).
        """
        if not candles:
            return
        prev_ts = candles[0].timestamp
        for candle in candles:
            # Calculate time delta (in seconds)
            delta = max(0.0, candle.timestamp - prev_ts)
            # Scale by time_source speed (if speed > 1, time passes faster)
            scaled_delta = delta / self.time_source.speed if self.time_source.speed > 0 else 0.0
            # Sleep scaled time
            if scaled_delta > 0:
                self.time_source.sleep(scaled_delta)
            # Emit candle
            self.event_bus.publish(EventType.FAKE_CANDLE, candle.to_dict(), source=self.__class__.__name__)
            # Optionally emit tick
            if self.emit_ticks:
                self.event_bus.publish(EventType.TICK, {"tick_number": candle.timestamp}, source=self.__class__.__name__)
            prev_ts = candle.timestamp
