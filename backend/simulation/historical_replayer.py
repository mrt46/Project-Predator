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
    def __init__(self, event_bus: EventBus, time_source: TimeSource):
        self.event_bus = event_bus
        self.time_source = time_source
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("HistoricalReplayer initialized")

    def replay(self, candles: Iterable[Candle]) -> None:
        """
        Replay candles sequentially (blocking).
        """
        for candle in candles:
            # Emit candle
            self.event_bus.publish(EventType.FAKE_CANDLE, candle.to_dict(), source=self.__class__.__name__)
            # Optionally emit tick
            self.event_bus.publish(EventType.TICK, {"tick_number": candle.timestamp}, source=self.__class__.__name__)
            # Sleep according to speed (use candle spacing if available)
            self.time_source.sleep(0.01)  # accelerated minimal pause

    def replay_with_spacing(self, candles: List[Candle]) -> None:
        """
        Replay respecting original timestamp spacing (scaled by speed).
        """
        if not candles:
            return
        prev_ts = candles[0].timestamp
        for candle in candles:
            delta = max(0.0, candle.timestamp - prev_ts)
            self.time_source.sleep(delta)
            self.event_bus.publish(EventType.FAKE_CANDLE, candle.to_dict(), source=self.__class__.__name__)
            prev_ts = candle.timestamp
